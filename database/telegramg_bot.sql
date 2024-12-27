--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: newbooks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.newbooks (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    published_date date,
    genre character varying(100),
    price numeric(10,2)
);


ALTER TABLE public.newbooks OWNER TO postgres;

--
-- Name: newbooks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.newbooks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.newbooks_id_seq OWNER TO postgres;

--
-- Name: newbooks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.newbooks_id_seq OWNED BY public.newbooks.id;


--
-- Name: newbooks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.newbooks ALTER COLUMN id SET DEFAULT nextval('public.newbooks_id_seq'::regclass);


--
-- Data for Name: newbooks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.newbooks (id, title, author, published_date, genre, price) FROM stdin;
1	1984	George Orwell	1949-06-08	Dystopian	9.99
2	To Kill a Mockingbird	Harper Lee	1960-07-11	Fiction	12.99
3	The Great Gatsby	F. Scott Fitzgerald	1925-04-10	Classic	8.99
4	Moby-Dick	Herman Melville	1851-11-14	Adventure	11.50
\.


--
-- Name: newbooks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.newbooks_id_seq', 4, true);


--
-- Name: newbooks newbooks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.newbooks
    ADD CONSTRAINT newbooks_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

