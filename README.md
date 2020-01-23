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
* [Incorporación del almacén de datos.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/incorporacion_bd.md)
* [Estudio de prestaciones para el microservicio de las mascotas.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/estudio_prestaciones.md)

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

#### Direcciones de los contenedores desplegados para los microservicios.

En la dirección correspondiente a **Docker Hub** se encuentran desplegados los contenedores de los dos microservicios.

Contenedor: https://hub.docker.com/r/lidiasm/mascotas

Contenedor desplegado en Heroku: https://obtenermascotas.herokuapp.com/

#### Avance del proyecto: microservicios de estadísticas.

En este último avance del proyecto se ha implementado la clase asociada a la lógica de negocio de la segunda entidad denominada **Estadísticas**. En ella se encuentran tres métodos cuyas funciones consisten en calcular hasta tres tipos de informes estadísticos en función de los datos de mascotas recopilados hasta el momento. Cabe destacar que la generación de estadísticas se encuentra **desacoplada de la función encargada de descargar datos de mascotas de la API Petfinder**. De este modo proporcionamos una total independencia entre ambas funcionalidades, lo cual es bastante recomendable en relación a mantener unas prestaciones medianamente aceptables. Asimismo, se ha creado una **colección de Estadísticas en la base de datos** para poder almacenarlas una vez se hayan generado. De nuevo, al igual que en el primer microservicio, se ha hecho uso de la **inyección de dependencias** de forma que solo la clase *Estadísticas* podrá realizar operaciones con la base de datos, que en este caso, tratan de insertar los informes estadísticos en su correspondiente colección de documentos.
De igual forma, se han desarrollado los tests correspondientes a esta clase comprobando el correcto funcionamiento de todos los métodos implementados.

Para la generación de informes se ha desarrollado un **microservicio en Celery** compuesto de **una tarea periódica** con el objetivo de generar las estadísticas de las mascotas registradas en la base de datos también de forma independiente. De este modo el microservicio se activará de forma automática cada hora para generar nuevos informes estadísticos que, posteriormente, se almacenarán en su correspondiente coleción.

Por último se ha implementado un **microservicio REST** que permite acceder y visualizar los distintos tipos de informes estadísticos a través de sus respectivas rutas. De nuevo se le ha otorgado total independencia del microservicio anterior por lo que ambos se encuentran **desacoplados**. De este modo este microservicio no tendrá que esperar a que se generen los informes, simplemente cuando le llegue una petición accederá a la base de datos y devolverá el conjunto de estadísticas relacionados con el tópico requerido, si estas existen. Si no, informará acerca de este suceso mediante un mensaje informativo.
El objetivo que se persigue con almacenar diferentes informes de una misma temática es que, en un futuro, se puedan utilizar, por ejemplo, para obtener datos históricos acerca de un determinado tópico. Los tres que se han desarrollado son:

* Informe estadístico acerca de la relación entre los niños y los animales en adopción, ordenados en función de aquellos que son más sociables.
* Informe estadístico acerca de la sociabilidad de las diferentes razas de perro tanto con niños como con otro tipo de animales en adopción.
* Informe estadístico acerca de los tipos de mascotas que se pueden encontrar en adopción así como su número de ejemplares.

Tal y como se puede comprobar a continuación, estos microservicios se han desarrollado siguiendo una **arquitectura por capas**. La capa inferior es la clase **MongoDB** encargada de implementar las operaciones con la base de datos. Mediante un objeto de dicha clase, la clase *Estadísticas* puede almacenar los informes estadísticos una vez han sido generados. Es por ello por lo que el microservicio ubicado en *Celery* hará uso de estos métodos para generar los informes estadísticos de forma periódica y automática para su posterior almacenamiento. Por último el microservicio *REST* hará uso de los tres métodos asociados a la visualización de los tres tipos de informes estadísticos también a través de la clase *Estadísticas*, la cual de nuevo hará uso del objeto de la clase *MongoDB* para devolver las estadísticas asociadas a un determinado tópico, si existen.

![Arquitectura en capas del microservicio de estadísticas.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Microservicio%20Estad%C3%ADsticas.png)

