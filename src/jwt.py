from datetime import datetime, timedelta, timezone
from passlib.hash import pbkdf2_sha256
from jose import jwt

from settings import settings, logger


async def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


async def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)


async def create_access_token(data: dict, expires_secondss: int = settings.access_token_expire_seconds) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_secondss)
    to_encode.update({"exp": expire})
    logger.debug(f'payload: {to_encode}')
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
