#!/bin/bash
psql \
    -c "create database zearjch;" \
    -c "create role zearjch_admin with login password 'shhhItsASecret';" \
    -c "\connect zearjch" \
    -c "create schema corpus_u_of_o_courses authorization zearjch_admin;" \
        
