from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List, Dict
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


# Базовые схемы для каждой модели

class BrigadeBase(BaseModel):
    brig_name: Optional[str] = None

class BrigadeCreate(BrigadeBase):
    pass

class Brigade(BrigadeBase):
    id_brig: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    ord_price: Optional[Decimal] = None  # Используем Decimal для дробных значений
    ord_data: Optional[date] = None
    id_client: int
    ord_status: Optional[str] = None
    ord_payment: Optional[Decimal] = None
    ord_prepayment: Optional[Decimal] = None
    id_obj: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id_order: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderBrigadeBase(BaseModel):
    brig_work_price: Optional[int] = None

class OrderBrigadeCreate(OrderBrigadeBase):
    id_brig: int
    id_order: int

class OrderBrigade(OrderBrigadeBase):
    id_brig: int
    id_order: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderMaterialBase(BaseModel):
    ord_material_quantity: Optional[int] = None

class OrderMaterialCreate(OrderMaterialBase):
    id_material: int
    id_order: int

class OrderMaterial(OrderMaterialBase):
    id_material: int
    id_order: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderEquipmentBase(BaseModel):
    ord_equipment_quantity: Optional[int] = None

class OrderEquipmentCreate(OrderEquipmentBase):
    id_equipment: int
    id_order: int

class OrderEquipment(OrderEquipmentBase):
    id_equipment: int
    id_order: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderServiceBase(BaseModel):
    ord_service_quantity: Optional[int] = None

class OrderServiceCreate(OrderServiceBase):
    id_service: int
    id_order: int

class OrderService(OrderServiceBase):
    id_service: int
    id_order: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class MaterialApplicationBase(BaseModel):
    applic_material_quantity: Optional[int] = None
    data_applic_material: Optional[date] = None
    id_provider: int
    id_postavka: int
    applic_material_status: Optional[str] = None

class MaterialApplicationCreate(MaterialApplicationBase):
    id_material: int

class MaterialApplication(MaterialApplicationBase):
    id_material: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class EquipmentApplicationBase(BaseModel):
    applic_equipment_quantity: Optional[int] = None
    data_applic_equipment: Optional[date] = None
    id_postavka: int
    applic_equipment_status: Optional[str] = None

class EquipmentApplicationCreate(EquipmentApplicationBase):
    id_provider: int
    id_equipment: int

class EquipmentApplication(EquipmentApplicationBase):
    id_provider: int
    id_equipment: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class ClientBase(BaseModel):
    client_last_name: Optional[str] = None
    client_name: Optional[str] = None
    client_mid_name: Optional[str] = None
    client_phone_number: Optional[str] = None
    client_self_sale: Optional[int] = None
    client_email: Optional[str] = None
    client_password: Optional[str] = None
    #права доступа
    is_user: bool = True
    is_admin: bool = False



class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id_client: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class MaterialBase(BaseModel):
    material_name: Optional[str] = None
    material_quantity: Optional[int] = None
    material_unit_quantity: Optional[str] = None
    id_postavka: int
    material_price_of_one: Optional[int] = None

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id_material: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class EquipmentBase(BaseModel):
    equipment_name: Optional[str] = None
    equipment_quant: Optional[int] = None
    equipment_use_start: Optional[date] = None
    equipment_use_end: Optional[date] = None
    equipment_ammortiz: Optional[int] = None
    equipment_buy_price: Optional[float] = None
    id_postavka: int

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id_equipment: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class ObjectBase(BaseModel):
    obj_name: Optional[str] = None
    obj_city: Optional[str] = None
    obj_addres: Optional[str] = None
    id_client: int

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id_obj: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class PostavkaBase(BaseModel):
    postavka_price: Optional[int] = None
    postavka_data: Optional[date] = None
    id_provider: int
    postavka_status: Optional[str] = None

class PostavkaCreate(PostavkaBase):
    pass

class Postavka(PostavkaBase):
    id_postavka: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class ProviderBase(BaseModel):
    provider_name: Optional[str] = None
    provider_debt_to_the_supplier: Optional[int] = None
    supplier_debt: Optional[int] = None
    provider_contact_person: Optional[str] = None  #
    provider_city: Optional[str] = None
    provider_email: Optional[str] = None
    provider_phone: Optional[str] = None

class ProviderCreate(ProviderBase):
    pass

class Provider(ProviderBase):
    id_provider: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class StaffBase(BaseModel):
    staff_last_name: Optional[str] = None
    staff_first_name: Optional[str] = None
    staff_phone_number: Optional[str] = None
    staff_post: Optional[str] = None
    staff_salary: Optional[int] = None
    staff_expirience: Optional[int] = None
    staff_mid_name: Optional[str] = None
    staff_passport_data: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id_staff: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class StaffBrigadeBase(BaseModel):
    pass

class StaffBrigadeCreate(StaffBrigadeBase):
    id_staff: int
    id_brig: int

