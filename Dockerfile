# Establecemos la imagen para el contenedor. En mi caso voy a optar por el 
# sistema operativo Debian con la versión slim de Python 3.6, puesto que es en la
# que estoy desarrollando el proyecto.
FROM python:3.6-slim

# Datos sobre el dueño del contenedor.
LABEL maintainer="Lidia Sánchez lidiasm96@correo.ugr.es"

# Le pasamos como argumento el puerto donde deberá escuchar las peticiones.
ARG PUERTO
# Establecemos el puerto pasado como parámetro como una variable de entorno 
# para que persista tras la construcción del contenedor. 
ENV PUERTO ${PUERTO}

# Establecemos el directorio de trabajo del proyecto.
WORKDIR Escritorio/CC/ProyectoCC

# Copiamos el fichero donde se encuentran las dependencias necesarias para ejecutar
# la aplicación a la carpeta temporal.
COPY docker_requirements.txt /tmp/
# Actualizamos el sistema operativo y pip. Además instalamos las dependencias 
# del fichero anterior.
RUN apt-get update && pip install --upgrade pip && pip install --requirement /tmp/docker_requirements.txt

# Copiamos los ficheros correspondientes al módulo "mascotas" y su microservicio
# al directorio de trabajo.
COPY src/mascotas/mascotas.py src/mascotas/ficha_mascota.py src/mascotas/mascotas_rest.py ./

# Especificamos el puerto para que las peticiones lleguen al contenedor.
EXPOSE ${PUERTO}

# Ejecutamos el servidor Gunicorn estableciendo como puerto el anterior.
CMD gunicorn -b 0.0.0.0:5000 mascotas_rest:app
