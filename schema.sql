-- Setup (as Postgres user)
CREATE ROLE covid WITH createdb LOGIN PASSWORD 'covid' ;
-- Tentative schema: (as covid user)
create database covid;

-- id generator from https://rob.conery.io/2014/05/28/a-better-id-generator-for-postgresql/
create sequence global_id_sequence;

CREATE OR REPLACE FUNCTION id_generator(OUT result bigint) AS $$
DECLARE
    our_epoch bigint := 1586195872721;
    seq_id bigint;
    now_millis bigint;
    -- the id of this DB shard, must be set for each schema shard you have
    shard_id int := 1;
BEGIN
    SELECT nextval('global_id_sequence') % 1024 INTO seq_id;
    SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000) INTO now_millis;
    result := (now_millis - our_epoch) << 23;
    result := result | (shard_id << 10);
    result := result | (seq_id);
END;
$$ LANGUAGE PLPGSQL;

-- tables
create table users ( id bigint primary key default id_generator(), username text not null, name text, email text, phone text, password text);
create table test_templates (id serial primary key, num_users int not null, num_tests int not null);
create table test_uploads (id bigint primary key default id_generator(), user_id bigint references users(id), 
    created_at timestamptz default now(), updated_at timestamptz default now(), test_data real[]);
create table test_results (test_id bigint references test_uploads(id) primary key, updated_at timestamptz default now(),result_data int[]);