class StaffBrigade(StaffBrigadeBase):
    id_staff: int
    id_brig: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class ServiceBase(BaseModel):
    service_name: Optional[str] = None
    service_units: Optional[str] = None
    service_price: Optional[int] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id_service: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

#############################################################################################################
#############################################################################################################
# Сложные схемы для комбинированных запросов

class OrderWithClient(BaseModel):
    order: OrderBase
    client: ClientBase

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderWithBrigade(BaseModel):
    order: OrderBase
    brigade: BrigadeBase

    class Config:
        model_config = ConfigDict(from_attributes=True)

class MaterialWithQuantity(BaseModel):
    material: MaterialBase
    quantity: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderWithTotalPrice(BaseModel):
    order: OrderBase
    total_price: float

    class Config:
        model_config = ConfigDict(from_attributes=True)

class PostavkaWithProvider(BaseModel):
    postavka: PostavkaBase
    provider: ProviderBase

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderWithClientAndObject(BaseModel):
    order: OrderBase
    client: ClientBase
    object: ObjectBase

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderWithBrigadeAndClient(BaseModel):
    order: OrderBase
    brigade: BrigadeBase
    client: ClientBase

    class Config:
        model_config = ConfigDict(from_attributes=True)

class OrderWithDetails(BaseModel):
    order: OrderBase
    materials: List[MaterialBase] = []
    equipments: List[EquipmentBase] = []
    services: List[ServiceBase] = []

    class Config:
        # Используем новый синтаксис для Pydantic V2
        model_config = ConfigDict(from_attributes=True)

class MaterialQuantityInput(BaseModel):
    materials: Dict[int, int]  # Ключ: id_material, Значение: количество

    model_config = ConfigDict(from_attributes=True)

#######################################################################################################################
########################################################################################################################

class MaterialInput(BaseModel):
    material_name: str
    quantity: int

class ServiceItem(BaseModel):
    service_name: str  # Название услуги
    quantity: int       # Количество услуги
class ServiceInput(BaseModel):
    services: List[ServiceItem]  # Список услуг

##
class MaterialInfo(BaseModel):
    material_name: str  # Название материала
    quantity: float       # Количество материала
    total_price: float  # Общая стоимость материала

class EquipmentInfo(BaseModel):
    equipment_name: str
    quantity: int
    total_price: float
class EquipmentInfo(BaseModel):
    equipment_name: str  # Название оборудования
    quantity: int        # Количество оборудования
    total_price: float   # Общая стоимость оборудования
    transport_price: float

class ServiceInfo(BaseModel):
    service_name: str  # Название Услуги
    quantity: int        # Количество Услуги
    total_price: float   # Общая стоимость Услуг

class ServicePriceResponse(BaseModel):
    service_name: str            # Название услуги
    total_service_price: float   # Общая стоимость услуги
    total_materials_cost: float  # Общая стоимость материалов
    total_equipment_cost: float  # Общая стоимость оборудования
    total_delivery_cost : float
    total_materials_delivery_cost : float
    total_equipment_delivery_cost : float
    total_cost: float            # Общая стоимость (услуга + материалы + оборудование)
    materials: List[MaterialInfo]  # Список материалов
    equipment: List[EquipmentInfo] # Список оборудования
    services: List[ServiceInfo]  # Добавляем поле для услуг

class EquipmentRequirement(BaseModel):
    equipment_name: str
    required_quantity: int  # Количество единиц оборудования
    required_trips: int     # Количество рейсов/использований
    total_cost: float

class EnhancedServicePriceResponse(ServicePriceResponse):
    #equipment_requirements: List[EquipmentRequirement]
    total_equipment_cost: float

# Новые модели для данных из Redis
class RedisMaterial(BaseModel):
    material_name: str  # Название материала
    quantity: float  # Количество материала
    total_price: float  # Общая стоимость материала

class RedisEquipment(BaseModel):
    equipment_name: str  # Название оборудования
    quantity: int  # Количество оборудования
    total_price: float  # Общая стоимость оборудования

class RedisService(BaseModel):
    service_name: str  # Название услуги
    quantity: int  # Количество услуг
    total_price: float  # Общая стоимость услуги

class RedisOrder(BaseModel):
    total_cost: float  # Общая стоимость заказа
    materials: List[RedisMaterial]  # Список материалов
    equipment: List[RedisEquipment]  # Список оборудования
    services: List[RedisService] = []  # Список услуг (необязательное поле)

# Модели для создания связей в базе данных
class OrderMaterialCreate(BaseModel):
    id_material: int  # ID материала
    id_order: int  # ID заказа
    ord_material_quantity: int  # Количество материала

class OrderEquipmentCreate(BaseModel):
    id_equipment: int  # ID оборудования
    id_order: int  # ID заказа
    ord_equipment_quantity: int  # Количество оборудования

class OrderServiceCreate(BaseModel):
    id_service: int  # ID услуги
    id_order: int  # ID заказа
    ord_service_quantity: int  # Количество услуг