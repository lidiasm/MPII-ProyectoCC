## Proyecto de Cloud Computing 2019-2020.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/lidiasm/ProyectoCC.svg?branch=master)](https://travis-ci.org/lidiasm/ProyectoCC)
[![CircleCI](https://circleci.com/gh/lidiasm/ProyectoCC/tree/master.svg?style=svg)](https://circleci.com/gh/lidiasm/ProyectoCC/tree/master)
[![Codecov](https://codecov.io/gh/lidiasm/ProyectoCC/branch/master/graphs/badge.svg)](https://codecov.io/gh/lidiasm/ProyectoCC)
[![Heroku](https://www.herokucdn.com/deploy/button.svg)](https://obtenermascotas.herokuapp.com/)

### Máster en Ingeniería Informática en la Universidad de Granada.

[Directorio que contiene toda la documentación del proyecto.](https://github.com/lidiasm/ProyectoCC/tree/master/docs)

### Índice

* [Entidades del proyecto.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/entidades.md)
* [Arquitectura basada en microservicios.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/ampliacion_microservicios.md)
* [Lenguajes de programación y *frameworks* para su desarrollo.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/lenguajes_y_herramientas.md)
* [Servicios adicionales.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/servicios.md)
* [Herramientas de construcción e integración continua.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/herramientas_construccion_e_integracion.md)
* [Arquitectura en capas de los microservicios e incorporación de *Gunicorn*.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/arquitecturas_microservicios.md)
* [Contenedores y despliegue automático.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/contenedores_y_despliegue.md)

#### Descripción del proyecto

El proyecto de esta asignatura consiste en desarrollar un sistema informático que facilite la adopción de las diferentes especies de animales domésticas. Con este fin nuestro sistema será capaz de realizar recomendaciones personalizadas en función de las preferencias y necesidades especificadas. De este modo podrá sugerir posibles mascotas que puedan adaptarse al ritmo de vida de cada usuario en particular. Asimismo este software será capaz de analizar y generar un conjunto de datos estadísticos cuya utilidad consiste en poder resolver las cuestiones principales que se plantean en el tema de las adopciones.
Los datos que se utilizarán en este proyecto se obtienen de la **API Petfinder**. Sus numerosas ventajas, tales como que cuenta con un almacenamiento masivo de datos además de que ha sido partícipe en [diferentes competiciones relacionadas con el ámbito de la Inteligencia Artificial](https://www.linkedin.com/pulse/kaggle-competition-multi-class-classification-image-alexandra), la convierten en una buena opción para usarla en este proyecto.
[Más información acerca de las entidades y sus respectivas funcionalidades.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/entidades.md)

#### Herramienta de construcción.

    buildtool: Makefile

1. `make` para construir el entorno virtual e instalar las dependencias necesarias.
2. `make test` para ejecutar los tests.
3. `make start` para iniciar el microservicio en *Celery* y en *Gunicorn*.
4. `make stop` para finalizar la ejecución de los dos anteriores microservicios.

#### Dirección de los contenedores desplegados para el primer microservicio.

Contenedor: https://hub.docker.com/r/lidiasm/mascotas

Contenedor desplegado en Heroku: https://obtenermascotas.herokuapp.com/

#### Incorporación del almacén de datos.

Tal y como se comentó anteriormente, se va a utilizar como almacén de datos **MongoDB** local, en particular haré uso de la biblioteca especial para esta base de datos escrita en *Python* denominada ***pymongo***. Para integrarla en mi proyecto utilizaré el mecanismo de *inyección de dependencias* de modo que se implemente una única clase específica en la que se desarrollen las diferentes operaciones que se pueden realizar en la base de datos, como añadir elementos, obtener uno en particular, entre otros. Posteriormente, se incluirá un atributo en cada una de las clases de la lógica de la aplicación, como es la clase *Mascotas* y de esa forma se le pasará a su constructor un argumento que será un objeto de la clase asociada a la base de datos ya inicializado. De este modo inyectamos en cada clase de la lógica de la aplicación un objeto de la base de datos con el fin de aportar cierta independencia entre el almacén de información y las clases del proyecto.

Para añadir el almacén de datos escogido de forma local, en primer lugar, deberemos instalar la biblioteca mencionada anteriormente y configurar tanto una base de datos como un usuario con el que acceder a ella mediante la *shell de mongo*. Una vez realizado este proceso ya podemos construir la variable de entorno `MONGODB_URI` necesaria para poder conectarnos a la base de datos que acabamos de crear y configurar. Esta variable es **imprescindible** para que el microservicio disponga de un almacén de datos.

Los siguientes cambios que se han producido han consistido en añadir a *mongo* como servicio tanto en **Travis** como en **CircleCI**. En este último, además, se debe añadir una imagen adicional en la que esté instalada *MongoDB*. En mi caso he utilizado aquella que se encuentra disponible en la propia herramienta: `circleci/mongo:latest`. Del mismo modo, en ambos casos, se ha añadido como **variable de entorno encriptada la URI a la base de datos local** para poder realizar los tests de la clase en la que se encuentran las operaciones de esta.

En relación a las herramientas de despliegue simplemente se ha añadido la clase de la base de datos para copiarla dentro del contenedor y tras construir el contenedor se deberá pasar una variable de entorno más denominada `MONGODB_URI` donde se encuentre la dirección con la que se llevará a cabo la conexión al almacén de datos. Este aspecto en **Heroku** se lleva a cabo de forma distinta puesto que, en primer lugar, la base de datos debe ser remota. Para ello he utilizado la plataforma [***MongoDB Atlas***]() y he seguido los pasos descritos a continuación:

* Nos damos de alta en la plataforma y a continuación creamos un nuevo *cluster* donde alojar la base de datos.
* Escoger el proveedor del servicio en la nube así como la región en la que se encuentra el servidor. En mi caso he optado por establecer los valores por defecto que definen un plan gratuito.
* Una vez establecida esta configuración podemos crear la base de datos, que en mi caso se denomina *Petfinder* así como un usuario para acceder a ella.
* Por último podremos crear en dicho almacén de datos una colección donde almacenar las mascotas, que en mi caso se llama *mascotas*.

Tras crear y configurar el almacén de datos basta con obtener la *URI* de la base de datos remota y añadirla como variable de entorno a **Heroku** mediante su interfaz dentro de la opción *Settings/Config Vars*. Por último, se han añadido las dependencias necesarias para instalar la librería *pymongo* en el fichero `docker_requirements.txt` de modo que en todas las futuras construcciones del contenedor se instalen las librerías necesarias para ejecutar el microservicio.

#### Medición de prestaciones.

Prestaciones: obtener_mascotas.yml

En esta primera evaluación se pretende conseguir que el primer microservicio sea capaz de servir mínimo 1.000 peticiones por segundo con 10 usuarios concurrentes. Para ello en primer lugar lanzará la tarea periódica en *Celery* para obtener los datos de hasta veinte mascotas con el objetivo de, posteriormente, almacenarlas en la base de datos configurada como caché y recopilarlos para visualizarlos mediante el servicio REST. Tras el [estudio de las prestaciones](https://github.com/lidiasm/ProyectoCC/blob/master/docs/estudio_prestaciones.md) llevado a cabo se han conseguido servir **1.497 peticiones/s**.