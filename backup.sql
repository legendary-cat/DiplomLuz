--
-- PostgreSQL database dump
--

\restrict Mu8BrHl3cEJ51u9VOnodWhO22M8FiPWjwdaVFXXL73VmdBe3nBsELbFhlnAgDIS

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.6 (Debian 17.6-2.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Бригады; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Бригады" (
    id_brig integer NOT NULL,
    brig_name character varying(20)
);


ALTER TABLE public."Бригады" OWNER TO postgres;

--
-- Name: Заказы; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заказы" (
    id_order integer NOT NULL,
    ord_price numeric,
    ord_data date,
    id_client integer NOT NULL,
    ord_status character varying(20),
    ord_payment numeric,
    ord_prepayment numeric,
    id_obj integer NOT NULL
);


ALTER TABLE public."Заказы" OWNER TO postgres;

--
-- Name: Заказы_id_order_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Заказы" ALTER COLUMN id_order ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Заказы_id_order_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 270000
    CACHE 1
);


--
-- Name: Заказы_Бригады; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заказы_Бригады" (
    id_brig integer NOT NULL,
    id_order integer NOT NULL,
    brig_work_price integer
);


ALTER TABLE public."Заказы_Бригады" OWNER TO postgres;

--
-- Name: Заказы_Материалы; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заказы_Материалы" (
    id_material integer NOT NULL,
    ord_material_quantity integer,
    id_order integer NOT NULL
);


ALTER TABLE public."Заказы_Материалы" OWNER TO postgres;

--
-- Name: Заказы_Оборудование; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заказы_Оборудование" (
    id_equipment integer NOT NULL,
    ord_equipment_quantity integer,
    id_order integer NOT NULL
);


ALTER TABLE public."Заказы_Оборудование" OWNER TO postgres;

--
-- Name: Заказы_Услуги; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заказы_Услуги" (
    id_service integer NOT NULL,
    id_order integer NOT NULL,
    ord_service_quantity integer
);


ALTER TABLE public."Заказы_Услуги" OWNER TO postgres;

--
-- Name: Заявка_на_поставку_материалов; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заявка_на_поставку_материалов" (
    id_material integer NOT NULL,
    applic_material_quantity integer,
    data_applic_material date,
    id_provider integer NOT NULL,
    id_postavka integer,
    applic_material_status character varying(20),
    id_applic_material integer NOT NULL
);


ALTER TABLE public."Заявка_на_поставку_материалов" OWNER TO postgres;

--
-- Name: Заявка_на_поставку_оборудования; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Заявка_на_поставку_оборудования" (
    id_provider integer NOT NULL,
    id_equipment integer NOT NULL,
    applic_equipment_quantity integer,
    data_applic_equipment date,
    id_postavka integer,
    applic_equipment_status character(20),
    id_applic_equipment integer NOT NULL
);


ALTER TABLE public."Заявка_на_поставку_оборудования" OWNER TO postgres;

--
-- Name: Клиенты; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Клиенты" (
    id_client integer NOT NULL,
    client_last_name character varying(20),
    client_name character varying(20),
    client_mid_name character varying(20),
    client_phone_number character varying(20),
    client_self_sale integer,
    client_email character varying(50),
    client_password character varying(255),
    is_user boolean,
    is_admin boolean
);


ALTER TABLE public."Клиенты" OWNER TO postgres;

--
-- Name: Клиенты_id_client_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Клиенты" ALTER COLUMN id_client ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Клиенты_id_client_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2700000
    CACHE 1
);


--
-- Name: Материалы; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Материалы" (
    id_material integer NOT NULL,
    material_name character varying(50),
    material_quantity integer,
    material_unit_quantity character varying(20),
    id_postavka integer NOT NULL,
    material_price_of_one integer,
    material_transport_volume numeric
);


ALTER TABLE public."Материалы" OWNER TO postgres;

--
-- Name: Оборудование; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Оборудование" (
    id_equipment integer NOT NULL,
    equipment_name character varying(50),
    equipment_quant integer,
    equipment_use_start date,
    equipment_use_end date,
    equipment_ammortiz integer,
    id_postavka integer NOT NULL,
    equipment_capacity integer,
    equipment_transport_price_of_one numeric,
    equipment_buy_price numeric
);


ALTER TABLE public."Оборудование" OWNER TO postgres;

--
-- Name: Объекты; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Объекты" (
    id_obj integer NOT NULL,
    obj_name character varying(30),
    obj_city character varying(30),
    obj_addres character varying(30),
    id_client integer NOT NULL
);


ALTER TABLE public."Объекты" OWNER TO postgres;

--
-- Name: Объекты_id_obj_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Объекты" ALTER COLUMN id_obj ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Объекты_id_obj_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 270000
    CACHE 1
);


