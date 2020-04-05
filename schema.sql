-- Setup (as Postgres user)
CREATE ROLE covid WITH createdb LOGIN PASSWORD 'covid' ;
-- Tentative schema: (as covid user)
create database covid;
create table users ( id bigserial primary key, username text not null, name text, email text, phone text, password text);
create table test_templates (id serial primary key, num_users int not null, num_tests int not null);
create table test_uploads (id bigserial primary key, user_id bigint references users(id), template_id int references test_templates(id), test_data real[]);
create table test_results (test_id bigint references test_uploads(id) primary key, result_data text);