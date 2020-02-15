#!/bin/bash
psql \
    -c "create database if not exists zearjch;" \
    -c "create role if not exists zearjch_admin with login password 'shhhItsASecret';" \
    -c "\connect zearjch" \
    -c "create schema if not exists corpus_u_of_o_courses authorization zearjch_admin;" \
    -c "create table if not exists corpus_u_of_o_courses.documents (docid serial primary key, title text not null, description text);"
        