--
-- Name: Поставки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Поставки" (
    id_postavka integer NOT NULL,
    postavka_price integer,
    postavka_data date,
    id_provider integer NOT NULL,
    postavka_status character(20)
);


ALTER TABLE public."Поставки" OWNER TO postgres;

--
-- Name: Поставщики; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Поставщики" (
    id_provider integer NOT NULL,
    provider_name character varying(20),
    provider_debt_to_the_supplier integer,
    supplier_debt integer,
    provider_contact_person character varying(50),
    provider_city character varying(20),
    provider_email character varying(50),
    provider_phone character varying(20)
);


ALTER TABLE public."Поставщики" OWNER TO postgres;

--
-- Name: Сотрудники; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Сотрудники" (
    id_staff integer NOT NULL,
    staff_last_name character(18),
    staff_first_name character varying(20),
    staff_phone_number character varying(20),
    staff_post character varying(20),
    staff_salary integer,
    staff_expirience integer,
    staff_mid_name character varying(20),
    staff_passport_data character varying(20)
);


ALTER TABLE public."Сотрудники" OWNER TO postgres;

--
-- Name: Сотрудники_Бригады; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Сотрудники_Бригады" (
    id_staff integer NOT NULL,
    id_brig integer NOT NULL
);


ALTER TABLE public."Сотрудники_Бригады" OWNER TO postgres;

--
-- Name: Услуги; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Услуги" (
    id_service integer NOT NULL,
    service_name character varying(60),
    service_units character varying(20),
    service_price numeric
);


ALTER TABLE public."Услуги" OWNER TO postgres;

--
-- Name: Услуги_Материалы; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Услуги_Материалы" (
    id_service integer NOT NULL,
    id_material integer NOT NULL,
    service_material_quantity numeric
);


ALTER TABLE public."Услуги_Материалы" OWNER TO postgres;

--
-- Name: Услуги_Оборудование; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Услуги_Оборудование" (
    id_service integer NOT NULL,
    id_equipment integer NOT NULL,
    service_equipment_quantity numeric
);


ALTER TABLE public."Услуги_Оборудование" OWNER TO postgres;

--
-- Data for Name: Бригады; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Бригады" (id_brig, brig_name) FROM stdin;
1	Водители 1
2	Строители 1
\.


--
-- Data for Name: Заказы; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заказы" (id_order, ord_price, ord_data, id_client, ord_status, ord_payment, ord_prepayment, id_obj) FROM stdin;
1	892791	2025-03-14	1	Создан	0	0	1
2	1924758	2025-03-15	1	Создан	0	0	2
3	440754	2025-03-26	1	Создан	0	0	1
4	440754	2025-03-26	1	Создан	0	0	2
5	636591	2025-03-26	1	Создан	0	0	1
6	636591	2025-03-26	1	Создан	0	0	1
7	692235	2025-03-26	1	Создан	0	0	2
8	692235	2025-03-26	1	Создан	0	0	1
9	5588978	2025-03-27	1	Создан	0	0	3
10	154091	2025-03-27	1	Создан	0	0	5
11	403844	2025-04-07	1	Создан	0	0	5
12	65682	2025-04-27	4	Создан	0	0	7
13	399925	2025-04-28	6	Создан	0	0	8
14	1350931	2025-04-29	7	Создан	0	0	10
15	1445872	2025-04-29	8	Создан	0	0	11
16	374141	2025-04-30	1	Создан	0	0	3
17	220568	2025-05-01	4	Создан	0	0	13
18	368666	2025-05-02	6	Создан	0	0	8
19	450	2025-05-02	6	Создан	0	0	8
20	7500	2025-05-02	6	Создан	0	0	8
21	273455	2025-05-06	6	Создан	0	0	9
22	7500	2025-05-14	1	Создан	0	0	3
23	579323	2025-05-18	6	Создан	0	0	8
24	405340	2025-06-10	1	Создан	0	0	1
25	75220	2025-06-16	9	Создан	0	0	14
26	27200	2025-06-16	9	Создан	0	0	14
27	126325	2025-06-16	9	Создан	0	0	14
28	216325	2025-06-16	9	Создан	0	0	14
29	164285	2025-06-16	9	Создан	0	0	14
\.


--
-- Data for Name: Заказы_Бригады; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заказы_Бригады" (id_brig, id_order, brig_work_price) FROM stdin;
\.


