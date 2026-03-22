# Passos para criação de um projeto Django

### Criar diretorio e ambiente virtual
    mkdir Schedule && cd Schedule

    python3 -m venv .venv
    source .venv/bin/activate

    pip install django

### Criar um novo projeto Django
    django-admin startproject Schedule

### executar servidor
    python3 manage.py runserver



## Alterando banco de dados para MySQL

### Alterações em settings.py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'schedule_database',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            }
    }
<i>documentação: https://docs.djangoproject.com/en/6.0/ref/settings/</i>

### Criação do banco via docker, Dockerfile
    FROM mysql:8.0.32

    ENV MYSQL_ROOT_PASSWORD password
    COPY ./database/01_create_database.sql /docker-entrypoint-initdb.d/data.sql

### Build da imagem definindo tag (-t)
    docker build -t schedule-db .

### Script de criação do banco
    mkdir database && cd database
    touch 01_create_database.sql

    CREATE DATABASE schedule_database;
    USE schedule_database;

### Executar container, mapeando a porta 3306 do host para 3306 do container
    docker run -d -p 3306:3306 --name=schedule-mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=schedule_database schedule-db
<em>Esse comando não deve ser necessario caso tenha rodado o docker compose feito na pasta 'schedule'</em>

### Instalar mysqlclient
    pip install mysqlclient

### Executar migrations do Django
    python3 manage.py makemigrations
    python3 manage.py migrate

# Criar uma nova aplicação

### criar uma aplicacao chamada task
    django-admin startapp tasks

### Adicionar a aplicacao task ao 'INSTALLED_APPS' em settings.py
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "tasks",
    ]

# Criando nova tabela no banco de dados

### Mudanças sao feitas no 'models.py' da task criada
    from django.db import models

    class Task(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField()
        due_date = models.DateField()
        completed = models.BooleanField(default=False)
        priority = models.IntegerField(choices=((1, 'Baixa'), (2, 'Média'), (3, 'Alta')))
        created_at = models.DateTimeField(auto_now_add=True)
<i>documentação: https://docs.djangoproject.com/en/3.2/topics/db/models/#module-django.db.models</i>

### Faça novamente as atualizacoes no banco
    python3 manage.py makemigrations
    python3 manage.py migrate
<em>Verifique no cliente (no meu caso, DBeaver) se a tabela foi criada</em>


# Criar novo SuperUsuario para a url '/admin'

### Criando usuario
    python3 manage.py createsuperuser
<p>Forneca usuario/email e senha quando solicitado</p>

### Registre o modelo 'Task' no arquivo 'admin.py' da aplicação 'task'
    from django.contrib import admin
    from .models import Task


    admin.site.register(Task)