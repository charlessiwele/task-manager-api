# Project Documentation
## Description
This project is a task management system built with Django and Django REST Framework. It provides endpoints for user authentication, task management, and status management. The application uses JWT for secure authentication and includes Docker support for easy deployment.

## Table of Contents
- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Endpoints](#endpoints)
    - [Register](#register)
    - [Login Token](#login-token)
    - [Refresh Login Token](#refresh-login-token)
    - [Login Auth](#login-auth)
    - [Logout Token](#logout-token)
    - [Logout Auth](#logout-auth)
    - [Status](#status)
    - [Tasks](#tasks)
- [Models](#models)
    - [Status](#status-1)
    - [Task](#task)
- [Serializers](#serializers)
    - [StatusSerializer](#statusserializer)
    - [RegisterSerializer](#registerserializer)
    - [TaskSerializer](#taskserializer)
- [PostgreSQL Connection](#postgresql-connection)
    - [Using Access Credentials](#using-access-credentials)
    - [Using Connection String](#using-connection-string)
    - [Configuration Check](#configuration-check)
- [CICD Configuration](#cicd-configuration)
    - [Workflow](#workflow)
    - [Configuration](#configuration)
- [Default user credentials](#default-user-credentials)
    - [Default Admin/Superuser](#default-adminsuperuser)
    - [Default Staff](#default-staff)
    - [Default Generic](#default-generic)
- [Progressive Technical Notes](#progressive-technical-notes)
    - [Install virtualenv](#install-virtualenv)
    - [Create a project venv](#create-a-project-venv)
    - [To build the docker tm-app image](#to-build-the-docker-tm-app-image)
    - [To run the docker tm-app container](#to-run-the-docker-tm-app-container)
    - [To stop the docker tm-app container](#to-stop-the-docker-tm-app-container)
    - [To remove the docker tm-app container before re-running](#to-remove-the-docker-tm-app-container-before-re-running)
    - [To rebuild & restart](#to-rebuild--restart)
    - [To remove docker network](#to-remove-docker-network)
    - [To create docker network](#to-create-docker-network)
    - [Fetch PostgreSQL image](#fetch-postgresql-image)
    - [Starting the PostgreSQL Container](#starting-the-postgresql-container)
    - [Starting the PostgreSQL Container on the Network "tm-network"](#starting-the-postgresql-container-on-the-network-tm-network)
    - [Stop-Start PostgreSQL Container on the Network "tm-network"](#stop-start-postgresql-container-on-the-network-tm-network)
    - [To rebuild & restart tm-app on the Network "tm-network"](#to-rebuild--restart-tm-app-on-the-network-tm-network)
    - [Inspecting the Network "tm-network"](#inspecting-the-network-tm-network)

## Endpoints
### Register
- **URL**: `/register/`
- **Methods**: `POST`
- **Description**: Registers a new user.
- **Request Body**:
    - `username` (string): Required. The username of the user.
    - `email` (string): Required. The email of the user.
    - `password` (string): Required. The password of the user.
- **Response**:
    - `200 OK`: User registered successfully.
    - `500 Internal Server Error`: Error message.

### Login Token
- **URL**: `/login_token/`
- **Methods**: `POST`
- **Description**: Generates a login token.
- **Request Body**:
    - `username` (string): Required. The username of the user.
    - `password` (string): Required. The password of the user.
- **Response**:
    - `200 OK`: Token generated successfully.
    - `500 Internal Server Error`: Error message.

### Refresh Login Token
- **URL**: `/refresh_login_token/`
- **Methods**: `POST`
- **Description**: Refreshes the login token.
- **Request Body**:
    - `refresh` (string): Required. The refresh token.
- **Response**:
    - `200 OK`: Token refreshed successfully.
    - `500 Internal Server Error`: Error message.

### Login Auth
- **URL**: `/login_auth/`
- **Methods**: `POST`
- **Description**: Authenticates and logs in a user.
- **Request Body**:
    - `username` (string): Required. The username of the user.
    - `password` (string): Required. The password of the user.
- **Response**:
    - `200 OK`: User authenticated and logged in successfully.
    - `401 Unauthorized`: Invalid login credentials.
    - `500 Internal Server Error`: Error message.

### Logout Token
- **URL**: `/logout_token/`
- **Methods**: `POST`
- **Description**: Logs out a user by blacklisting the refresh token.
- **Request Body**:
    - `refresh` (string): Required. The refresh token.
- **Response**:
    - `200 OK`: User logged out successfully.
    - `400 Bad Request`: Refresh token is required.
    - `404 Not Found`: No user detected to logout.
    - `401 Unauthorized`: Error message.

### Logout Auth
- **URL**: `/logout_auth/`
- **Methods**: `GET`
- **Description**: Logs out a user by ending the session.
- **Response**:
    - `200 OK`: User logged out successfully.
    - `404 Not Found`: No user detected to logout.
    - `401 Unauthorized`: Error message.

### Status
- **URL**: `/status/`
- **Methods**: `GET`, `POST`, `PUT`
- **Description**: Manages status entities.
- **Request Body** (for `POST` and `PUT`):
    - `name` (string): Required. The name of the status.
    - `description` (string): Optional. The description of the status.
- **Response**:
    - `200 OK`: Status retrieved/updated successfully.
    - `201 Created`: Status created successfully.
    - `500 Internal Server Error`: Error message.

### Tasks
- **URL**: `/tasks/`
- **Methods**: `GET`, `POST`, `PUT`
- **Description**: Manages task entities.
- **Request Body** (for `POST` and `PUT`):
    - `title` (string): Required. The title of the task.
    - `description` (string): Required. The description of the task.
    - `due_date` (datetime): Required. The due date of the task.
    - `status` (integer): Optional. The ID of the status.
- **Response**:
    - `200 OK`: Task retrieved/updated successfully.
    - `201 Created`: Task created successfully.
    - `500 Internal Server Error`: Error message.

## Models

### Status
- **Fields**:
    - `id` (integer): The ID of the status.
    - `name` (string): The name of the status.
    - `description` (string): The description of the status.
- **Meta**:
    - `verbose_name_plural`: "Statuses"

### Task
- **Fields**:
    - `id` (integer): The ID of the task.
    - `title` (string): The title of the task.
    - `description` (string): The description of the task.
    - `due_date` (datetime): The due date of the task.
    - `status` (ForeignKey): The status of the task.
    - `user` (ForeignKey): The user assigned to the task.
- **Meta**:
    - `verbose_name_plural`: "Tasks"

## Serializers

### StatusSerializer
- **Fields**:
    - `id` (integer): The ID of the status.
    - `name` (string): The name of the status.
    - `description` (string): The description of the status.

### RegisterSerializer
- **Fields**:
    - `id` (integer): The ID of the user.
    - `username` (string): The username of the user.
    - `email` (string): The email of the user.
    - `password` (string): The password of the user.

### TaskSerializer
- **Fields**:
    - `id` (integer): The ID of the task.
    - `title` (string): The title of the task.
    - `description` (string): The description of the task.
    - `due_date` (datetime): The due date of the task.
    - `status` (integer): The ID of the status.

    ## PostgreSQL Connection

    To connect the Django application to a PostgreSQL database, you must provide either the connection string or the access credentials. The application is configured to check for these variables and use them accordingly.

    ### Using Access Credentials
    If you choose to use access credentials, you need to provide the following environment variables:
    - `POSTGRES_USER`: The username for the PostgreSQL database.
    - `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
    - `POSTGRES_HOST`: The host address of the PostgreSQL database.
    - `POSTGRES_PORT`: The port number of the PostgreSQL database.

    **Note**: Ensure that you exclude the `POSTGRES_DB` variable from the environment variables when using access credentials.

    ### Using Connection String
    Alternatively, you can provide a connection string using the `POSTGRES_CONN_STRING` environment variable. This connection string should include all necessary details to connect to the PostgreSQL database.

    **Example Connection String**:
    ```
    POSTGRES_CONN_STRING=postgres://<username>:<password>@<host>:<port>/<database>
    ```

    ### Configuration Check
    The application includes a check condition to determine which method to use for connecting to the PostgreSQL database. If the `POSTGRES_CONN_STRING` variable is provided, it will take precedence over the individual access credentials.

    Ensure that your environment variables are set correctly to avoid connection issues.

    ## CICD Configuration

    The current Continuous Integration and Continuous Deployment (CICD) configuration is set up to ensure code quality and seamless deployment. The process involves running tests on the development branch and then merging the changes to the testing branch if all tests pass.

    ### Workflow
    1. **Development Branch**:
        - Developers push their changes to the `development` branch.
        - Automated tests are triggered to run on the `development` branch.
        - If all tests pass, the changes are automatically merged into the `testing` branch.

    2. **Testing Branch**:
        - The `testing` branch receives the merged changes from the `development` branch.
        - Additional integration tests can be run on the `testing` branch to ensure the stability of the application before deploying to production.

    This configuration ensures that only code that passes all tests in the `development` branch is merged into the `testing` branch, maintaining the integrity and stability of the application.

## Default user credentials:
The default credentials are generated as a step in the Dockerfile. This ensures that the application has a set of credentials to use when it is first built and run. You can find the relevant section in the Dockerfile where these credentials are created.

Make sure to update these credentials in a production environment to ensure the security of your application.
### Default Admin/Superuser:
username: admin
password: admin
### Default Staff:
username: staff
password: staff
### Default Generic:
username: generic
password: generic

## Postman Collection

A Postman collection is available in the `postman_scripts` folder. This collection includes pre-configured requests for all the endpoints provided by the application. You can import this collection into Postman to easily test and interact with the API.

### Importing the Collection
1. Open Postman.
2. Click on the `Import` button.
3. Select the `postman_scripts` folder and choose the collection file.
4. Click `Open` to import the collection.

Once imported, you can use the requests in the collection to test the various endpoints of the application.

# Progressive Technical Notes
## Install virtualenv: 
<code>
sudo apt install python3-virtualenv
</code>

## Create a project venv: 
<code>
virtualenv .venv
</code>
<code>
pip install django djangorestframework djangorestframework_simplejwt psycopg2-binary dj-database-url
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
