#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para la clase singleton que se encarga de realizar la conexión con la 
API Petfinder.

@author: Lidia Sánchez Mérida.
"""
import os
import pytest
import sys
sys.path.append("src/mascotas")
sys.path.append("src")
from conexion_api_petfinder import ConexionAPIPetfinder, ApiPetfinderConnectionError, OneInstanceConexionAPIPetfinder

def test_comprobar_clase_singleton():
    """Test 1: comprobamos que la clase se comporte como una clase singleton,
        de la cual solo se pueda instanciar un único objeto."""
    ConexionAPIPetfinder.conectarConPetfinder()
    instancia1 = ConexionAPIPetfinder.getInstance()
    with pytest.raises(OneInstanceConexionAPIPetfinder):
        assert ConexionAPIPetfinder()

def test_comprobar_conexion():
    """Test 2: conexión correcta con la API Petfinder. Para ello se deberán
        declarar las dos variables de entorno correspondientes a las credenciales."""
    conexion = ConexionAPIPetfinder.conectarConPetfinder()
    assert conexion != None
    
def test_comprobar_conexion_incorrecta():
    """Test 3: conexión incorrecta con la API Petfinder causada por credenciales
        incorrectas."""
    os.environ["API_KEY"] = 'hola'
    with pytest.raises(ApiPetfinderConnectionError):
        assert ConexionAPIPetfinder.conectarConPetfinder()