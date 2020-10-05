# Developer Notes

These notes are both for me keeping track of what I've done and my thought process along the way of trying to build out a simple RSS reader using Python, Django, and Django REST Framework.

## Getting Setup

```
# Create and activate a virutal environment
python3 -m venv env
source env/bin/activate

# Install djanog and djangorestframework
python -m pip install django
python -m pip install djangorestframework

# Create a Django project
django-admin.py startproject rssreader
cd rssreader

# Create an app for the api
django-admin startapp api
```

- NOTE: Would have to revist settings if this were ever to be deployed in a production environement.

- Using sqlite as database for now, again if this were to be used in production I'd go with something else (postgres, mysql, etc.).

- Add Django REST Framework and api to INSTALLED_APPS in project settings.py

- Run initial migrate:

```
python manage.py migrate
```
