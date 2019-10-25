## Proyecto de Cloud Computing 2019-2020.

### Máster en Ingeniería Informática en la Universidad de Granada.

**Índice de contenidos.**
- [Descripción del proyecto.](#id1)
- [Arquitectura del sistema.](#id2)
- [Microservicios.](#id3)
- [Lenguajes de programación y frameworks.](#id4)
- [Directorio que contiene toda la documentación del proyecto.](https://github.com/lidiasm/ProyectoCC/tree/master/documentacion)

#### Descripción del proyecto. <a name="id1"></a>

El proyecto de esta asignatura consiste en desarrollar un sistema informático que facilite la adopción de las diferentes especies de animales domésticas. Con este fin se incluirá un servicio de registro de usuarios para que estos puedan especificar sus necesidades y gustos de modo que el sistema sea capaz de sugerirles las posibles mascotas que puedan adaptarse a su ritmo de vida. Asimismo este software será capaz de analizar y generar un conjunto de datos estadísticos cuya utilidad consiste en poder resolver las cuestiones principales que se plantean en el tema de las adopciones. Algunos ejemplos son:

- Analizar las características de aquellas razas que se encuentran en mayor medida en estos centros de adopción.
- Comprobar cuáles son las especies que tienen un mejor comportamiento con niños así como con otras especies de animales.
- Las ciudades con un mayor número de animales en adopción.
- Las localizaciones donde se encuentran las mayores concentraciones de centros de adopción.

Los datos que se utilizarán en este proyecto se obtienen de la **API Petfinder**. Sus numerosas ventajas, tales como que cuenta con un almacenamiento masivo de datos además de que ha sido partícipe en [diferentes competiciones relacionadas con el ámbito de la Inteligencia Artificial](https://www.linkedin.com/pulse/kaggle-competition-multi-class-classification-image-alexandra), la convierten en una buena opción para usarla en este proyecto.

#### Arquitectura. <a name="id2"></a>

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura basada en microservicios**. La principal razón de ello se fundamenta en las diversas ventajas que presenta este tipo de arquitectura. La más destacada se basa en la posibilidad de desarrollar los diversos microservicios de forma independiente así como su mantenimiento, depuración y actualización gracias a que cada uno de ellos ofrece la posibilidad de ejecutarse de forma individual. Es por esto mismo por lo que en el caso de que algún microservicio no estuviese disponible debido a un fallo el resto de microservicios podrían seguir en ejecución sin verse afectados. Además también cabe destacar la posibilidad de desarrollar nuevos microservicios adicionales con el fin de, posteriormente, integrarlos con el resto de microservicios y así ampliar las funcionalidades del sistema.

#### Microservicios. <a name="id3"></a>

1.  Un primer microservicio destinado a la recopilación y procesamiento de los datos recopilados de la API Petfinder. Esta API trabaja principalmente con ficheros *JSON* por lo que será en este formato en el que se encuentren los datos recopilados. De entre todos ellos solo obtendremos aquellos que sean necesarios para generar las estadísticas y realizar las búsquedas personalizadas.

2. Un segundo microservicio que realice un análisis de los datos almacenados para calcular estadísticas que sean útiles para comprender los diversos factores que influyen en un proceso de adopción.

3. Un microservicio capaz de realizar búsquedas en la base de datos en función de un conjunto de criterios especificados. De este modo se generarán las recomendaciones personalizadas con el objetivo de proponer animales afines a la personalidad de los usuarios. 

Asimismo cada microservicio dispondrá de su propia base de datos ya sea para solo almacenar datos relativos a la caché del microservicio en cuestión como es el caso del que recopila datos de la API Petfinder o el microservicio encargado de realizar las búsquedas de mascotas en base a preferencias. Del mismo modo el microservicio que genera los datos estadísticos también será responsable de una base de datos particular para almacenar las estadísticas que vaya extrayendo de los datos recopilados.

Si bien este proyecto no cuenta con muchos microservicios con el objetivo de que pueda ampliarse en un futuro se hará uso de una [***API Gateway***](https://tyk.io/microservices-api-gateway/) con el fin de establecer una única entrada. Su uso conlleva diferentes ventajas como la posibilidad de añadir y modificar microservicios sin provocar ningún impacto negativo en las aplicaciones cliente que los utilicen, así como ocultar los detalles de implementación de estos. Además al incoporar una API Gateway solo a través de ella se podrán realizar peticiones a los microservicios a los que esté conectada prorpocionando así una única entrada más segura y controlada.
En el caso particular de mi proyecto los microservicios que estarán conectados con ella serán los relacionados con la búsqueda de mascotas y con la generación de datos estadísticos. 
A continuación se presenta el esquema de comunicación de los microservicios detallados anteriormente así como la arquitectura que se ha definido al comienzo.

![Esquema representativo de la arquitectura.](https://github.com/lidiasm/ProyectoCC/blob/master/documentacion/imagenes/Comunicaci%C3%B3n%20microservicios.png)

Como medio de comunicación entre los microservicios así como entre la API Gateway y los dos microservicios que se conectarán a ella se implementarán diversas [***API REST***](https://searchapparchitecture.techtarget.com/definition/RESTful-API), tal y como se puede comprobar en el esquema anterior. La principal razón del desarrollo de una API REST se fundamenta en que se encuentra entre una de las tecnologías más utilizadas para la gestión de peticiones a un servidor cuando se diseña un servicio web. Asimismo está caracterizada por su sencillez en relación al uso del protocolo *HTTP* puesto que con los cuatro verbos disponibles se pueden realizar diversas operaciones de gran relevancia. En este proyecto, por ejemplo, se podría utilizar el verbo *GET* para obtener los resultados estadísticos.

Para finalizar se integrarán dos servicios en este proyecto a los que se conectarán todos los microservicios. Un servicio *LOG* cuyo objetivo será monitorizar el sistema almacenando los registros de las acciones que se realizan en cada uno de los microservicios con el fin de analizar qué está ocurriendo en el sistema en cada momento así como detectar los posibles errores que surjan. 
El segundo servicio estará destinado al almacenamiento de todos los archivos de configuración relevantes. Su principal objetivo es centralizar en un único sistema distribuido toda la información necesaria para que los microservicios puedan comunicarse, por ejemplo, con sus respectivas bases de datos.

#### Lenguajes de programación y frameworks. <a name="id4"></a>

Los microservicios se implementarán en **Python** puesto que este lenguaje de programación cuenta con un conjunto muy amplio de librerías, entre ellas existe una librería *open source* llamada [*Pandas*](https://pandas.pydata.org/) que convierte los datos extraídos en formato JSON proporcionados por la API a un diccionario sencillo con el que poder trabajar. Además este lenguaje de programación es especialmente popular en el desarrollo de aplicaciones estadísticas debido a su gran velocidad de ejecución que facilita la realización de diversos cálculos.

Se han considerado diversos *frameworks* tales como Flask o Django para el desarrollo de las API REST que intercomuniquen los microservicios entre sí o con la API Gateway. Si bien Django dispone de muchas más funcionalidades debido a que está orientado al desarrollo de sistemas más complejos, también está caracterizado por su complejidad en relación a su aprendizaje desde cero. Es por ello por lo que finalmente he optado por usar **Flask**, el cual, además, es ampliamente utilizado por diversas [empresas](https://github.com/rochacbruno/flask-powered). Asimismo dentro de todas las posibilidades que ofrece este *framework* he optado por hacer uso de una extensión en particular denominada [***Flask-RESTful***](https://flask-restful.readthedocs.io/en/latest/) debido a su sencillez en relación a aprender a desarrollar una API REST desde cero.

En referencia al almacenamiento de datos he optado por utilizar una base de datos NoSQL debido a que las bases de datos SQL no cuentan con una gestión eficiente a la hora de trabajar con grandes cantidades de datos. Además otra de las ventajas asociadas a las bases de datos no estructuradas como MongoDB es que se pueden almacenar datos sin especificar la estructura ni las relaciones que existen entre ellos. Esta ventaja aporta una gran flexibilidad a la hora de desarrollar una aplicación que a priori se conoce que va a hacer uso de una cantidad masiva de datos pero cuyas conexiones entre sí pueden variar a lo largo del tiempo. Por lo tanto el sistema de almacenamiento que mi proyecto usará es **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**.