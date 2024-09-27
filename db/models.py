import datetime
from typing import Annotated, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
create_at = Annotated[str, mapped_column(default=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)]
update_at = Annotated[str, mapped_column(default=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         onupdate=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         nullable=True)]


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    create_at: Mapped[create_at]
    update_at: Mapped[update_at]


class FavoritesMovie(Base):
    __tablename__ = 'favorites_movie'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id: Mapped[int] = mapped_column(nullable=False)
    movie_name: Mapped[str] = mapped_column(nullable=False)
    genres: Mapped[Optional[str]]
    release_year: Mapped[Optional[int]]
    country: Mapped[Optional[str]]
    create_at: Mapped[create_at]

    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),
    )
