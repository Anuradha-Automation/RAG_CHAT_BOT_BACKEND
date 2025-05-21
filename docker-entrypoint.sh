#!/bin/bash

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "MySQL started"
fi

# Décommenter pour supprimer la bdd à chaque redémarrage (danger)
# echo "Clear entire database"
# python manage.py flush --no-input
chromedriver --url-base=/wd/hub &

echo "Appling database migrations..."
python manage.py makemigrations  RAG_CHATBOT_BACKEND_APIS
python manage.py migrate
python manage.py seed_data
# Collect static files (if needed)

echo "Collecting static files..."
python manage.py collectstatic --noinput
# Start the Django server
echo "Starting Django server..."
exec watchmedo auto-restart --directory=/app --pattern="*.py" --recursive -- python manage.py runserver 0.0.0.0:8000
exec "$@"