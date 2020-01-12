#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Microservicio Celery para generar las estadísticas de forma periódica y asíncrona.

@author: Lidia Sánchez Mérida
"""

import os
from celery import Celery
app = Celery('estadisticas_celery', broker='redis://guest@localhost//', backend='redis://')
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import sys
sys.path.append("src")  # ../ para ejecutar el worker de celery
sys.path.append("../")
from excepciones import PetsNotFound, EmptyCollection
import estadisticas
sys.path.append("src/mascotas")
sys.path.append("../mascotas")
import mascotas
from mongodb import MongoDB

"""Creamos un objeto de la base de datos donde se almacenan las mascotas."""
bdMascotas = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')
"""Creamos un objeto de la clase Mascotas para obtener todas las mascotas de la base
de datos y así generar las estadísticas, en lugar de conenectarnos con el microservicio
Celery que descarga los datos. Así desacoplamos la obtención de datos del resto de microservicios."""
m = mascotas.Mascotas(bdMascotas)

"""Creamos un objeto de la clase Estadísticas para acceder a los métodos que generan
los diferentes tipos de infomes"""
bdEstd = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'estadisticas')
estd = estadisticas.Estadisticas(bdEstd)

@periodic_task(run_every=(crontab(minute='*/60')), name="generar_estadisticas")
def generar_estadisticas():
    """Genera los tres informes estadísticos a partir de los datos de las mascotas
        descargados. """
    try:
        mascotasbd = m.obtener_mascotas()
        estd_ninios = estd.generar_estadistica_ninios(mascotasbd)
        estd_razas_perro = estd.generar_estadistica_razas_perro(mascotasbd)
        estd_tipos_mascotas = estd.generar_estadistica_tipos_mascotas(mascotasbd)
        return [estd_ninios, estd_razas_perro, estd_tipos_mascotas]
    except PetsNotFound:
        raise PetsNotFound("Celery Estadísticas: no existen mascotas sobre las que generar estadísticas.")
    except EmptyCollection:
        raise EmptyCollection("Celery Estadísticas: no existen mascotas sobre las que generar estadísticas.")
