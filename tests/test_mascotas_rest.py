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
import ficha_mascota
import mascotas
import mascotas_rest

app = mascotas_rest.app.test_client()
        
def test_obtener_mascotas_incorrecto():
    """Test 1: intento fallido de obtener los datos de todas las mascotas porque 
    no hay datos almacenados."""
    lista_mascotas = mascotas.Mascotas()
    lista_mascotas.borrar_datos()
    respuesta = app.get('/obtener_mascotas')
    assert (respuesta.status_code == 404)
    
def test_obtener_mascotas():
    """Test 2: obtener los datos de todas las mascotas registradas correctamente."""
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas = mascotas.Mascotas()
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    respuesta = app.get('/obtener_mascotas')
    # Para acceder a los datos de la mascota devueltos -> respuesta.data
    """ Comprobamos el código devuelto y que la cabecera sea JSON que significa
        que se devuelve el diccionario con los datos de la mascota en dicho formato"""
    assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")
    
def test_obtener_una_mascota():
    """"Test 3: obtener los datos de una mascota de forma correcta."""
    respuesta = app.get('/obtener_una_mascota/0')
    assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")

def test_obtener_una_mascota_incorrecto():
    """Test 4: intento fallido de obtener los datos de una mascota determinada."""
    respuesta = app.get('/obtener_una_mascota/-1')
    assert respuesta.status_code == 404
    
def test_conectar_api():
    """Test 5: conexión correcta con la API Petfinder."""
    respuesta = app.get('/conectar_petfinder')
    assert respuesta.status_code == 200
    
def test_descargar_datos_mascotas():
    """Test 6: descarga correcta de datos de nuevas mascotas."""
    respuesta = app.get('/descargar_datos_mascotas')
    if (respuesta.data == "Límite de peticiones superado."): assert (respuesta.status_code == 400)
    else: assert (respuesta.status_code == 200 and respuesta.headers["Content-Type"] == "application/json")
    
def test_descargar_datos_mascotas_incorrecto():
    """Test 7: intento fallido de descargar nuevos datos de mascotas porque
    no se ha realizado una conexión previamente con la API Petfinder."""
    mascotas.Mascotas.api_petifinder = None
    respuesta = app.get('/descargar_datos_mascotas')
    assert respuesta.status_code == 400