from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.responses import JSONResponse, Response, HTMLResponse, RedirectResponse

from config import create_access_token
from users.auth import get_password_hash, authenticate_user
from users.dependencies import get_current_client
from users.schemas import SClientRegister, SClientAuth
from database import sessionmaker, async_engine, get_session
from models import Client
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter(prefix='/auth', tags=['Auth'])

# Добавляем в начало файла
templates = Jinja2Templates(directory="templates")

####################################################################################################
@router.get("/login")
async def login_page(request: Request):
    """Отображает страницу входа"""
    return templates.TemplateResponse("login.html", {"request": request})

#бэк авторизации
@router.post("/login")
async def login_user(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    """Обрабатывает данные входа"""
    user = await authenticate_user(
        client_email=form_data.username,
        client_password=form_data.password,
        session=session
    )

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверный email или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token = create_access_token({"sub": str(user.id_client)})

    response = templates.TemplateResponse(
        "login_success.html",
        {"request": request, "user": user}
    )
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)

    return response

#фронт регистрации
@router.get("/register")
async def register_page(request: Request):
    """Отображает страницу регистрации"""
    return templates.TemplateResponse("register.html", {"request": request})

#бэк регистрации
@router.post("/register")
async def register_user(
        request: Request,
        client_last_name: str = Form(...),
        client_name: str = Form(...),
        client_mid_name: str = Form(None),
        client_phone_number: str = Form(...),
        client_email: str = Form(...),
        client_password: str = Form(...),
        client_password_confirm: str = Form(...),
        session: AsyncSession = Depends(get_session)
):
    """Обрабатывает данные регистрации"""

    # Проверка совпадения паролей
    if client_password != client_password_confirm:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Пароли не совпадают",
                "form_data": {
                    "client_last_name": client_last_name,
                    "client_name": client_name,
                    "client_mid_name": client_mid_name,
                    "client_phone_number": client_phone_number,
                    "client_email": client_email
                }
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Проверка существования пользователя
    query = select(Client).where(Client.client_email == client_email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Пользователь с таким email уже существует",
                "form_data": {
                    "client_last_name": client_last_name,
                    "client_name": client_name,
                    "client_mid_name": client_mid_name,
                    "client_phone_number": client_phone_number,
                    "client_email": client_email
                }
            },
            status_code=status.HTTP_409_CONFLICT
        )

    # Хэширование пароля
    hashed_password = get_password_hash(client_password)

    # Создание нового пользователя
    new_client = Client(
        client_last_name=client_last_name,
        client_name=client_name,
        client_mid_name=client_mid_name,
        client_phone_number=client_phone_number,
        client_email=client_email,
        client_password=hashed_password,
        client_self_sale=0,  # По умолчанию скидка 0%
        is_user=True,
        is_admin=False
    )

    session.add(new_client)
    await session.commit()
    await session.refresh(new_client)

    # Автоматический вход после регистрации
    access_token = create_access_token({"sub": str(new_client.id_client)})

    response = templates.TemplateResponse(
        "register_success.html",
        {"request": request, "user": new_client}
    )
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)

    return response

#окно после успешной регистрации
@router.get("/register/success")
async def register_success_page(
    request: Request,
    user: Client = Depends(get_current_client)
):
    """Отображает страницу успешной регистрации"""
    return templates.TemplateResponse(
        "register_success.html",
        {
            "request": request,
            "user": user
        }
    )

#Выход из аккаунта
@router.get("/logout")
async def logout_user(response: Response):
    # Создаем ответ с редиректом
    response = RedirectResponse(url="/auth/logout-success")

    response.delete_cookie(key="users_access_token")

    return response

#Успешый выход из аккаунта
@router.get("/logout-success")
async def logout_success(request: Request):
    # Показываем страницу с сообщением о успешном выходе
    return templates.TemplateResponse(
        "logout_success.html",
        {"request": request}
    )