Por último se ha redactado el fichero [*dockerfile*](https://github.com/lidiasm/ProyectoCC/blob/master/Dockerfile_Estadisticas) asociado a esta entidad y se ha desplegado en [**Docker Hub**](https://hub.docker.com/r/lidiasm/mascotas) configurando su construcción de forma automática, como con el contenedor del primer microservicio.

#### Creación de máquinas virtuales en Azure.

Para realizar el despliegue de mi proyecto en máquinas virtuales voy a utilizar la plataforma **Azure** para crearlas puesto que al utilizar una máquina virtual con Ubuntu esta no permite crear máquinas virtuales dentro de ella. El primer paso que se debe realizar es crearse una **cuenta para estudiantes** con la que te proporcionan hasta 100$. A continuación instalo el [**cliente de Azure**](https://docs.microsoft.com/es-es/cli/azure/install-azure-cli-apt?view=azure-cli-latest) para poder crear y configurar las máquinas virtuales desde la línea de comandos.

Una vez instalado este cliente de órdenes e iniciado sesión con nuestra cuenta recién creada, podemos visualizar el listado de sistemas operativos disponibles con los que poder crear la primera máquina virtual. Para ello haremos uso del comando `az vm image list` según la propia [documentación](https://docs.microsoft.com/es-es/cli/azure/azure-cli-vm-tutorial?tutorial-step=3&view=azure-cli-latest) de Azure. Si bien al comienzo me decanté por probar el sistema operativo **Debian**, he encontrado diversos problemas a la hora de provisionarlo con **MongoDB**, el almacén de datos que se utiliza en el proyecto, hasta el punto de no poder instalarlo por muchos tutoriales que he buscado. También he redactado el problema en [*Stackoverflow*](https://stackoverflow.com/questions/59830351/cant-install-mongodb-with-ansible-on-debian-10) pero sin éxito.
Por lo tanto, he decidido probar con la última versión del sistema operativo **UbuntuServer 18.04-LTS** disponible en Azure.

El primer paso consiste en registrar un **grupo de recursos** en los que alojar las máquinas virtuales. Para ello ejecutamos el comando `az group create --name mascotas --location eastus` desde el cliente de Azure, proporcionando como nombre del grupo *mascotas* y como ubicación el este de EEUU tal y como se especifica en la [documentación](https://docs.microsoft.com/es-es/azure/virtual-network/quick-create-cli?toc=%2Fazure%2Fvirtual-machines%2Flinux%2Ftoc.json).

![Crear grupo de recursos.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Grupo%20de%20recursos.png)

A continuación podemos proceder a crear la máquina virtual, con el sistema operativo elegido anteriormente, ejecutando el siguiente comando en el cliente de Azure tal y como se especifica en la [documentación](https://docs.microsoft.com/es-es/cli/azure/azure-cli-vm-tutorial?tutorial-step=4&view=azure-cli-latest):

`az vm create --resource-group mascotas --name ubuntu --image UbuntuLTS --generate-ssh-keys --output json --public-ip-address-dns-name ubuntulidia --public-ip-address-allocation static --verbose`

En primer lugar asignamos la máquina que vamos a crear al grupo de recursos registrado como *mascotas*. Con la opción `--name` especificamos el nombre que va a tener nuestra máquina, que en mi caso será *ubuntu*. A continuación especificamos el sistema operativo que se le va a instalar y genera las claves *SSH* para poder conectarnos a la máquina a través de este protocolo. Para poder realizarlo mediate la dirección IP especificamos que la IP pública sea estática con la opción `--public-ip-address-allocation static` para que aunque se apague la máquina, la dirección que se asigne al comienzo no varíe. No obstante, tal y como se expresa en los apuntes, también es recomendable configurar una dirección DNS mediante la opción `--public-ip-address-dns-name`. De este modo podremos acceder a la máquina mediante una segunda dirección compuesta por el nombre DNS especificado, la localización de los recursos y el prefijo de la plataforma de Azure. En mi caso sería: `ubuntulidia.eastus.cloudapp.azure.com`.

![Creación máquina virtual ubuntu.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/VM%20Ubuntu%20Azure.png)