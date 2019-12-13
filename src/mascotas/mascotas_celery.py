#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 19:36:22 2019

@author: Lidia Sánchez Mérida
"""

from celery import Celery
app = Celery('mascotas_celery', broker='pyamqp://guest@localhost//', backend='rpc://')
from celery.task.schedules import crontab
from celery.decorators import periodic_task

import mascotas
"""Creamos un objeto de la clase Mascotas cuyo constructor se encarga de inicializar
la conxión con la API Petfinder."""
m = mascotas.Mascotas()

@periodic_task(run_every=(crontab(minute='*/1')), name="descargar_mascotas")
def descargar_mascotas():
    """Descarga nuevos datos de viente mascotas siempre y cuando se haya realizado
    una conexión correcta con la API Petfinder."""
    return m.descargar_datos_mascotas()