--
-- Data for Name: Заказы_Материалы; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заказы_Материалы" (id_material, ord_material_quantity, id_order) FROM stdin;
1	35	1
2	35	1
9	100	1
10	30	1
7	25	1
13	100	1
1	80	2
2	80	2
9	200	2
10	60	2
7	54	2
13	250	2
1	15	4
2	15	4
9	100	4
10	30	4
7	10	4
15	25	4
1	15	5
2	15	5
9	100	5
10	30	5
7	10	5
15	25	5
12	200	5
16	7	5
1	15	6
2	15	6
9	100	6
10	30	6
7	10	6
15	25	6
12	200	6
16	7	6
1	15	7
2	15	7
9	100	7
10	30	7
7	10	7
15	25	7
12	200	7
16	7	7
1	15	8
2	15	8
9	100	8
10	30	8
7	10	8
15	25	8
12	200	8
16	7	8
1	240	9
2	150	9
9	1400	9
10	300	9
7	50	9
4	500	9
11	500	9
14	78	9
6	1600	9
15	25	9
12	120	9
16	4	9
1	7	10
2	7	10
9	50	10
10	15	10
7	2	10
1	6	11
2	4	11
9	27	11
10	8	11
7	1	11
11	20	11
14	2	11
5	20	11
12	160	11
16	6	11
1	1	12
2	0	12
9	5	12
10	1	12
7	0	12
13	1	12
4	1	12
11	2	12
14	0	12
5	1	12
6	4	12
15	0	12
12	4	12
16	0	12
1	13	13
11	30	13
14	10	13
5	30	13
6	400	13
9	100	13
1	35	14
2	23	14
9	25	14
10	7	14
7	33	14
13	100	14
1	60	15
2	30	15
13	150	15
7	22	15
4	300	15
11	300	15
14	30	15
15	35	15
1	20	16
2	15	16
9	100	16
10	30	16
7	5	16
4	50	16
11	50	16
14	5	16
1	2	17
2	0	17
9	8	17
10	0	17
7	1	17
13	2	17
4	5	17
11	11	17
14	1	17
5	6	17
6	28	17
15	4	17
12	40	17
16	1	17
1	17	18
2	17	18
9	50	18
10	15	18
7	10	18
13	50	18
1	45	21
9	100	21
10	30	21
2	35	21
7	30	21
13	100	21
1	0	22
9	1	22
10	0	22
2	0	22
7	0	22
1	42	23
9	51	23
10	15	23
2	27	23
7	32	23
13	100	23
14	0	23
4	1	23
11	2	23
5	1	23
6	4	23
15	50	23
12	4	23
16	0	23
14	30	24
1	30	24
4	200	24
11	300	24
5	100	24
1	15	25
9	100	25
10	30	25
2	15	25
7	5	25
15	0	25
1	7	27
9	50	27
10	15	27
2	7	27
7	12	27
1	7	28
9	50	28
10	15	28
2	7	28
7	12	28
1	15	29
9	100	29
10	30	29
2	15	29
7	10	29
\.


--
-- Data for Name: Заказы_Оборудование; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заказы_Оборудование" (id_equipment, ord_equipment_quantity, id_order) FROM stdin;
1	1	1
3	1	1
6	1	1
9	1	1
13	1	1
2	7	1
1	3	2
3	3	2
6	3	2
9	3	2
13	1	2
2	15	2
1	1	4
3	1	4
6	1	4
9	1	4
13	1	4
11	1	4
2	3	4
1	1	5
3	1	5
6	1	5
9	1	5
13	1	5
11	1	5
8	1	5
12	1	5
2	4	5
1	1	6
3	1	6
6	1	6
9	1	6
13	1	6
11	1	6
8	1	6
12	1	6
2	4	6
1	1	7
3	1	7
6	1	7
9	1	7
13	1	7
4	1	7
11	1	7
8	1	7
12	1	7
2	4	7
1	1	8
3	1	8
6	1	8
9	1	8
13	1	8
4	1	8
11	1	8
8	1	8
12	1	8
2	4	8
1	10	9
3	10	9
6	10	9
9	10	9
8	4	9
10	8	9
11	1	9
12	1	9
2	46	9
1	1	10
3	1	10
6	1	10
9	1	10
2	2	10
1	1	11
3	1	11
6	1	11
9	1	11
8	1	11
12	1	11
2	2	11
1	1	12
3	1	12
6	1	12
9	1	12
13	1	12
8	1	12
10	1	12
4	1	12
11	1	12
12	1	12
2	1	12
6	1	13
8	1	13
10	2	13
9	1	13
2	5	13
1	2	14
3	1	14
6	1	14
9	2	14
13	1	14
4	1	14
2	6	14
6	3	15
9	2	15
1	2	15
3	2	15
8	2	15
11	1	15
2	14	15
1	1	16
3	1	16
6	1	16
9	1	16
8	1	16
2	4	16
1	1	17
3	1	17
6	1	17
9	1	17
13	1	17
8	1	17
10	1	17
4	1	17
11	1	17
12	1	17
2	1	17
1	1	18
3	1	18
6	1	18
9	1	18
2	4	18
1	1	21
3	1	21
6	1	21
9	1	21
2	7	21
1	1	22
3	1	22
6	1	22
9	1	22
2	1	22
1	2	23
3	1	23
6	1	23
9	2	23
13	1	23
8	1	23
10	1	23
4	1	23
11	1	23
12	1	23
2	8	23
8	2	24
6	2	24
2	7	24
1	1	25
3	1	25
6	1	25
9	1	25
11	1	25
2	3	25
4	1	26
1	1	27
3	1	27
6	1	27
9	1	27
13	1	27
2	2	27
1	1	28
3	1	28
6	1	28
9	1	28
13	1	28
2	2	28
1	1	29
3	1	29
6	1	29
9	1	29
13	1	29
2	3	29
\.


