## Proyecto de Cloud Computing 2019-2020.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/lidiasm/ProyectoCC.svg?branch=master)](https://travis-ci.org/lidiasm/ProyectoCC)
[![CircleCI](https://circleci.com/gh/lidiasm/ProyectoCC/tree/master.svg?style=svg)](https://circleci.com/gh/lidiasm/ProyectoCC/tree/master)
[![Coverage](https://codecov.io/gh/lidiasm/ProyectoCC/branch/master/graphs/badge.svg)](https://codecov.io/gh/lidiasm/ProyectoCC)

### Máster en Ingeniería Informática en la Universidad de Granada.

[Directorio que contiene toda la documentación del proyecto.](https://github.com/lidiasm/ProyectoCC/tree/master/docs)

#### Descripción del proyecto

El proyecto de esta asignatura consiste en desarrollar un sistema informático que facilite la adopción de las diferentes especies de animales domésticas. Con este fin nuestro sistema será capaz de realizar recomendaciones personalizadas en función de las preferencias y necesidades especificadas. De este modo podrá sugerir posibles mascotas que puedan adaptarse al ritmo de vida de cada usuario en particular. Asimismo este software será capaz de analizar y generar un conjunto de datos estadísticos cuya utilidad consiste en poder resolver las cuestiones principales que se plantean en el tema de las adopciones. 
Los datos que se utilizarán en este proyecto se obtienen de la **API Petfinder**. Sus numerosas ventajas, tales como que cuenta con un almacenamiento masivo de datos además de que ha sido partícipe en [diferentes competiciones relacionadas con el ámbito de la Inteligencia Artificial](https://www.linkedin.com/pulse/kaggle-competition-multi-class-classification-image-alexandra), la convierten en una buena opción para usarla en este proyecto.
[Más información acerca de las entidades y sus respectivas funcionalidades.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/entidades.md)

#### Arquitectura.

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura basada en microservicios**. [Más información acerca de la arquitectura y de los microservicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/ampliacion_microservicios.md)

#### Lenguajes de programación y frameworks.

Los microservicios se implementarán en **Python**, se utilizará [***Celery***](http://www.celeryproject.org/) para ejecutar periódicamente los microservicios que recopilan datos de mascotas y el que genera las estadísticas a partir de ellos, se comunicarán con el *broker* de mensajería [***RabbitMQ***](https://www.rabbitmq.com/). También se hará uso de la API Gateway [***Kong API Gateway***](https://konghq.com/solutions/gateway/) y como almacén de datos se utilizará **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**. [Más información acerca de las herramientas.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/lenguajes_y_herramientas.md)

#### Servicios LOG y de configuración distribuida.

Se integrarán un servicio de *loggin* mediante la librería [***logging***](https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/logging-de-python/) de Python y el servicio de configuración distribuida [***etcd***](https://etcd.io/). [Más información acerca de estos servicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/servicios.md)

#### Herramienta de construcción e integración continua.

    buildtool: Makefile

1. `make` para construir el entorno virtual e instalar las dependencias necesarias.
2. `make test` para ejecutar los tests.

Como herramientas de integración continua se utilizarán [***Travis***](https://docs.travis-ci.com/) y [***CircleCI***](https://circleci.com/).

[Más información acerca de las herramientas de construcción e integración.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/herramientas_construccion_e_integracion.md)

#### Primer microservicio. Recopilar datos de la API Petfinder

Este microservicio es fundamental para el desarrollo del proyecto, pues es el encargado de conectarse con la API Petfinder, para lo cual debemos de proporcionarle nuestras correspondientes API key y secret, así como descargar datos de mascotas, filtrarlos para solo almacenar los que nos interesan en una estructura de datos y, posteriormente, visualizarlos. Este conjunto de funcionalidades se corresponden con [uno de los pasos necesarios](https://github.com/lidiasm/ProyectoCC/issues/23#issue-512987660) para cumplir las dos historias de usuario que han sido definidas anteriormente. Para su implementación se ha aplicado una *arquitectura basada en capas* puesto que la lógica de negocio reside en la clase *Mascotas* y los servicios *REST* que acceden a las funciones de esta clase se encuentran en una capa distinta. Como todos los servicios REST asociados a la clase *Mascotas* se encargan de realizar peticiones, como conectar con la API Petfinder, o de proporcionar información, como obtener los datos de las mascotas, todos son accesibles mediante el verbo *GET* de *HTTP*. Esto se ejemplifica con la siguiente representación gráfica:

![Esquema de la arquitectura por capas del primer microservicio.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Primer%20microservicio.png)

Del mismo modo que se han desarrollado *tests* para comprobar el correcto funcionamiento de los métodos de la clase *Mascotas* también se han desarrollado *tests* para verificar que el comportamiento de los servicios *REST* es el adecuado. Por ello se han realizado diversas comprobaciones tales como la conexión a la API Petfinder, la descarga de datos de mascotas así como su visualización.

#### Servidor Web

Tal y como se advierte en diversas páginas de desarrollo, como [esta](https://www.toptal.com/flask/flask-production-recipes), se recomienda utilizar un servidor web adicional para controlar los diferentes aspectos que intervienen en la futura fase de producción. Asimismo, teniendo en cuenta que el proyecto se desarrolla en Python utilizaré un [*WSGI*](https://www.fullstackpython.com/wsgi-servers.html) que proprociona tanto un gestor de procesos como una interfaz web para acceder a las funciones de las clases. Tras investigar las diversas alternativas existentes se puede decir que los más utilizados son [***uWSGI***](https://uwsgi-docs.readthedocs.io/en/latest/), [***Waitress***](https://waitress.readthedocs.io/en/stable/) y [***Gunicorn (Green Unicorn)***](https://gunicorn.org/#docs). En esta [comparativa](https://docs.python-guide.org/scenarios/web/) *uWSGI* destaca por su versatilidad pero también por su complejidad para utilizarlo mientras que *Gunicorn* tiene como ventaja su facilidad de uso y es popularmente utilizada junto con *Flask*. Por lo tanto en mi proyecto haré uso de ***Gunicorn*** como WSGI.

Para **ejecutar el microservicio** usando *Gunicorn* y desde la herramienta de construcción basta con ejecutar: `make start`.
Para **detener el microservicio** utilizando los mismos mecanismos deberemos de ejecutar la orden: `make stop`.

Para más información acerca de estos dos procesos automatizados puede acceder al [*makefile*](https://github.com/lidiasm/ProyectoCC/blob/master/Makefile) donde se encuentran todos los pasos documentados.

#### Contenedor y despliegue de la imagen en *Docker Hub.*

[Contenedor *obtener_mascotas* en *Docker Hub*.](https://hub.docker.com/r/lidiasm/obtener_mascotas)

Con el fin de construir el contenedor para albergar el microservicio anterior, en primer lugar se debe definir el sistema operativo que va a utilizar. Si bien existen diferentes sistemas operativos para usar en un contenedor, el más popular es [*Alpine*](https://hub.docker.com/_/alpine) puesto que destaca, principalmente, por su ligereza. Sin embargo investigando acerca de las diversas alternativas encontré una [comparación](https://www.turnkeylinux.org/blog/alpine-vs-debian) en la que se proporcionaban las ventajas e inconvenientes de ambos, destacando que [*Debian*](https://hub.docker.com/_/debian/) dispone de una mejor infraestructura, un mayor número de paquetes y una mejor documentación. En base a esto y a que quería utilizar un sistema operativo diferente al típico *Alpine*, mi contenedor hará uso de **Debian**, en particular la **versión *slim* para *Python* 3.6**, en la cual se presenta una versión más liviana de este sistema operativo.

Para construir el contenedor se ha redactado el fichero [Dockerfile](https://github.com/lidiasm/ProyectoCC/blob/master/Dockerfile) en el cual se detallan las instrucciones que se han llevado a cabo y su respectiva justificación. Para construirlo se debe ejecutar la siguiente instrucción `docker run -e API_KEY="tu api key de Petfinder" -e API_SECRET="tu api secret de Petfinder" -p <puerto host>:<puerto Gunicorn> -d obtener_mascotas`, en la cual la opción *-e* le proporcionamos las dos variables de entorno necesarias para conectar con la API Petfinder, con *-p* especificamos los dos puertos por los que se van a enviar las peticiones y recibir los resultados y por último con la opción *-d* indicamos que el *docker* se ejecute en segundo plano.

En cambio, si desea ejecutar el contenedor sin construirlo basta con descargarlo desde *Docker Hub* a través del enlace incluido al principio de esta sección y ejecutar el comando anterior modificando el nombre por el del contenedor descargado, es decir, *lidiasm/obtener_mascotas*.