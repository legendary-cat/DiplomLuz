from datetime import datetime
from _pydecimal import Decimal
from urllib import request
import json
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, Query, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.testing import db
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional

from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database import get_db, get_session
from models import Client, Order, OrderMaterial, OrderEquipment, OrderService, Material, Equipment, Service, \
    ServiceMaterial, ServiceEquipment, Object  # Импортируем модели SQLAlchemy
from schemas import ClientBase, OrderWithClient, MaterialWithQuantity, OrderWithDetails, MaterialQuantityInput, \
    MaterialInput, ServiceInput, MaterialInfo, ServicePriceResponse, EquipmentInfo, \
    EnhancedServicePriceResponse, EquipmentRequirement, OrderServiceCreate, \
    OrderEquipmentCreate, OrderMaterialCreate, OrderCreate, RedisOrder  # Импортируем Pydantic схемы
from math import ceil

from users.dependencies import get_current_client
from users.router import router as router_user
from jose import JWTError, jwt
from starlette.exceptions import HTTPException as StarletteHTTPException
from redis import Redis
from pathlib import Path as PathLib  # Переименовываем для избежания конфликта
##############################################################################################
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для теста разрешите все origins
    allow_credentials=True,
    allow_methods=["*"],  # Разрешите все методы
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), 'static')
templates = Jinja2Templates(directory='templates')

app.include_router(router_user)

###################################################################################################################
###################################################################################################################
#главная страница
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "main_page.html",
        {
            "request": request,
        }
    )


########################################################################################
def get_redis() -> Redis:
    return Redis(host="localhost", port=6379, db=0)

# Загрузка описаний и изображений из JSON
def load_service_data() -> Dict[str, Any]:
    # Определяем путь к файлу относительно расположения main.py
    json_path = PathLib("C:\\Users\\Sung Jin-Woo\\PycharmProjects\\DiplomLuz\\data_description.json")

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {json_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле: {json_path}")
        return {}
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке данных: {str(e)}")
        return {}
#####################################################################################
#####################################################################################
#3 функции для поиска материалов, услуг и оборудования по их id
async def find_material_id_by_name(db: AsyncSession, material_name: str) -> int:
    """
    Находит ID материала по его имени.
    """
    query = select(Material.id_material).where(Material.material_name == material_name)
    result = await db.execute(query)
    material = result.scalar_one_or_none()
    if not material:
        raise HTTPException(status_code=404, detail=f"Материал с именем '{material_name}' не найден")
    return material

async def find_equipment_id_by_name(db: AsyncSession, equipment_name: str) -> int:
    """
    Находит ID оборудования по его имени.
    """
    query = select(Equipment.id_equipment).where(Equipment.equipment_name == equipment_name)
    result = await db.execute(query)
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=404, detail=f"Оборудование с именем '{equipment_name}' не найдено")
    return equipment

async def find_service_id_by_name(db: AsyncSession, service_name: str) -> int:
    """
    Находит ID услуги по ее имени.
    """
    query = select(Service.id_service).where(Service.service_name == service_name)
    result = await db.execute(query)
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail=f"Услуга с именем '{service_name}' не найдена")
    return service


######################################################################################################
#ФРОНТ################################################################################################


#html онлайн-калькулятора
@app.get('/calc_front')
async def get_main_page(request: Request, client: Client = Depends(get_current_client),):
    if not client:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse(name='index.html', context={'request': request})

