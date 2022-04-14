from pydantic import BaseModel, Field
from datetime import date


class UserResponseV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class UserAddRequestV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str

class UserInfo(BaseModel):
    user_id: int = Field(..., ge=1)
    repo_id: int = Field(..., ge=1)
    stargazers: int
    date: date
    forks: int
    watchers: int