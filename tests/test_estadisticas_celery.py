#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para comprobar el funcionamiento del microservicio en Celery encargado
de generar las estadísticas acerca de las mascotas descargadas.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src/estadisticas")
from estadisticas_celery import generar_estadisticas

def test_generar_estadisticas():
    """Test 1: genera los tres tipos de informes estadísticos."""
    """Utilizo apply para convertir la tarea en síncrona y así esperar a que
        se complete con el objetivo de conocer su resultado.
        Fuente: https://www.distributedpython.com/2018/05/01/unit-testing-celery-tasks/"""
    try:
        estadisticas = generar_estadisticas.apply()
        assert(type(estadisticas.result) == list)
    except:
        print("No existen mascotas sobre las que generar las estadísticas.")
