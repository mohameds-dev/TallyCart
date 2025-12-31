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
  "python manage.py load_products_data ../data/receipts_data.csv       # load products data from CSV"
  "delete_migrations                                # delete all migration files"
  "exit"
)

# Check if fzf is installed
if ! command -v fzf &> /dev/null; then
  echo "fzf could not be found. Please install it first using 'sudo apt install fzf'"
  exit 1
fi

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
elif [[ "$cmd" == "delete_migrations" ]]; then
  echo "🗑️  Deleting all migration files (except __init__.py)..."
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  echo "✅ All migration files deleted!"
else
  eval "$cmd"
fi
