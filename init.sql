-- Инициализация базы данных LuzDiplom
-- Упрощенная версия без неподдерживаемых команд

-- Создание основных таблиц
CREATE TABLE IF NOT EXISTS "Бригады" (
    id_brig INTEGER PRIMARY KEY,
    brig_name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "Клиенты" (
    id_client SERIAL PRIMARY KEY,
    client_last_name VARCHAR(20),
    client_name VARCHAR(20),
    client_mid_name VARCHAR(20),
    client_phone_number VARCHAR(20),
    client_self_sale INTEGER,
    client_email VARCHAR(50),
    client_password VARCHAR(255),
    is_user BOOLEAN,
    is_admin BOOLEAN
);

CREATE TABLE IF NOT EXISTS "Объекты" (
    id_obj SERIAL PRIMARY KEY,
    obj_name VARCHAR(30),
    obj_city VARCHAR(30),
    obj_addres VARCHAR(30),
    id_client INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "Поставщики" (
    id_provider INTEGER PRIMARY KEY,
    provider_name VARCHAR(20),
    provider_debt_to_the_supplier INTEGER,
    supplier_debt INTEGER,
    provider_contact_person VARCHAR(50),
    provider_city VARCHAR(20),
    provider_email VARCHAR(50),
    provider_phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "Поставки" (
    id_postavka INTEGER PRIMARY KEY,
    postavka_price INTEGER,
    postavka_data DATE,
    id_provider INTEGER NOT NULL,
    postavka_status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "Материалы" (
    id_material INTEGER PRIMARY KEY,
    material_name VARCHAR(50),
    material_quantity INTEGER,
    material_unit_quantity VARCHAR(20),
    id_postavka INTEGER NOT NULL,
    material_price_of_one INTEGER,
    material_transport_volume NUMERIC
);

CREATE TABLE IF NOT EXISTS "Оборудование" (
    id_equipment INTEGER PRIMARY KEY,
    equipment_name VARCHAR(50),
    equipment_quant INTEGER,
    equipment_use_start DATE,
    equipment_use_end DATE,
    equipment_ammortiz INTEGER,
    id_postavka INTEGER NOT NULL,
    equipment_capacity INTEGER,
    equipment_transport_price_of_one NUMERIC,
    equipment_buy_price NUMERIC
);

CREATE TABLE IF NOT EXISTS "Услуги" (
    id_service INTEGER PRIMARY KEY,
    service_name VARCHAR(60),
    service_units VARCHAR(20),
    service_price NUMERIC
);

CREATE TABLE IF NOT EXISTS "Сотрудники" (
    id_staff INTEGER PRIMARY KEY,
    staff_last_name VARCHAR(18),
    staff_first_name VARCHAR(20),
    staff_phone_number VARCHAR(20),
    staff_post VARCHAR(20),
    staff_salary INTEGER,
    staff_expirience INTEGER,
    staff_mid_name VARCHAR(20),
    staff_passport_data VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "Сотрудники_Бригады" (
    id_staff INTEGER NOT NULL,
    id_brig INTEGER NOT NULL,
    PRIMARY KEY (id_staff, id_brig)
);

CREATE TABLE IF NOT EXISTS "Заказы" (
    id_order SERIAL PRIMARY KEY,
    ord_price NUMERIC,
    ord_data DATE,
    id_client INTEGER NOT NULL,
    ord_status VARCHAR(20),
    ord_payment NUMERIC,
    ord_prepayment NUMERIC,
    id_obj INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "Заказы_Бригады" (
    id_brig INTEGER NOT NULL,
    id_order INTEGER NOT NULL,
    brig_work_price INTEGER,
    PRIMARY KEY (id_brig, id_order)
);

CREATE TABLE IF NOT EXISTS "Заказы_Материалы" (
    id_material INTEGER NOT NULL,
    ord_material_quantity INTEGER,
    id_order INTEGER NOT NULL,
    PRIMARY KEY (id_material, id_order)
);

CREATE TABLE IF NOT EXISTS "Заказы_Оборудование" (
    id_equipment INTEGER NOT NULL,
    ord_equipment_quantity INTEGER,
    id_order INTEGER NOT NULL,
    PRIMARY KEY (id_equipment, id_order)
);

CREATE TABLE IF NOT EXISTS "Заказы_Услуги" (
    id_service INTEGER NOT NULL,
    id_order INTEGER NOT NULL,
    ord_service_quantity INTEGER,
    PRIMARY KEY (id_service, id_order)
);

CREATE TABLE IF NOT EXISTS "Услуги_Материалы" (
    id_service INTEGER NOT NULL,
    id_material INTEGER NOT NULL,
    service_material_quantity NUMERIC,
    PRIMARY KEY (id_service, id_material)
);

CREATE TABLE IF NOT EXISTS "Услуги_Оборудование" (
    id_service INTEGER NOT NULL,
    id_equipment INTEGER NOT NULL,
    service_equipment_quantity NUMERIC,
    PRIMARY KEY (id_service, id_equipment)
);

-- Вставка данных
INSERT INTO "Бригады" (id_brig, brig_name) VALUES
(1, 'Водители 1'),
(2, 'Строители 1');

INSERT INTO "Клиенты" (id_client, client_last_name, client_name, client_mid_name, client_phone_number, client_self_sale, client_email, client_password, is_user, is_admin) VALUES
(1, 'Колпаков', 'Мирослав', 'Владимирович', '+76772226677', 0, 'sadsad@gmail.com', '$2b$12$y.HLDqpoUcKnEVZu2nuKM.M1650zczNWS4FOGcBDPrZ2gnxlsNJcW', true, true),
(2, 'Шапира', 'Нета', 'Иосифович', '+9723377733', 0, '33dota2@gmail.com', '$2b$12$b1Rrc8z1vSIb65lZvj.9K.CN0sR0V8qYOgFI0BgivXnsqy3Vlu5.u', true, false),
(3, 'Зубенко', 'Михаил', 'Петрович', '88005553535', 0, 'zubenko228@gmai.com', '$2b$12$FxpnGmPOFMM6GOwhdpQYXe7UXfiW37rK4JhTR19enozFaekv5yFM.', true, false),
(4, 'Форелева', 'Семга', 'Лососевна', '89696969696', 0, 'Pupochkazalupochka69@ok.ru', '$2b$12$tKzdHA.xdLML9wOv42xLV.UdFrx8k.u1uHXm6KPzZpcOhecUxtRwa', true, false),
(5, 'Робенович', 'Геннадий', 'Петрович', '88775557575', 0, 'test123@gmail.com', '$2b$12$YYQgD1KKyyKqzH83Tar54.EMzWe4JAwjlZKrnK6WdYr90QBgtrIqG', true, false),
(6, 'ТАМАЕВ', 'АЯЗ', 'Кадрович', '88007776565', 0, '50PROcentFiuchMaster@gamer.com', '$2b$12$FGxQ8QGUX51Zkae6Itl2V.t8qkifaSyO2kir65QVu3VEXPD0PlKVm', true, false),
(7, 'Ойойой', 'Бобрито', 'Бандито', '7896456778', 0, 'moxnatyieyaichki@gmail.com', '$2b$12$Mte/EezjFKGEDB9aS8zWjOwD07NF7IZ1g0FfoqAMbWsl.DTJ3NXmu', true, false),
(8, 'Шкредов', 'Сахур', 'ТУТУТУТУТУТУТУНОВИЧ', '78964567787', 0, 'timofei.vereshchagin@gmail.com', '$2b$12$JhnO.0TlauEbIymZEck8MuX0jfTt7rH5cVOoAmkNHxaFpYiNRO0HC', true, false),
(9, 'Лузин', 'Иван', 'Николаевич', '+7 (999) 123-33-33', 0, 'saderwent97@mail.ru', '$2b$12$boCXHw1QPv4OjXD5uj5RY.wnGTQhrZxTmflv3jXViTpsfVIFn2CcW', true, false);

INSERT INTO "Объекты" (id_obj, obj_name, obj_city, obj_addres, id_client) VALUES
(1, 'Мост', 'Москва', 'ул. Пушкина', 1),
(2, 'Дорога', 'Москва', 'Ул. Колотушкина', 1),
(3, 'Шоссе', 'Москва', 'Ул. Арбат', 1),
(4, 'Частный дом', 'Люберцы', 'Ул. Капибарова дом 69', 1),
(5, 'Трасса М2', 'Москва', 'Трасса', 1),
(6, 'Дорога куда-то', 'Москва', 'Обочина', 1),
(7, 'Рыбная дача', 'Рыбинск', 'Улица речная дом 69', 4),
(8, 'Рыбинская АЭС', 'Вельск', 'ул. Залупкина 69 к.2', 6),
(9, 'Общага', 'Рыбинск', 'ул. Валорантреская 15', 6),
(10, 'МКАД', 'Москва', 'МОЙ ДОМ МОЯ РАБОТА МОЙ ХЛЕБ!!!', 7),
(11, 'Трасса Е95 (дом Хача)', 'Москва', 'ул. Ленина д.1', 8),
(12, 'Стрим-хата', 'Москва', 'ул. Чилловая д.2', 1),
(13, 'Частный дом', 'ставрополь', 'мне лень думать я объелась', 4),
(14, 'Дача', 'Москва', 'Улица Парусная дом 3', 9);

INSERT INTO "Поставщики" (id_provider, provider_name, provider_debt_to_the_supplier, supplier_debt, provider_contact_person, provider_city, provider_email, provider_phone) VALUES
(1, 'ТИМ СПИРИТ', 0, 0, NULL, NULL, NULL, NULL),
(2, 'ТУНДРА', 0, 0, NULL, NULL, NULL, NULL);

INSERT INTO "Поставки" (id_postavka, postavka_price, postavka_data, id_provider, postavka_status) VALUES
(1, 450, '2025-01-14', 1, 'Поставлено');

INSERT INTO "Материалы" (id_material, material_name, material_quantity, material_unit_quantity, id_postavka, material_price_of_one, material_transport_volume) VALUES
(1, 'Песок', 400, 'м³', 1, 1100, 1),
(2, 'Щебень', 150, 'м³', 1, 1500, 1),
(3, 'Гравий', 350, 'м³', 1, 1700, 1),
(4, 'Дорожный бардюр Фабрика «Готика»', 700, 'штука', 1, 270, 0.4),
(5, 'Тратуарный бордюр Фабрика «Готика»', 450, 'штука', 1, 320, 0.5),
(6, 'Тратуарная плитка Фабрика «Готика»', 500, 'штука', 1, 200, 0.25),
(7, 'Асфальтовая смесь', 900, 'м³', 1, 3500, 0.20),
(8, 'Смесь асфальтобетонная горячая крупнозернистая', 4000, 'м³', 1, 4500, 1),
(9, 'Геотекстиль', 8000, 'м²', 1, 30, 0.1),
(10, 'Битумная эмульсия', 7000, 'м³', 1, 20, 1),
(11, 'Арматура', 2000, 'шт', 1, 500, 0.1),
(12, 'Анкерные болты', 3000, 'шт', 1, 25, 0.01),
(13, 'Рубероид', 500, 'м³', 1, 100, 1),
(14, 'Цемент', 300, 'м³', 1, 3000, 1),
(15, 'Краска', 300, 'м²', 1, 150, 1),
(16, 'Бетон', 250, 'м³', 1, 350, 1);

INSERT INTO "Оборудование" (id_equipment, equipment_name, equipment_quant, equipment_use_start, equipment_use_end, equipment_ammortiz, id_postavka, equipment_capacity, equipment_transport_price_of_one, equipment_buy_price) VALUES
(1, 'Асфальтоукладчик', 5, '2023-06-14', '2027-10-18', 50, 1, 100, 100, 12000000),
(2, 'Грузовик', 3, '2023-06-14', '2028-07-14', 60, 1, 35, 300, 7000000),
(3, 'Каток', 3, '2023-06-14', '2027-11-12', 55, 1, 100, 100, 2500000),
(4, 'Дорожная фреза', 2, '2023-06-14', '2026-12-31', 50, 1, 150, 150, 15000000),
(5, 'Кохер для асфальта', 2, '2023-06-14', '2026-12-31', 55, 1, 100, 100, 10000000),
(6, 'Экскаватор-погрузчик', 4, '2023-06-14', '2027-11-12', 50, 1, 100, 130, 6500000),
(7, 'Трактор-экскаватор', 3, '2023-06-14', '2027-11-12', 50, 1, 100, 125, 5700000),
(8, 'Бетономешалка', 5, '2023-06-14', '2026-12-31', 70, 1, 150, 60, 1100000),
(9, 'Виброплита', 12, '2023-06-14', '2026-12-31', 30, 1, 100, 20, 38000),
(10, 'Резиновая киянка', 30, '2023-06-14', '2029-10-11', 5, 1, 50, 5, 300),
(11, 'Разметочная машина', 7, '2023-06-14', '2027-11-12', 40, 1, 150, 50, 135000),
(12, 'Автовышка', 3, '2023-06-14', '2027-10-18', 30, 1, 100, 100, 3800000),
(13, 'Бетоносмесительная установка', 4, '2023-06-14', '2027-10-18', 40, 1, 100, 130, 450000);

INSERT INTO "Услуги" (id_service, service_name, service_units, service_price) VALUES
(1, 'Доставка материалов', 'руб/м³', 20),
(4, 'Укладка асфальта', 'руб/м²', 100),
(5, 'Двухслойное асфальтирование', 'руб/м²', 150),
(6, 'Ямочный ремонт', 'руб/м²', 80),
(7, 'Асфальтирование частных территорий', 'руб/м³', 180),
(8, 'Транспортировка спецтехники', 'руб/рейс', 5000),
(9, 'Установка дорожного бордюра', 'руб/м²', 100),
(10, 'Установка тротуарного бордюра', 'руб/м²', 100),
(11, 'Укладка тротуарной плитки', 'руб/м²', 110),
(12, 'Нанесение разметки краской', 'руб/м²', 30),
(13, 'Установка дорожных знаков', 'руб/штука', 50),
(14, 'Вывоз строительного мусора', 'руб/рейс', 5000),
(15, 'Разработка асфальтобетонного покрытия толщ. 5 см. ручная', 'руб/м²', 450),
(16, 'Фрезерование асфальтобетонного покрытия толщ. 5 см.', 'руб/м²', 150),
(17, 'Доставка оборудования и спецтехники', 'руб/штуку', 7000);

INSERT INTO "Сотрудники" (id_staff, staff_last_name, staff_first_name, staff_phone_number, staff_post, staff_salary, staff_expirience, staff_mid_name, staff_passport_data) VALUES
(1, 'Халилов', 'Магомед', '89152581395', 'водитель', 55000, 5, 'Мурадович', '6263123199'),
(2, 'Шкредов', 'Антон', '89192563213', 'водитель', 53000, 4, 'Алексеевич', '6162345611'),
(3, 'Найденов', 'Ярослав', '88001293411', 'рабочий', 67000, 9, 'Сергеевич', '4246322322'),
(4, 'Малерчук', 'Илья', '89993124455', 'рабочий', 65000, 7, 'Владимирович', '4512345199'),
(5, 'Сигитов', 'Денис', '89131251432', 'рабочий', 64000, 6, 'Владимирович', '5412777912');

INSERT INTO "Сотрудники_Бригады" (id_staff, id_brig) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 2);

-- Добавление внешних ключей
ALTER TABLE "Объекты" ADD CONSTRAINT fk_objects_clients FOREIGN KEY (id_client) REFERENCES "Клиенты"(id_client);
ALTER TABLE "Заказы" ADD CONSTRAINT fk_orders_clients FOREIGN KEY (id_client) REFERENCES "Клиенты"(id_client);
ALTER TABLE "Заказы" ADD CONSTRAINT fk_orders_objects FOREIGN KEY (id_obj) REFERENCES "Объекты"(id_obj);
ALTER TABLE "Заказы_Бригады" ADD CONSTRAINT fk_order_brigades_brigades FOREIGN KEY (id_brig) REFERENCES "Бригады"(id_brig);
ALTER TABLE "Заказы_Бригады" ADD CONSTRAINT fk_order_brigades_orders FOREIGN KEY (id_order) REFERENCES "Заказы"(id_order);
ALTER TABLE "Заказы_Материалы" ADD CONSTRAINT fk_order_materials_materials FOREIGN KEY (id_material) REFERENCES "Материалы"(id_material);
ALTER TABLE "Заказы_Материалы" ADD CONSTRAINT fk_order_materials_orders FOREIGN KEY (id_order) REFERENCES "Заказы"(id_order);
ALTER TABLE "Заказы_Оборудование" ADD CONSTRAINT fk_order_equipment_equipment FOREIGN KEY (id_equipment) REFERENCES "Оборудование"(id_equipment);
ALTER TABLE "Заказы_Оборудование" ADD CONSTRAINT fk_order_equipment_orders FOREIGN KEY (id_order) REFERENCES "Заказы"(id_order);
ALTER TABLE "Заказы_Услуги" ADD CONSTRAINT fk_order_services_services FOREIGN KEY (id_service) REFERENCES "Услуги"(id_service);
ALTER TABLE "Заказы_Услуги" ADD CONSTRAINT fk_order_services_orders FOREIGN KEY (id_order) REFERENCES "Заказы"(id_order);
ALTER TABLE "Материалы" ADD CONSTRAINT fk_materials_deliveries FOREIGN KEY (id_postavka) REFERENCES "Поставки"(id_postavka);
ALTER TABLE "Оборудование" ADD CONSTRAINT fk_equipment_deliveries FOREIGN KEY (id_postavka) REFERENCES "Поставки"(id_postavka);
ALTER TABLE "Поставки" ADD CONSTRAINT fk_deliveries_providers FOREIGN KEY (id_provider) REFERENCES "Поставщики"(id_provider);
ALTER TABLE "Сотрудники_Бригады" ADD CONSTRAINT fk_staff_brigades_staff FOREIGN KEY (id_staff) REFERENCES "Сотрудники"(id_staff);
ALTER TABLE "Сотрудники_Бригады" ADD CONSTRAINT fk_staff_brigades_brigades FOREIGN KEY (id_brig) REFERENCES "Бригады"(id_brig);