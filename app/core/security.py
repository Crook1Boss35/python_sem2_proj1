from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.errors import UnauthorizedError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({
        "iat": now,
        "exp": expire,
    })

    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
        return payload
    except JWTError as e:
        raise UnauthorizedError("Invalid or expired token") from e
