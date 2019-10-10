## Proyecto de Cloud Computing 2019-2020

[Enlace al directorio que contiene la documentación.](https://github.com/lidiasm/ProyectoCC/tree/master/documentacion)

#### Descripción del proyecto

El proyecto de esta asignatura consiste en desarrollar una plataforma en la que se facilite la adopción de las diferentes especies de animales domésticas. Para ello se habilitará un registro de usuarios con el fin de especificar sus necesidades y gustos de modo que la plataforma sea capaz de sugerirles las posibles mascotas que puedan adaptarse a su ritmo de vida.  Asímismo la plataforma también mostrará un conjunto de datos estadísticos útiles que posteriormente sirvan para resolver las cuestiones principales que se plantean en el tema de las adopciones. Algunos ejemplos son: 

- Analizar las características de aquellas razas que se encuentran en mayor medida en estos centros de adopción.
- Comprobar cuáles son las especies que tienen un mejor comportamiento con niños así como con otras especies de animales.
- Las ciudades con un mayor número de animales en adopción.
- Las localizaciones donde se encuentran las mayores concentraciones de centros de adopción.

De manera adicional se realizarán publicaciones en *Twitter* acerca de los animales de los que se permite su adopción recientemente así como de los cachorros que se encuentran en la organización. La razón de ello se fundamenta en el hecho de que, con mayor frecuencia, la sociedad utiliza más las redes sociales como medio de información que cualquier otro y por lo tanto se convierten en una herramienta muy útil para divulgar información.

Los datos que se utilizarán en este proyecto se obtienen de la **API Petfinder**. Sus numerosas ventajas, tales como que cuenta con un almacenamiento masivo de datos además de que ha sido partícipe en [diferentes competiciones relacionadas con el ámbito de la Inteligencia Artificial](https://www.linkedin.com/pulse/kaggle-competition-multi-class-classification-image-alexandra), la convierten en una buena opción para usarla en este proyecto.

#### Arquitectura

Con el objetivo de implementar este proyecto se aplicará una **arquitectura basada en microservicios**. Su principal ventaja reside en la posibilidad de desarrollar los diversos microservicios de forma independiente así como su mantenimiento, depuración y actualización. Así mismo se pueden ampliar el número de funcionalidades de la plataforma mediante el desarrollo e integración de nuevos microservicios.

#### Microservicios

1.  Un primer microservicio destinado a la recopilación y procesamiento de los datos realizando, para ello, peticiones a la API Petfinder.

2. Otro microservicio encargado de almacenar la información en una base de datos no estructurada.

3. Un microservicio que realice un análisis de los datos recopilados para calcular estadísticas que sean útiles para comprender los diversos factores que influyen en un proceso de adopción.

4. Un microservicio encargado de realizar el registro de nuevos usuarios con el objetivo de facilitarles la adopción de su futuro compañero. Para ello podrán especificar sus requisitos con el fin de que el microservicio sea capaz de proponerles animales afines a su personalidad.

5. Otro microservicio cuya tarea consistirá en publicar tweets acerca de aquellos animales que sean más interesantes con el objetivo de darlos a conocer a la comunidad de Twitter.

6. Por último se desarrollará un microservicio que sea capaz de comunicarse con todos los microservicios anteriores.

#### Lenguajes de programación y frameworks 

Los microservicios se implementarán en **Python** puesto que este lenguaje de programación cuenta con un conjunto muy amplio de librerías, entre ellas existe una librería *open source* llamada ![Panda](https://pandas.pydata.org/) que convierte los datos extraídos en formato JSON proporcionados por la API a un diccionario sencillo con el que poder trabajar. Además este lenguaje de programación es especialmente popular en el desarrollo de aplicaciones estadísticas debido a su gran velocidad de ejecución que facilita la realización de diversos cálculos. 

Como framework se han considerado el uso de Flask o Django. Este último dispone de muchas más funcionalidades debido a que está orientado al desarrollo de aplicaciones más complejas. Por ello y debido a la complejidad que caracteriza su aprendizaje desde cero finalmente he optado por usar **Flask**, el cual, además, es ampliamente utilizado por diversas [empresas](https://github.com/rochacbruno/flask-powered).

En referencia al almacenamiento de datos he optado por utilizar una base de datos NoSQL debido a que las bases de datos SQL no cuentan con una gestión eficiente a la hora de trabajar con grandes cantidades de datos. Además otra de las ventajas asociadas a las bases de datos no estructuradas como MongoDB es que se pueden almacenar datos sin especificar la estructura ni las relaciones que existen entre ellos. Esta ventaja aporta una gran flexibilidad a la hora de desarrollar una aplicación que a priori se conoce que va a hacer uso de una cantidad masiva de datos pero cuyas conexiones entre sí pueden variar a lo largo del tiempo. Por lo tanto el sistema de almacenamiento que mi proyecto usará es **[MongoDB](https://dzone.com/articles/comparing-mongodb-amp-mysql)**.

Por último para implementar el microservicio destinado a la publicación de tweets se hará uso de la librería **[tweepy](http://www.tweepy.org/)**.

Con el objetivo de interconectar todos los microservicios se utilizará un [*broker*](https://dzone.com/articles/how-to-make-microservices-communicate) para brindar la posibilidad de que los microservicios se comuniquen de forma directa mediante el envío y la recepción de mensajes. Entre todos los *brokers* disponibles he optado por utilizar **[RabbitMQ](https://www.rabbitmq.com/)** por ser de código libre además del soporte que proporciona sobre diversos tipos de protocolos de mensajes.