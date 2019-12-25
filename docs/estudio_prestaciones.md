## Estudio de las prestaciones.

### Situación inicial.

En primer lugar realizaremos una medición de las prestaciones que puede proporcionar el primer microservicio destinado
a recopilar y visualizar datos de mascotas. Partimos de la siguiente situación inicial:

* Ejecución de una tarea periódica en *Celery* para recopilar datos de mascotas procedentes de la API Petfinder de forma **asíncrona** y almacenarlos en la base de datos configurada como caché.
* El microservicio REST recopila la información descargada accediendo a la base de datos y, posteriormente, la visualiza en formato JSON.
* El microservicio REST será ejecutado mediante el servidor *Gunicorn* con tantos *workers* como tareas en paralelo deseemos servir, en nuestro caso, se ejecutarán hasta 10 copias del servidor.

Si bien, como se ha podido comprobar, he configurado el fichero para realizar las mediciones con la herramienta *Taurus*, no he podido conseguir encontrar la fuente del error que se puede observar en la siguiente captura. Cabe destacar que, obviamente probé a reinstalarlo desde cero en diversas ocasiones en dos ordenadores diferentes, busqué documentación acerca de este fallo en internet sin éxito, pedí ayuda a otros compañeros, pero al parecer este error no es nada conocido.

![Error taurus.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Error%20Taurus.jpg)

En base a estas circunstancias me he visto forzada a realizar este estudio con otra herramienta, con la cual ya trabajé en la práctica anterior para realizar el estudio de imágenes base para el docker: *ab*.

En la siguiente captura podemos comprobar el resultado de evaluar el servicio *obtener_mascotas* lanzando 1.000 peticiones en total atendiendo hasta 10 simultáneamente bajo las condiciones explicadas anteriormente.

![Situación inicial.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Situaci%C3%B3n%20inicial.png)

Tal y como podemos comprobar **no se han producido errores** pero solo ha podido llevar a cabo **400 peticiones por segundo**.

### Optimización de Gunicorn.

Como segundo experimento vamos a intentar mejorar las prestaciones del servidor en el que se ejecuta el microservicio. Investigando acerca de sus características he comprobado que, si no se especifica otro tipo de *worker*, por defecto este servidor atiende las peticiones de forma síncrona. Esta cualidad puede afectar de forma considerable a la eficiencia de los servicios que se ejecutan en él. Para mejorarlo he buscado información acerca de las mejores opciones que se pueden incluir, y entre las diversas fuentes consultadas, encontré [esta](https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7) en particular en la que se detallan diversas posibilidades:

1. Para que el servidor sea capaz de atender peticiones de forma asíncrona, se especifica una de las diversas librerías que permiten esta característica como la clase de los *workers*. En mi caso utilizaré ***gevent***. Asimismo, se establecen el número de peticiones que podrá atender cada uno de los *worker*, que en mi proyecto se trata de **1000 peticiones cada uno**.

2. En lugar de establecer el número de *workers* de forma que concuerde con el número de peticiones concurrentes, en la fuente anterior se propone calcular el valor exacto considerando el número de *CPUs* que tiene el ordenador sobre el que se ejecuta el microservicio. En mi caso dispongo de 4 núcleos por lo que siguiendo la fórmula *(2*CPUs)+1* especifico la ejecución de hasta **9 workers** en total.

En base a estas modificaciones se ha realizado una nueva prueba con *ab* repitiendo, para ello, el proceso anterior. A continuación se muestran los resultados de este segundo experimento.

![Mejora Gunicorn.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Mejora%20gunicorn.png)

Como se puede comprobar el número de peticiones por segundo no ha mejorado, incluso ha empeorado pese a incorporar un módulo para permitir servir peticiones de forma asíncrona. Sin embargo, reflexionando acerca de los resultados y las características de este segundo experimento, caí en la cuenta de que solo había un único servidor *Celery* recopilando datos de mascotas. Por ello, esto da lugar a un tercer experimento en el que se investigue la concurrencia que puede brindar este servidor.  

### Concurrencia en Celery.

