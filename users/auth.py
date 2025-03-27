from passlib.context import CryptContext

from models import Client

#######################REGIN####################################################################
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    hashed = pwd_context.hash(password).strip()  # Удаляем пробелы
    if len(hashed) > 255:
        raise ValueError("Хэш пароля слишком длинный")
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password.strip()  # Чистим пробелы из базы
    )
#############################################################################################
#logIN
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

async def authenticate_user(
    client_email: EmailStr,
    client_password: str,
    session: AsyncSession
):
    # Выполняем запрос к базе данных для поиска пользователя по email
    query = select(Client).where(Client.client_email == client_email)
    result = await session.execute(query)
    client = result.scalar_one_or_none()

    # Проверяем, существует ли пользователь и совпадает ли пароль
    if not client or not verify_password(plain_password=client_password, hashed_password=client.client_password):
        return None

    return client