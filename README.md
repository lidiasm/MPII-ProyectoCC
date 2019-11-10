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
[Más información acerca de las entidades y sus respectivas funcionalidades.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/entidades.md).

#### Arquitectura.

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura basada en microservicios**. [Más información acerca de la arquitectura y de los microservicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/ampliacion_microservicios.md)

#### Lenguajes de programación y frameworks.

Los microservicios se implementarán en **Python**, se utilizará [***Celery***](http://www.celeryproject.org/) para ejecutar periódicamente los microservicios que recopilan datos de mascotas y el que genera las estadísticas a partir de ellos, se comunicarán con el *broker* de mensajería [***RabbitMQ***](https://www.rabbitmq.com/). También se hará uso de la API Gateway [***Kong API Gateway***](https://konghq.com/solutions/gateway/) y como almacén de datos se utilizará **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**. [Más información acerca de las herramientas.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/lenguajes_y_herramientas.md)

#### Servicios LOG y de configuración distribuida.

Se integrarán un servicio de *loggin* mediante la librería [***logging***](https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/logging-de-python/) de Python y el servicio de configuración distribuida [***etcd***](https://etcd.io/). [Más información acerca de estos servicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/servicios.md)

#### Herramienta de construcción.

    buildtool: Makefile

La herramienta de construcción elegida es ***make*** puesto que presenta diversas [ventajas](http://www.chuidiang.org/clinux/herramientas/makefile.php), como la posibilidad de reunir en un solo fichero de construcción los comandos necesarios para instalar las dependencias del sistema así como generar los tests y sus respectivos informes. En mi caso particular el fichero *Makefile* incluirá las órdenes necesarias para instalar un entorno virtual con [*pipenv*](https://pipenv-fork.readthedocs.io/en/latest/), con el objetivo de no utilizar la versión de *Python* del sistema operativo, así como la instalación de las dependencias especificadas en el fichero [*requirements.txt*](https://github.com/lidiasm/ProyectoCC/blob/master/requirements.txt). La primera de ellas consiste en instalar una librería de *Python* denominada [*petpy*](https://pypi.org/project/petpy/) que está orientada a facilitar el uso de la API Petfinder con el fin de obtener unos datos concretos de las mascotas. Del mismo modo se instala [*pytest*](https://docs.pytest.org/en/latest/) puesto que es la librería que he utilizado para ejecutar los tests, así como *codecov* y su librería para *Python* [*pytest-cov*](https://pypi.org/project/pytest-cov/) con el objetivo de incluir tests de cobertura y generar sus respectivos informes.

Para usar este fichero de construcción basta con realizar dos sencillos pasos:

1. `make` para construir el entorno virtual e instalar las dependencias necesarias.
2. `make test` para ejecutar los tests.

#### Herramientas de integración continua.

La primera herramienta de integración continua que he configurado para mi proyecto es [***Travis***](https://docs.travis-ci.com/), ya que destaca por su sencillo uso y su fácil conexión con *GitHub*. Asimismo es capaz de comprobar la compatibilidad del sistema que se está desarrollando en las versiones que se le especifique. En mi caso particular, he compuesto el rango de versiones válidas para mi proyecto mediante [*tox*](https://pypi.org/project/tox/), cuyo funcionamiento reside en crear un entorno virtual por cada versión de *Python* concretada para comprobar la compatibilidad de mi sistema con cada una de las versiones de este lenguaje. Para este proyecto la **versión mínima de Python es la 3.4 y la máxima es la 3.8**, incluyendo la versión de desarrollo.

Como segunda herramienta de integración continua he elegido [***CircleCI***](https://circleci.com/) por diversas razones, entre ellas destaca la facilidad para conectarla con *GitHub* así como para redactar el fichero de configuración *yml*, la rapidez con la que ejecuta los tests y proporciona los resultados, además del soporte para el lenguaje *Python* con el que estoy desarrollando el proyecto.  