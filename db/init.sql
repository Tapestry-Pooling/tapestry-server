-- Setup (as Postgres user)
CREATE ROLE covid WITH createdb LOGIN PASSWORD 'covid' ;
-- Tentative schema: (as covid user)
create database covid;