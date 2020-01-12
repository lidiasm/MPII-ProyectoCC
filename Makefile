install:
	# Instala y crea un entorno virtual con Python 3.
	pipenv install --three
	# Instala las dependencias necesarias para la aplicación en el entorno virtual.
	pipenv run pip install -r requirements.txt

test:
	# Ejecuta todos los tests existentes para cada una de las clases de la lógica
	# de la aplicación así como los microservicios REST y Celery, y la base de datos.
	pipenv run python -m pytest tests/*
	# Tests de covertura para todas las clases actuales.
	pipenv run python -m pytest --cov=mascotas --cov=conexion_api_petfinder \
		--cov=mascotas_celery --cov=mascotas_rest --cov=mongodb --cov=estadisticas \
		--cov=estadisticas_celery --cov=estadisticas_rest tests/

start_mascotas:
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
	# 1. Si bien Python es síncrono, existen diversas librerías que permiten añadir concurrencia
	# 	a los programas escritos en este lenguaje. En mi caso utilizaré gevent estableciéndolo como
 	# 	el módulo a utilizar para ejecutar los workers de Gunicorn. De este modo, ahora el servidor
	#		Gunicorn atenderá peticiones de forma asíncrona.
	# 2. A continuación establecemos el número de workers que se van a ejecutar. Como mi máquina tiene
	#		cuatro CPUs, según la fuente anterior el número de workers es (2*4 CPUs)+1, por lo que se ejecutarán
	#		9 instancias de Gunicorn.
	# 3. Por último establecemos que el número de peticiones que asimilará cada worker serán 1.000. De este
	#		modo el número máximo de peticiones concurrentes que podrá soportar será 9.000.
	pipenv run gunicorn --worker-class=gevent --worker-connections=1000 --workers=10 \
	  --chdir src/mascotas/ mascotas_rest:app -p pid_gunicorn.pid -b :${PORT1} -D
	# Ejecutamos este script para iniciar el servidor Celery, su scheduled así como el microservicio
	# que contiene una tarea periódica consistente en descargar datos de mascotas cada 23 horas.
	pipenv run bash run_mascotas_celery.sh

start_estadisticas:
	# Iniciamos el microservicio REST asociado a las estadísticas en otro puerto.
	pipenv run gunicorn --worker-class=gevent --worker-connections=1000 --workers=10 \
	  --chdir src/estadisticas/ estadisticas_rest:app -p pid_gunicorn.pid -b :${PORT2} -D
	# Ejecutamos el microservicio en Celery que genera las Estadísticas
	pipenv run bash run_estadisticas_celery.sh

stop:
	# Fin de la ejecución de los microservicios RESTs.
	pipenv run kill `cat src/mascotas/pid_gunicorn.pid`
	pipenv run kill `cat src/estadisticas/pid_gunicorn.pid`
	# Fin de los workers de Celery.
	pipenv run pkill -9 -f 'celery worker'
	pipenv run pkill -9 -f 'celery.sh'