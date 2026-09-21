from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from agent_auth.jwt import JWTManager
from agent_auth.models import CurrentUser


def create_auth_dependency(
    jwt_manager: JWTManager,
    token_url: str = "/auth/login",
):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

    async def get_current_user(
        token: str = Depends(oauth2_scheme),
    ) -> CurrentUser:

        payload = jwt_manager.decode_access_token(token)

        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid or expired token",
                                headers={"WWW-Authenticate": "Bearer"})

        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return CurrentUser(
            user_id=user_id,
            role=role,
        )

    return get_current_user


def create_user_loader_dependency(
        jwt_manager: JWTManager,
        load_user: Callable,
        token_url: str = "/auth/login",
    ):
    current_user_dependency = create_auth_dependency(jwt_manager, token_url)

    async def get_loaded_user(
            current_user: CurrentUser = Depends(current_user_dependency),
        ):
        user = await load_user(current_user.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    return get_loaded_user