#бэк калькулятора и все расчеты, что идут в redis
@app.post("/calc_inp")
async def calculate_order_cost(
        input_data: ServiceInput,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis)
) -> ServicePriceResponse:
    # Теперь client содержит авторизованного пользователя
    user_id = client.id_client

    # Инициализация переменных
    total_service_price = 0.0
    total_materials_cost = 0.0
    total_equipment_cost = 0.0
    total_materials_delivery_cost = 0.0
    total_equipment_delivery_cost = 0.0
    material_info = []
    equipment_info = []
    service_info = []  # Список для хранения информации об услугах

    # Словари для агрегации данных
    materials_aggregated = {}
    equipment_usage = {}

    # Получаем стоимость доставки материалов
    result = await db.execute(select(Service.service_price).where(Service.id_service == 1))
    delivery_cost_per_material_unit = result.scalar()

    if not delivery_cost_per_material_unit:
        raise HTTPException(status_code=404, detail="Стоимость доставки материалов не найдена")

    # Получаем данные о грузовике (id = 2)
    result = await db.execute(
        select(
            Equipment.equipment_name,
            Equipment.equipment_capacity,
            Equipment.equipment_ammortiz,
            Equipment.equipment_transport_price_of_one
        ).where(Equipment.id_equipment == 2)
    )
    truck_data = result.first()

    if not truck_data:
        raise HTTPException(status_code=404, detail="Грузовик с id = 2 не найден")

    truck_name, truck_capacity, truck_ammortiz, truck_transport_price = truck_data

    # Обработка услуг
    for service_item in input_data.services:
        # Получаем услугу
        result = await db.execute(select(Service).where(Service.service_name == service_item.service_name))
        service = result.scalar()

        if not service:
            raise HTTPException(status_code=404, detail=f"Услуга '{service_item.service_name}' не найдена")

        total_service_price += float(service.service_price) * float(service_item.quantity)

        # Добавляем информацию об услуге
        service_info.append({
            "service_name": service.service_name,
            "quantity": service_item.quantity,
            "price_per_unit": float(service.service_price),
            "total_price": float(service.service_price) * float(service_item.quantity)
        })

        # Обработка материалов
        result = await db.execute(
            select(
                Material.material_name,
                ServiceMaterial.service_material_quantity,
                Material.material_price_of_one,
                Material.material_transport_volume
            )
            .join(ServiceMaterial, ServiceMaterial.id_material == Material.id_material)
            .where(ServiceMaterial.id_service == service.id_service)
        )
        materials = result.all()

        for material_name, quantity_per_unit, price, transport_volume in materials:
            total_material_quantity = quantity_per_unit * service_item.quantity
            total_material_price = price * total_material_quantity
            total_material_volume = transport_volume * total_material_quantity

            if material_name in materials_aggregated:
                materials_aggregated[material_name]["total_quantity"] += total_material_quantity
                materials_aggregated[material_name]["total_price"] += total_material_price
                materials_aggregated[material_name]["transport_volume"] += total_material_volume
            else:
                materials_aggregated[material_name] = {
                    "total_quantity": total_material_quantity,
                    "total_price": total_material_price,
                    "transport_volume": total_material_volume
                }

            total_materials_cost += float(total_material_price)

        # Обработка оборудования
        result = await db.execute(
            select(
                Equipment.equipment_name,
                ServiceEquipment.service_equipment_quantity,
                Equipment.equipment_ammortiz,
                Equipment.equipment_transport_price_of_one,
                Equipment.equipment_capacity
            )
            .join(ServiceEquipment, ServiceEquipment.id_equipment == Equipment.id_equipment)
            .where(ServiceEquipment.id_service == service.id_service)
        )
        equipment_data = result.all()

        # Агрегация данных оборудования
        for equipment_name, quantity_per_service, ammortiz, transport_price, capacity in equipment_data:
            if equipment_name in equipment_usage:
                equipment_usage[equipment_name]["services"].add(service_item.service_name)
                equipment_usage[equipment_name]["max_quantity"] = max(
                    equipment_usage[equipment_name]["max_quantity"],
                    service_item.quantity
                )
            else:
                equipment_usage[equipment_name] = {
                    "services": {service_item.service_name},
                    "max_quantity": service_item.quantity,
                    "ammortiz": ammortiz,
                    "transport_price": transport_price,
                    "capacity": capacity
                }

    # Расчёт грузовиков для материалов
    total_materials_volume = sum(data["transport_volume"] for data in materials_aggregated.values())
    required_trucks = ceil(total_materials_volume / truck_capacity) if total_materials_volume > 0 else 0

    # Добавление грузовиков в оборудование
    if required_trucks > 0:
        equipment_usage[truck_name] = {
            "services": {"Доставка материалов"},
            "max_quantity": required_trucks,
            "ammortiz": truck_ammortiz,
            "transport_price": truck_transport_price,
            "capacity": truck_capacity
        }

    # Формирование списка материалов
    for material_name, data in materials_aggregated.items():
        material_info.append(MaterialInfo(
            material_name=material_name,
            quantity=data["total_quantity"],
            total_price=data["total_price"],
            transport_volume=data["transport_volume"]
        ))

    # Формирование списка оборудования
    for equipment_name, data in equipment_usage.items():
        ammortiz = data["ammortiz"]
        max_quantity = data["max_quantity"]
        services_used = data["services"]
        transport_price = data["transport_price"]
        capacity = data.get("capacity", 1)

        # Логика для грузовика
        if equipment_name == truck_name:
            required_quantity = max_quantity
            total_equipment_price = ammortiz * required_quantity
        else:
            # Логика для остального оборудования
            if len(services_used) > 1:
                total_quantity = max_quantity
            else:
                total_quantity = max_quantity

            threshold = capacity if capacity and capacity > 0 else 1
            required_quantity = ceil(total_quantity / threshold)
            total_equipment_price = ammortiz * required_quantity

        total_equipment_cost += total_equipment_price

        # Расчёт стоимости доставки
        if transport_price is not None:
            total_equipment_delivery_cost += float(transport_price) * float(required_quantity)

        equipment_info.append(EquipmentInfo(
            equipment_name=equipment_name,
            quantity=required_quantity,
            total_price=total_equipment_price,
            transport_price=transport_price if transport_price is not None else 0.0
        ))

    # Финалные расчёты
    total_materials_delivery_cost = sum(
        data["total_quantity"] for data in materials_aggregated.values()) * delivery_cost_per_material_unit
    total_delivery_cost = float(total_materials_delivery_cost) + float(total_equipment_delivery_cost)
    total_cost = total_service_price + total_materials_cost + total_equipment_cost + total_delivery_cost

    # Формируем полный объект ответа
    response_data = ServicePriceResponse(
        service_name="Ваш заказ",
        total_service_price=float(total_service_price),
        total_materials_cost=float(total_materials_cost),
        total_equipment_cost=float(total_equipment_cost),
        total_materials_delivery_cost=float(total_materials_delivery_cost),
        total_equipment_delivery_cost=float(total_equipment_delivery_cost),
        total_delivery_cost=float(total_delivery_cost),
        total_cost=float(total_cost),
        materials=material_info,
        equipment=equipment_info,
        services=service_info  # Добавляем информацию об услугах
    )

    # Сериализуем данные через FastAPI encoder
    redis_data = jsonable_encoder(response_data)

    # Сохраняем полные данные в Redis
    redis_key = f"order_result:{user_id}"
    redis.set(redis_key, json.dumps(redis_data), ex=3600)  # TTL 1 час

    return response_data

