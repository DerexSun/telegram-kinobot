from typing import List, Optional, Tuple

from sqlalchemy import exc, func, delete
from sqlalchemy.future import select

from db import AsyncSessionLocal
from db.models import Users, FavoritesMovie


# Получение пользователя по его Telegram ID
async def get_user_by_telegram_id(user_telegram_id: int) -> Optional[Users]:
    async with AsyncSessionLocal() as session:
        try:
            stmt = select(Users).filter(Users.telegram_id == user_telegram_id)
            user = await session.scalar(stmt)
            return user
        except Exception as e:
            print(f'Error in get_user_by_telegram_id: {e}')
            return None


# Добавление или обновление пользователя
async def add_or_update_user(user_telegram_id: int, user_username: str, user_first_name: str,
                             user_last_name: str) -> None:
    async with AsyncSessionLocal() as session:
        try:
            # Получаем пользователя
            user = await get_user_by_telegram_id(user_telegram_id)
            if user:
                # Обновление данных пользователя
                user.username = user_username
                user.first_name = user_first_name
                user.last_name = user_last_name
                session.add(user)  # Возможно, нужно добавить объект для отслеживания изменений
            else:
                # Создание нового пользователя
                new_user = Users(
                    telegram_id=user_telegram_id,
                    username=user_username,
                    first_name=user_first_name,
                    last_name=user_last_name,
                )
                session.add(new_user)

            await session.commit()

        except exc.IntegrityError as e:
            await session.rollback()
            print(f'IntegrityError in add_or_update_user: {e}')
        except Exception as e:
            await session.rollback()
            print(f'Error in add_or_update_user: {e}')


# Проверка текущего количества избранных фильмов
async def check_current_favorites_count(user_telegram_id: int) -> Tuple[int, Optional[int]]:
    async with AsyncSessionLocal() as session:
        try:
            user = await get_user_by_telegram_id(user_telegram_id)
            if user:
                count_query = await session.execute(
                    select(func.count(FavoritesMovie.id)).filter(FavoritesMovie.user_id == user.id)
                )
                current_favorites_count = count_query.scalar()
                return current_favorites_count, user.id
            return 0, None
        except Exception as e:
            print(f'Error in check_current_favorites_count: {e}')
            return 0, None


# Добавление фильма в избранное
async def add_movie_to_favourites_in_db(user_id: int, movie_id: int, movie_name: str, release_year: int,
                                        genres: List[str], country: str) -> bool:
    async with AsyncSessionLocal() as session:
        try:
            new_favorite_movie = FavoritesMovie(
                user_id=user_id,
                movie_id=movie_id,
                movie_name=movie_name,
                release_year=release_year,
                genres=genres,
                country=country
            )

            session.add(new_favorite_movie)
            await session.commit()
            return True

        except exc.IntegrityError:
            await session.rollback()
            print(f'IntegrityError in add_movie_to_favourites_in_db for movie: {movie_name}')
            return False
        except Exception as e:
            await session.rollback()
            print(f'Error in add_movie_to_favourites_in_db: {e}')
            return False


# Получение избранных фильмов
async def get_favourites(user_telegram_id: int) -> Optional[List[FavoritesMovie]]:
    async with AsyncSessionLocal() as session:
        try:
            user = await get_user_by_telegram_id(user_telegram_id)
            if user:
                favorites_stmt = select(FavoritesMovie).where(FavoritesMovie.user_id == user.id)
                favorites = await session.execute(favorites_stmt)
                return favorites.scalars().all()
            return None
        except Exception as e:
            print(f'Error in get_favourites: {e}')
            return None


# Удаление фильмов из избранного
async def delete_movies(favourites: List[FavoritesMovie], movie_numbers: List[int]) -> List[str]:
    async with AsyncSessionLocal() as session:
        try:
            deleted_movies = []
            for movie_number in movie_numbers:
                movie_to_delete = favourites[movie_number - 1]
                await session.delete(movie_to_delete)
                deleted_movies.append(movie_to_delete.movie_name)

            await session.commit()
            return deleted_movies
        except Exception as e:
            await session.rollback()
            print(f'Error in delete_movies: {e}')
            return []


async def clear_all_favourites(user_telegram_id: int) -> None:
    async with AsyncSessionLocal() as session:
        try:
            user = await get_user_by_telegram_id(user_telegram_id)
            if user:
                # Удаляем все фильмы из избранного пользователя
                await session.execute(
                    delete(FavoritesMovie).where(FavoritesMovie.user_id == user.id)
                )
                await session.commit()
                print(f'Все избранные фильмы для пользователя {user_telegram_id} были успешно удалены.')
            else:
                print(f'Пользователь с Telegram ID {user_telegram_id} не найден.')
        except Exception as e:
            await session.rollback()
            print(f'Error in clear_favourites: {e}')
