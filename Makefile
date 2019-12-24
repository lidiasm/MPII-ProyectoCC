install:
	# Instala y crea un entorno virtual con Python 3.
	pipenv install --three
	# Instala las dependencias necesarias para la aplicación en el entorno virtual.
	pipenv run pip install -r requirements.txt

test:
	# Ejecuta todos los tests existentes para cada una de las clases de la lógica
	# de la aplicación así como los microservicios REST y Celery.
	pipenv run python -m pytest tests/*
	# Tests de covertura para todas las clases actuales.
	pipenv run python -m pytest --cov=mascotas --cov=conexion_api_petfinder \
		--cov=mascotas_celery --cov=mascotas_rest --cov=mongodb tests/

start:
	# Iniciamos el servidor Gunicorn con los siguientes parámetros:
	# 1. Mediante el parámetro "--chdir" cambiamos al directorio del módulo Mascotas
	#		donde se encuentra el microservicio REST dedicado a visualizar los datos de estas.
	# 2. Con el parámetro "-p" escribe el identificador del proceso asociado al servidor
	#		en un archivo para, posteriormente, poder finalizar su ejecución.
	# 3. Con la opción "-b" especificamos el puerto donde se atenderán las peticiones.
	#			Para ello se deberá definir, préviamente, un variable de entorno denominada PORT.
	# 4. Con la opción "-D" silenciamos la salida del inicio del servidor.

	### MEJORAS DE LAS PRESTACIONES.
	# Tras investigar cómo mejorar las prestaciones que puede ofrecer Gunicorn, me encontré con
	# esta fuente: https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
	# en la que se especifican ciertos parámetros que optimizan su ejecución.
	# 1. Si bien Gunicorn es asíncrono, se le puede añadir un módulo con el que este





		# De la página:
		# sacamos el número de workers (2*CPU)+1 y el número de hebras.
		# Lo repartimos en workers y hebras para atender hasta 9 peticiones simultáneas.
		pipenv run gunicorn --worker-class=gevent --worker-connections=1000 --workers=3 \
		  --chdir src/mascotas/ mascotas_rest:app -p pid_gunicorn.pid -b :${PORT1} -D
		pipenv run bash run_celery.sh
		#pipenv run gunicorn --worker-class=gevent --worker-connections=1000 --workers=3 \
			--chdir src/mascotas/ mascotas_rest:app -p pid_gunicorn.pid -b :${PORT1} -D
		# Hypercorn
		#pipenv run hypercorn --worker-class=asyncio --workers=3 src/mascotas/mascotas_rest:app -p ./src/mascotas/pid_hypercorn.pid -b :${PORT1}
		# Uvicorn
		#pipenv run gunicorn -k uvicorn.workers.UvicornWorker --workers=3 --chdir src/mascotas/ mascotas_rest:app -p pid_gunicorn.pid -b :${PORT1}


		#pipenv run gunicorn --chdir src/busqueda/ busqueda_rest:app -p pid_gunicorn.pid -D -b :${PORT2}

stop:
	# Fin de la ejecución del proceso asociado al servidor Gunicorn. Para ello se hará uso del comando
	# 	'kill', el cual solo necesita el identificador de un proceso para terminar su ejecución.
	#		Como se comentaba anteriormente, este ID se encuentra en el fichero "pid_gunicorn.pid".
	pipenv run kill `cat src/mascotas/pid_gunicorn.pid`
	# Matamos todos los workers e hijos de Celery
	pipenv run pkill -9 -f 'celery worker'