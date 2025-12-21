from datetime import datetime, timezone
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from settings import settings, logger


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(detail='Token not found', status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_user_id(token: str = Depends(get_token)) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
    logger.debug(f'payload: {payload}')
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
    user_id = payload.get('id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    return int(user_id)
