from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    host: str = Field("localhost", env='DB_HOST')
    port: str = Field(5439, env='DB_PORT')
    username: str = Field("serafim", env='DB_USERNAME')
    password: str = Field(1234, env='DB_PASSWORD')
    database: str = Field("postgres", env='DB_DATABASE')
