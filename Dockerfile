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

# Copiamos los ficheros correspondientes al módulo "mascotas" compuesto por las clases
# Mascota, FichaMascota que contiene la estructura con los datos que nos interesan de las mascotas,
# ConexionAPIPetfinder que se trata de una clase singleton para instanciar un único objeto con la conexión a la api.
# Del mismo modo también copiamos el fichero del microservicio REST y el correspondiente al servidor de tareas Celery. 
COPY src/mascotas/conexion_api_petfinder.py src/mascotas/mascotas.py src/mascotas/ficha_mascota.py src/mascotas/mascotas_rest.py src/mascotas/mascotas_celery.py ./

# Iniciamos el servidor Celery del mismo modo que lo hacemos en el fichero makefile. 
RUN python3 ./mascotas_celery.py celery worker --beat

# Informamos acerca del puerto en el que se van a escuchar las peticiones.
EXPOSE ${PORT}

# Ejecutamos el servidor Gunicorn estableciendo como puerto el anterior.
CMD gunicorn -b 0.0.0.0:${PORT} mascotas_rest:app