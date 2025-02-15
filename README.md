# Project Setup

## Install virtualenv: 
<code>
sudo apt install python3-virtualenv
</code>

## Create a project venv: 
<code>
virtualenv .venv
</code>

## Activate venv:
<code>
source .venv/bin/activate
</code>

## Install dependencies:
<code>
pip install django djangorestframework djangorestframework_simplejwt
</code>

## Create a django project:
<code>
django-admin startproject task_manager
</code>

## Create a django apps:
<code>
cd task_manager
python manage.py startapp tm_admin
python manage.py startapp tm_api
</code>


## Configuring Django Rest Framework and Apps
<code>
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    tm_admin,
    tm_api
]
</code>


## Configuring JWT Settings
<code>
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}
</code>

## Setup Token Endpoints
<code>
TokenObtainPairView
TokenRefreshView
</code>



## Make Migrations
<code>
python manage.py makemigrations
python manage.py migrate
</code>

## Generate default admin user
<code>
python manage.py generatedefaultsuperuser
</code>

## Run application
<code>
python manage.py runserver
</code>

