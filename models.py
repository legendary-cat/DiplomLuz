from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Sequence, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Brigade(Base):
    __tablename__ = 'Бригады'
    id_brig = Column(Integer, primary_key=True)
    brig_name = Column(String(20), nullable=True)
    employees = relationship("StaffBrigade", back_populates="brigade")
    orders = relationship("OrderBrigade", back_populates="brigade")

class Order(Base):
    __tablename__ = 'Заказы'
    id_order = Column(Integer, primary_key=True)
    ord_price = Column(Integer, nullable=True)
    ord_data = Column(Date, nullable=True)
    id_client = Column(Integer, ForeignKey('Клиенты.id_client'), nullable=False)
    ord_status = Column(String(20), nullable=True)
    ord_payment = Column(Integer, nullable=True)
    ord_prepayment = Column(Integer, nullable=True)
    id_obj = Column(Integer, ForeignKey('Объекты.id_obj'), nullable=False)
    client = relationship("Client", back_populates="orders")
    object = relationship("Object", back_populates="orders")
    brigades = relationship("OrderBrigade", back_populates="order")
    materials = relationship("OrderMaterial", back_populates="order")
    equipments = relationship("OrderEquipment", back_populates="order")
    services = relationship("OrderService", back_populates="order")

class OrderBrigade(Base):
    __tablename__ = 'Заказы_Бригады'
    id_brig = Column(Integer, ForeignKey('Бригады.id_brig'), primary_key=True)
    id_order = Column(Integer, ForeignKey('Заказы.id_order'), primary_key=True)
    brig_work_price = Column(Integer, nullable=True)
    brigade = relationship("Brigade", back_populates="orders")
    order = relationship("Order", back_populates="brigades")

class OrderMaterial(Base):
    __tablename__ = 'Заказы_Материалы'
    id_material = Column(Integer, ForeignKey('Материалы.id_material'), primary_key=True)
    id_order = Column(Integer, ForeignKey('Заказы.id_order'), primary_key=True)
    ord_material_quantity = Column(Integer, nullable=True)
    material = relationship("Material", back_populates="orders")
    order = relationship("Order", back_populates="materials")

class OrderEquipment(Base):
    __tablename__ = 'Заказы_Оборудование'
    id_equipment = Column(Integer, ForeignKey('Оборудование.id_equipment'), primary_key=True)
    id_order = Column(Integer, ForeignKey('Заказы.id_order'), primary_key=True)
    ord_equipment_quantity = Column(Integer, nullable=True)
    equipment = relationship("Equipment", back_populates="orders")
    order = relationship("Order", back_populates="equipments")

class OrderService(Base):
    __tablename__ = 'Заказы_Услуги'
    id_service = Column(Integer, ForeignKey('Услуги.id_service'), primary_key=True)
    id_order = Column(Integer, ForeignKey('Заказы.id_order'), primary_key=True)
    ord_service_quantity = Column(Integer, nullable=True)
    service = relationship("Service", back_populates="orders")
    order = relationship("Order", back_populates="services")

class MaterialApplication(Base):
    __tablename__ = 'Заявка_на_поставку_материалов'
    id_applic_material = Column(Integer, primary_key=True, autoincrement=True)#
    id_material = Column(Integer, ForeignKey('Материалы.id_material'), primary_key=True)#
    applic_material_quantity = Column(Integer, nullable=True)
    data_applic_material = Column(Date, nullable=True)
    id_provider = Column(Integer, ForeignKey('Поставщики.id_provider'), primary_key=True)#
    id_postavka = Column(Integer, ForeignKey('Поставки.id_postavka'), nullable=False)
    applic_material_status = Column(String(20), nullable=True)

    ################################################################################
    provider = relationship("Provider", back_populates="material_applications")
    postavka = relationship("Postavka", back_populates="material_applications")
    material = relationship("Material", back_populates="material_applications")

class EquipmentApplication(Base):
    __tablename__ = 'Заявка_на_поставку_оборудования'
    id_applic_equipment = Column(Integer, primary_key=True, autoincrement=True)#
    id_provider = Column(Integer, ForeignKey('Поставщики.id_provider'), primary_key=True)#
    id_equipment = Column(Integer, ForeignKey('Оборудование.id_equipment'), primary_key=True)#
    applic_equipment_quantity = Column(Integer, nullable=True)
    data_applic_equipment = Column(Date, nullable=True)
    id_postavka = Column(Integer, ForeignKey('Поставки.id_postavka'), nullable=False)
    applic_equipment_status = Column(String(20), nullable=True)

    #######################################################################################
    provider = relationship("Provider", back_populates="equipment_applications")
    postavka = relationship("Postavka", back_populates="equipment_applications")
    equipment_rel = relationship("Equipment")  # Измененное имя отношения

class Client(Base):
    __tablename__ = 'Клиенты'
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    client_last_name = Column(String(20), nullable=True)
    client_name = Column(String(20), nullable=True)
    client_mid_name = Column(String(20), nullable=True)
    client_phone_number = Column(String(20), nullable=True)
    client_self_sale = Column(Integer, nullable=True)
    orders = relationship("Order", back_populates="client")
    objects = relationship("Object", back_populates="client")
    client_email = Column(String(50), nullable=True)
    client_password = Column(String(255), nullable=True)

    # Права доступа
    is_user = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    #is_super_admin = Column(Boolean, default=False)
    #вот тут может быть пробелма
    orders = relationship("Order", back_populates="client")
    objects = relationship("Object", back_populates="client")

