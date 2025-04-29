from typing import Optional, List, Dict

from fastapi import APIRouter, Request, Depends, HTTPException, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from models import (
    Material, Equipment, Provider,
    MaterialApplication, EquipmentApplication,
    Client, Postavka
)
from users.dependencies import get_current_client
from database import get_db
from datetime import datetime
import json

router = APIRouter(
    prefix="/super_user",
    tags=["super_user"]
)

templates = Jinja2Templates(directory='templates')

@router.get("/create_supply", response_class=HTMLResponse)
async def create_supply_request(
    request: Request,
    client: Client = Depends(get_current_client),
    db: AsyncSession = Depends(get_db)
):
    if not client or not client.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    # Получаем материалы, оборудование и поставщиков
    materials = await db.execute(select(Material))
    equipment = await db.execute(select(Equipment))
    providers = await db.execute(select(Provider))

    return templates.TemplateResponse("add_application.html", {
        "request": request,
        "materials": materials.scalars().all(),
        "equipment": equipment.scalars().all(),
        "providers": providers.scalars().all(),
        "now": datetime.now()
    })


from pydantic import BaseModel


class SupplyRequest(BaseModel):
    provider_id: int
    materials: Optional[List[Dict[str, int]]] = None
    equipment: Optional[List[Dict[str, int]]] = None


# super_user_router.py
@router.post("/submit_supply")
async def submit_supply_request(
        request: Request,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_db)
):
    if not client or not client.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    try:
        data = await request.json()
        provider_id = data.get('provider_id')
        materials = data.get('materials', [])
        equipment = data.get('equipment', [])

        if not provider_id:
            raise HTTPException(status_code=400, detail="Не выбран поставщик")

        # Получаем максимальный ID из обеих таблиц
        max_material_id = await db.execute(select(func.max(MaterialApplication.id_applic_material)))
        max_equipment_id = await db.execute(select(func.max(EquipmentApplication.id_applic_equipment)))

        max_id = max(
            max_material_id.scalar() or 0,
            max_equipment_id.scalar() or 0
        )
        common_applic_id = max_id + 1
        current_date = datetime.now().date()

        # Обработка материалов
        for item in materials:
            material_app = MaterialApplication(
                id_applic_material=common_applic_id,
                id_material=item["material_id"],
                id_provider=provider_id,
                applic_material_quantity=item["quantity"],
                data_applic_material=current_date,
                applic_material_status="Ожидает поставки",
                id_postavka=None
            )
            db.add(material_app)

        # Обработка оборудования
        for item in equipment:
            equipment_app = EquipmentApplication(
                id_applic_equipment=common_applic_id,
                id_equipment=item["equipment_id"],
                id_provider=provider_id,
                applic_equipment_quantity=item["quantity"],
                data_applic_equipment=current_date,
                applic_equipment_status="Ожидает поставки",
                id_postavka=None
            )
            db.add(equipment_app)

        await db.commit()

        return JSONResponse({
            "status": "success",
            "application_id": common_applic_id,
            "redirect_url": f"/super_user/supply_confirmation/{common_applic_id}"
        })

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка при создании заявки: {str(e)}")


@router.get("/supply_confirmation/{applic_id}", response_class=HTMLResponse)
async def supply_confirmation(
        request: Request,
        applic_id: int,
        client: Client = Depends(get_current_client),
        db: AsyncSession = Depends(get_db)
):
    if not client or not client.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    try:
        # Получаем все материалы заявки
        materials_result = await db.execute(
            select(MaterialApplication, Material)
            .join(Material)
            .where(MaterialApplication.id_applic_material == applic_id)
        )
        materials = materials_result.all()

        # Получаем все оборудование заявки
        equipment_result = await db.execute(
            select(EquipmentApplication, Equipment)
            .join(Equipment)
            .where(EquipmentApplication.id_applic_equipment == applic_id)
        )
        equipment = equipment_result.all()

        if not materials and not equipment:
            raise HTTPException(status_code=404, detail="Заявка не найдена")

        # Получаем информацию о поставщике из первой найденной записи
        provider_id = None
        application_date = None

        if materials:
            provider_id = materials[0][0].id_provider
            application_date = materials[0][0].data_applic_material
        elif equipment:
            provider_id = equipment[0][0].id_provider
            application_date = equipment[0][0].data_applic_equipment

        provider = await db.get(Provider, provider_id) if provider_id else None

        # Считаем общую стоимость
        total_cost = 0
        for mat_app, material in materials:
            total_cost += mat_app.applic_material_quantity * material.material_price_of_one
        for equip_app, equip in equipment:
            total_cost += equip_app.applic_equipment_quantity * equip.equipment_ammortiz

        return templates.TemplateResponse(
            "supply_confirmation.html",
            {
                "request": request,
                "application_id": applic_id,
                "provider": provider,
                "materials": materials,
                "equipment": equipment,
                "total_cost": total_cost,
                "application_date": application_date,
                "now": datetime.now()
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных заявки: {str(e)}")