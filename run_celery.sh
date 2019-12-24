#!/bin/bash
# Nos movemos al directorio donde se encuentra el microservicio en Celery.
cd src/mascotas/
# Ejecutamos el servidor Celery, especificando el microservicio con el parámetro "-A".
# Con el argumento "--beat" iniciamos el scheduled de Celery para que la tarea
# periódica en la que se recopilan los datos de las mascotas se ejecute cuando le corresponda.
# Mediante el parámetro "--concurrency" especificamos el número de hijos/hebras
# que lanzará el servidor. Como nuestro requisito es poder llegar a 10 usuarios
# concurrentes, especificamos este mismo número.
# Por último, mediante el argumento "--loglevel=info" podremos controlar el inicio
# del servidor así como la ejecución de la tarea periódica.
pipenv run celery worker -A mascotas_celery --beat --concurrency=10 --loglevel=info