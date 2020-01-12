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
from datetime import datetime

"""Conexiones a la colección de mascotas y a la de estadísticas."""
conexionMascotas = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'mascotas')
conexionEstadisticas = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'estadisticas')

def test_vaciar_coleccion_correcto():
    """Test 1: borramos los registros de la colección para poder realizar los
        sucesivos tests y probar la función al mismo tiempo."""
    resultado = conexionMascotas.vaciar_coleccion()
    assert resultado.acknowledged == True

def test_vaciar_coleccion_incorrecto():
    """Test 2: intento fallido de borrar los registros de una colección puesto
        que ya está vacía."""
    with pytest.raises(EmptyCollection):
        conexionMascotas.vaciar_coleccion()
        
def test_get_coleccion_incorrecto():
    """Test 3: intento fallido de obtener todos los elementos de la colección
        debido a que está vacía."""
    with pytest.raises(EmptyCollection):
        assert conexionMascotas.get_coleccion()
        
def test_get_coleccion_especifica_incorrecto():
    """Test 4: intento fallido de obtener los elementos de un identificador
        determinado debido a que la colección está vacía."""
    with pytest.raises(EmptyCollection):
        assert conexionMascotas.get_coleccion_especifica('id', '1')

def test_insertar_elemento_correcto():
    """Test 5: insertar datos de una mascota en la base de datos."""
    nueva_mascota = {'id': '0', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small', 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'} 
    id_nueva_mascota_bd = conexionMascotas.insertar_elemento(nueva_mascota) 
    assert id_nueva_mascota_bd != None

def test_insertar_elemento_incorrecto():
    """Test 6: intento fallido de insertar una nueva mascota puesto que alguno
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
    """Test 7: intento fallido de insertar una nueva mascota debido a que no
        existen los datos de la nueva mascota."""
    """Para ello modificamos la conexión a la base de datos para que sea incorrecta."""
    with pytest.raises(NewItemNotFound):
        assert conexionMascotas.insertar_elemento({})

def test_get_elemento_correcto():
    """Test 8: obtenemos el elemento préviamente insertado a través de su identificador."""
    nueva_mascota = {'id': '2', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small'
        , 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'}
    conexionMascotas.insertar_elemento(nueva_mascota)
    mascota_insertada = conexionMascotas.get_elemento('id', '2')
    assert type(mascota_insertada) == dict
    
def test_get_elemento_incorrecto():
    """Test 9: intento fallido de obtener un elemento debido a que el identificador
        no existe."""
    assert conexionMascotas.get_elemento('id', '-1') == None
    
def test_get_coleccion_especifica_correcto():
    """Test 10: obtenemos los documentos asociados al informe relacionado con la
        relación entre niños y mascotas de forma satisfactoria. Para ello añadimos
        unos cuantos."""
    informe1 = {'id':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")),
            'id_informe':'ninios', 'informe':{'dog':'75%', 'cat':'55%'}}
    informe2 = {'id':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")),
            'id_informe':'ninios', 'informe':{'dog':'69%', 'cat':'40%'}}
    informe3 = {'id':str(datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")),
            'id_informe':'ninios', 'informe':{'dog':'72%', 'cat':'65%'}}
    conexionEstadisticas.insertar_elemento(informe1)
    conexionEstadisticas.insertar_elemento(informe2)
    conexionEstadisticas.insertar_elemento(informe3)
    informes = conexionEstadisticas.get_coleccion_especifica('id_informe', 'ninios')
    assert type(informes) == dict
        
def test_get_coleccion_correcto():
    """Test 10: obtener la colección completa. Para ello añadiremos dos elementos."""
    nueva_mascota = {'id': '4', 'nombre': 'Simba', 'tipo_animal': 'cat', 
        'raza': 'angora', 'tamanio': 'small'
        , 'genero': 'male', 'edad': 'young',
        'tipo_pelaje': 'short', 'estado': 'adoptable', 'ninios': 'no', 
        'gatos': 'yes', 'perros': 'no', 'ciudad': 'Granada', 'pais': 'España'}
    conexionMascotas.insertar_elemento(nueva_mascota)
    nueva_mascota2 = {'id': '5', 'nombre': 'Balto', 'tipo_animal': 'dog', 
        'raza': 'husky', 'tamanio': 'medium'
        , 'genero': 'male', 'edad': 'adult',
        'tipo_pelaje': 'medium', 'estado': 'adoptable', 'ninios': 'yes', 
        'gatos': 'yes', 'perros': 'yes', 'ciudad': 'Malaga', 'pais': 'España'}
    conexionMascotas.insertar_elemento(nueva_mascota2)
    assert type(conexionMascotas.get_coleccion()) == dict 

def test_eliminar_elemento_correcto():
    """Test 11: eliminar un elemento de la colección proporcionando, para ello,
        su identificador."""
    resultado = conexionMascotas.eliminar_elemento('id', '0')
    assert resultado.acknowledged == True 
    
def test_eliminar_elemento_incorrecto():
    """Test 12: intento fallido de eliminar un elemento de la colección por 
        especificar un identificador incorrecto."""
    with pytest.raises(ItemNotFound):
        conexionMascotas.eliminar_elemento('id', '-1')