#фрон, который появляется после рассчетов в калькуляторе
@app.get("/get_redis_data")
async def get_redis_data(
    request: Request,
    client: Client = Depends(get_current_client),
    redis: Redis = Depends(get_redis)
):
    user_id = client.id_client
    redis_key = f"order_result:{user_id}"

    redis_data = redis.get(redis_key)
    if not redis_data:
        raise HTTPException(status_code=404, detail="Данные в Redis не найдены")

    try:
        order_data = json.loads(redis_data)
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "order_data": order_data,
            },
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при десериализации данных из Redis: {str(e)}"
        )

#запись в бд заказа и в связанные таблицы
@app.get("/order_create", response_class=HTMLResponse)
async def create_order(
        request: Request,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis),
        object_id: Optional[int] = None
):
    # Проверяем авторизацию
    if not client:
        return RedirectResponse(url=f"/auth/login?return_url=/order_create")

    # Получаем расчет из Redis
    redis_key = f"order_result:{client.id_client}"
    redis_data = redis.get(redis_key)

    if not redis_data:
        raise HTTPException(status_code=404, detail="Данные расчета не найдены")

    try:
        order_data = json.loads(redis_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Неверный формат данных расчета")

    # Получаем объекты пользователя
    query = select(Object).where(Object.id_client == client.id_client)
    result = await db.execute(query)
    client_objects = result.scalars().all()

    if not client_objects:
        raise HTTPException(status_code=400, detail="У вас нет объектов. Сначала создайте объект.")

    # Если объект уже выбран (из query параметра)
    if object_id:
        # Проверяем, что объект принадлежит пользователю
        selected_obj = next((obj for obj in client_objects if obj.id_obj == object_id), None)
        if not selected_obj:
            raise HTTPException(status_code=400, detail="Указан неверный объект")

        try:
            # Создаем заказ
            new_order_data = {
                "ord_price": float(Decimal(str(order_data["total_cost"]))),
                "ord_data": datetime.now(),
                "id_client": client.id_client,
                "ord_status": "Создан",
                "ord_payment": 0.0,
                "ord_prepayment": 0.0,
                "id_obj": object_id
            }

            stmt = insert(Order).values(**new_order_data).returning(Order)
            result = await db.execute(stmt)
            new_order = result.scalars().first()
            await db.flush()

            # Добавляем материалы в заказ
            for material in order_data.get("materials", []):
                material_id = await find_material_id_by_name(db, material["material_name"])
                if material_id:
                    material_data = {
                        "id_material": material_id,
                        "id_order": new_order.id_order,
                        "ord_material_quantity": int(material["quantity"])
                    }
                    stmt = insert(OrderMaterial).values(**material_data)
                    await db.execute(stmt)

            # Добавляем оборудование в заказ
            for equipment in order_data.get("equipment", []):
                equipment_id = await find_equipment_id_by_name(db, equipment["equipment_name"])
                if equipment_id:
                    equipment_data = {
                        "id_equipment": equipment_id,
                        "id_order": new_order.id_order,
                        "ord_equipment_quantity": int(equipment["quantity"])
                    }
                    stmt = insert(OrderEquipment).values(**equipment_data)
                    await db.execute(stmt)

            # Добавляем услуги в заказ
            for service in order_data.get("services", []):
                service_id = await find_service_id_by_name(db, service["service_name"])
                if service_id:
                    service_data = {
                        "id_service": service_id,
                        "id_order": new_order.id_order,
                        "ord_service_quantity": int(service["quantity"])
                    }
                    stmt = insert(OrderService).values(**service_data)
                    await db.execute(stmt)

            await db.commit()

            # Очищаем данные расчета из Redis после успешного создания заказа
            redis.delete(redis_key)

            # Перенаправляем на страницу успешного оформления
            return RedirectResponse(url=f"/order_success/{new_order.id_order}")

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка при создании заказа: {str(e)}")

    # Если объект не выбран - показываем страницу выбора
    return templates.TemplateResponse("select_object.html", {
        "request": request,
        "client": client,
        "objects": client_objects,
        "order_data": order_data,
        "total_cost": order_data.get("total_cost", 0)
    })

#Ваш заказ успешло создать и остальные детали о заказе
@app.get("/order_success/{order_id}", response_class=HTMLResponse)
async def order_success(
        request: Request,
        order_id: int,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_session)
):
    # Проверяем, что заказ принадлежит текущему клиенту
    query = select(Order).where(
        (Order.id_order == order_id) &
        (Order.id_client == client.id_client)
    )
    result = await db.execute(query)
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    # Получаем информацию об объекте
    query = select(Object).where(Object.id_obj == order.id_obj)
    result = await db.execute(query)
    order_object = result.scalars().first()

    # Формируем ФИО клиента (используем доступные атрибуты)
    # Вариант 1: Если есть отдельные поля имени, фамилии и отчества
    full_name = getattr(client, 'full_name', None)  # Проверяем, есть ли полное имя

    if not full_name:
        # Собираем ФИО из отдельных компонентов (если они есть)
        surname = getattr(client, 'surname', '') or getattr(client, 'client_surname', '')
        name = getattr(client, 'name', '') or getattr(client, 'client_name', '')
        patronymic = getattr(client, 'patronymic', '') or getattr(client, 'client_patronymic', '')
        full_name = f"{surname} {name} {patronymic}".strip()

    # Вариант 2: Если есть только одно поле с именем
    if not full_name:
        full_name = getattr(client, 'name', 'Не указано')

    # Получаем email клиента
    email = getattr(client, 'email', '') or getattr(client, 'client_email', '') or 'Не указан'

    # Форматируем данные для отображения
    client_info = {
        "full_name": full_name,
        "email": email,
        "object_name": getattr(order_object, 'obj_name', 'Не указан') if order_object else "Не указан",
        "object_address": f"{getattr(order_object, 'obj_city', '')}, {getattr(order_object, 'obj_addres', '')}".strip(
            ', ') if order_object else "",
        "order_price": f"{getattr(order, 'ord_price', 0):.2f} ₽",
        "order_date": getattr(order, 'ord_data', datetime.now()).strftime("%d.%m.%Y %H:%M"),
        "order_status": getattr(order, 'ord_status', 'Неизвестен')
    }

    return templates.TemplateResponse("order_success.html", {
        "request": request,
        "client": client,
        "client_info": client_info,
        "order": order,
        "order_object": order_object
    })


