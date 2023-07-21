#!/bin/sh

until cd /app/meeting
do
    echo "Waiting for server volume..."
done

celery -A meeting worker -l INFO
