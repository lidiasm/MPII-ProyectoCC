#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para la clase Búsqueda.

@author: Lidia Sánchez Mérida.
"""
import sys
sys.path.append("src/busqueda")
sys.path.append("src/")
import busqueda 
import pytest
from excepciones import WrongNumberSearchParameters, PetsNotFound, WrongSearchParametersValues

busquedas = busqueda.Busqueda()

def test_comparar_variables_busqueda_incorrecto():
    """Test 1: comparación entre dos variables de diferente tipo para comprobar
        el lanzamiento de la excepción."""
    with pytest.raises(TypeError):
        assert busquedas.comparar_variables_busqueda(1, 'hola')

def test_comparar_variables_busqueda_incorrecto2():
    """Test 2: comparación entre dos variables del mismo tipo pero con diferente
        valor."""
    assert busquedas.comparar_variables_busqueda('hola', 'holaa') == False

def test_comparar_variables_busqueda_incorrecto3():
    """Test 3: comparación entre dos variables en la que la segunda está vacía.
        Con este test queremos comprobar que si algún término de búsqueda está
        sin completar, no interfiera en la consulta.
    """
    assert busquedas.comparar_variables_busqueda('hola', '') == True

def test_comparar_variables_busqueda_correcto():
    """Test 4: comparación entre dos variales del mismo tipo y con el mismo valor."""
    assert busquedas.comparar_variables_busqueda('hola', 'hola') == True

def test_busqueda_incorrecto():
    """Test 5: búsqueda con insuficientes parámetros."""
    with pytest.raises(WrongNumberSearchParameters):
        assert busquedas.buscar({}, {})
        
def test_busqueda_incorrecto2():
    """Test 6: búsqueda con los siete parámetros de consulta vacíos."""
    with pytest.raises(WrongSearchParametersValues):
        assert busquedas.buscar({}, {'tipo_animal':'', 'edad':'', 'genero':'',
            'tamanio':'', 'ninios':'', 'gatos':'', 'perros':''})
    
def test_busqueda_incorrecto3():
    """Test 7: búsqueda con los siete parámetros pero sin mascotas."""
    with pytest.raises(PetsNotFound):
        assert busquedas.buscar({}, {'tipo_animal':'a', 'edad':'b', 'genero':'c',
            'tamanio':'d', 'ninios':True, 'gatos':False, 'perros':True})

def test_busqueda_correcto():
    """Test 8: búsqueda con los siete parámetros, dejando algunos sin completar,
        y con las mascotas."""
    mascotas = {}
    mascotas[0] = {'tipo_animal':'dog', 'edad':'senior', 'genero':'man',
            'tamanio':'big', 'ninios':False, 'gatos':True, 'perros':True}
    mascotas[1] = {'tipo_animal':'cat', 'edad':'young', 'genero':'female',
            'tamanio':'small', 'ninios':False, 'gatos':True, 'perros':False}
    mascotas_coincidentes = busquedas.buscar(mascotas, {'tipo_animal':'cat', 
        'edad':'young', 'genero':'', 'tamanio':'', 'ninios':False, 
        'gatos':True, 'perros':False})
    assert type(mascotas_coincidentes) == dict   