# Эндпоинт для добавления объектов(на которых будут вестись работы)
@app.post("/api/objects")
async def add_object(
        request: Request,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_session)
):
    data = await request.json()

    new_object = Object(
        obj_name=data["obj_name"],
        obj_city=data["obj_city"],
        obj_addres=data["obj_addres"],
        id_client=client.id_client
    )

    db.add(new_object)
    await db.commit()
    await db.refresh(new_object)

    return {
        "id_obj": new_object.id_obj,
        "obj_name": new_object.obj_name,
        "obj_city": new_object.obj_city,
        "obj_addres": new_object.obj_addres
    }

#личный кабинет пользователя
@app.get("/profile", response_class=HTMLResponse)
async def user_profile(
        request: Request,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_db),
        page: int = 1,
        objects_page: int = 1
):
    if not client:
        return RedirectResponse(url="/auth/login")

    # Основные параметры пагинации
    orders_per_page = 5
    objects_per_page = 3

    # Информация о клиенте
    client_info = {
        "full_name": f"{getattr(client, 'client_last_name', '')} {client.client_name}",
        "email": getattr(client, 'client_email', ''),
        "discount": getattr(client, 'discount', 0)  # Добавляем скидку
    }

    # Запрос заказов (сортировка по дате - новые сначала)
    orders_query = (
        select(Order)
        .where(Order.id_client == client.id_client)
        .options(selectinload(Order.object))
        .order_by(Order.ord_data.desc())
        .offset((page - 1) * orders_per_page)
        .limit(orders_per_page)
    )
    orders_result = await db.execute(orders_query)
    orders = orders_result.scalars().all()

    # Запрос объектов клиента (сортировка по ID)
    objects_query = (
        select(Object)
        .where(Object.id_client == client.id_client)
        .order_by(Object.id_obj.desc())
        .offset((objects_page - 1) * objects_per_page)
        .limit(objects_per_page)
    )
    objects_result = await db.execute(objects_query)
    client_objects = objects_result.scalars().all()

    # Подсчет общего количества заказов и объектов
    total_orders = (
        await db.execute(select(func.count()).select_from(Order).where(Order.id_client == client.id_client))).scalar()
    total_objects = (
        await db.execute(select(func.count()).select_from(Object).where(Object.id_client == client.id_client))).scalar()

    total_order_pages = max(1, (total_orders + orders_per_page - 1) // orders_per_page)
    total_object_pages = max(1, (total_objects + objects_per_page - 1) // objects_per_page)

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "client": client,
        "client_info": client_info,
        "orders": orders,
        "client_objects": client_objects,
        "current_page": min(page, total_order_pages),
        "objects_page": min(objects_page, total_object_pages),
        "total_order_pages": total_order_pages,
        "total_object_pages": total_object_pages,
        "now": datetime.now()
    })

