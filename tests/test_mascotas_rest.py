#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:45:55 2019

Tests para el servicio REST que accede a los métodos de obtener_mascota y 
obtener_mascotas de la clase Mascota.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src/mascotas")
import mascotas_rest

app = mascotas_rest.app.test_client()
        
def test_obtener_mascotas():
    """Test 1: recopilar los datos de mascotas descargados por el microservicio
        de Celery para mostrarlos."""
    respuesta = app.get('/obtener_mascotas')
    # Para acceder a los datos de la mascota devueltos -> respuesta.data
    """ Comprobamos el código devuelto y que la cabecera sea JSON que significa
        que se devuelve el diccionario con los datos de la mascota en dicho formato"""
    assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")
    
def test_obtener_una_mascota():
    """Test 2: obtener los datos de una mascota en particular aportando, para ello,
        su identificador correspondiente."""
    respuesta = app.get('/obtener_una_mascota/0')
    assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")
        
def test_obtener_una_mascota_incorrecto():
    """Test 3: intento fallido de obtener los datos de una mascota en particular
        aportando un identificador incorrecto."""
    respuesta = app.get('/obtener_una_mascota/-1')
    assert respuesta.status_code == 404
