## Estudio de prestaciones con máquinas virtuales en Azure.

Comenzamos evaluando las peticiones que es capaz de soportar la máquina virtual creada en primera instancia. En este sistema se encuentra *Ubuntu Server* como sistema operativo y cuenta con las siguientes características que se pueden comprobar en la captura que se adjunta a continuación.

![Máquina 1.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/VM%201%20Ubuntu.png)

De nuevo se ha hecho uso de [*Apache Benchmark*](https://httpd.apache.org/docs/2.4/programs/ab.html) para realizar el estudio de las prestaciones. Al comienzo se optó por realizar la evaluación desde mi máquina local, es decir, de forma remota. Para ello se deben **abrir los puertos asociados a los microservicios** para que nos deje acceder a ellos y mandarle las peticiones. Según la [documentación](https://docs.microsoft.com/es-es/azure/virtual-machines/linux/nsg-quickstart) basta con ejecutar una primera vez el comando `az vm open-port --resource-group mascotas --name ubuntu --port 8000` para permitir la llegada de tráfico al microservicio de las mascotas, y posteriormente una segunda ejecución cambiando el puerto por el 8001 para hacer lo mismo con el segundo microservicio. Una vez hecho esto, podemos realizar el estudio para esta primera máquina desde mi máquina local. Los resultados se pueden comprobar a continuación.

![Prestaciones remotas máquina 1.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/VM1%20mascotas%20remoto.png)

Tal y como se puede comprobar el número de prestaciones/segundo es sumamente bajo. Intentado buscar una explicación a este fenómeno se propuso analizar la **latencia** existente al mandar las peticiones desde mi máquina local a la máquina en Azure. Para ello basta con hacer **ping** a la máquina. No obstante, como en el caso de los puertos de los microservicios, se debe habilitar el protocolo **ICMP** utilizando para ello la orden `az network nsg rule create --name ubuntu --resource-group mascotas --nsg ubuntuNSG --priority 1100 --protocol Icmp`, tal y como se explica en la [documentación](https://docs.microsoft.com/en-us/cli/azure/network/nsg/rule?view=azure-cli-latest). Tras permitir el tráfico utilizando este protocolo, a continuación se puede llevar a cabo el experimento que nos permitirá conocer cuánto tardan las peticiones en mandarse a la máquina en Azure. Para ello ejecutamos la orden `ping 23.96.122.39` y como resultado proporcionó tiempos de latencia en torno a **121 ms**, lo cual es suficiente como para que el estudio de prestaciones resulte en unas prestaciones/segundo bastante inferiores al objetivo prefijado. Sin embargo, si las evaluamos desde la propia máquina de Azure, conectándonos a ella a través de SSH, los resultados varían enormemente.

![Prestaciones local máquina.](https://github.com/lidiasm/ProyectoCC/blob/master/docs/imgs/VM1%20mascotas%20remoto.png)

En base a los resultados observados en ambas mediciones podemos confirmar que sí existe una gran diferencia entre evaluar el rendimiento de los microservicios de forma local o de forma remota, mandando las peticiones desde mi máquina local a la máquina de Azure. Es por ello por lo que el resto de mediciones que se muestran a continuación se van a realizar localmente, desde la máquina en Azure.

Si bien las prestaciones obtenidas de forma local con el **primer microservicio** están próximas a las 1.000 peticiones/segundo, he probado dos configuraciones más obteniendo los siguientes resultados elegidas de entre las [disponibles en Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/compute-benchmark-scores#dv2---general-compute). Asimismo, en lugar de crear dos máquinas diferentes más se ha modificado el tamaño de la que ya estaba creada tal y como se explica en la [documentación](https://docs.microsoft.com/bs-latn-ba/azure/virtual-machines/linux/change-vm-size) a través del comando `az vm resize --resource-group mascotas --name ubuntu --size <nombre de la configuración>`. A continuación se muestra los resultados obtenidos:

| Tamaño. | CPUs. | RAM total. | Discos duros. | E/S máxima. | Costo al mes. | Peticiones/segundo. |
| --- | --- | --- | --- | --- | --- | --- |
| DS1_v2 | 1 | 3.5 GB | 4 | 3.200 | 45.80€ | 974.80 |
| DS2_v2 | 2 | 7 GB | 8 | 6.400 | 91.60€ | 1457.26 |
| D4s_v3 | 4 | 16 GB | 8 | 6.400 | 120.46€ | 1980.25 |

Tal y como se puede comprobar, con máquinas con mejores características se consiguen mejores resultados pero también se paga más. Por lo tanto, en este caso, siendo la diferencia entre las prestaciones obtenidas y las establecidas tan mínima y considerando, sin embargo, la gran diferencia de costo al mes entre las diferentes máquinas, para el primer microservicio apostaría por la máquina con la primera configuración *DS1_v2*. A continuación visualizamos las prestaciones medidas con las mismas máquinas anteriores para el **segundo microservicio**.

| Tamaño. | CPUs. | RAM total. | Discos duros. | E/S máxima. | Costo al mes. | Peticiones/segundo. |
| --- | --- | --- | --- | --- | --- | --- |
| DS1_v2 | 1 | 3.5 GB | 4 | 3.200 | 45.80€ | 787.79 |
| DS2_v2 | 2 | 7 GB | 8 | 6.400 | 91.60€ | 1516.70 |
| D4s_v3 | 4 | 16 GB | 8 | 6.400 | 120.46€ | 1942.80 |

En este caso las diferencias entre las prestaciones obtenidas con la máquina más básica y la segunda más completa sí que son considerables, puesto que esta última es capaz de atender a casi más del doble de peticiones. Por ello para maximizar el rendimiento de este microservicio y cumplir las prestaciones establecidas, se debería escoger la máquina con la segunda configuración.