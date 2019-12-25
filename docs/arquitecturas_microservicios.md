## Arquitecturas de los microservicios y ejecución mediante *Gunicorn*.

#### Microservicios de la clase *Mascotas*.

Esta clase incopora la lógica de la aplicación asociada a recopilar datos de mascotas para su posterior visualización. Para ello serán necesarios dos microservicios. El primer de ellos se encargará de realizar la conexión con la API Petfinder y, a continuación, ejecutará la tarea correspondiente a la descarga de datos de mascotas de forma periódica. Por lo tanto, será necesario incluirla en un servidor de tareas como es *Celery* para que se lance automáticamente, en mi caso, cada 24 horas. De ese modo todos los días se descargarán datos de la aplicación para disponer de información actualizada asociada a las mascotas.

Por otro lado se desarrolla un microservicio *REST* que sea capaz de recoger los datos de mascotas, que han sido descargados por el anterior microservicio, con el objetivo de poder visualizarlos en su conjunto o mostrar solo la información asociada a una mascota en particular proporcionando, para ello, su respectivo identificador.

Ambas funcionalidades se corresponden con [uno de los pasos necesarios](https://github.com/lidiasm/ProyectoCC/issues/23#issue-512987660) para cumplir las dos historias de usuario que han sido definidas anteriormente. Para su implementación se ha aplicado una *arquitectura basada en capas* puesto que la lógica de negocio reside en la clase *Mascotas*, de la cual harán uso ambos microservicios para acceder a las métodos correspondientes que les permitan llevar a cabo sus respectivos servicios. En el caso del microservicio *REST*, solo se han implementado servicios *GET* puesto que sus funciones consisten en obtener los datos de las mascotas y visualizarlos. Esta arquitectura queda representada en la siguiente captura.

![Esquema de la arquitectura por capas del primer microservicio.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/Primer%20microservicio.png)

Del mismo modo que se han desarrollado *tests* para comprobar el correcto funcionamiento de los métodos de la clase *Mascotas* también se han desarrollado [tests para el microservicio *REST*](https://github.com/lidiasm/ProyectoCC/blob/master/tests/test_mascotas_rest.py) así como [tests para el microservicio en *Celery*](https://github.com/lidiasm/ProyectoCC/blob/master/tests/test_mascotas_celery.py), con el objetivo de verificar que el comportamiento de ambos es el adecuado.

#### Servidor Web

Tal y como se advierte en diversas páginas de desarrollo, como [esta](https://www.toptal.com/flask/flask-production-recipes), se recomienda utilizar un servidor web adicional para controlar los diferentes aspectos que intervienen en la futura fase de producción. Asimismo, teniendo en cuenta que el proyecto se desarrolla en Python utilizaré un [*WSGI*](https://www.fullstackpython.com/wsgi-servers.html) que proprociona tanto un gestor de procesos como una interfaz web para acceder a las funciones de las clases. Tras investigar las diversas alternativas existentes se puede decir que los más utilizados son [***uWSGI***](https://uwsgi-docs.readthedocs.io/en/latest/), [***Waitress***](https://waitress.readthedocs.io/en/stable/) y [***Gunicorn (Green Unicorn)***](https://gunicorn.org/#docs). En esta [comparativa](https://docs.python-guide.org/scenarios/web/) *uWSGI* destaca por su versatilidad pero también por su complejidad para utilizarlo mientras que *Gunicorn* tiene como ventaja su facilidad de uso y es popularmente utilizada junto con *Flask*. Por lo tanto en mi proyecto haré uso de ***Gunicorn*** como WSGI.

Para ejecutar tanto el microservicio en *Celery* como el microservicio *REST* haciendo uso, para ello, de *Gunicorn* basta con ejecutar el comando: `make start`.
Para detener ambos microservicios se deberá de ejecutar la instrucción: `make stop`.

Para más información acerca de estos dos procesos automatizados puede acceder al [*makefile*](https://github.com/lidiasm/ProyectoCC/blob/master/Makefile) donde se encuentran todos los pasos documentados, así como al [*script*](https://github.com/lidiasm/ProyectoCC/blob/master/run_celery.sh) encargado de configurar e iniciar el microservicio *Celery* utilizando los comandos del propio servidor de tareas.
