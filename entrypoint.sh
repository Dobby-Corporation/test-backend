#!/bin/bash

# Database migration
python3 manage.py migrate

# Run server
python3 manage.py runserver 0.0.0.0:8000
