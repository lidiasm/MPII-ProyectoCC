### Pruebas de los servicios REST del contenedor *obtener_mascotas*.

#### Conexión con la API Petfinder.

Si tenemos definidas las variables de entorno correspondientes a la API key y a la API secret podremos realizar la conexión con la API Petfinder obteniendo la siguiente pantalla.

![Conexión Petfinder.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/REST%20conectar%20petfinder.png)

#### Descarga de datos de mascotas.

Una vez nos hemos conectado con la API podremos descargar datos de mascotas, en este caso, se recopilará información de hasta 20 mascotas. Una prueba del resultado que obtenemos se encuentra en la siguiente captura, en la cual podemos contemplar los diferentes campos que contiene Petfinder asociados a cada mascota.

![Descarga de datos.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/REST%20descargar%20datos.png)

#### Visualización de los datos de mascotas actuales.

Si bien la API Petfinder cuenta con numerosos datos acerca de las mascotas, solo almacenaremos aquellos que realmente son relevantes para el desarrollo del proyecto. Por lo tanto, a continuación se pueden observar los campos que se guardan en la clase *Mascotas* para cada uno de los animales.

![Visualización mascotas.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/REST%20visualizar%20mascotas.png)

#### Visualización de los datos de una mascota concreta.

Por útlimo también es posible visualizar los datos de una mascota en concreto. Para ello será necesario especificar su identificador asociado. En la siguiente captura se puede observar cómo se obtienen los datos relacionados con la mascota cuyo identificador es el 7.

![Visualización una mascota.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/REST%20visualizar%20una%20mascota.png)