--
-- Data for Name: Заказы_Услуги; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заказы_Услуги" (id_service, id_order, ord_service_quantity) FROM stdin;
4	1	100
6	1	50
5	1	100
4	2	200
6	2	70
5	2	250
4	4	100
6	4	50
12	4	50
4	5	100
6	5	50
12	5	50
13	5	50
4	6	100
6	6	50
12	6	50
13	6	50
4	7	100
6	7	50
15	7	100
16	7	30
12	7	50
13	7	50
4	8	100
6	8	50
15	8	100
16	8	30
12	8	50
13	8	50
4	9	1000
9	9	500
11	9	400
12	9	50
13	9	30
14	9	450
4	10	50
15	10	40
4	11	27
10	11	20
15	11	30
13	11	40
14	11	70
4	12	4
5	12	1
7	12	1
6	12	1
9	12	1
10	12	1
11	12	1
15	12	1
16	12	1
12	12	1
13	12	1
14	12	1
10	13	30
11	13	100
14	13	30
4	14	25
5	14	100
7	14	120
6	14	50
15	14	300
16	14	100
5	15	150
9	15	300
12	15	70
4	16	100
9	16	50
4	17	1
5	17	2
7	17	3
6	17	4
9	17	5
10	17	6
11	17	7
15	17	8
16	17	69
12	17	9
13	17	10
14	17	11
4	18	50
5	18	50
15	19	1
15	20	10
4	21	100
5	21	100
7	21	100
4	22	1
4	23	50
5	23	100
7	23	150
6	23	1
9	23	1
10	23	1
11	23	1
15	23	300
16	23	52
12	23	100
13	23	1
14	23	30
9	24	200
10	24	100
4	25	100
12	25	1
15	26	40
16	26	60
4	27	50
6	27	100
15	27	100
4	28	50
6	28	100
15	28	300
4	29	100
6	29	50
15	29	150
\.


--
-- Data for Name: Заявка_на_поставку_материалов; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заявка_на_поставку_материалов" (id_material, applic_material_quantity, data_applic_material, id_provider, id_postavka, applic_material_status, id_applic_material) FROM stdin;
15	2	2025-04-27	1	\N	Ожидает поставки	2
14	1	2025-04-27	1	\N	Ожидает поставки	2
16	10	2025-04-28	1	\N	Ожидает поставки	4
9	80	2025-04-28	1	\N	Ожидает поставки	4
3	10	2025-04-29	1	\N	Ожидает поставки	5
16	1	2025-04-29	1	\N	Ожидает поставки	6
2	500	2025-05-05	2	\N	Ожидает поставки	10
16	5269	2025-05-05	2	\N	Ожидает поставки	10
9	1	2025-05-05	2	\N	Ожидает поставки	10
3	5	2025-05-14	1	\N	Ожидает поставки	11
1	400	2024-12-20	1	1	Выполнена	1
2	150	2024-12-20	1	1	Выполнена	1
3	350	2024-12-20	1	1	Выполнена	1
4	700	2024-12-20	1	1	Выполнена	1
5	450	2024-12-20	1	1	Выполнена	1
6	500	2024-12-20	1	1	Выполнена	1
\.


--
-- Data for Name: Заявка_на_поставку_оборудования; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Заявка_на_поставку_оборудования" (id_provider, id_equipment, applic_equipment_quantity, data_applic_equipment, id_postavka, applic_equipment_status, id_applic_equipment) FROM stdin;
1	2	3	2024-12-21	1	Выполнена           	1
1	1	5	2024-12-21	1	Выполнена           	1
2	9	12	2025-04-27	\N	Ожидает поставки    	3
1	9	2	2025-04-29	\N	Ожидает поставки    	7
1	7	1	2025-04-29	\N	Ожидает поставки    	7
1	6	1	2025-04-29	\N	Ожидает поставки    	7
1	1	1	2025-05-05	\N	Ожидает поставки    	8
1	13	52	2025-05-05	\N	Ожидает поставки    	9
1	10	69	2025-05-05	\N	Ожидает поставки    	9
1	8	1	2025-05-18	\N	Ожидает поставки    	12
\.


