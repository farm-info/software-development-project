#!/bin/bash

pip install -r requirements.txt

# make migrations
python3.9 recipeapp/manage.py migrate --noinput
python3.9 recipeapp/manage.py collectstatic --noinput
