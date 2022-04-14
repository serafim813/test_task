import sqlalchemy as sa
from fastapi import FastAPI
import time
import src.api.protocols
from src.api import users, protocols
from src.database import DatabaseSettings, create_database_url
from src.user.service import UserService
from tests.test_api.test_users import drop


def get_application() -> FastAPI:
    application = FastAPI(
        title='GitHub Repo Stats',
        description='Сервис сбора статистических данных о популярности репозиториев на GitHub.',
        version='1.0.0'
    )

    application.include_router(users.router)

    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True
    )
    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    return application


async def user_info():
    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True
    )
    user_service = UserService(engine)
    while (True):
        drop()
        ids = user_service.get_id()
        for id in ids:
            user_service.add_user_info(id)
        time.sleep(86400)

app = get_application()