#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el servidor de tareas Celery que se encarga de conectar con la API Petfinder
y descargar los datos de hasta 20 mascotas.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src/mascotas")
from mascotas_celery import descargar_mascotas

def test_descargar_datos_mascotas():
    """Test 1: Descarga de datos de hasta veinte mascotas."""
    """Utilizo apply para convertir la tarea en síncrona y así esperar a que
        se complete con el objetivo de conocer su resultado.
        Fuente: https://www.distributedpython.com/2018/05/01/unit-testing-celery-tasks/"""
    try:
        mascotas = descargar_mascotas.apply()
        assert(type(mascotas.result) == dict)
    except:
        print("Número de peticiones máximo excedido.")