--
-- Data for Name: Клиенты; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Клиенты" (id_client, client_last_name, client_name, client_mid_name, client_phone_number, client_self_sale, client_email, client_password, is_user, is_admin) FROM stdin;
2	Шапира	Нета	Иосифович	+9723377733	0	33dota2@gmail.com	$2b$12$b1Rrc8z1vSIb65lZvj.9K.CN0sR0V8qYOgFI0BgivXnsqy3Vlu5.u	t	f
3	Зубенко	Михаил	Петрович	88005553535	0	zubenko228@gmai.com	$2b$12$FxpnGmPOFMM6GOwhdpQYXe7UXfiW37rK4JhTR19enozFaekv5yFM.	t	f
1	Колпаков	Мирослав	Владимирович	+76772226677	0	sadsad@gmail.com	$2b$12$y.HLDqpoUcKnEVZu2nuKM.M1650zczNWS4FOGcBDPrZ2gnxlsNJcW	t	t
4	Форелева	Семга	Лососевна	89696969696	0	Pupochkazalupochka69@ok.ru	$2b$12$tKzdHA.xdLML9wOv42xLV.UdFrx8k.u1uHXm6KPzZpcOhecUxtRwa	t	f
5	Робенович	Геннадий	Петрович	88775557575	0	test123@gmail.com	$2b$12$YYQgD1KKyyKqzH83Tar54.EMzWe4JAwjlZKrnK6WdYr90QBgtrIqG	t	f
6	ТАМАЕВ	АЯЗ	Кадрович	88007776565	0	50PROcentFiuchMaster@gamer.com	$2b$12$FGxQ8QGUX51Zkae6Itl2V.t8qkifaSyO2kir65QVu3VEXPD0PlKVm	t	f
7	Ойойой	Бобрито	Бандито	7896456778	0	moxnatyieyaichki@gmail.com	$2b$12$Mte/EezjFKGEDB9aS8zWjOwD07NF7IZ1g0FfoqAMbWsl.DTJ3NXmu	t	f
8	Шкредов	Сахур	ТУТУТУТУТУТУТУНОВИЧ	78964567787	0	timofei.vereshchagin@gmail.com	$2b$12$JhnO.0TlauEbIymZEck8MuX0jfTt7rH5cVOoAmkNHxaFpYiNRO0HC	t	f
9	Лузин	Иван	Николаевич	+7 (999) 123-33-33	0	saderwent97@mail.ru	$2b$12$boCXHw1QPv4OjXD5uj5RY.wnGTQhrZxTmflv3jXViTpsfVIFn2CcW	t	f
\.


--
-- Data for Name: Материалы; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Материалы" (id_material, material_name, material_quantity, material_unit_quantity, id_postavka, material_price_of_one, material_transport_volume) FROM stdin;
14	Цемент	300	м³	1	3000	1
1	Песок	400	м³	1	1100	1
3	Гравий	350	м³	1	1700	1
4	Дорожный бардюр Фабрика «Готика»	700	штука	1	270	0.4
6	Тратуарная плитка Фабрика «Готика»	500	штука	1	200	0.25
9	Геотекстиль	8000	м²	1	30	0.1
10	Битумная эмульсия	7000	м³	1	20	1
11	Арматура	2000	шт	1	500	0.1
12	Анкерные болты	3000	шт	1	25	0.01
13	Рубероид	500	м³	1	100	1
15	Краска	300	м²	1	150	1
16	Бетон	250	м³	1	350	1
5	Тратуарный бордюр Фабрика «Готика»	450	штука	1	320	0.5
2	Щебень	150	м³	1	1500	1
7	Асфальтовая смесь	900	м³	1	3500	0.20
8	Смесь асфальтобетонная горячая крупнозернистая	4000	м³	1	4500	1
\.


