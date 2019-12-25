# Sistema base elegido a partir de un estudio de prestaciones.
FROM python:3.6-slim-stretch

# Datos sobre el dueño del contenedor.
LABEL maintainer="Lidia Sánchez lidiasm96@correo.ugr.es"

# Pasamos el puerto al que debe conectarse Gunicorn estableciendo, para ello,
# una variable de entorno para que persista tras la construcción del contenedor.
ENV PORT ${PORT}

# Establecemos el directorio de trabajo del proyecto.
WORKDIR Escritorio/CC/ProyectoCC

# Copiamos el fichero donde se encuentran las dependencias necesarias para ejecutar
# la aplicación a la carpeta temporal.
COPY docker_requirements.txt /tmp/
# Actualizamos el sistema operativo y pip. Además instalamos las dependencias
# del fichero anterior.
RUN apt-get update && pip install --upgrade pip && pip install --requirement /tmp/docker_requirements.txt

# Copiamos los ficheros correspondientes al módulo Mascotas, la base de datos y
# los microservicios RESTs y en Celery.
COPY src/mongodb.py src/excepciones.py src/mascotas/conexion_api_petfinder.py src/mascotas/mascotas.py src/mascotas/mascotas_rest.py src/mascotas/mascotas_celery.py ./

# Iniciamos el servidor de tareas Celery, en particular, el microservicio encargado de recopilar
# datos de mascotas de forma periódica. Para ello iniciamos también su planificador y le añadimos
# un componente asociado al autoescalado para que pueda generar de 10 a 20 hebras.
RUN python3 ./mascotas_celery.py celery worker --beat --autoscale=20,10

# Informamos acerca del puerto en el que se van a escuchar las peticiones.
EXPOSE ${PORT}

# Ejecutamos el microservicio REST en diez copias del servidor Gunicorn de forma asíncrona.
CMD gunicorn --worker-class=gevent --worker-connections=1000 --workers=10 -b 0.0.0.0:${PORT} mascotas_rest:app