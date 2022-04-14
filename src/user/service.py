from typing import List
from datetime import date
from fastapi.responses import JSONResponse
import requests

from sqlalchemy import select, insert, delete
from sqlalchemy.future import Engine

from src.database import tables
from src.user.models import UserResponseV1, UserAddRequestV1, UserInfo


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_user_stat(self) -> JSONResponse():
        query = select(tables.stats)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        stat = []
        for user_data in users_data:
            stats = UserInfo(
                user_id=user_data['user_id'],
                repo_id=user_data['repo_id'],
                date=user_data['date'],
                stargazers = user_data['stargazers'],
                forks = user_data['forks'],
                watchers = user_data['watchers']
            )
            stat.append(stats)
        return stat

    def get_user(self) -> JSONResponse():
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(
                id=user_data['id'],
                login=user_data['login'],
                name=user_data['name']
            )
            users.append(user)
        return users

    def get_id(self):
        query = select(tables.users)
        with self._engine.connect() as connection:
            ids_data = connection.execute(query)
        ids = []
        for id_data in ids_data:
            id = id_data['id']
            ids.append(id)

        return ids

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(
                id=user_data['id'],
                login=user_data['login'],
                name=user_data['name']
            )
            users.append(user)
        return users

    def get_user_by_id(self, id: int) -> UserResponseV1:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user_data = user_data.fetchall()[0]
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        return user

    def add_user(self, user: UserAddRequestV1) -> None:
        query = insert(tables.users).values(
            id=user.id,
            login=user.login,
            name=user.name
        )
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def add_user_info(self, id: int) -> None:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user_data = user_data.fetchall()
        login = user_data[0][1]

        def get_info(username: str):
            data = requests.get('https://api.github.com/users/' + username)
            data = data.json()
            url = data['repos_url']
            repos_data = []
            while (True):
                response = requests.get(url)
                response = response.json()
                repos_data = repos_data + response
                break

            repos_information = []
            for i, repo in enumerate(repos_data):
                data = []
                data.append(repo['id'])
                data.append(repo['created_at'])
                data.append(repo['forks_count'])
                data.append(repo['stargazers_count'])
                data.append(repo['watchers_count'])
                repos_information.append(tuple(data))

            return repos_information
        repos_information = get_info(login)
        info = []
        for repo_information in repos_information:
            data = UserInfo(
                user_id= id,
                repo_id= repo_information[0],
                stargazers= repo_information[2],
                date= date.today(),
                forks= repo_information[3],
                watchers= repo_information[4]
            )
            info.append(data)
            print(data)
            query = insert(tables.stats).values(
                user_id= id,
                repo_id= repo_information[0],
                stargazers= repo_information[2],
                date= date.today(),
                forks= repo_information[3],
                watchers= repo_information[4]
            )
            with self._engine.connect() as connection:
                connection.execute(query)
                connection.commit()


    def delete_user_by_id(self, id: int) -> None:
        query = delete(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()



