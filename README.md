# Project Setup

# Project Progressive Notes
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

## Freeze dependencies:
<code>
pip ## Install dependencies:
<code>
pip freeze > requirements.txt
</code>

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


## To build the docker tm-app image:
sudo docker build -t tm-app .

## To run the docker tm-app container:
sudo docker run --name tm-app-1 -p 8000:8000 tm-app

## To stop the docker tm-app container:
sudo docker stop tm-app-1

## To remove the docker tm-app container before re-running:
sudo docker rm tm-app-1

## To rebuild & restart:
sudo docker stop tm-app-1 && \
sudo docker rm tm-app-1 && \
sudo docker build -t tm-app . && \
sudo docker run --name tm-app-1 -p 8000:8000 tm-app

## To remove  docker network:
sudo docker network rm tm-network

## To create docker network:
sudo docker network create -d bridge tm-network

## Fetch PostgreSQL image
sudo docker pull postgres

## Starting the PostgreSQL Container
sudo docker run --name tm-postgres-1 -e POSTGRES_PASSWORD=admin postgres

## Starting the PostgreSQL Container on the Network "tm-network"
sudo docker run --name tm-postgres-1 \
-e POSTGRES_DB=tm_db \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin \
-d --network=tm-network postgres

## Stop-Start PostgreSQL Container on the Network "tm-network"
sudo docker stop tm-postgres-1 && \
sudo docker rm tm-postgres-1 && \
sudo docker run --name tm-postgres-1 \
-e POSTGRES_DB=tm_db \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin \
-d --network=tm-network \
-p 5432:5432 postgres

## To rebuild & restart tm-app on the Network "tm-network":
sudo docker stop tm-app-1 && \
sudo docker rm tm-app-1 && \
sudo docker build -t tm-app . && \
sudo docker run --name tm-app-1 -p 8000:8000 --network=tm-network tm-app

## Inspecting the Network "tm-network":
docker network inspect tm-network


## Default user credentials:
# Admin:
username: admin
password: admin
# Staff:
username: staff
password: staff
# Genric:
username: genric
password: genric
