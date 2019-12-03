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

# Copiamos los ficheros correspondientes al módulo "mascotas" y su microservicio
# al directorio de trabajo.
COPY src/mascotas/mascotas.py src/mascotas/ficha_mascota.py src/mascotas/mascotas_rest.py ./

# Informamos acerca del puerto en el que se van a escuchar las peticiones.
EXPOSE ${PORT}

# Ejecutamos el servidor Gunicorn estableciendo como puerto el anterior.
CMD gunicorn -b 0.0.0.0:${PORT} mascotas_rest:app