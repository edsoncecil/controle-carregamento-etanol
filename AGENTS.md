# AGENTS.md - controle_etanol

## Project Overview
Django 6.0.4 project for ethanol transport control/weighbridge management. SQLite database.

## Key Commands
```bash
# Run development server
python manage.py runserver

# Make migrations (after model changes)
python manage.py makemigrations
python manage.py migrate

# Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser
```

## Structure
- `controle_etanol/` - Django project settings (settings.py, urls.py, wsgi.py)
- `core/` - Main app with Carregamento model (motorista, placa, distribuidora, transportador, litragem_sem_excesso, ordem, situacao, lacres)
- `db.sqlite3` - SQLite database (already exists)

## Notes
- DEBUG=True, ALLOWED_HOSTS=[] in settings (dev only)
- No templates or static files configured yet
- `core/views.py` is empty - views need to be created
- Root URL only has admin enabled (`/admin/`)