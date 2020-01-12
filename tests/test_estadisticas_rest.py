#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para comprobar el funcionamiento de las diferentes rutas encargadas de
obtener y mostrar un informe estadístico en particular de los tres existentes.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src/estadisticas")
import estadisticas_rest
app = estadisticas_rest.app.test_client()
sys.path.append("src")
import os
import mongodb
import estadisticas
"""Creamos un objeto de la base de datos y lo configuramos."""
bd = mongodb.MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'estadisticas')
"""Objeto que nos conecta con la clase Mascotas."""
estd = estadisticas.Estadisticas(bd)

def test_ver_estadistica_ninios():
    """Test 1: obtiene el primer tipo de informe donde se muestran las mascotas que
        mejor se relacionan con niños."""
    respuesta = app.get('/ver_estadistica_ninios')
    if (respuesta.status_code == 400):
        """No se ha generado el informe aún."""
        assert (respuesta.status_code == 400)
    else:
        assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json") 
        
def test_ver_estadistica_tipos_mascotas():
    """Test 2: obtiene el segundo tipo de informe donde se muestran las mascotas
        que se pueden adoptar así como el número de ejemplares disponibles."""
    respuesta = app.get('/ver_estadistica_tipos_mascotas')
    if (respuesta.status_code == 400):
        """No se ha generado el informe aún."""
        assert (respuesta.status_code == 400)
    else:
        assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json") 
        
def test_ver_estadistica_razas_perro():
    """Test 3: obtiene el tercer tipo de informe donde se muestra la sociabilidad
        de las razas de perro registradas."""
    respuesta = app.get('/ver_estadistica_razas_perro')
    if (respuesta.status_code == 400):
        """No se ha generado el informe aún."""
        assert (respuesta.status_code == 400)
    else:
        assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json") 