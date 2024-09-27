from aiogram import Dispatcher

from handlers.custom_handlers.actor_details import get_actor_details
from handlers.custom_handlers.actor_search_name import (
    handle_actor_search_name,
    process_actor_name,
    process_actor_search,
    ActorSearchStatesName
)
from handlers.custom_handlers.add_to_favourites import add_movie_to_favourites
from handlers.custom_handlers.back_to_main_menu import back_to_main_menu
from handlers.custom_handlers.deleting_or_clearing_favorites import (
    delete_movie_callback_handler,
    clear_favorites_callback_handler,
    cancel_deletion_callback_handler,
    delete_movie_by_number,
    FavoritesStates
)
from handlers.default_handlers.help import process_help_command
from handlers.custom_handlers.movie_search import (
    handle_movie_search,
    process_movie_name,
    process_movie_limit,
    MovieSearchStates
)
from handlers.custom_handlers.show_movies_actor import handle_show_movies_actor
from handlers.custom_handlers.view_favorites import favourites_callback_handler


class HandlerRegistry:
    """
    Класс для регистрации обработчиков команд и колбеков в диспетчере Aiogram.
    """

    def __init__(self, dp: Dispatcher):
        """
        Инициализация класса HandlerRegistry.

        :param dp: Диспетчер Aiogram, который будет использоваться для регистрации обработчиков.
        """
        self.dp = dp

    def register_actor_handlers(self):
        """Регистрирует обработчики для поиска актеров."""
        self.dp.callback_query.register(handle_actor_search_name, lambda c: c.data == 'name_search')
        self.dp.callback_query.register(handle_show_movies_actor, lambda c: c.data == 'show_movies')
        self.dp.message.register(process_actor_name, ActorSearchStatesName.waiting_for_actor_name)
        self.dp.callback_query.register(process_actor_search, lambda c: c.data.startswith('limit_'),
                                        ActorSearchStatesName.waiting_for_actor_limit)

    def register_add_movie_to_favourites(self):
        """Регистрирует обработчик для добавления фильмов в избранное."""
        self.dp.callback_query.register(
            add_movie_to_favourites,
            lambda callback_data: callback_data.data.startswith('add_to_favourites:')
        )

    def register_actor_details(self):
        """Регистрирует обработчик для получения информации об актере."""
        self.dp.callback_query.register(
            get_actor_details,
            lambda callback_data: callback_data.data.startswith('actor_details:')
        )

    def register_deleting_or_clearing_favorites(self):
        """Регистрирует обработчики для удаления или очистки избранного."""
        self.dp.callback_query.register(delete_movie_callback_handler, lambda c: c.data.startswith('delete_movie:'))
        self.dp.callback_query.register(clear_favorites_callback_handler, lambda c: c.data == 'clear_favorites')
        self.dp.callback_query.register(cancel_deletion_callback_handler, lambda c: c.data == 'cancel_deletion')
        self.dp.message.register(delete_movie_by_number, FavoritesStates.waiting_for_movie_number)

    def register_back_to_main_menu(self):
        """Регистрирует обработчик для возврата в главное меню."""
        self.dp.callback_query.register(back_to_main_menu, lambda c: c.data == 'main_menu')

    def register_help(self):
        """Регистрирует обработчик для команды помощи."""
        self.dp.callback_query.register(process_help_command, lambda c: c.data == 'help_command')

    def register_movie_handlers(self):
        """Регистрирует обработчики для поиска фильмов."""
        self.dp.callback_query.register(handle_movie_search, lambda c: c.data == 'move_search')
        self.dp.message.register(process_movie_name, MovieSearchStates.waiting_for_movie_name)
        self.dp.callback_query.register(process_movie_limit, lambda c: c.data.startswith('limit_'),
                                        MovieSearchStates.waiting_for_movie_limit)

    def register_view_favorites_handlers(self):
        """Регистрирует обработчик для просмотра избранных фильмов."""
        self.dp.callback_query.register(favourites_callback_handler, lambda c: c.data == 'favourites')

    @classmethod
    def register_all_handlers(cls, dp: Dispatcher) -> None:
        """
        Регистрирует все обработчики в диспетчере.

        :param dp: Диспетчер Aiogram, который будет использоваться для регистрации обработчиков.
        """
        registry = HandlerRegistry(dp)
        registry.register_actor_handlers()
        registry.register_add_movie_to_favourites()
        registry.register_actor_details()
        registry.register_deleting_or_clearing_favorites()
        registry.register_back_to_main_menu()
        registry.register_help()
        registry.register_movie_handlers()
        registry.register_view_favorites_handlers()
