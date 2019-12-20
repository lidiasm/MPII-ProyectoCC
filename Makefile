install:
	# Instala y crea un entorno virtual con Python 3.
	pipenv install --three
	# Instala las dependencias necesarias para la aplicación en el entorno virtual.
	pipenv run pip install -r requirements.txt

test:
	# Ejecuta los tests de la clase Mascotas y de la clase de su API REST.
	pipenv run python -m pytest tests/*
	# Tests de covertura para la clase Mascotas y la clase de su API REST.
	pipenv run python -m pytest --cov=mascotas --cov=conexion_api_petfinder --cov=mascotas_celery --cov=mascotas_rest --cov=busqueda tests/

start:
	# Inicio del servidor de tareas Celery mediante la consola de Python.
	# Con la opción --beat iniciamos también el programador de tareas de Celery parar
	# ejecutar las tareas periódicas.
	pipenv run python3 src/mascotas/mascotas_celery.py celery worker --beat --concurrency=3 #-n celery1@lidiaubuntu
	#pipenv run python3 src/mascotas/mascotas_celery.py celery worker --beat --concurrency=3 -n celery2@lidiaubuntu
	#pipenv run python3 src/mascotas/mascotas_celery.py celery worker --beat --concurrency=3 -n celery3@lidiaubuntu

	# Inicio del servidor Green Unicorn. Para ello se realizan una serie de pasos:
		# 1) Cambio al directorio del módulo "mascotas" donde se encuentran las clases
		#			de la lógica de la aplicación y del microservicio.
		# 2) Escribe en el directorio del módulo mascotas un fichero con el identificador del proceso
		# 		asociado al servidor. Esto nos será de utilidad cuando deseemos terminar su ejecución sin
		# 		utilizar un gestor de procesos adicional.
		# 3) Con la opción "-D" evitamos que el terminal se quede bloqueado por la ejecución del servidor.
		# 4) Con la opción "-b" especificamos los puertos en los que se atenderán las peticiones.
		#			Por razones de seguridad estos puertos se establecerán mediante variables de entorno que deberán
		#			estar creadas antes de iniciar los microservicios REST.


		# De la página: https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
		# sacamos el número de workers (2*CPU)+1 y el número de hebras.
		# Lo repartimos en workers y hebras para atender hasta 9 peticiones simultáneas.
	pipenv run gunicorn --worker-class=gevent --worker-connections=1000 --workers=3 --chdir src/mascotas/ mascotas_rest:app -p pid_gunicorn.pid -b :${PORT1}
#	pipenv run gunicorn --chdir src/busqueda/ busqueda_rest:app -p pid_gunicorn.pid -D -b :${PORT2}

stop:
	#pipenv run pkill -f `mascotas_celery`
	# Fin de la ejecución del proceso asociado al servidor Gunicorn. Para ello se hará uso del comando
	# 	'kill', el cual solo necesita el identificador de un proceso para terminar su ejecución.
	#		Como se comentaba anteriormente, este ID se encuentra en el fichero "pid_gunicorn.pid".
	pipenv run kill `cat src/mascotas/pid_gunicorn.pid`