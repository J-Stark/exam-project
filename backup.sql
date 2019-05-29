--
-- PostgreSQL database dump
--

-- Dumped from database version 10.7 (Ubuntu 10.7-1.pgdg16.04+1)
-- Dumped by pg_dump version 10.7 (Ubuntu 10.7-1.pgdg16.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: coordinates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.coordinates (
    name character varying(255) NOT NULL,
    x real NOT NULL,
    y real NOT NULL,
    bike_id integer NOT NULL,
    avaibility integer,
    rent_date timestamp without time zone
);


ALTER TABLE public.coordinates OWNER TO postgres;

--
-- Name: coordinates_bike_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.coordinates ALTER COLUMN bike_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.coordinates_bike_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    username character varying(255),
    pass character varying(255),
    rented integer,
    credits double precision
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: coordinates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.coordinates (name, x, y, bike_id, avaibility, rent_date) FROM stdin;
Rutebilstation	56.1203003	10.1604004	2	0	\N
Q	56.1497459	10.2040672	4	\N	\N
test	12	13	7	\N	\N
tester	24	26	9	\N	\N
qerye	36	7726	10	\N	\N
testaga	666	66	11	\N	\N
testData	85	94	13	\N	\N
Gellerup	56.1528511	10.134551	14	\N	\N
finalTest	44	44	15	\N	\N
Glenn	47	74	16	\N	\N
Glenn4	17	14	17	\N	\N
Glenn7	100	140	18	\N	\N
Glenn17	999	140	19	\N	\N
test	55	77	20	\N	\N
test	999	999	21	\N	\N
qqqq	111	111	22	\N	\N
testname	666	666	23	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (username, pass, rented, credits) FROM stdin;
test	test	0	0
Admin	Pass	0	0
		0	0
		0	0
		0	0
tester	tester	0	140.919999999999987
\.


--
-- Name: coordinates_bike_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.coordinates_bike_id_seq', 23, true);


--
-- Name: coordinates coordinates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coordinates
    ADD CONSTRAINT coordinates_pkey PRIMARY KEY (bike_id);


--
-- PostgreSQL database dump complete
--

