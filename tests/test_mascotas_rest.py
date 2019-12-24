#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el servicio REST que accede a los métodos de obtener_mascota y 
obtener_mascotas de la clase Mascota.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src/mascotas")
import mascotas_rest
app = mascotas_rest.app.test_client()
sys.path.append("src")
import os
import mongodb
import mascotas
"""Creamos un objeto de la base de datos y lo configuramos."""
bd = mongodb.MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')
"""Objeto que nos conecta con la clase Mascotas."""
m = mascotas.Mascotas(bd)
        
def test_obtener_mascotas():
    """Test 1: recopilar los datos de mascotas descargados por el microservicio
        de Celery para mostrarlos."""
    respuesta = app.get('/obtener_mascotas')
    if (respuesta.status_code == 400):
        """No existen datos de mascotas aún."""
        assert (respuesta.status_code == 400)
    else:
        # Para acceder a los datos de la mascota devueltos -> respuesta.data
        """ Comprobamos el código devuelto y que la cabecera sea JSON que significa
            que se devuelve el diccionario con los datos de la mascota en dicho formato"""
        assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")        
        
def test_obtener_una_mascota():
    """Test 2: obtener los datos de una mascota en particular aportando, para ello,
        su identificador correspondiente. Para ello se inserta una mascota préviamente
        de modo que conozcamos su identificado válido."""
    nueva_mascota = {'id':'2', 'nombre':'Nala', 'tipo_animal':'cat', 'raza':None,
     'tamanio':'medium', 'genero':'female', 'edad':'adult', 'tipo_pelaje':None,
     'estado':'adoptable', 'ninios':True, 'gatos':True, 'perros':True,
     'ciudad':'Granada', 'pais':'España'}
    m.aniadir_nueva_mascota(nueva_mascota)
    respuesta = app.get('/obtener_una_mascota/2')
    if (respuesta.status_code == 400):
        """No existen datos de mascotas aún."""
        assert (respuesta.status_code == 400)
    else:
        assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")
        
def test_obtener_una_mascota_incorrecto():
    """Test 3: intento fallido de obtener los datos de una mascota en particular
        aportando un identificador incorrecto."""
    respuesta = app.get('/obtener_una_mascota/-1')
    if (respuesta.status_code == 400):
        """No existen datos de mascotas aún."""
        assert (respuesta.status_code == 400)
    else:
        assert respuesta.status_code == 404
