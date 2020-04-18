-- Setup (as Postgres user)
CREATE ROLE covid WITH createdb LOGIN PASSWORD 'covid' ;
create database covid OWNER covid;