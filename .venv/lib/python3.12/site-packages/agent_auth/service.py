from collections.abc import Awaitable, Callable
from typing import Protocol

from agent_auth.exceptions import InvalidCredentialsError
from agent_auth.jwt import JWTManager
from agent_auth.passwords import verify_password


class AuthUser(Protocol):
    id: int
    role: str
    password_hash: str


async def authenticate_user(
        identifier: str,
        password: str,
        load_user: Callable[[str], Awaitable[AuthUser | None]],
        jwt_manager: JWTManager,
        *,
        get_user_id: Callable[[AuthUser], int] = lambda user: user.id,
        get_role: Callable[[AuthUser], str] = lambda user: str(user.role),
        get_password_hash: Callable[[AuthUser], str] = (
            lambda user: user.password_hash
        ),
    ) -> str:
    user = await load_user(identifier)
    if user is None or not verify_password(
            password,
            get_password_hash(user),
        ):
        raise InvalidCredentialsError("Invalid credentials.")

    return jwt_manager.create_access_token(
        user_id=get_user_id(user),
        role=get_role(user),
    )