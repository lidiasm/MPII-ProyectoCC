#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el microservicio REST asociado a la clase Busqueda. Mediante él
podremos realizar búsquedas de mascotas en base a preferencias.

@author: Lidia Sánchez Mérida.
"""
import sys
sys.path.append("src/busqueda")
import busqueda_rest

app = busqueda_rest.app.test_client()
        
#def test_buscar_mascotas_correcto():
#    """Test 1: búsqueda de mascotas en función de unos parámetros."""
#    respuesta = app.get('/buscar_mascotas?tipo_animal=cat')
#    if (respuesta.status_code == 412):
#        """Causas: 1) Número de peticiones a la API Petfinder superado.
#                   2) No hay mascotas registradas sobre las que realizar la búsqueda."""
#        assert (respuesta.status_code == 412)
#    else:
#        assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")        
#       
def test_buscar_mascotas_incorrecto():
    """Test 2: intento fallido de búsqueda de mascotas por falta de parámetros."""
    respuesta = app.get('/buscar_mascotas')
    if (respuesta.status_code == 412):
        """Causas: 1) Número de peticiones a la API Petfinder superado.
                   2) No hay mascotas registradas sobre las que realizar la búsqueda."""
        assert (respuesta.status_code == 412)
    else:
        assert (respuesta.status_code == 400)        

def test_buscar_mascotas_incorrecto2():
    """Test 3: intento fallido de búsqueda de mascotas por falta de valores válidos
        en los parámetros."""
    respuesta = app.get('/buscar_mascotas?tipo_pelaje=')
    if (respuesta.status_code == 412):
        """Causas: 1) Número de peticiones a la API Petfinder superado.
                   2) No hay mascotas registradas sobre las que realizar la búsqueda."""
        assert (respuesta.status_code == 412)
    else:
        assert (respuesta.status_code == 400)