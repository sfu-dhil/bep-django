# Books in English Parishes

[Books in English Parishes][https://dhil.lib.sfu.ca/bep] (affectionately known as BEP) is a Python application written using the [Django][https://www.djangoproject.com/] framework. It is a digital tool for collecting data and metadata
about books used in English parishes.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Initialize the Application

    docker compose up -d --build

Frontend will be available at `http://localhost:8080/`
Admin Interface will be available at `http://localhost:8080/admin/`

### Create your superuser

    docker exec -it bep_app python manage.py createsuperuser

Enter `username`, `email`, and `password` as prompted

example:

    docker exec -it bep_app python manage.py createsuperuser --username="admin" --email="dhil@sfu.ca"

## General Usage

### Starting the Application

    docker compose up -d

### Stopping the Application

    docker compose down

### Rebuilding the Application (after upstream or js/python package changes)

    docker compose up -d --build

### Viewing logs (each container)

    docker logs -f bep_app
    docker logs -f bep_db
    docker logs -f bep_mail

### Accessing the Application

    http://localhost:8080/

### Accessing the Database

Command line:

    docker exec -it bep_db mysql -u bep -ppassword bep

Through a database management tool:
- Host:`127.0.0.1`
- Port: `15432`
- Username: `bep`
- Password: `password`

### Accessing Mailhog (catches emails sent by the app)

    http://localhost:8025/

### Database Migrations

Migrate up to latest

    docker exec -it bep_app python manage.py migrate

Create new migrations

    docker exec -it bep_app python manage.py makemigrations

## Updating Application Dependencies

### Yarn (javascript)

First setup an image to build the yarn deps in

    docker build -t bep_yarn_helper --target bep-prod-assets .

Then run the following as needed

    # add new package
    docker run -it --rm -v $(pwd):/app bep_yarn_helper yarn add [package]

    # update a package
    docker run -it --rm -v $(pwd):/app bep_yarn_helper yarn upgrade [package]

    # update all packages
    docker run -it --rm -v $(pwd):/app bep_yarn_helper yarn upgrade

Note: If you are having problems starting/building the application due to javascript dependencies issues you can also run a standalone node container to help resolve them

    docker run -it --rm -v $(pwd):/app -w /app node:22.3 bash

    [check Dockerfile for the 'apt-get update' code piece of bep-prod-assets]

    yarn ...

After you update a dependency make sure to rebuild the images

    docker compose down
    docker compose up -d

### Pip (python)

Manage python dependencies in `requirements.txt`
>All packages should be locked to a specific version number if possible (Ex `Django==4.2.7`)
>Some special packages cannot be locked and should be noted as such (Ex `psycopg[binary]`)

After making changes, you need to run pip or rebuild the image

    docker exec -it bep_app pip install -r requirements.txt
    # or
    docker compose up -d --build

#### Update a package

Edit version number in `requirements.txt` with new locked version number
>Ex `pip==24.0.0`

    docker exec -it bep_app pip install -r requirements.txt
    # or
    docker compose up -d --build
