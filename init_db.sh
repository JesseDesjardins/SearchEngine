#!/bin/bash
psql \
    -c "create role zearjch_admin with superuser login password 'shhhItsASecret';" \
    -c "create database zearjch;" \
    -c "\connect zearjch zearjch_admin" \
    -c "create schema corpus_u_of_o_courses authorization zearjch_admin;" \
    -c "grant all privileges on all tables in schema corpus_u_of_o_courses to zearjch_admin;" \
    -c "create table corpus_u_of_o_courses.documents (docid serial primary key, title text, description text);"
        