--
-- Data for Name: Оборудование; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Оборудование" (id_equipment, equipment_name, equipment_quant, equipment_use_start, equipment_use_end, equipment_ammortiz, id_postavka, equipment_capacity, equipment_transport_price_of_one, equipment_buy_price) FROM stdin;
1	Асфальтоукладчик	5	2023-06-14	2027-10-18	50	1	100	100	12000000
2	Грузовик	3	2023-06-14	2028-07-14	60	1	35	300	7000000
3	Каток	3	2023-06-14	2027-11-12	55	1	100	100	2500000
4	Дорожная фреза	2	2023-06-14	2026-12-31	50	1	150	150	15000000
5	Кохер для асфальта	2	2023-06-14	2026-12-31	55	1	100	100	10000000
6	Экскаватор-погрузчик	4	2023-06-14	2027-11-12	50	1	100	130	6500000
7	Трактор-экскаватор	3	2023-06-14	2027-11-12	50	1	100	125	5700000
8	Бетономешалка	5	2023-06-14	2026-12-31	70	1	150	60	1100000
9	Виброплита	12	2023-06-14	2026-12-31	30	1	100	20	38000
10	Резиновая киянка	30	2023-06-14	2029-10-11	5	1	50	5	300
11	Разметочная машина	7	2023-06-14	2027-11-12	40	1	150	50	135000
12	Автовышка	3	2023-06-14	2027-10-18	30	1	100	100	3800000
13	Бетоносмесительная установка	4	2023-06-14	2027-10-18	40	1	100	130	450000
\.


--
-- Data for Name: Объекты; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Объекты" (id_obj, obj_name, obj_city, obj_addres, id_client) FROM stdin;
1	Мост	Москва	ул. Пушкина	1
2	Дорога	Москва	Ул. Колотушкина	1
3	Шоссе	Москва	Ул. Арбат	1
4	Частный дом	Люберцы	Ул. Капибарова дом 69	1
5	Трасса М2	Москва	Трасса	1
6	Дорога куда-то	Москва	Обочина	1
7	Рыбная дача	Рыбинск	Улица речная дом 69	4
8	Рыбинская АЭС	Вельск	ул. Залупкина 69 к.2	6
9	Общага	Рыбинск	ул. Валорантреская 15	6
10	МКАД	Москва	МОЙ ДОМ МОЯ РАБОТА МОЙ ХЛЕБ!!!	7
11	Трасса Е95 (дом Хача)	Москва	ул. Ленина д.1 	8
12	Стрим-хата	Москва	ул. Чилловая д.2	1
13	Частный дом	ставрополь	мне лень думать я объелась	4
14	Дача	Москва	Улица Парусная дом 3	9
\.


--
-- Data for Name: Поставки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Поставки" (id_postavka, postavka_price, postavka_data, id_provider, postavka_status) FROM stdin;
1	450	2025-01-14	1	Поставлено          
\.


--
-- Data for Name: Поставщики; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Поставщики" (id_provider, provider_name, provider_debt_to_the_supplier, supplier_debt, provider_contact_person, provider_city, provider_email, provider_phone) FROM stdin;
1	ТИМ СПИРИТ	0	0	\N	\N	\N	\N
2	ТУНДРА	0	0	\N	\N	\N	\N
\.


--
-- Data for Name: Сотрудники; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Сотрудники" (id_staff, staff_last_name, staff_first_name, staff_phone_number, staff_post, staff_salary, staff_expirience, staff_mid_name, staff_passport_data) FROM stdin;
1	Халилов           	Магомед	89152581395	водитель	55000	5	Мурадович	6263123199
2	Шкредов           	Антон	89192563213	водитель	53000	4	Алексеевич	6162345611
3	Найденов          	Ярослав	88001293411	рабочий	67000	9	Сергеевич	4246322322
4	Малерчук          	Илья	89993124455	рабочий	65000	7	Владимирович	4512345199
5	Сигитов           	Денис	89131251432	рабочий	64000	6	Владимирович	5412777912
\.


--
-- Data for Name: Сотрудники_Бригады; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Сотрудники_Бригады" (id_staff, id_brig) FROM stdin;
1	1
2	1
3	2
4	2
5	2
\.


--
-- Data for Name: Услуги; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Услуги" (id_service, service_name, service_units, service_price) FROM stdin;
16	Фрезерование асфальтобетонного покрытия толщ. 5 см.	руб/м²	150
17	Доставка оборудования и спецтехники	руб/штуку	7000
15	Разработка асфальтобетонного покрытия толщ. 5 см. ручная	руб/м²	450
14	Вывоз строительного мусора	руб/рейс	5000
1	Доставка материалов	руб/м³	20
4	Укладка асфальта	руб/м²	100
5	Двухслойное асфальтирование	руб/м²	150
6	Ямочный ремонт	руб/м²	80
7	Асфальтирование частных территорий	руб/м³	180
8	Транспортировка спецтехники	руб/рейс	5000
9	Установка дорожного бордюра	руб/м²	100
10	Установка тротуарного бордюра	руб/м²	100
11	Укладка тротуарной плитки	руб/м²	110
12	Нанесение разметки краской	руб/м²	30
13	Установка дорожных знаков	руб/штука	50
\.


