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
create table users ( id bigint primary key default id_generator(), username text, email text, phone text unique not null);
-- create table test_templates (id serial primary key, num_users int not null, num_tests int not null);
create table test_uploads (id bigint primary key default id_generator(), user_id bigint references users(id), updated_at timestamptz default now(), test_data real[]);
create table test_results (test_id bigint references test_uploads(id) primary key, updated_at timestamptz default now(),result_data int[]);

-- audit tables for test_uploads and test_results
create table test_uploads_audit ( auditid bigserial primary key, test_id bigint not null, user_id bigint, test_data real[], operation text, updated_at timestamptz default now());

CREATE OR REPLACE FUNCTION test_uploads_audit_proc() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'INSERT' or (TG_OP = 'UPDATE' and OLD.test_data <> NEW.test_data)) THEN
            INSERT INTO test_uploads_audit VALUES (DEFAULT, NEW.id, NEW.user_id, NEW.test_data, TG_OP, now());
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO test_uploads_audit VALUES (DEFAULT, OLD.id, OLD.user_id, OLD.test_data, TG_OP, now());
            RETURN OLD;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER test_uploads_IUD_TG AFTER INSERT OR UPDATE OR DELETE ON test_uploads FOR EACH ROW EXECUTE PROCEDURE test_uploads_audit_proc();

create table test_results_audit ( auditid bigserial primary key, test_id bigint not null, result_data int[], operation text, updated_at timestamptz default now());

CREATE OR REPLACE FUNCTION test_results_audit_proc() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'INSERT' or (TG_OP = 'UPDATE' and OLD.result_data <> NEW.result_data)) THEN
            INSERT INTO test_results_audit VALUES (DEFAULT, NEW.id, NEW.result_data, TG_OP, now());
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO test_results_audit VALUES (DEFAULT, OLD.id, OLD.result_data, TG_OP, now());
            RETURN OLD;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER test_results_IUD_TG AFTER INSERT OR UPDATE OR DELETE ON test_results FOR EACH ROW EXECUTE PROCEDURE test_results_audit_proc();