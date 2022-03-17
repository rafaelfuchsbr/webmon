CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: public.website

-- DROP TABLE public.website;

CREATE TABLE IF NOT EXISTS public.website
(
    website_id uuid NOT NULL DEFAULT uuid_generate_v1(),
    name character varying NOT NULL,
    url character varying NOT NULL,
    regex character varying NOT NULL,
    status character varying NOT NULL,
    "timestamp" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT website_pkey PRIMARY KEY (website_id)
)

TABLESPACE pg_default;

ALTER TABLE public.website
    OWNER to <YOUR_DB_USER>;

-- Table: public.check_entry

-- DROP TABLE public.check_entry;

CREATE TABLE IF NOT EXISTS public.check_entry
(
    check_entry_id uuid NOT NULL DEFAULT uuid_generate_v1(),
    website_id uuid NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    response_time integer NOT NULL,
    http_status smallint NOT NULL,
    regex character varying NOT NULL,
    regex_match boolean NOT NULL DEFAULT false,
    CONSTRAINT check_entry_pkey PRIMARY KEY (check_entry_id)
)

TABLESPACE pg_default;

ALTER TABLE public.check_entry
    OWNER to <YOUR_DB_USER>;