Consultando la [documentación de Celery](https://docs.celeryproject.org/en/latest/userguide/workers.html#concurrency) acerca de la posibilidad de atender diversas peticiones simultáneas, descubrí la posibilidad de iniciar varias hebras dentro de una misma instancia de Celery para atender diversas peticiones de forma simultánea. Sin embargo, *Celery* también proporciona un componente denominado [*autoscaler*](https://docs.celeryproject.org/en/latest/userguide/workers.html#autoscaling) que es capaz de balancear la carga del servidor aumentando el número de hebras dentro de un mismo *worker* cuando existen un mayor número de peticiones. Para ello basta con añadir el modificador ***--autoscale=20,10*** especificando como primer valor el número máximo de hebras al que puede llegar, que en mi caso serán 10 puesto que deseamos servir hasta 10 peticiones concurrentes, y como segundo valor el número de procesos mínimo que ejecutará desde el inicio, el cual en mi caso he establecido como el doble del mínimo. Por lo tanto, comenzará ejecutando 10 hebras e irá iniciando más conforme se realicen un mayor número de peticiones.

![Celery concurrente.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Celery%20concurrente.png)

En este experimento sí que podemos observar una notable mejora de las prestaciones proporcionadas puesto que hemos conseguido servir hasta **745 peticiones por segundo**, ejecutando 10 de forma concurrente y con 0 errores. No obstante, aún debemos de introducir alguna mejora más para poder escalar aún más este microservicio y conseguir alcanzar las prestaciones establecidas.

### Flask caché.

Investigando acerca de la [importancia del uso de cachés en API RESTs](https://restfulapi.net/caching/) encontré una librería de *Flask* especializada en la inclusión de este tipo de componentes denominada [**Flask-Cache**](https://flask-caching.readthedocs.io/en/latest/). El objetivo que pretendía alcanzar añadiendo una caché para el microservicio *REST* consistía en reducir el número de llamadas a la base de datos para obtener los datos de las mascotas, los cuales, además, solo se amplían cuando el microservicio periódico en *Celery* es lanzado para descargar nueva información de mascotas. Por lo tanto durante un largo período de tiempo esta información permanece inalterable.

Para añadirla basta con incluir dicha librería en el microservicio *REST* y establecer una sencilla configuración referente al tipo de caché, que en mi caso es *simple*, y al tiempo en el que expira, que he establecido en 1 hora pero que se puede ampliar si fuese necesario. Por último basta con añadir el decorador ***@cache.cached()*** a los dos servicios *REST* que visualizan los datos de todas las mascotas o de una en particular, respectivamente. A continuación repetimos el mismo experimento que venimos haciendo durante este estudio para comprobar si las nuevas prestaciones.

![Flask caché 1000 peticiones.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Flask%20cach%C3%A9%201000.png)

Tal y como se puede observar la mejoría es sumamente notable puesto que hemos alcanzado, e incluso superado, la meta impuesta de 1.000 peticiones/s obteniendo **1267 peticiones/s**. Esto supone que el microservicio es capaz de servir más peticiones por segundo que las que hemos establecido en un principio, por lo tanto, procedo a realizar más evaluaciones aumentando el número de peticiones para comprobar su escalabilidad. A continuación se muestra un resumen de los resultados obtenidos.

| Nº de peticiones. | Nº de peticiones concurrentes. | Peticiones/s. | % error. | Tiempo total. |
| --- | --- | --- | --- | --- |
| 1.000 | 10 | 1267.02 peticiones/s. | 0%. | 0.789 s. |
| 3.000 | 10 | 1311.09 peticiones/s. | 0%. | 2.288 s. |
| 5.000 | 10 | 1399.74 peticiones/s. | 0%. | 3.572 s. |
| 13.000 | 10 | 1464.37 peticiones/s. | 0%. | 8.878 s. |
| 15.000 | 10 | 1497.76 peticiones/s. | 0%. | 10.015 s. |
| 20.000 | 10 | 1451.60 peticiones/s. | 0%. | 13.778 s. |
| 50.000 | 10 | 905.38 peticiones/s. | 0%. | 55.225 s. |
| 100.000 | 10 | 993.93 peticiones/s. | 0%. | 100.611 s. |

Como podemos comprobar el microservicio proporciona unas buenas prestaciones aumentando el número de peticiones total hasta las 50.000, en las que comienza a degradarse perdiendo eficiencia y por lo tanto disminuyendo el número de peticiones que puede atender por segundo. No obstante, cabe destacar que continua sirviendo todas las peticiones con un 0% de error.