from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import get_auth_data
from database import get_session  # Функция для получения асинхронной сессии
from models import Client  # Ваша модель пользователя


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        # Для HTML запросов - вызываем исключение с редиректом
        if "text/html" in request.headers.get("accept", ""):
            raise HTTPException(
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                headers={"Location": "/auth/login?return_url=" + str(request.url)}
            )
        # Для API запросов - стандартная ошибка
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found'
        )
    return token

async def get_current_client(
    token: str = Depends(get_token),
    session: AsyncSession = Depends(get_session)
):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не валидный!'
        )

    # Проверяем срок действия токена
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен истек'
        )

    # Получаем ID пользователя из токена
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не найден ID пользователя'
        )

    # Ищем пользователя в базе данных
    query = select(Client).where(Client.id_client == int(user_id))
    result = await session.execute(query)
    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    return client