#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para verificar el comportamiento de las operaciones definidas para la base
de datos.

@author: Lidia Sánchez Mérida.
"""
import sys
sys.path.append("src")
import os
import pytest
from excepciones import CollectionNotFound, NewItemNotFound, ItemNotFound, EmptyCollection
from mongodb import MongoDB

"""Realizamos la conexión con la base de datos Petfinder, y en particular, con
la colección mascotas."""
conexionBD = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')

def test_vaciar_coleccion_correcto():
    """Test 1: borramos los registros de la colección para poder realizar los
        sucesivos tests y probar la función al mismo tiempo."""
    resultado = conexionBD.vaciar_coleccion()
    assert resultado.acknowledged == True

def test_vaciar_coleccion_incorrecto():
    """Test 2: intento fallido de borrar los registros de una colección puesto
        que ya está vacía."""
    with pytest.raises(EmptyCollection):
        conexionBD.vaciar_coleccion()
        
def test_get_coleccion_incorrecto():
    """Test 3: intento fallido de obtener todos los elementos de la colección
        debido a que está vacía."""
    with pytest.raises(EmptyCollection):
        assert conexionBD.get_coleccion()

def test_insertar_elemento_correcto():
    """Test 4: insertar datos de una mascota en la base de datos."""
    nueva_mascota = {'id': '0', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small', 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'} 
    id_nueva_mascota_bd = conexionBD.insertar_elemento(nueva_mascota) 
    assert id_nueva_mascota_bd != None

def test_insertar_elemento_incorrecto():
    """Test 5: intento fallido de insertar una nueva mascota puesto que alguno
        de los parámetros para establecer la conexión no son correctos."""
    nueva_mascota = {'id': '1', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small'
        , 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'} 
    """Para ello modificamos la conexión a la base de datos para que sea incorrecta."""
    conexion_incorrecta = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')
    conexion_incorrecta.coleccion = None
    with pytest.raises(CollectionNotFound):
        assert conexion_incorrecta.insertar_elemento(nueva_mascota)

def test_insertar_elemento_incorrecto2():
    """Test 6: intento fallido de insertar una nueva mascota debido a que no
        existen los datos de la nueva mascota."""
    """Para ello modificamos la conexión a la base de datos para que sea incorrecta."""
    with pytest.raises(NewItemNotFound):
        assert conexionBD.insertar_elemento({})

def test_get_elemento_correcto():
    """Test 7: obtenemos el elemento préviamente insertado a través de su identificador."""
    nueva_mascota = {'id': '2', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small'
        , 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'}
    conexionBD.insertar_elemento(nueva_mascota)
    mascota_insertada = conexionBD.get_elemento('id', '2')
    assert type(mascota_insertada) == dict
    
def test_get_elemento_incorrecto():
    """Test 8: intento fallido de obtener un elemento debido a que el identificador
        no existe."""
    assert conexionBD.get_elemento('id', '-1') == None
        
def test_get_coleccion_correcto():
    """Test 9: obtener la colección completa. Para ello añadiremos dos elementos."""
    nueva_mascota = {'id': '4', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small'
        , 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'}
    conexionBD.insertar_elemento(nueva_mascota)
    nueva_mascota2 = {'id': '5', 'nombre': 'Balto', 'tipo_animal': 'dog', 
        'raza': 'husky', 'tamanio': 'medium'
        , 'genero': 'male', 'edad': 'adult',
        'tipo_pelaje': 'medium', 'estado': 'adoptable', 'ninios': 'yes', 
        'gatos': 'yes', 'perros': 'yes', 'ciudad': 'Malaga', 'pais': 'España'}
    conexionBD.insertar_elemento(nueva_mascota2)
    assert type(conexionBD.get_coleccion()) == dict 

def test_eliminar_elemento_correcto():
    """Test 10: eliminar un elemento de la colección proporcionando, para ello,
        su identificador."""
    resultado = conexionBD.eliminar_elemento('id', '0')
    assert resultado.acknowledged == True 
    
def test_eliminar_elemento_incorrecto():
    """Test 11: intento fallido de eliminar un elemento de la colección por 
        especificar un identificador incorrecto."""
    with pytest.raises(ItemNotFound):
        conexionBD.eliminar_elemento('id', '-1')
