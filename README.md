# Doriane World

E-commerce Django pour produits alimentaires et beaute.

## Setup rapide
1. Creer un venv et l'activer
2. Installer les deps: `pip install -r requirements.txt`
3. Migrations: `python manage.py migrate`
4. Superuser: `python manage.py createsuperuser`
5. Donnees initiales: `python manage.py loaddata fixtures/initial_data.json`
6. Lancer: `python manage.py runserver`

## Images produits
Ajouter les images dans `media/products/` et les lier aux produits via l'admin.

## Production
- Mettre `DEBUG = False`
- Renseigner `ALLOWED_HOSTS`
- Utiliser PostgreSQL
- Definir `SECRET_KEY` via variable d'environnement
