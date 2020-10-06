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

## User Registration/Login

- Created UserSerializer to handle serializing users on registration.
- Wired up the URLconf for the users/register endpoint
- Added rest_framework.authtoken to INSTALLED_APPS in project settings.py
  - Run migrate:
    ```
    python manage.py migrate
    ```
- Created REST_FRAMEWORK config in project settings.py and set TokenAuthentication as default for auth.
- Created a test view for auth test
- Wired up the URL conf for the users/login and test endpoints
- Registration is working and has tests.
- Login is working and has tests.

---

## Making CLI API Test Calls With httpie

Making note of some helper calls using httpie to test out the endpoints.

For testing on the command line you can use something like this to create new non-conflicting users:

```
usr="user_$(date +%y%d%H%M%S)"
pwd=testing###42
post_data=("username=$usr password=$pwd")
echo Registering: $post_data
http --verbose post http://127.0.0.1:8000/users/register $post_data
```

### users/register: Register A User

http --verbose post http://127.0.0.1:8000/users/register username="user\_\$(date +%H%M%S)" password=tatltuae42

### users/login: Log A User In

http --verbose post http://127.0.0.1:8000/users/login username="cacciaresi" password="cacciaresi"

---

## TODO - Things I Need To Come Back To

- [_] For the users/registers & users/login endpoints, username needs to become user to match the specs.
- [_] Will also need to verify that the headers in use match the specs
- [_] Is there a better way to do the regex based assertion testing (in api/tests.py)
- [_] Tests between register and login endpoints can probably be refactored to eliminate duplication for common tests.
