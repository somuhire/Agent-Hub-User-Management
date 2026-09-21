from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt


class JWTManager:

    def __init__(
            self,
            secret_key: str,
            algorithm: str = "HS256",
            access_token_expire_minutes: int = 30,
        ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
            self,
            user_id: int,
            role: str,
        ) -> str:

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(
            self,
            token: str,
        ) -> dict | None:

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload

        except JWTError:
            return None