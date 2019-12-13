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
import pytest

lista_mascotas = mascotas.Mascotas()

def test_comprobar_variable_correcta():
    """Test 1: comprobación del tipo y el valor de una variable."""
    variable = True
    resultado = lista_mascotas.variable_correcta(variable, bool)
    assert resultado == True
    
def test_comprobar_variable_incorrecta():
    """Test 2: comprobación del tipo y el valor de una variable de forma incorrecta.
        El objetivo es comprobar que realmente el método reconoce que la variable
        es de tipo booleano mientras le decimos que es una cadena."""
    variable = True
    resultado = lista_mascotas.variable_correcta(variable, str)
    assert resultado == False

def test_aniadir_nueva_mascota_datos_incompletos():
    """Test 3: añadir una nueva mascota con datos inválidos."""
    nueva_mascota = ficha_mascota.FichaMascota("Sussi", None, "Pitbull", None,
        None, None, None, "adoptable", True, False, "False", "Granada", "España")
    mascota_aniadida = lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert type(mascota_aniadida) == dict

def test_aniadir_nueva_mascota_datos_completos():
    """Test 4: añadir una nueva mascota con todos sus datos válidos."""
    nueva_mascota = ficha_mascota.FichaMascota("Kitty", "Cat", "Angora", "Medium",
        "Female", "Adult", "Large", "adoptable", True, False, False, "New York", "EEUU")
    mascota_aniadida = lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert type(mascota_aniadida) == dict

def test_descargar_datos_mascotas():
    """Test 5: descargar datos de hasta veinte mascotas. Para ello se debe haber
        realizado una conexión con la API Petfinder previamente."""
    resultado = lista_mascotas.descargar_datos_mascotas()
    if (resultado != "Número de peticiones máximo excedido."):
        assert type(resultado == dict)
    
def test_descargar_datos_mascotas_incorrecto():
    """Test 6: intento fallido de descargar nuevos datos de mascotas. Para ello
        anulamos la conexión realizada con la API Petfinder."""
    lista_mascotas.api_petfinder = None
    with pytest.raises(ConnectionError):
        assert lista_mascotas.descargar_datos_mascotas()



#def test_obtener_mascota_sin_indice():
#    """Test 1: obtener los datos de una mascota sin pasarle un índice."""
#    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
#        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
#    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
#    assert lista_mascotas.obtener_datos_mascota(None) == "Identificador de mascota inválido."
#    
#def test_obtener_mascota_indice_invalido():
#    """Test 2: obtener los datos de una mascota con un índice inválido."""
#    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
#        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
#    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
#    assert lista_mascotas.obtener_datos_mascota(True) == "Identificador de mascota inválido."
#    
#def test_obtener_mascota_indice_invalido2():
#    """Test 3: obtener los datos de una mascota con un índice mayor al número de elementos."""
#    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
#        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
#    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
#    assert lista_mascotas.obtener_datos_mascota(len(lista_mascotas.mascotas)) == "Identificador de mascota inválido."
#    
#def test_obtener_mascota_indice_correcto():
#    """Test 4: obtener los datos de una mascota con un índice válido."""
#    nueva_mascota = ficha_mascota.FichaMascota("Kate", "Cat", "Pitbull", None,
#        None, None, None, "adoptable", True, False, True, "Atlanta", "EEUU")
#    lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
#    assert isinstance(lista_mascotas.obtener_datos_mascota(0), dict) == True
#    