class Material(Base):
    __tablename__ = 'Материалы'
    id_material = Column(Integer, primary_key=True)
    material_name = Column(String(20), nullable=True)
    material_quantity = Column(Integer, nullable=True)
    material_unit_quantity = Column(String(20), nullable=True)
    id_postavka = Column(Integer, ForeignKey('Поставки.id_postavka'), nullable=False)
    material_price_of_one = Column(Integer, nullable=True)
    material_transport_volume = Column(Numeric, nullable=True)

    postavka = relationship("Postavka", back_populates="materials")
    orders = relationship("OrderMaterial", back_populates="material")
    services = relationship("ServiceMaterial", back_populates="material")

    ##
    material_applications = relationship("MaterialApplication", back_populates="material")

class Equipment(Base):
    __tablename__ = 'Оборудование'
    id_equipment = Column(Integer, primary_key=True)
    equipment_name = Column(String(20), nullable=True)
    equipment_quant = Column(Integer, nullable=True)
    equipment_use_start = Column(Date, nullable=True)
    equipment_use_end = Column(Date, nullable=True)
    equipment_ammortiz = Column(Integer, nullable=True)
    equipment_capacity = Column(Integer, nullable=True)
    equipment_transport_price_of_one = Column(Numeric, nullable=True)
    equipment_buy_price = Column(Numeric, nullable=True)

    id_postavka = Column(Integer, ForeignKey('Поставки.id_postavka'), nullable=False)
    postavka = relationship("Postavka", back_populates="equipments")
    orders = relationship("OrderEquipment", back_populates="equipment")
    service_links = relationship("ServiceEquipment", back_populates="equipment")
    applications = relationship("EquipmentApplication", back_populates="equipment_rel")

class Object(Base):
    __tablename__ = 'Объекты'
    id_obj = Column(Integer, primary_key=True)
    obj_name = Column(String(20), nullable=True)
    obj_city = Column(String(20), nullable=True)
    obj_addres = Column(String(18), nullable=True)
    id_client = Column(Integer, ForeignKey('Клиенты.id_client'), nullable=False)
    client = relationship("Client", back_populates="objects")
    orders = relationship("Order", back_populates="object")

class Postavka(Base):
    __tablename__ = 'Поставки'
    id_postavka = Column(Integer, primary_key=True)
    postavka_price = Column(Integer, nullable=True)
    postavka_data = Column(Date, nullable=True)
    id_provider = Column(Integer, ForeignKey('Поставщики.id_provider'), nullable=False)
    postavka_status = Column(String(20), nullable=True)
    provider = relationship("Provider", back_populates="postavkas")
    materials = relationship("Material", back_populates="postavka")
    equipments = relationship("Equipment", back_populates="postavka")
    material_applications = relationship("MaterialApplication", back_populates="postavka")  # Добавлено
    equipment_applications = relationship("EquipmentApplication", back_populates="postavka")  # Добавлено

class Provider(Base):
    __tablename__ = 'Поставщики'
    id_provider = Column(Integer, primary_key=True)
    provider_name = Column(String(20), nullable=True)
    provider_debt_to_the_supplier = Column(Integer, nullable=True)
    supplier_debt = Column(Integer, nullable=True)
    postavkas = relationship("Postavka", back_populates="provider")
    material_applications = relationship("MaterialApplication", back_populates="provider")
    equipment_applications = relationship("EquipmentApplication", back_populates="provider")

class Staff(Base):
    __tablename__ = 'Сотрудники'
    id_staff = Column(Integer, primary_key=True)
    staff_last_name = Column(String(20), nullable=True)
    staff_first_name = Column(String(20), nullable=True)
    staff_phone_number = Column(String(20), nullable=True)
    staff_post = Column(String(20), nullable=True)
    staff_salary = Column(Integer, nullable=True)
    staff_expirience = Column(Integer, nullable=True)
    staff_mid_name = Column(String(20), nullable=True)
    staff_passport_data = Column(String(20), nullable=True)
    brigades = relationship("StaffBrigade", back_populates="staff")

class StaffBrigade(Base):
    __tablename__ = 'Сотрудники_Бригады'
    id_staff = Column(Integer, ForeignKey('Сотрудники.id_staff'), primary_key=True)
    id_brig = Column(Integer, ForeignKey('Бригады.id_brig'), primary_key=True)
    staff = relationship("Staff", back_populates="brigades")
    brigade = relationship("Brigade", back_populates="employees")

class Service(Base):
    __tablename__ = 'Услуги'
    id_service = Column(Integer, primary_key=True)
    service_name = Column(String(20), nullable=True)
    service_units = Column(String(20), nullable=True)
    service_price = Column(Numeric, nullable=True)
    orders = relationship("OrderService", back_populates="service")
    materials = relationship("ServiceMaterial", back_populates="service")
    equipment_links = relationship("ServiceEquipment", back_populates="service")
##################################################################################################
class ServiceMaterial(Base):
    __tablename__ = 'Услуги_Материалы'
    id_service = Column(Integer, ForeignKey('Услуги.id_service'), primary_key=True)
    id_material = Column(Integer, ForeignKey('Материалы.id_material'), primary_key=True)
    service_material_quantity = Column(Numeric, nullable=False)  # Количество материала для услуги

    service = relationship("Service", back_populates="materials")
    material = relationship("Material", back_populates="services")

class ServiceEquipment(Base):
    __tablename__ = 'Услуги_Оборудование'
    id_service = Column(Integer, ForeignKey('Услуги.id_service'), primary_key=True)
    id_equipment = Column(Integer, ForeignKey('Оборудование.id_equipment'), primary_key=True)
    service_equipment_quantity = Column(Numeric, nullable=False)  # Количество оборудования для услуги

    service = relationship("Service", back_populates="equipment_links")
    equipment = relationship("Equipment", back_populates="service_links")

