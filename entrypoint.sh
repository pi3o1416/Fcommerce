#!/bin/bash

# Waiting for database to become live
sleep 20

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Start server
echo "Starting server"

#python manage.py remove_stale_contenttypes --noinput
hypercorn core.wsgi:application --workers 1 --bind 0.0.0.0:8000
