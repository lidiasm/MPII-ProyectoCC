## Elección del sistema operativo base.

En primer lugar comienzo por mostrar los resultados proporcionados por [*ab*](https://httpd.apache.org/docs/2.4/programs/ab.html) para las versiones de *Python*, las cuales se pueden encontrar [aquí](https://hub.docker.com/_/python).

### Slim.

Esta versión es una de las más ligeras en las que se incluyen solo los paquetes imprescindibles para ejecutar aplicaciones de *Python*. El tamaño del contenedor con este sistema operativo como base es de `346MB`. Si bien uno de los objetivos de investigar diversos sistemas operativos para la base de un contenedor es encontrar alguno que sea ligero para que su despliegue sea más rápido, también hay que tener en cuenta las necesidades de la aplicación que se vaya a ejecutar. En mi caso consta del microservicio encargado de realizar una conexión con la API Petfinder, descargar datos de mascotas y visualizarlos. Por lo tanto, es necesario comprobar la velocidad con la que se satisfacen las peticiones a estos servicios REST así como su grado de completitud. De entre todos los servicios he escogido los dos que a mi parecer tienen una mayor complejidad y consumo de recursos: conectar con la API Petfinder y descargar datos de hasta 20 mascotas. A continuación se muestran los resultados proporcionados por [*ab*] al realizar 100 peticiones con 10 hebras a cada uno de los dos servicios.

![Slim petfinder.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20slim%20conexi%C3%B3n.png)

![Slim descarga.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20slim%20descargar%20datos.png)

### Slim buster.

Esta versión se trata del sistema operativo [**Debian 10**](https://wiki.debian.org/DebianBuster) en su versión minimalista y con la cual el contenedor pasa a ser de `363MB`. Al igual que en el caso anterior se repite de nuevo el mismo procedimiento y a continuación se presentan los resultados.

![Slim-buster petfinder.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20slim-buster%20conexi%C3%B3n.png)

![Slim-buster descarga.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20slim-buster%20descargar%20datos.png)

### Slim stretch.

En este caso, de nuevo, se trata de una versión mínima pero del sistema operativo [**Debian 9**](https://wiki.debian.org/DebianStretch) con el que al construir el contenedor su tamaño disminuye hasta los `323MB`. A continuación se presentan los resultados obtenidos al realizar el mismo procedimiento de peticiones pero con este sistema como base.

![Slim-stretch petfinder.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20slim-stretch%20conexi%C3%B3n.png)

![Slim-stretch descarga.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20slim-stretch%20descargar%20datos.png)

### Stretch.

Se trata de la versión completa del sistema operativo anterior **Debian 9**, el cual ha sido incluido en este estudio para destacar la considerable diferencia de tamaño con respecto a la versión minimalista anterior, puesto que en este caso el tamaño del contenedor utilizando esta base aumenta hasta `1.1GB`. Aunque no lo considere como una opción, a continuación se adjuntan sus resultados de las peticiones.

![Stretch petfinder.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20stretch%20conexi%C3%B3n.png)

![Stretch descarga.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20stretch%20descargar%20datos.png)

### Alpine.

Por último consideraremos este sistema base puesto que es uno de los más ligeros. Sin embargo, como mi proyecto utiliza la librería *pandas* y *Alpine* no dispone de herramientas de compilación para construir esta librería necesito utilizar una versión que de este sistema en la que ya se encuentre *pandas* instalada previamente. Para realizar las pruebas con este sistema he utilizado [esta imagen](https://hub.docker.com/r/quoinedev/python3.6-pandas-alpine). 
El tamaño del contenedor al construirlo con esta versión base es de `655 MB` y los resultados de las peticiones se presentan a continuación.

![Alpine petfinder.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20alpine%20conexi%C3%B3n.png)

![Alpine descarga.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/ab%20alpine%20descargar%20datos.png)

Todos los tamaños de los contenedores generados para cada sistema base se pueden visualizar en la siguiente captura.

![Tamaños](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/tams.png)

## Resumen de las prestaciones.

A continuación se muestra una tabla resumen de las prestaciones ofrecidas por cada uno de los sistemas base en relación a las peticiones realizadas al servicio REST *conectar_petfinder*.

| Sistema base. | Tiempo total. | Tiempo/petición en paralelo. | Peticiones/segundo. |
| --- | --- | --- | --- | --- | --- | --- |
| Slim. | 73,891 s. | 0,738 s/peticion | 1,35 peticiones/s |
| Slim buster. | 48,758 s. | 0,487 s/petición | 2,05 peticiones/s |
| Slim stretch. | 50,895 s. | 0,508 s/petición | 1,96 peticiones/s |
| Stretch. | 49,636 s. | 0,493 s/petición | 2,01 peticiones/s |
| Alpine. | 47,184 s. | 0,471 s/petición | 2,12 peticiones/s |

Tal y como podemos comprobar en la tabla anterior el sistema base más rápido para ejecutar las peticiones al servicio REST que conecta con la API Petfinder es **Alpine**, ya que su tiempo es el menor de todos y es el que, además, atiende un mayor número de peticiones. Sin embargo las diferencias con *slim-buster*, *slim-stretch* y *stretch* no son considerables puesto que presentan prestaciones similares para este servicio. Por lo tanto, teniendo en cuenta, además, que el tamaño de la imagen de *Alpine* duplica a la de *slim-stretch* el sistema base con mejor relación prestaciones-tamaño es **slim-stretch**. 

Por otro lado procedo a mostrar también un resumen de los resultados obtenidos con cada uno de los sistemas operativos al realizar las peticiones al servicio REST *descargar_datos_mascotas*.

| Sistema base. | Tiempo total. | Tiempo/petición en paralelo. | Peticiones/segundo. |
| --- | --- | --- | --- | --- | --- | --- |
| Slim. | 92,537 s. | 0,925 s/petición | 1.08 peticiones/s |
| Slim buster. | 113,139 s. | 1,131 s/petición | 0,88 peticiones/s |
| Slim stretch. | 90,496 s. | 0,904 s/petición | 1,11 peticiones/s |
| Stretch. | 83,809 s. | 0,838 s/petición | 1,19 peticiones/s |
| Alpine. | 85,562 s. | 0,855 s/petición | 1,17 peticiones/s |

En este caso el mejor resultado lo proporciona el sistema *Debian 9* o *Stretch* en base tanto a su tiempo total de satisfacción de las peticiones así como al número de estas que atiende por segundo. No obstante, tanto *Alpine* como *slim-stretch* consiguen resultados bastante similares, y de nuevo, teniendo en cuenta el gran tamaño del contenedor con *Stretch* como imagen base no merece la pena escogerlo para nuestro contenedor puesto que ralentizaría mucho el despliegue. 

Un hecho destacable consiste en que los peores resultados para este servicio REST han sido obtenidos por uno de los sistemas base que proporcionó unas buenas prestaciones para el servicio REST anterior, se trata de *slim-buster*. Es por este tipo de sucesos por los que he decidido probar con dos servicios REST diferentes, puesto que si elijo este sistema como base para el contenedor será capaz de resolver rápidamente las peticiones para conectar con la API Petfinder pero no será adecuado para el servicio encargado de descargarse los datos de las mascotas. 

En base a los dos estudios de prestaciones realizados con dos servicios REST diferentes el sistema operativo base que se caracteriza por una mejor relación prestaciones-tamaño es **slim-stretch**, y por lo tanto será el que use para construir este primer contenedor.