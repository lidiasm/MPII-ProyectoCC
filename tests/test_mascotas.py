#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 12:27:19 2019

Clase para testear las funciones de la clase Mascotas.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("src/mascotas")
import mascotas 
import ficha_mascota

# Test 1: añadir una mascota con datos inválidos.
def test_nueva_mascota_datos_invalidos():
    nueva_mascota = ficha_mascota.FichaMascota("Sussi", None, "Pitbull", None,
        None, None, None, "adoptable", True, False, "False", "Granada", "España")
    lista_mascotas = mascotas.Mascotas()
    assert lista_mascotas.aniadir_nueva_mascota(nueva_mascota) == "Algunos datos de la mascota no son válidos."

# Test 2: añadir una nueva mascota con todos sus datos válidos
def test_nueva_mascota_datos_correctos():
    nueva_mascota = ficha_mascota.FichaMascota("Kitty", "Cat", "Angora", "Medium",
        "Female", "Adult", "Large", "adoptable", True, False, False, "New York", "EEUU")
    lista_mascotas = mascotas.Mascotas()
    assert lista_mascotas.aniadir_nueva_mascota(nueva_mascota) == "Nueva mascota añadida correctamente."
    
# Test 3: intento fallido para conectar con la API Petfinder
def test_conexion_API_Petfinder_fallida():
    lista_mascotas = mascotas.Mascotas()
    assert lista_mascotas.conectar_APIPetfinder("api_key", False) == "Credenciales no válidas."
    
# Test 4: segundo intento fallido para conectar con la API Petfinder
def test_conexion_API_Petfinder_fallida2():
    lista_mascotas = mascotas.Mascotas()
    assert lista_mascotas.conectar_APIPetfinder(None, "api_secret") == "Credenciales no válidas."

# Test 5: intento exitoso de conectar con la API Petfinder
def test_conexion_API_Petfinder_exitosa():
    lista_mascotas = mascotas.Mascotas()
    assert lista_mascotas.conectar_APIPetfinder("api_key", "api_secret") == "Credenciales correctas."

# Test 6: obtener los datos de una mascota sin pasarle un índice
def test_obtener_mascota_sin_indice():
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas = mascotas.Mascotas()
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert lista_mascotas.obtener_datos_mascota(None) == "Número de mascota inválido."
    
# Test 7: obtener los datos de una mascota con un índice inválido
def test_obtener_mascota_indice_invalido():
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas = mascotas.Mascotas()
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert lista_mascotas.obtener_datos_mascota(True) == "Número de mascota inválido."
    
# Test 8: obtener los datos de una mascota con un índice mayor al número de elementos
def test_obtener_mascota_indice_invalido2():
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas = mascotas.Mascotas()
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert lista_mascotas.obtener_datos_mascota(len(lista_mascotas.mascotas)) == "Número de mascota inválido."
    
# Test 9: obtener los datos de una mascota con un índice válido
def test_obtener_mascota_indice_correcto():
    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
    lista_mascotas = mascotas.Mascotas()
    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert isinstance(lista_mascotas.obtener_datos_mascota(0), ficha_mascota.FichaMascota) == True