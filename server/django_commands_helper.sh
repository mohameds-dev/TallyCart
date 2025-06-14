#!/bin/bash

# Define commands
commands=(
  "python manage.py runserver                # start development server"
  "python manage.py makemigrations           # create new migrations based on changes"
  "python manage.py migrate                  # apply database migrations"
  "python manage.py createsuperuser          # create admin user"
  "python manage.py shell                    # open Django shell"
  "python manage.py showmigrations           # list all migrations and their status"
  "python manage.py sqlmigrate               # show SQL for a migration"
  "python manage.py check                    # run system checks"
  "python manage.py test                     # run unit tests"
  "python manage.py collectstatic            # gather static files"
  "python manage.py startapp                 # create new app"
  "exit"
)

# Let user select a command
choice=$(printf "%s\n" "${commands[@]}" | fzf --prompt="Pick a Django command: ")

# Extract the actual command part
cmd=$(echo "$choice" | cut -d'#' -f1 | xargs)

# Handle special cases
if [[ "$cmd" == "exit" ]]; then
  echo "👋 Exiting..."
  exit 0
elif [[ "$cmd" == "python manage.py startapp" ]]; then
  read -p "Enter name of the new app: " app
  python manage.py startapp "$app"
elif [[ "$cmd" == "python manage.py sqlmigrate" ]]; then
  read -p "Enter app and migration name (e.g. users 0001): " args
  python manage.py sqlmigrate $args
else
  eval "$cmd"
fi
