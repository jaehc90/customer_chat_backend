#! /usr/bin/env bash

# Let the DB start
# python /app/app/backend_pre_start.py
PYTHONPATH=. python app/backend_pre_start.py


# Run migrations
alembic upgrade head

# Create initial data in DB
PYTHONPATH=. python app/initial_data.py
