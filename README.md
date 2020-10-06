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

auth="Authorization:Token 2a397c3a4ad0df9e0d417c02e13f2cf7bd096ab6"
http --verbose post http://127.0.0.1:8000/feeds/add url="https://example.com/rss/$(date +%y%d%H%M%S)" "$auth"
```

### users/register: Register A User

http --verbose post http://127.0.0.1:8000/users/register username="user\_\$(date +%H%M%S)" password=tatltuae42

### users/login: Log A User In

http --verbose post http://127.0.0.1:8000/users/login username="cacciaresi" password="cacciaresi"

### users/login: Subscribe To An RSS Feed

http --verbose post http://127.0.0.1:8000/feeds/add url="https://example.com/rss/$(date +%y%d%H%M%S)" 'Authorization:Token 2a397c3a4ad0df9e0d417c02e13f2cf7bd096ab6'

### users/login: Reed The Articles Of A Feed

#### List A User's Feeds

http --verbose get http://127.0.0.1:8000/feeds 'Authorization:Token 2a397c3a4ad0df9e0d417c02e13f2cf7bd096ab6'

---

## RSS Reader Data Design

- Feed Data

  - ID (pk)
  - URL (uk)
  - Users (many-to-many with Users)
  - Title

- Feed Actions

  - Add a feed
  - Delete a feed
  - Get list of all feeds
  - Get list of articles belonging to a feed
  - Refresh a feed

- Article Data

  - ID (pk)
  - URL (uk)
  - Feed (fk, many-to-one with Feed)
  - Read By (many-to-many with Users)
  - Title
  - Summary
  - Content
  - Date
  - Loaded

- Article Actions
  - Mark article read/unread

### Thoughts

- A naive implementation might just let users add to a feed and keep a one-to-many link between Users and Feeds.
  - This would end up duplicating feeds in the table, e.g. if 5 users all added the same feed they'd exist in the Feeds table once per user.
- Since a feed can belong to many users and a user can have many feeds, it could (probably should) be modeled as a many-to-many relationship.
  - Depending on how refreshing should work, may need to do something special if one users refresh of a feed should not affect another user with tha feed.
- Articles will be many-to-one with a Feed, and will have a many-to-many relations ship with Users for keeping track of who read the articles.
- When a feed is first introduced something should fetch the feed data and populate articles - will need to decide if this will be done inline or as a separate process
- Created the Feed model, serializer, view, and exposed the feeds/add endpoint.
- Created the list view for the feeds endpoint.

- Moved additional tests to TODO list for now.
  Want to work on fetching the rss and dealing with it.

---

## TODO - Things I Need To Come Back To

- [_] For the users/registers & users/login endpoints, username needs to become user to match the specs.
- [_] Will also need to verify that the headers in use match the specs
- [_] Is there a better way to do the regex based assertion testing (in api/tests.py)
- [_] Should come back to refactor/reorganize tests (separate files for each endpoint?)
- [_] Tests between register and login endpoints can probably be refactored to eliminate duplication for common tests.
- [_] The feeds/add endpoit doesn't notify if user is already subscribed to a feed; just silently ignores that they requested to add the feed again.
- [_] Need tests for feeds, feeds/add
