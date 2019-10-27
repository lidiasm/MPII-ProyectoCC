## Proyecto de Cloud Computing 2019-2020.

### Máster en Ingeniería Informática en la Universidad de Granada.

**Índice de contenidos.**
- [Descripción del proyecto.](#id1)
- [Arquitectura del sistema.](#id2)
- [Microservicios.](#id3)
- [Lenguajes de programación y frameworks.](#id4)
- [Servicios LOG y de configuración distribuida.](#id5)
- [Directorio que contiene toda la documentación del proyecto.](https://github.com/lidiasm/ProyectoCC/tree/master/documentacion)

#### Descripción del proyecto. <a name="id1"></a>

El proyecto de esta asignatura consiste en desarrollar un sistema informático que facilite la adopción de las diferentes especies de animales domésticas. Con este fin nuestro sistema será capaz de realizar recomendaciones personalizadas en función de las preferencias y necesidades especificadas. De este modo podrá sugerir posibles mascotas que puedan adaptarse al ritmo de vida de cada usuario en particular. Asimismo este software será capaz de analizar y generar un conjunto de datos estadísticos cuya utilidad consiste en poder resolver las cuestiones principales que se plantean en el tema de las adopciones. Algunos ejemplos son:

- Analizar las características de aquellas razas que se encuentran en mayor medida en estos centros de adopción.
- Comprobar cuáles son las especies que tienen un mejor comportamiento con niños así como con otras especies de animales.
- Las ciudades con un mayor número de animales en adopción.
- Las localizaciones donde se encuentran las mayores concentraciones de centros de adopción.

Los datos que se utilizarán en este proyecto se obtienen de la **API Petfinder**. Sus numerosas ventajas, tales como que cuenta con un almacenamiento masivo de datos además de que ha sido partícipe en [diferentes competiciones relacionadas con el ámbito de la Inteligencia Artificial](https://www.linkedin.com/pulse/kaggle-competition-multi-class-classification-image-alexandra), la convierten en una buena opción para usarla en este proyecto.

#### Arquitectura. <a name="id2"></a>

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura basada en microservicios**. La principal razón de ello se fundamenta en las diversas ventajas que presenta este tipo de arquitectura. La más destacada se basa en la posibilidad de desarrollar los diversos microservicios de forma independiente así como su mantenimiento, depuración y actualización gracias a que cada uno de ellos ofrece la posibilidad de ejecutarse de forma individual. Es por esto mismo por lo que en el caso de que algún microservicio no estuviese disponible debido a un fallo el resto de microservicios podrían seguir en ejecución sin verse afectados. Además también cabe destacar la posibilidad de desarrollar nuevos microservicios adicionales con el fin de, posteriormente, integrarlos con el resto de microservicios y así ampliar las funcionalidades del sistema.

#### Microservicios. <a name="id3"></a>

1.  Un primer microservicio destinado a la recopilación y procesamiento de los datos recopilados de la API Petfinder. Esta API trabaja principalmente con ficheros *JSON* por lo que será en este formato en el que se encuentren los datos recopilados. De entre todos ellos solo obtendremos aquellos que sean necesarios para generar las estadísticas y realizar las búsquedas personalizadas.

2. Un segundo microservicio que realice un análisis de los datos recopilados y genere estadísticas que sean útiles para comprender los diversos factores que influyen en un proceso de adopción.

3. Un tercer microservicio capaz de almacenar los informes estadísticos generados en su base de datos.

4. Un microservicio capaz de realizar búsquedas en la base de datos en función de un conjunto de criterios especificados. De este modo se generarán las recomendaciones personalizadas con el objetivo de proponer animales afines a la personalidad de los usuarios. 

![Esquema representativo de la arquitectura.](https://github.com/lidiasm/ProyectoCC/blob/master/documentacion/imagenes/Comunicaci%C3%B3n%20microservicios.png)

[Más información acerca de los microservicios.](https://github.com/lidiasm/ProyectoCC/blob/master/documentacion/ampliacion_microservicios.md)

#### Lenguajes de programación y frameworks. <a name="id4"></a>

Los microservicios se implementarán en **Python** debido a sus múltiples [ventajas](https://www.invensis.net/blog/it/benefits-of-python-over-other-programming-languages/). Algunas de ellas son las siguientes:
* Su velocidad en ejecución le posiciona como uno de los lenguajes más recomendados para desarrollar aplicaciones de red complejas o que necesiten realizar cálculos computacionales costosos.
* Este lenguaje se desarrolla bajo una licencia de código abierto verificada por la OSI y está respaldado por una comunidad que cada vez es más amplia.
* Cuenta con *Python Package Index (PyPI)* que dispone de diversos módulos con el objetivo de hacer que Python sea compatible con la mayoría de lenguajes así como con diversas plataformas.
* Y, por último, una de sus ventajas por la que es más conocido hace referencia al amplio conjunto de librerías disponibles relacionadas con diversos ámbitos como la minería de datos.

Existe una librería en particular denominada [***Pandas***](https://pandas.pydata.org/) que resulta súmamente útil en este proyecto. La razón de ello es que cuenta con un conjunto de métodos capaces de convertir los datos recopilados de la API Petfinder, que se encuentran en formato *JSON*, a un diccionario sencillo de manipular para analizar los datos.
Del mismo modo necesitaremos integrar la biblioteca [***Celery***](http://www.celeryproject.org/) con el fin de ejecutar periódicamente los microservicios encargados de recopilar los datos y de generar las estadísticas. De este modo se podrá disponer de información actualizada para generar nuevos informes estadísticos con los que completar el estudio de los factores influyentes en un proceso de adopción. Para la comunicación de los microservicios que se encuentren en este servidor de tareas se utilizará el *broker* de mensajería [***RabbitMQ***](https://www.rabbitmq.com/) que además de ser de código abierto implementa el protocolo *AMQP*, el cual garantiza la recepción de los mensajes enviados. A través de este *broker* se comunicará el microservicio que genera las estadísticas con el que recopila los datos para poder obtener la información de las mascotas con la que generar los informes estadísticos. Asimismo también será necesario establecer una comunicación entre el microservicio que obtiene los datos de la API Petfinder y el que realiza la búsqueda de mascotas. Por último se ha introducido un nuevo microservicio *Estadísticas* cuyo papel es el de ser el intermediario que recoge los informes estadísticos generados mediante *RabbitMQ*, los almacena en su base de datos y los recupera para que la API Gateway se los muestre al usuario.

Con el objetivo de integrar una API Gateway en mi sistema y tras analizar las diversas alternativas que existen tales como AWS API Gateway, WSO2, Apigee API Management, entre otras he decidido escoger la [***Kong API Gateway***](https://konghq.com/solutions/gateway/). Es una API *open source* caracterizada, principalmente, por su variedad de [complementos](https://luarocks.org/search?q=kong) que pueden añadirse en tiempo de ejecución y configurarse mediante la API RESTful de administración. Asimismo cuenta con otras numerosas [ventajas](https://www.itdo.com/blog/kong-como-alternativa-open-source-de-api-gateway/) como que es multiplataforma, puede ejecutarse tanto en la nube como en entornos locales y es capaz de adaptarse a varios tipos de arquitecturas incluyendo la arquitectura basada en microservicios.

Para el desarrollo de las API REST que intercomuniquen los microservicios entre sí o con la API Gateway se han considerado diversos *frameworks* tales como Flask o Django. Si bien este último dispone de muchas más funcionalidades debido a que está orientado al desarrollo de sistemas más complejos, también está caracterizado por su complejidad en relación a su aprendizaje desde cero. Es por ello por lo que finalmente he optado por usar **Flask**, el cual, además, es ampliamente utilizado por diversas [empresas](https://github.com/rochacbruno/flask-powered). Asimismo dentro de todas las posibilidades que ofrece este *framework* he optado por hacer uso de una extensión en particular denominada [***Flask-RESTful***](https://flask-restful.readthedocs.io/en/latest/) debido a su sencillez en relación a aprender a desarrollar una API REST desde cero.

En referencia al almacenamiento de datos he optado por utilizar una base de datos NoSQL debido a que las bases de datos SQL no cuentan con una gestión eficiente a la hora de trabajar con grandes cantidades de datos. Además otra de las ventajas asociadas a las bases de datos no estructuradas como MongoDB es que se pueden almacenar datos sin especificar la estructura ni las relaciones que existen entre ellos. Esta ventaja aporta una gran flexibilidad a la hora de desarrollar una aplicación que a priori se conoce que va a hacer uso de una cantidad masiva de datos pero cuyas conexiones entre sí pueden variar a lo largo del tiempo. Por lo tanto el sistema de almacenamiento que mi proyecto usará es **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**. Entre las múltiples [ventajas](https://www.oodlestechnologies.com/blogs/Advantages-and-Disadvantages-of-MongoDB/) de este almacén de datos la razón de haberlo elegido reside, principalmente, en su orientación a guardar documentos. Este aspecto es útil en mi proyecto puesto que una de las funcionalidades de mi sistema consiste en generar estadísticas para cada uno de los aspectos relevantes que influyen en una adopción. Asimismo, teniendo en cuenta que la implementación de los microservicios es en Python, este lenguaje cuenta con una librería denominada [***pymongo***](https://api.mongodb.com/python/current/) que facilita el acceso a un cliente de MongoDB para comenzar a trabajar con las bases de datos. 

#### Servicios LOG y de configuración distribuida. <a name="id4"></a>

Con el primero de ellos conseguiremos registrar toda la actividad de nuestro sistema de modo que nos permita monitorizar el funcionamiento de los distintos microservicios y detectar los posibles fallos que ocurran. Como el lenguaje en el que se van a desarrollar los microservicios es Python haré uso de otra de sus librerías denominada [***logging***](https://www.ionos.es/digitalguide/paginas-web/desarrollo-web/logging-de-python/). Esta biblioteca está pensada tanto para depuración como para registro de *logs*. En este último ámbito destaca la capacidad que ofrece para controlar el formato y el contenido de los registros, el tipo de información que se incluirá en dichos *logs*, desde dónde se han emitido y el destino en el que se almacenarán. Asimismo permite configurar diferentes niveles con el objetivo de reconocer rápidamente si un *log* requiere atención inmediata debido a un error del sistema o se corresponde con un registro informativo del inicio de un servicio. En el caso particular de mi proyecto se pretenden almacenar registros relativos a los accesos y peticiones de las bases de datos. Asimismo también se registrarán el inicio del sistema y las diferentes peticiones que lleguen a través de la API Gateway para generar las estadísticas además de la realización de las búsquedas basadas en preferencias.

En relación al servicio de configuración distribuida, tras analizar diversas [alternativas](https://technologyconversations.com/2015/09/08/service-discovery-zookeeper-vs-etcd-vs-consul/) como etcd, Zookeeper, Registrator, confd, he optado por [***Consul***](https://www.consul.io/). Se trata de un almacén de datos clave-valor capaz de registrar tanto datos como notificaciones personalizadas de las acciones de un sistema. La principal ventaja de Consul es que no es necesario utilizar el descubrimiento de servicios de terceras partes ni programarlo puesto que ya viene integrado. Asimismo es muy sencillo de utilizar puesto que basta con registrar los microservicios que deseemos desplegar y realizar el descubrimiento mediante HTTP. 
De nuevo, considerando el desarrollo de los microservicios en Python, voy a hacer uso de la librería de Python [***python-consul***](https://pypi.org/project/python-consul/) para integrar este servicio en mi proyecto.