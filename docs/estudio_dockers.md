## Elección del sistema operativo base.

Para verificar las prestaciones proporcionadas por los diversos sistemas base que a continuación probaré, voy a hacer uso de la herramienta [*ab*](https://httpd.apache.org/docs/2.4/programs/ab.html). Dichos sistemas operativos serán aquellos recomendados por la comunidad de *Python*, los cuales se pueden encontrar [aquí](https://hub.docker.com/_/python). Entre ellos podemos encontrar el sistema **slim-buster** que en realidad se trata del sistema [**Debian 10**](https://wiki.debian.org/DebianBuster) en su versión minimalista, **slim-stretch** que se corresponde con la versión mínima del sistema operativo [**Debian 9**](https://wiki.debian.org/DebianStretch), entre otros. 

Si bien uno de los objetivos de investigar diversos sistemas operativos para la base de un contenedor es encontrar alguno que sea **ligero** para que su despliegue sea más rápido, también hay que tener en cuenta las necesidades de la aplicación que se vaya a ejecutar. En mi caso se trata de la ejecución, por un lado de un microservicio situado en el servidor de tareas Celery para descargar datos de mascotas periódicamente, y un microservicio REST para visualizar los datos de dichas mascotas, tras validarlos y quedarnos con los que son interesantes para este proyecto. Por lo tanto, es necesario comprobar la velocidad con la que se satisfacen las peticiones a estos servicios REST así como su grado de completitud.

A continuación se muestran los resultados proporcionados por [*ab*] al realizar 100 peticiones, siendo 10 de ellas concurrentes, al servicio REST *obtener_mascotas*. 

| Sistema base. | Tamaño. | Tiempo total. | Tiempo/petición en paralelo. | Peticiones/segundo. |
| --- | --- | --- | --- | --- |
| Slim. | 374 MB. | 20.177 s. | 0.201 s. | 4.96 peticiones/s. |
| Slim stretch. | 350 MB. | 11.071 s. | 0.110 s. | 9.03 peticiones/s. |
| Slim buster. | 374 MB. | 24.236 s. | 0.242 s. | 4.13 peticiones/s. |
| Stretch. | 1.13 GB. | 22.170 s. | 0.221 s. | 4.51 peticiones/s. |

## Conclusiones.

Tal y como se puede comprobar el sistema operativo que mejores prestaciones ofrece es **slim-stretch**, tanto por el tamaño, puesto que es el que consigue la imagen más ligera, como por el número de prestaciones que ofrece, el cual es hasta dos veces superior a las del resto de sistemas base. Por todo ello, será este sistema el que utilice como base para el contenedor que proporcione el servicio REST encargado de visualizar los datos descargados y validados de mascotas.