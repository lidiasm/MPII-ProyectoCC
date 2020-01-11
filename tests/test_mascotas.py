#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase para testear las funciones de la clase Mascotas.

@author: Lidia Sánchez Mérida
"""

import os
import sys
import pytest
sys.path.append("src/mascotas")
import mascotas 
sys.path.append("src")
from excepciones import WrongPetIndex, MaxPetfinderRequestsExceeded, WrongNumberSearchParameters, WrongSearchParametersValues
sys.path.append("src")
from mongodb import MongoDB
"""Creamos la conexión para la base de datos."""
bd = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')
lista_mascotas = mascotas.Mascotas(bd)

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
    nueva_mascota = {'id':'10','nombre': 'Sussi', 'tipo_animal': None, 'raza': 'Pitbull', 
        'tamanio': None, 'genero': None, 'edad': None, 'tipo_pelaje': None, 
        'estado': 'adoptable', 'ninios': True, 'gatos': False, 'perros': 'False', 
        'ciudad': 'Granada', 'pais': 'España'
    }
    mascota_aniadida = lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert type(mascota_aniadida) == dict

def test_aniadir_nueva_mascota_datos_completos():
    """Test 4: añadir una nueva mascota con todos sus datos válidos."""
    nueva_mascota = {'id':'11', 'nombre': 'Sussi', 'tipo_animal': None, 'raza': 'Pitbull', 
        'tamanio': None, 'genero': None, 'edad': None, 'tipo_pelaje': None, 
        'estado': 'adoptable', 'ninios': True, 'gatos': False, 'perros': 'False', 
        'ciudad': 'Granada', 'pais': 'España'
    }
    mascota_aniadida = lista_mascotas.aniadir_nueva_mascota(nueva_mascota)
    assert type(mascota_aniadida) == dict

def test_descargar_datos_mascotas():
    """Test 5: descargar datos de hasta veinte mascotas. Para ello se debe haber
        realizado una conexión con la API Petfinder previamente."""
    try:
        resultado = lista_mascotas.descargar_datos_mascotas()
        assert type(resultado == dict)
    except MaxPetfinderRequestsExceeded:
        print("Número de peticiones máximo excedido.")
    
def test_descargar_datos_mascotas_incorrecto():
    """Test 6: intento fallido de descargar nuevos datos de mascotas. Para ello
        anulamos la conexión realizada con la API Petfinder."""
    lista_mascotas.api_petfinder = None
    try:
        with pytest.raises(WrongPetIndex):
            assert lista_mascotas.descargar_datos_mascotas()
    except MaxPetfinderRequestsExceeded:
        print("Número de peticiones máximo excedido.")

def test_busqueda_incorrecto():
    """Test 7: intento fallido de realizar una consulta por no pasar los términos
        de búsqueda."""
    with pytest.raises(WrongNumberSearchParameters):
        assert lista_mascotas.buscar({})
        
def test_busqueda_incorrecto2():
    """Test 8: intento fallido de realizar una consulta por parámetros de consulta
        no válidos."""
    with pytest.raises(WrongSearchParametersValues):
        assert lista_mascotas.buscar({'tipo_animal':'', 'edad':'', 'genero':'',
            'tamanio':'', 'ninios':'', 'gatos':'', 'perros':''})

def test_busqueda_correcto():
    """Test 9: búsqueda de mascotas satisfactoria."""
    mascotas_coincidentes = lista_mascotas.buscar({'tipo_animal':'cat', 
        'edad':'', 'genero':'', 'tamanio':'', 'ninios':'', 'gatos':'', 'perros':''})
    assert type(mascotas_coincidentes) == dict
    
def test_comparar_variables_busqueda_incorrecto():
    """Test 10: comprobación fallida por no ser dos variables del mismo tipo."""
    with pytest.raises(TypeError):
        assert lista_mascotas.comparar_variables_busqueda(True, "hola")

def test_comparar_variables_busqueda_correcto():
    """Test 11: comprobación de que si no existe valor para uno de los términos 
        de búsqueda no se tenga en cuenta y no afecte, por tanto, a la consulta."""
    assert lista_mascotas.comparar_variables_busqueda(True, "") == True
    
def test_comparar_variables_busqueda_correcto2():
    """Test 12: comprobación de dos variables del mismo tipo pero con distinto
        contenido. Deberá de devolver false."""
    assert lista_mascotas.comparar_variables_busqueda("hola", "adiós") == False
    
def test_comparar_variables_busqueda_correcto3():
    """Test 12: comprobación de dos variables del mismo tipo y con el mismo contenido."""
    assert lista_mascotas.comparar_variables_busqueda("hola", "hola") == True