#Детали заказа из личного кабинета
@app.get("/order_details/{order_id}", response_class=HTMLResponse)
async def order_details(
        request: Request,
        order_id: int,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_db)
):
    if not client:
        return RedirectResponse(url="/auth/login")

    # Получаем основной заказ с объектом
    order_query = (
        select(Order)
        .where(Order.id_order == order_id)
        .where(Order.id_client == client.id_client)
        .options(selectinload(Order.object)))

    order_result = await db.execute(order_query)
    order = order_result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    # Получаем материалы заказа с расчетом общей стоимости
    materials_query = (
        select(
            OrderMaterial,
            Material,
            (Material.material_price_of_one * OrderMaterial.ord_material_quantity).label("total_price")
        )
        .join(Material, OrderMaterial.id_material == Material.id_material)
        .where(OrderMaterial.id_order == order_id))

    materials_result = await db.execute(materials_query)
    order_materials = materials_result.all()

    # Получаем оборудование заказа с расчетом общей стоимости
    equipment_query = (
        select(
            OrderEquipment,
            Equipment,
            ((Equipment.equipment_ammortiz+ Equipment.equipment_transport_price_of_one) * OrderEquipment.ord_equipment_quantity).label("total_price")
        )
        .join(Equipment, OrderEquipment.id_equipment == Equipment.id_equipment)
        .where(OrderEquipment.id_order == order_id))

    equipment_result = await db.execute(equipment_query)
    order_equipment = equipment_result.all()

    # Получаем услуги заказа с расчетом общей стоимости
    services_query = (
        select(
            OrderService,
            Service,
            (Service.service_price * OrderService.ord_service_quantity).label("total_price")
        )
        .join(Service, OrderService.id_service == Service.id_service)
        .where(OrderService.id_order == order_id))

    services_result = await db.execute(services_query)
    order_services = services_result.all()

    # Подготавливаем данные для шаблона
    materials_data = []
    for order_material, material, total_price in order_materials:
        materials_data.append({
            "material": material,
            "ord_material_quantity": order_material.ord_material_quantity,
            "total_price": total_price,
            "unit_price": total_price/order_material.ord_material_quantity
        })

    equipment_data = []
    for order_equip, equip, total_price in order_equipment:
        equipment_data.append({
            "equipment": equip,
            "ord_equipment_quantity": order_equip.ord_equipment_quantity,
            "total_price": total_price,
            "unit_price": total_price/order_equip.ord_equipment_quantity
        })

    services_data = []
    for order_service, service, total_price in order_services:
        services_data.append({
            "service": service,
            "ord_service_quantity": order_service.ord_service_quantity,
            "total_price": total_price,
            "unit_price": service.service_price
        })

    return templates.TemplateResponse("order_details.html", {
        "request": request,
        "order": order,
        "client": client,
        "materials": materials_data,
        "equipment": equipment_data,
        "services": services_data
    })

