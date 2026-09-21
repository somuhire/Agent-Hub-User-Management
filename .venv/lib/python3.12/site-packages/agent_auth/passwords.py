from dataclasses import dataclass

import bcrypt

from agent_auth.exceptions import InvalidPasswordError


@dataclass(frozen=True)
class PasswordPolicy:
    max_bytes: int = 72


def validate_password(
        password: str,
        policy: PasswordPolicy | None = None,
    ) -> str:
    active_policy = policy or PasswordPolicy()
    if len(password.encode("utf-8")) > active_policy.max_bytes:
        raise InvalidPasswordError(
            f"Password cannot be longer than {active_policy.max_bytes} bytes."
        )
    return password


def hash_password(
        password: str,
        policy: PasswordPolicy | None = None,
    ) -> str:
    validated_password = validate_password(password, policy)
    return bcrypt.hashpw(
        validated_password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(
        password: str,
        hashed_password: str,
        policy: PasswordPolicy | None = None,
    ) -> bool:
    validated_password = validate_password(password, policy)
    try:
        return bcrypt.checkpw(
            validated_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (TypeError, ValueError):
        return False