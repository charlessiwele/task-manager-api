FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DEBUG_MODE 0
# ENV POSTGRES_DB tm_db
# ENV POSTGRES_USER admin
# ENV POSTGRES_PASSWORD admin
# ENV POSTGRES_HOST 172.18.0.1
# ENV POSTGRES_PORT 5432
# ENV POSTGRES_CONN_STRING = postgresql://admin:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.frankfurt-postgres.render.com/tm_db_6n22
# Set work directory
WORKDIR /usr/src/

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt /usr/src/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

RUN mkdir  /usr/src/task_manager/
RUN mkdir  /usr/src/task_manager/tm_api
RUN mkdir  /usr/src/task_manager/task_manager

WORKDIR /usr/src/task_manager

# Copy project
COPY ./task_manager/manage.py /usr/src/task_manager/
COPY ./task_manager/task_manager/ /usr/src/task_manager/task_manager
COPY ./task_manager/tm_api/ /usr/src/task_manager/tm_api/

# # Collect static files
RUN python manage.py collectstatic --noinput

# # Generate any migrations required
RUN python manage.py makemigrations

# # Run any  required migrations
RUN python manage.py migrate

# # Generate default superuser
RUN python manage.py generate_default_staff_user
RUN python manage.py generate_default_statuses
RUN python manage.py generate_default_superuser
RUN python manage.py generate_default_generic_user

# # Expose the port the app runs on
EXPOSE 8000

# # Run the application
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8000", "task_manager.wsgi:application"]