#Данные о Материалах, Услугах и оборудование с главной страницы сайта(когда переходим с нее)
@app.get("/service-details", response_class=HTMLResponse)
async def service_details(
        request: Request,
        category: str,
        id: int,
        db: AsyncSession = Depends(get_db)
):
    service_data = load_service_data()
    # Определяем модель в зависимости от категории
    if category == "services":
        model = Service
        id_field = "id_service"
        name_field = "service_name"
        price_field = "service_price"
        unit_field = "service_units"
    elif category == "materials":
        model = Material
        id_field = "id_material"
        name_field = "material_name"
        price_field = "material_price_of_one"
        unit_field = "material_unit_quantity"
    elif category == "equipment":
        model = Equipment
        id_field = "id_equipment"
        name_field = "equipment_name"
        price_field = "equipment_ammortiz"
        # Для оборудования unit_field будет определяться динамически
    else:
        raise HTTPException(status_code=404, detail="Invalid category")

    try:
        # Получаем данные из базы
        query = select(model).where(getattr(model, id_field) == id)

        # Для услуг загружаем связанные материалы и оборудование
        if category == "services":
            query = query.options(
                selectinload(Service.materials).selectinload(ServiceMaterial.material),
                selectinload(Service.equipment_links).selectinload(ServiceEquipment.equipment)
            )

        result = await db.execute(query)
        item = result.scalars().first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Для оборудования определяем единицу измерения
        if category == "equipment":
            # Проверяем, является ли оборудование грузовиком
            if "грузовик" in getattr(item, "equipment_name").lower():
                unit = "рейс"
            else:
                unit = "смена"
        else:
            unit = getattr(item, unit_field)

        # Получаем данные из JSON
        category_key = {
            "services": "services",
            "materials": "materials",
            "equipment": "equipment"
        }.get(category, category)

        item_info = service_data.get(category_key, {}).get(str(id), {})
        description = item_info.get("description", f"Профессиональная {category[:-1]}: {getattr(item, name_field)}")
        image_path = item_info.get("image", "default.jpg")
        image = f"/static/{category}/{image_path}"

        # Форматируем данные для шаблона
        item_data = {
            "id": getattr(item, id_field),
            "name": getattr(item, name_field),
            "description": description,
            "price": getattr(item, price_field),
            "unit": unit,  # Используем динамически определенную единицу измерения
            "image": image,
            "category": category
        }

        # Для услуг добавляем связанные материалы и оборудование
        if category == "services":
            materials = []
            for sm in item.materials:
                materials.append({
                    "name": sm.material.material_name,
                    "quantity": sm.service_material_quantity,
                    "unit": sm.material.material_unit_quantity,
                    "price": sm.material.material_price_of_one
                })

            equipments = []
            for se in item.equipment_links:
                # Для оборудования в связанных услугах также определяем единицы
                equipment_unit = "рейс" if "грузовик" in se.equipment.equipment_name.lower() else "смена"
                equipments.append({
                    "name": se.equipment.equipment_name,
                    "quantity": se.service_equipment_quantity,
                    "price": se.equipment.equipment_ammortiz,
                    "unit": equipment_unit
                })

            item_data["materials"] = materials
            item_data["equipments"] = equipments

        return templates.TemplateResponse("service_details.html", {
            "request": request,
            "item": item_data,
            #"client": client
        })

    except Exception as e:
        print(f"Error in service_details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

##################################################################################################################
##################################################################################################################
#кастомный обработчик ошибок
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Если это редирект (307)
    if exc.status_code == status.HTTP_307_TEMPORARY_REDIRECT:
        return RedirectResponse(url=exc.headers["Location"])

    # Если это ошибка 401 (Unauthorized) и запрос HTML
    if exc.status_code == 401 and "text/html" in request.headers.get("accept", ""):
        return RedirectResponse(url="/auth/login?return_url=" + str(request.url))

    # Для API запросов возвращаем стандартный JSON
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

#Логгирование запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Received {request.method} request to {request.url}")
    response = await call_next(request)
    return response
##################################################################################################################
##################################################################################################################


#python main.py
# http://127.0.0.1:8000/docs
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)