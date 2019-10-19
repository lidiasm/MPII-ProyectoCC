## Proyecto de Cloud Computing 2019-2020.

### Máster en Ingeniería Informática en la Universidad de Granada.

#### Arquitectura.

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura basada en microservicios**. La principal razón de ello se fundamenta en las diversas ventajas que presenta este tipo de arquitectura. La más destacada se basa en la posibilidad de desarrollar los diversos microservicios de forma independiente así como su mantenimiento, depuración y actualización gracias a que cada uno de ellos ofrece la posibilidad de ejecutarse de forma individual. Es por esto mismo por lo que en el caso de que algún microservicio no estuviese disponible debido a un fallo el resto de microservicios podrían seguir en ejecución sin verse afectados. Además también cabe destacar la posibilidad de desarrollar nuevos microservicios adicionales con el fin de, posteriormente, integrarlos con el resto de microservicios y así ampliar las funcionalidades del sistema.

#### Microservicios.

1.  Un primer microservicio destinado a la recopilación y procesamiento de los datos recopilados de la API Petfinder. Esta API trabaja principalmente con ficheros *JSON* por lo que será en este formato en el que se encuentren los datos recopilados. De entre todos ellos solo obtendremos aquellos que sean necesarios para generar las estadísticas y realizar las búsquedas personalizadas.

2. Otro microservicio encargado de almacenar la información en una base de datos no estructurada. Debido a que los microservicios se van a desarrollar en Python así como que el almacén de datos a utilizar será MongoDB por las razones que se detallan en el documento principal *(README)*, se ha optado por utilizar una librería en Python denominada ***[Pymongo](https://api.mongodb.com/python/current/)***. En ella se encuentran todas las clases necesarias para conectarse a una base de datos MongoDB.

3. Un microservicio que realice un análisis de los datos almacenados para calcular estadísticas que sean útiles para comprender los diversos factores que influyen en un proceso de adopción.

4. Un microservicio encargado de realizar el registro de nuevos usuarios o el inicio de sesión de aquellos ya existentes en el sistema.

5. Un microservicio capaz de realizar búsquedas en la base de datos en función de un conjunto de criterios especificados. De este modo se generarán las recomendaciones personalizadas con el objetivo de proponer animales afines a la personalidad de los usuarios.

6. Por último se desarrollará un microservicio LOG con el que se comunicarán todos los microservicios anteriores con el fin de poder monitorizar el sistema y analizar las diversas acciones que realizan cada uno así como detectar los posibles fallos que surjan.

A continuación se adjunta un esquema representativo sobre cómo se comunicarán los distintos microservicios detallados anteriormente. 

![Esquema de comunicación entre microservicios.](https://github.com/lidiasm/ProyectoCC/blob/master/documentacion/imagenes/Comunicaci%C3%B3n%20microservicios.png)

Tal y como se puede observar en la imagen se implementará una **[API REST](https://searchapparchitecture.techtarget.com/definition/RESTful-API)** con el fin de gestionar las transmisiones de datos. De este modo dará soporte a los microservicios destinados al registro de usuarios o inicio de sesión, a la búsqueda personalizada y a la generación de los datos estadísticos. La principal razón del desarrollo de una API REST se fundamenta en que se encuentra entre una de las tecnologías más utilizadas para la gestión de peticiones a un servidor cuando se diseña un servicio web. Asimismo está caracterizada por su sencillez en relación al uso del protocolo *HTTP* puesto que con los cuatro verbos disponibles se pueden realizar diversas operaciones de gran relevancia. En este proyecto, por ejemplo, se utilizará el verbo *GET* para obtener los resultados estadísticos o el método *PUT* para añadir los datos de un nuevo usuario.