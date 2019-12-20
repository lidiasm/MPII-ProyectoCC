#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Microservicio que se ejecuta en un servidor de tareas para descargar, periódicamente,
los datos de hasta veinte mascotas.

@author: Lidia Sánchez Mérida
"""

from celery import Celery
app = Celery('mascotas_celery', broker='pyamqp://guest@localhost//', backend='rpc://')
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import mascotas
import sys
sys.path.append("src/")
from excepciones import MaxPetfinderRequestsExceeded 

"""Creamos un objeto de la clase Mascotas cuyo constructor se encarga de inicializar
la conexión con la API Petfinder.

Este bloque try-except evita que la excepción impida construir el contenedor al
iniciar celery durante su construcción."""
try:
    m = mascotas.Mascotas()
except:
    print("No se ha podido establecer la conexión aún.")

@periodic_task(run_every=(crontab(hour='*/23')), name="descargar_mascotas")
def descargar_mascotas():
    """Descarga nuevos datos de viente mascotas siempre y cuando se haya realizado
    una conexión correcta con la API Petfinder."""
    try:
        return m.descargar_datos_mascotas()
    except:
        raise MaxPetfinderRequestsExceeded("Número de peticiones máximo excedido.")
