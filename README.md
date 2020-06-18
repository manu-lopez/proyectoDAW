

![image-20200618200959076](/home/work/.config/Typora/typora-user-images/image-20200618200959076.png)

# Best Learning Resources (BLR)

## Manuel López Ramos, 2º DAW

Cuando se quiere aprender un lenguaje de programación o alguna nueva tecnología, encontramos una enorme cantidad de recursos. Pero..., ¿realmente son de calidad?. A partir de la gran cantidad de material con el que aprender disponible hoy día sería buena idea crear una plataforma donde se puedan aportar recursos que, con un sistema de puntuación para clasificarlos, nos permita disponer de aquellos que alcancen una calidad máxima.

## Construido con 🛠️

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Django](https://www.djangoproject.com/)
  - [Django Cripsy Forms](https://github.com/django-crispy-forms/django-crispy-forms)
  - [Django Filter](https://github.com/carltongibson/django-filter)
  - [Django Taggit](https://github.com/jazzband/django-taggit)
  - [Django Vote](https://github.com/shellfly/django-vote)
  - [Django Comment](https://github.com/Radi85/Comment)
- [PostgreSQL](https://www.postgresql.org/)

## Documentación

La realización del proyecto la podemos dividir en tres partes, la primera sería el desarrollo de la plataforma de despliegue en **Docker**, la segunda el desarrollo del backend con **Django** y **Postgresql** y la última sería maquetación con **Bootstrap**.

### Primera parte:

> Para esta parte me ha venido genial la realización del curso de OpenWebinars de [Docker para Desarrolladores](https://openwebinars.net/academia/portada/docker/)

El usar Docker como plataforma de despliegue nos aporta bastantes ventajas, ya que nos abstrae de nuestra plataforma personal de desarrollo y luego en producción con tener un VPS corriendo Linux es suficiente. De esta forma no tendremos problemas de compatibilidades ni conflictos con el resto de proyectos que podamos tener.

Docker contiene imagenes oficiales en [docker hub](https://hub.docker.com/), para este proyecto usaremos una imagen oficial y ademas crearemos una nosotros.

La imagen que vamos a crear es partir de la imagen oficial de [python](https://hub.docker.com/_/python). El archivo dockerfile es el siguiente.

> ### dockerfile

```dockerfile
# Pull from official image
FROM python:3.8-buster

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# Create and set work directory
RUN mkdir /code
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt /code/

# Update system
RUN apt-get update

# Cloning and installing comment repository because installing with pip gives errors
RUN git clone https://github.com/radi85/Comment.git && cd Comment && python setup.py install

# Install rest django requeriments
RUN pip install -r requirements.txt

# Copy project
COPY /proyecto /code/
```

Como podemos ver, partimos de la imagen oficial `python:3.8-buster` (buster es una versión debian) y luego procedemos a "formar" nuestra imagen Python con **Django**.

Hemos comentado que haciamos uso de dos imagenes, por lo que tenemos que tener hacer uso de `docker-compose` y por lo tanto necesitamos el siguiente archivo.

> ### docker-compose.yml

```yaml
version: '3'

services:
  db:
    image: postgres:11.7
    container_name: container_postgres
    restart: always
    environment:
      POSTGRES_USER: "YOUR USER"
      POSTGRES_PASSWORD: "YOUR PASSWORD"
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data/

  web:
    image: djangoslim
    container_name: container_django
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./proyecto:/code
    ports:
      - "8000:8000"
    depends_on:
      - db 
      
volumes:
  postgres_data:
```

Lo más relevante que podemos comentar de este documento para que comprendan es lo siguiente:

- `services`: Tenemos dos servicios, que son `db`y `web`, que corresponde a nuestros dos contenedores y además tenemos `volumes` que como el nombre indica, es un volumen donde tenemos los datos de la base de datos y de está manera conseguimos cierta persistencia, ya que podremos borrar y reconstruir los contenedores si lo necesitamos, pero no perderemos los datos.
- `image`: En este campo procedemos a seleccionar la imagen que usaremos en nuestro contenedor, para el contenedor `db` usamos la imagen oficial de postgres en su version `11.7` y para `web` la imagen que creamos antes en el archivo [`dockerfile`](#dockerfile) (se lo indicamos en `build`: .).
- `depends_on`: Le indicamos dependencia entre servicios.
- `ports` y `volumes`: Funcionan de la siguiente manera: `"puerto local":"puerto contenedor"` || `"ruta local":"ruta contenedor"`. Al tener los volumes, tanto nosotros como el contenedor accedemos al código en el mismo lugar (nuestra carpeta `proyecto`en este caso concreto)

De esta manera tenemos nuestra paltaforma de desarrollo y despliegue. [Aquí](#instalación)

# Instalación

### Pre-requisitos 📋

Independientemente del sistema operativo que tengamos (Linux/MacOs/Windows), tenemos que tener instalado (mediante repositorio/Homebrew/instalador desde web oficial) lo indicado a continuación:

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop)
- Editor de código

### Instalación 🔧

Una vez tengamos todo instalado, el primer paso será clonar este repositorio.

```bash
git clone https://github.com/manu-lopez/proyectoDAW.git
```

A continuación debemos asegurarnos que tenemos Docker corriendo. 

```bash
# Podemos ejecutar uno de estos comandos
docker version 
docker info
```

Nos dará información de Docker o en el caso de que no esté corriendo, nos dirá que no consiguió conectar con el daemon.

Cuando tengamos seguro que Docker está funcionando, pasamos a construir el contenedor django.

```bash
docker-compose build
```

Una vez termine este proceso, pasamos a ejecutar el siguiente comando.

```bash
docker-compose up
```

De esta manera tendremos tanto django como postgres funcionando, a continuación debemos realizar un par de pasos dentro del contenedor de django.

```bash
# Entramos dentro del contenedor
docker exec -it container_django bash

# Lo siguiente será crear las migraciones y migrarlas.
python manage.py makemigrations
python manage.py migrate

# Por último creamos un super usuario
python manage.py createsuperuser

```

Ya podremos acceder a la plataforma como vemos en esta imagen.

![image-20200618194023682](/home/work/.config/Typora/typora-user-images/image-20200618194023682.png)

El último paso para tener completamente funcional la plataforma, es crear los tipos que creas convenientes para los recursos que aportaran los usuarios. Para ello entramos con nuestra cuenta de super usuario en `/admin` y añadimos los tipos en Types.

![image-20200618194820946](/home/work/.config/Typora/typora-user-images/image-20200618194820946.png)

En este caso por ejemplo he añadido los siguientes.

![image-20200618194929268](/home/work/.config/Typora/typora-user-images/image-20200618194929268.png)

Con esto ya podemos crear recursos perfectamente.

## Autor ✒️

- [Manuel López Ramos](https://github.com/manu-lopez)