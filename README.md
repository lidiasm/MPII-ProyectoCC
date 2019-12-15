## Proyecto de Cloud Computing 2019-2020.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/lidiasm/ProyectoCC.svg?branch=master)](https://travis-ci.org/lidiasm/ProyectoCC)
[![CircleCI](https://circleci.com/gh/lidiasm/ProyectoCC/tree/master.svg?style=svg)](https://circleci.com/gh/lidiasm/ProyectoCC/tree/master)
[![Codecov](https://codecov.io/gh/lidiasm/ProyectoCC/branch/master/graphs/badge.svg)](https://codecov.io/gh/lidiasm/ProyectoCC)
[![Heroku](https://www.herokucdn.com/deploy/button.svg)](https://obtenermascotas.herokuapp.com/)

### Máster en Ingeniería Informática en la Universidad de Granada.

[Directorio que contiene toda la documentación del proyecto.](https://github.com/lidiasm/ProyectoCC/tree/master/docs)

#### Descripción del proyecto

El proyecto de esta asignatura consiste en desarrollar un sistema informático que facilite la adopción de las diferentes especies de animales domésticas. Con este fin nuestro sistema será capaz de realizar recomendaciones personalizadas en función de las preferencias y necesidades especificadas. De este modo podrá sugerir posibles mascotas que puedan adaptarse al ritmo de vida de cada usuario en particular. Asimismo este software será capaz de analizar y generar un conjunto de datos estadísticos cuya utilidad consiste en poder resolver las cuestiones principales que se plantean en el tema de las adopciones. 
Los datos que se utilizarán en este proyecto se obtienen de la **API Petfinder**. Sus numerosas ventajas, tales como que cuenta con un almacenamiento masivo de datos además de que ha sido partícipe en [diferentes competiciones relacionadas con el ámbito de la Inteligencia Artificial](https://www.linkedin.com/pulse/kaggle-competition-multi-class-classification-image-alexandra), la convierten en una buena opción para usarla en este proyecto.
[Más información acerca de las entidades y sus respectivas funcionalidades.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/entidades.md)

#### Arquitectura.

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura basada en microservicios**. [Más información acerca de la arquitectura y de los microservicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/ampliacion_microservicios.md)

#### Lenguajes de programación y frameworks.

Los microservicios se implementarán en **Python** y se comunicarán mediante *API REST* utilizando, para ello, el *framework* [**Flask**](https://www.flaskapi.org/). Asimismo se hará uso de la API Gateway [***Kong API Gateway***](https://konghq.com/solutions/gateway/) y como almacén de datos se utilizará **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**. 

[Más información acerca de las herramientas.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/lenguajes_y_herramientas.md)

#### Servicios LOG y de configuración distribuida.

Se integrarán un servicio de *logging* mediante la librería [***logging***](https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/logging-de-python/) de Python y el servicio de configuración distribuida [***etcd***](https://etcd.io/). [Más información acerca de estos servicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/servicios.md)

#### Herramienta de construcción e integración continua.

    buildtool: Makefile

1. `make` para construir el entorno virtual e instalar las dependencias necesarias.
2. `make test` para ejecutar los tests.

Como herramientas de integración continua se utilizarán [***Travis***](https://docs.travis-ci.com/) y [***CircleCI***](https://circleci.com/).

[Más información acerca de las herramientas de construcción e integración.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/herramientas_construccion_e_integracion.md)

#### Microservicios de la clase *Mascotas*.

Esta clase incopora la lógica de la aplicación asociada a recopilar datos de mascotas para su posterior visualización. Para ello serán necesarios dos microservicios. El primer de ellos se encargará de realizar la conexión con la API Petfinder y, a continuación, ejecutará la tarea correspondiente a la descarga de datos de mascotas de forma periódica. Por lo tanto, será necesario incluirla en un servidor de tareas como es *Celery* para que se lance automáticamente, en mi caso, cada 24 horas. De ese modo todos los días se descargarán datos de la aplicación para disponer de información actualizada asociada a las mascotas.

Por otro lado se desarrolla un microservicio *REST* que sea capaz de recoger los datos de mascotas, que han sido descargados por el anterior microservicio, con el objetivo de poder visualizarlos en su conjunto o mostrar solo la información asociada a una mascota en particular proporcionando, para ello, su respectivo identificador. 

Ambas funcionalidades se corresponden con [uno de los pasos necesarios](https://github.com/lidiasm/ProyectoCC/issues/23#issue-512987660) para cumplir las dos historias de usuario que han sido definidas anteriormente. Para su implementación se ha aplicado una *arquitectura basada en capas* puesto que la lógica de negocio reside en la clase *Mascotas*, de la cual harán uso ambos microservicios para acceder a las métodos correspondientes que les permitan llevar a cabo sus respectivos servicios. En el caso del microservicio *REST*, solo se han implementado servicios *GET* puesto que sus funciones consisten en obtener los datos de las mascotas y visualizarlos. Esta arquitectura queda representada en la siguiente captura.

![Esquema de la arquitectura por capas del primer microservicio.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Primer%20microservicio.png)

Del mismo modo que se han desarrollado *tests* para comprobar el correcto funcionamiento de los métodos de la clase *Mascotas* también se han desarrollado [tests para el microservicio *REST*](https://github.com/lidiasm/ProyectoCC/blob/master/tests/test_mascotas_rest.py) así como [tests para el microservicio en *Celery*](https://github.com/lidiasm/ProyectoCC/blob/master/tests/test_mascotas_celery.py), con el objetivo de verificar que el comportamiento de ambos es el adecuado.

#### Servidor Web

Tal y como se advierte en diversas páginas de desarrollo, como [esta](https://www.toptal.com/flask/flask-production-recipes), se recomienda utilizar un servidor web adicional para controlar los diferentes aspectos que intervienen en la futura fase de producción. Asimismo, teniendo en cuenta que el proyecto se desarrolla en Python utilizaré un [*WSGI*](https://www.fullstackpython.com/wsgi-servers.html) que proprociona tanto un gestor de procesos como una interfaz web para acceder a las funciones de las clases. Tras investigar las diversas alternativas existentes se puede decir que los más utilizados son [***uWSGI***](https://uwsgi-docs.readthedocs.io/en/latest/), [***Waitress***](https://waitress.readthedocs.io/en/stable/) y [***Gunicorn (Green Unicorn)***](https://gunicorn.org/#docs). En esta [comparativa](https://docs.python-guide.org/scenarios/web/) *uWSGI* destaca por su versatilidad pero también por su complejidad para utilizarlo mientras que *Gunicorn* tiene como ventaja su facilidad de uso y es popularmente utilizada junto con *Flask*. Por lo tanto en mi proyecto haré uso de ***Gunicorn*** como WSGI.

Para **ejecutar el microservicio** usando *Gunicorn* y desde la herramienta de construcción basta con ejecutar: `make start`.

Para **detener el microservicio** utilizando los mismos mecanismos deberemos de ejecutar la orden: `make stop`.

Para más información acerca de estos dos procesos automatizados puede acceder al [*makefile*](https://github.com/lidiasm/ProyectoCC/blob/master/Makefile) donde se encuentran todos los pasos documentados.

#### Contenedor del primer microservicio.

Contenedor: https://hub.docker.com/r/lidiasm/mascotas

En primer lugar se debe decidir la imagen base sobre la que se va a construir el contenedor. Considerando que mi aplicación se desarrolla en *Python* y que se especifican las dependencias necesarias para su ejecución, según la [documentación de Python](https://pythonspeed.com/articles/base-image-python-docker-images/) lo más adecuado es utilizar alguna de las versiones especiales para este lenguaje, entre las cuales existen algunas bastante ligeras que contienen solo los paquetes imprescindibles. Con el objetivo de escoger el mejor sistema operativo para el contenedor de mi aplicación procedo a realizar un estudio de las diferentes versiones de *Python* así como de *Alpine* puesto que destaca por su ligereza. Para ello he utilizado [*ab*](https://httpd.apache.org/docs/2.4/programs/ab.html), con el que podré realizar diversas peticiones paralelas al servidor con las que comprobar el rendimiento particular de cada base. Este estudio se puede encontrar [aquí](https://github.com/lidiasm/ProyectoCC/blob/master/docs/estudio_dockers.md).

Tal y como se ha podido observar en el estudio anterior, el sistema operativo base con una mejor relación tamaño-velocidad es **slim-stretch**, y por lo tanto será este el que utilice para construir el contenedor de este primer microservicio. Para esta tarea se ha redactado el fichero [Dockerfile](https://github.com/lidiasm/ProyectoCC/blob/master/Dockerfile) en el cual se detallan las instrucciones que se han llevado a cabo y su respectiva justificación. 

#### Despliegue y construcción automática en *Docker Hub*.

Para realizar el despliegue en *Docker Hub* basta con crearse una cuenta en esta plataforma y un repositorio para subir el contenedor de este primer microservicio. Con el objetivo de construir automáticamente el contenedor a partir de la versión actualizada del fichero *dockerfile* que se encuentra en mi repositorio del proyecto he vinculado este último a *Docker Hub*. Para ello he seguido los pasos recopilados en la [documentación](https://docs.docker.com/docker-hub/builds/link-source/) de la plataforma en cuestión, los cuales consisten en vincular el repositorio de *GitHub* con *Docker Hub* y permitirle el acceso al mismo. A continuación se realiza la [configuración](https://docs.docker.com/docker-hub/builds/) necesaria para automatizar la construcción del contenedor. Para ello accedo a la pestaña *Build* desde el repositorio de *Docker Hub* con el fin de indicar dónde se encuentra el fichero *dockerfile* con el que se construirá el contenedor y activar la opción *Autobuild*, entre otros parámetros. Una vez se han configurado las reglas de construcción cada vez que realice un *push* al repositorio de *GitHub* del proyecto se construirá automáticamente el contenedor de este primer microservicio.

Para ejecutar el contenedor basta con descargarlo desde *Docker Hub* con el comando `docker pull lidiasm/mascotas:obtener_mascotas
` y ejecutar el comando `docker run -e PUERTO=<puerto host> -e API_KEY="tu api key de Petfinder" -e API_SECRET="tu api secret de Petfinder" -p <puerto host>:<puerto Gunicorn> -d lidiasm/mascotas:obtener_mascotas`, en el cual con la opción *-e* le proporcionamos las dos variables de entorno necesarias para conectar con la API Petfinder así como el puerto al que deberá conectarse *Gunicorn* siguiendo esta [documentación](https://vsupalov.com/docker-arg-vs-env/). La opción *-p* nos permite especificar los puertos por los que se van a enviar las peticiones y recibir los resultados, y por último, con la opción *-d* indicamos que el *docker* se ejecute en segundo plano para que no bloquee la consola.

A continuación se puede comprobar en este [enlace](https://github.com/lidiasm/ProyectoCC/blob/master/docs/pruebas_rest.md) el funcionamiento de los diferentes servicios REST que se han definido para este primer microservicio.

#### Despliegue en Heroku.

Contenedor desplegado en Heroku: https://obtenermascotas.herokuapp.com/

Para desplegar el microservicio en *Heroku* en primer lugar debemos darnos de alta en esta plataforma. A continuación definimos el fichero [heroku.yml](https://github.com/lidiasm/ProyectoCC/blob/master/heroku.yml), que se encuentra en el directorio raíz del repositorio asociado al proyecto, en el que se indica que el contenedor se construirá mediante el fichero *dockerfile*. Con el objetivo de realizar un despliegue del contenedor actualizado conectamos mi repositorio del proyecto de *GitHub* con *Heroku* para habilitar la **construcción y despliegue automático** siguiendo los pasos de la [documentación](https://devcenter.heroku.com/articles/github-integration#automatic-deploys) de esta última plataforma. Por último configuramos las tres variables de entorno necesarias para ejecutar mi aplicación: la API key, API secret y el puerto al que se conectará *Gunicorn*. En este último caso hay que tener en cuenta que *Heroku* transmite esta variable mediante el nombre `PORT`, por lo que la variable de entorno que se defina deberá nombrarse de esa forma.

Si accedemos al contenedor desplegado podremos realizar todas las acciones que han sido descritas en la sección anterior.