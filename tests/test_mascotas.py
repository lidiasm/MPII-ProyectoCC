#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 12:27:19 2019

Clase para testear las funciones de la clase Mascotas.

@author: Lidia Sánchez Mérida
"""
import os
import sys
sys.path.append("src/mascotas")
import mascotas 
import ficha_mascota

lista_mascotas = mascotas.Mascotas()

def test_nueva_mascota_datos_invalidos():
    """Test 1: añadir una mascota con datos inválidos."""
    nueva_mascota = ficha_mascota.FichaMascota("Sussi", None, "Pitbull", None,
        None, None, None, "adoptable", True, False, "False", "Granada", "España")
    assert lista_mascotas.aniadir_nueva_mascota(nueva_mascota) == "Algunos datos de la mascota no son válidos."

def test_nueva_mascota_datos_correctos():
    """Test 2: añadir una nueva mascota con todos sus datos válidos."""
    nueva_mascota = ficha_mascota.FichaMascota("Kitty", "Cat", "Angora", "Medium",
        "Female", "Adult", "Large", "adoptable", True, False, False, "New York", "EEUU")
    assert lista_mascotas.aniadir_nueva_mascota(nueva_mascota) == "Nueva mascota añadida correctamente."
    
def test_conexion_API_Petfinder_fallida():
    """Test 3: intento fallido para conectar con la API Petfinder."""
    assert lista_mascotas.conectar_APIPetfinder("api_key", False) == "Credenciales no válidas."
    
def test_conexion_API_Petfinder_fallida2():
    """Test 4: segundo intento fallido para conectar con la API Petfinder."""
    assert lista_mascotas.conectar_APIPetfinder(None, "api_secret") == "Credenciales no válidas."

def test_conexion_API_Petfinder_exitosa():
    """Test 5: intento exitoso de conectar con la API Petfinder."""
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    assert lista_mascotas.conectar_APIPetfinder(api_key, api_secret) == "Conexión realizada correctamente."

def test_obtener_mascota_sin_indice():
    """Test 6: obtener los datos de una mascota sin pasarle un índice."""
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert lista_mascotas.obtener_datos_mascota(None) == "Identificador de mascota inválido."
    
def test_obtener_mascota_indice_invalido():
    """Test 7: obtener los datos de una mascota con un índice inválido."""
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert lista_mascotas.obtener_datos_mascota(True) == "Identificador de mascota inválido."
    
def test_obtener_mascota_indice_invalido2():
    """Test 8: obtener los datos de una mascota con un índice mayor al número de elementos."""
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert lista_mascotas.obtener_datos_mascota(len(lista_mascotas.mascotas)) == "Identificador de mascota inválido."
    
def test_obtener_mascota_indice_correcto():
    """Test 9: obtener los datos de una mascota con un índice válido."""
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert isinstance(lista_mascotas.obtener_datos_mascota(0), dict) == True
    
def test_descargar_datos_mascotas():
    """Test 10: descargar datos de nuevas mascotas habiendo realizado previamente
    una correcta conexión con la API Petfinder."""
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    lista_mascotas.conectar_APIPetfinder(api_key, api_secret)
    assert type(lista_mascotas.descargar_datos_mascotas() == dict)
    
def test_descargar_datos_mascotas_incorrecto():
    """Test 11: intento fallido de descargar datos de mascotas nuevas."""
    api_key = "hola"
    api_secret = "hola"
    mascotas.Mascotas.api_petifinder = None
    lista_mascotas.conectar_APIPetfinder(api_key, api_secret)
    assert lista_mascotas.descargar_datos_mascotas() == "Error. Primero debe conectarse a la API Petfinder."