--
-- Data for Name: Услуги_Материалы; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Услуги_Материалы" (id_service, id_material, service_material_quantity) FROM stdin;
4	7	0.05
4	2	0.15
4	1	0.15
4	9	1
4	10	0.3
5	7	0.15
5	2	0.2
5	1	0.2
5	13	1
6	7	0.1
7	1	0.1
7	7	0.1
9	1	0.1
9	14	0.1
9	4	1
9	11	1
10	5	1
10	1	0.1
10	11	1
10	14	0.1
11	9	1
11	14	0.07
11	1	0.1
11	6	4
12	15	0.5
13	16	0.15
13	12	4
1	1	1
\.


--
-- Data for Name: Услуги_Оборудование; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Услуги_Оборудование" (id_service, id_equipment, service_equipment_quantity) FROM stdin;
3	2	1
2	2	1
1	2	1
4	1	1
4	3	1
4	6	1
4	9	1
5	6	1
5	9	1
5	1	1
5	3	1
6	13	1
7	9	1
7	1	1
8	2	1
9	8	1
9	6	1
10	6	1
10	8	1
11	10	1
11	9	1
12	11	1
13	8	1
13	12	1
16	4	1
17	2	1
14	2	1
\.


--
-- Name: Заказы_id_order_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Заказы_id_order_seq"', 29, true);


--
-- Name: Клиенты_id_client_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Клиенты_id_client_seq"', 9, true);


--
-- Name: Объекты_id_obj_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Объекты_id_obj_seq"', 14, true);


--
-- Name: Бригады Бригады_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Бригады"
    ADD CONSTRAINT "Бригады_pkey" PRIMARY KEY (id_brig);


--
-- Name: Заказы Заказы_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы"
    ADD CONSTRAINT "Заказы_pkey" PRIMARY KEY (id_order);


--
-- Name: Заказы_Бригады Заказы_Бригады_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Бригады"
    ADD CONSTRAINT "Заказы_Бригады_pkey" PRIMARY KEY (id_brig, id_order);


--
-- Name: Заказы_Материалы Заказы_Материалы_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Материалы"
    ADD CONSTRAINT "Заказы_Материалы_pkey" PRIMARY KEY (id_material, id_order);


--
-- Name: Заказы_Оборудование Заказы_Оборудование_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Оборудование"
    ADD CONSTRAINT "Заказы_Оборудование_pkey" PRIMARY KEY (id_equipment, id_order);


--
-- Name: Заказы_Услуги Заказы_Услуги_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Услуги"
    ADD CONSTRAINT "Заказы_Услуги_pkey" PRIMARY KEY (id_service, id_order);


--
-- Name: Заявка_на_поставку_материалов Заявка_на_поставку_материалов_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_материалов"
    ADD CONSTRAINT "Заявка_на_поставку_материалов_pkey" PRIMARY KEY (id_material, id_applic_material, id_provider);


--
-- Name: Заявка_на_поставку_оборудования Заявка_на_поставку_оборудовани_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_оборудования"
    ADD CONSTRAINT "Заявка_на_поставку_оборудовани_pkey" PRIMARY KEY (id_equipment, id_applic_equipment, id_provider);


--
-- Name: Клиенты Клиенты_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Клиенты"
    ADD CONSTRAINT "Клиенты_pkey" PRIMARY KEY (id_client);


--
-- Name: Материалы Материалы_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Материалы"
    ADD CONSTRAINT "Материалы_pkey" PRIMARY KEY (id_material);


--
-- Name: Оборудование Оборудование_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Оборудование"
    ADD CONSTRAINT "Оборудование_pkey" PRIMARY KEY (id_equipment);


--
-- Name: Объекты Объекты_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Объекты"
    ADD CONSTRAINT "Объекты_pkey" PRIMARY KEY (id_obj);


--
-- Name: Поставки Поставки_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Поставки"
    ADD CONSTRAINT "Поставки_pkey" PRIMARY KEY (id_postavka);


--
-- Name: Поставщики Поставщики_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Поставщики"
    ADD CONSTRAINT "Поставщики_pkey" PRIMARY KEY (id_provider);


--
-- Name: Сотрудники Сотрудники_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Сотрудники"
    ADD CONSTRAINT "Сотрудники_pkey" PRIMARY KEY (id_staff);


--
-- Name: Сотрудники_Бригады Сотрудники_Бригады_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Сотрудники_Бригады"
    ADD CONSTRAINT "Сотрудники_Бригады_pkey" PRIMARY KEY (id_staff, id_brig);


--
-- Name: Услуги Услуги_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Услуги"
    ADD CONSTRAINT "Услуги_pkey" PRIMARY KEY (id_service);


--
-- Name: Услуги_Материалы Услуги_Материалы_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Услуги_Материалы"
    ADD CONSTRAINT "Услуги_Материалы_pkey" PRIMARY KEY (id_service, id_material);


