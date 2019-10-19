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

Tras la búsqueda de información acerca de las arquitecturas existentes he decidido que este proyecto se basará en una **arquitectura de microservicios**. Su razón de ser se fundamenta en las diversas ventajas que presenta tales como la posibilidad de desarrollar los diversos microservicios de forma independiente así como su mantenimiento, depuración y actualización. Además permite desarrollar microservicios adicionales con el fin de ampliar las funcionalidades del sistema.
[Más información acerca de la arquitectura y microservicios.]()

#### Microservicios. <a name="id3"></a>

1.  Un primer microservicio destinado a la recopilación y procesamiento de los datos recopilados de la API Petfinder.

2. Otro microservicio encargado de almacenar la información en una base de datos no estructurada.

3. Un microservicio que realice un análisis de los datos almacenados para calcular estadísticas que sean útiles para comprender los diversos factores que influyen en un proceso de adopción.

4. Un microservicio encargado de realizar el registro de nuevos usuarios o el inicio de sesión de aquellos ya existentes en el sistema.

5. Un microservicio capaz de realizar búsquedas en la base de datos en función de un conjunto de criterios especificados.

6. Por último se desarrollará un microservicio LOG con el que se comunicarán todos los microservicios anteriores.

#### Lenguajes de programación y frameworks. <a name="id4"></a>

Los microservicios se implementarán en **Python** puesto que este lenguaje de programación cuenta con un conjunto muy amplio de librerías, entre ellas existe una librería *open source* llamada [Pandas](https://pandas.pydata.org/) que convierte los datos extraídos en formato JSON proporcionados por la API a un diccionario sencillo con el que poder trabajar. Además este lenguaje de programación es especialmente popular en el desarrollo de aplicaciones estadísticas debido a su gran velocidad de ejecución que facilita la realización de diversos cálculos.

Con el fin de implementar la ***API REST*** se han considerado diversos *frameworks* tales como Flask o Django. Este último dispone de muchas más funcionalidades debido a que está orientado al desarrollo de sistemas más complejos. Por ello y debido a la complejidad que caracteriza su aprendizaje desde cero finalmente he optado por usar **Flask**, el cual, además, es ampliamente utilizado por diversas [empresas](https://github.com/rochacbruno/flask-powered). Asimismo dentro de todas las posibilidades que ofrece este *framework* he optado por hacer uso de una extensión en particular denominada [***Flask-RESTful***](https://flask-restful.readthedocs.io/en/latest/) debido a su sencillez en relación a aprender a desarrollar una API REST desde cero.

En referencia al almacenamiento de datos he optado por utilizar una base de datos NoSQL debido a que las bases de datos SQL no cuentan con una gestión eficiente a la hora de trabajar con grandes cantidades de datos. Además otra de las ventajas asociadas a las bases de datos no estructuradas como MongoDB es que se pueden almacenar datos sin especificar la estructura ni las relaciones que existen entre ellos. Esta ventaja aporta una gran flexibilidad a la hora de desarrollar una aplicación que a priori se conoce que va a hacer uso de una cantidad masiva de datos pero cuyas conexiones entre sí pueden variar a lo largo del tiempo. Por lo tanto el sistema de almacenamiento que mi proyecto usará es **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**.

Con el objetivo de interconectar todos los microservicios se utilizará un [*broker*](https://dzone.com/articles/how-to-make-microservices-communicate) para brindar la posibilidad de que los microservicios se comuniquen de forma directa mediante el envío y la recepción de mensajes. Entre todos los *brokers* disponibles he optado por utilizar **[RabbitMQ](https://www.rabbitmq.com/)** por ser de código libre además del soporte que proporciona sobre diversos tipos de protocolos de mensajes.
