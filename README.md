## Proyecto de Cloud Computing 2019-2020.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/lidiasm/ProyectoCC.svg?branch=master)](https://travis-ci.org/lidiasm/ProyectoCC/)
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