--
-- Name: Услуги_Оборудование Услуги_Оборудование_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Услуги_Оборудование"
    ADD CONSTRAINT "Услуги_Оборудование_pkey" PRIMARY KEY (id_service, id_equipment);


--
-- Name: Заказы r_18; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы"
    ADD CONSTRAINT r_18 FOREIGN KEY (id_client) REFERENCES public."Клиенты"(id_client);


--
-- Name: Заказы_Услуги r_33; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Услуги"
    ADD CONSTRAINT r_33 FOREIGN KEY (id_service) REFERENCES public."Услуги"(id_service);


--
-- Name: Заказы_Услуги r_34; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Услуги"
    ADD CONSTRAINT r_34 FOREIGN KEY (id_order) REFERENCES public."Заказы"(id_order);


--
-- Name: Заказы_Материалы r_37; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Материалы"
    ADD CONSTRAINT r_37 FOREIGN KEY (id_material) REFERENCES public."Материалы"(id_material);


--
-- Name: Заказы_Оборудование r_41; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Оборудование"
    ADD CONSTRAINT r_41 FOREIGN KEY (id_equipment) REFERENCES public."Оборудование"(id_equipment);


--
-- Name: Объекты r_42; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Объекты"
    ADD CONSTRAINT r_42 FOREIGN KEY (id_client) REFERENCES public."Клиенты"(id_client);


--
-- Name: Заказы_Бригады r_46; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Бригады"
    ADD CONSTRAINT r_46 FOREIGN KEY (id_brig) REFERENCES public."Бригады"(id_brig);


--
-- Name: Заказы_Бригады r_47; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Бригады"
    ADD CONSTRAINT r_47 FOREIGN KEY (id_order) REFERENCES public."Заказы"(id_order);


--
-- Name: Заказы_Материалы r_48; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Материалы"
    ADD CONSTRAINT r_48 FOREIGN KEY (id_order) REFERENCES public."Заказы"(id_order);


--
-- Name: Заказы_Оборудование r_49; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы_Оборудование"
    ADD CONSTRAINT r_49 FOREIGN KEY (id_order) REFERENCES public."Заказы"(id_order);


--
-- Name: Заявка_на_поставку_оборудования r_52; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_оборудования"
    ADD CONSTRAINT r_52 FOREIGN KEY (id_provider) REFERENCES public."Поставщики"(id_provider);


--
-- Name: Материалы r_57; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Материалы"
    ADD CONSTRAINT r_57 FOREIGN KEY (id_postavka) REFERENCES public."Поставки"(id_postavka);


--
-- Name: Оборудование r_58; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Оборудование"
    ADD CONSTRAINT r_58 FOREIGN KEY (id_postavka) REFERENCES public."Поставки"(id_postavka);


--
-- Name: Заявка_на_поставку_материалов r_59; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_материалов"
    ADD CONSTRAINT r_59 FOREIGN KEY (id_material) REFERENCES public."Материалы"(id_material);


--
-- Name: Заявка_на_поставку_материалов r_61; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_материалов"
    ADD CONSTRAINT r_61 FOREIGN KEY (id_provider) REFERENCES public."Поставщики"(id_provider);


--
-- Name: Заявка_на_поставку_оборудования r_62; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_оборудования"
    ADD CONSTRAINT r_62 FOREIGN KEY (id_equipment) REFERENCES public."Оборудование"(id_equipment);


--
-- Name: Поставки r_63; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Поставки"
    ADD CONSTRAINT r_63 FOREIGN KEY (id_provider) REFERENCES public."Поставщики"(id_provider);


--
-- Name: Заявка_на_поставку_оборудования r_65; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_оборудования"
    ADD CONSTRAINT r_65 FOREIGN KEY (id_postavka) REFERENCES public."Поставки"(id_postavka);


--
-- Name: Заявка_на_поставку_материалов r_66; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заявка_на_поставку_материалов"
    ADD CONSTRAINT r_66 FOREIGN KEY (id_postavka) REFERENCES public."Поставки"(id_postavka);


--
-- Name: Заказы r_67; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Заказы"
    ADD CONSTRAINT r_67 FOREIGN KEY (id_obj) REFERENCES public."Объекты"(id_obj);


--
-- Name: Сотрудники_Бригады r_68; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Сотрудники_Бригады"
    ADD CONSTRAINT r_68 FOREIGN KEY (id_staff) REFERENCES public."Сотрудники"(id_staff);


--
-- Name: Сотрудники_Бригады r_69; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Сотрудники_Бригады"
    ADD CONSTRAINT r_69 FOREIGN KEY (id_brig) REFERENCES public."Бригады"(id_brig);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict Mu8BrHl3cEJ51u9VOnodWhO22M8FiPWjwdaVFXXL73VmdBe3nBsELbFhlnAgDIS

