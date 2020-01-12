#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para comprobar el funcionamiento de los métodos que generan las estadísticas
de la clase Estadísticas.

@author: Lidia Sánchez Mérida
"""
import os
import pytest
import sys
sys.path.append("src")
from excepciones import PetsNotFound
sys.path.append("src/estadisticas")
import estadisticas

from mongodb import MongoDB
"""Creamos la conexión para la base de datos."""
bd = MongoDB(os.environ.get("MONGODB_URI"), 'PetfinderBD', 'estadisticas')
estd = estadisticas.Estadisticas(bd)

def test_generar_estadistica_ninios_incorrecto():
    """Test 1: intento fallido de generar el primer tipo de informe estadístico
        puesto que no hay mascotas disponibles para realizar el análisis."""
    with pytest.raises(PetsNotFound):
        assert estd.generar_estadistica_ninios({})
        
def test_generar_estadistica_ninios_incorrecto2():
    """Test 2: intento fallido de generar el primer tipo de informe estadístico
        por no pasar un diccionario."""
    with pytest.raises(PetsNotFound):
        assert estd.generar_estadistica_ninios(True)
        
def test_generar_estadistica_ninios_correcto():
    """Test 3: generar el primer tipo de informe acerca de las mascotas que 
        se relacionan bien con niños."""
    mascota1 = {'id':'0', 'nombre':'Kira', 'tipo_animal':'cat', 'raza':'DNV',
                'tamanio':'small', 'genero':'female', 'edad':'young', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'no', 'perros':'yes', 'ciudad':'Málaga', 'pais':'España'}
    mascota2 = {'id':'1', 'nombre':'Alem', 'tipo_animal':'dog', 'raza':'bulldog',
                'tamanio':'small', 'genero':'male', 'edad':'DNV', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Málaga', 'pais':'España'}
    mascota3 = {'id':'2', 'nombre':'Kobu', 'tipo_animal':'dog', 'raza':'Siberian Husky',
                'tamanio':'medium', 'genero':'male', 'edad':'adult', 'tipo_pelaje':'medium',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Granada', 'pais':'España'}
    mascota4 = {'id':'3', 'nombre':'Brayan', 'tipo_animal':'cat', 'raza':'DNV',
                'tamanio':'DNV', 'genero':'male', 'edad':'adult', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'no', 'gatos':'no', 'perros':'yes', 'ciudad':'Sevilla', 'pais':'España'}
    mascota5 = {'id':'4', 'nombre':'Nora', 'tipo_animal':'dog', 'raza':'DNV',
                'tamanio':'medium', 'genero':'female', 'edad':'senior', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Granada', 'pais':'España'}
    mascotas = {'0':mascota1, '1':mascota2, '2':mascota3, '3':mascota4, '4':mascota5}
    estadistica = estd.generar_estadistica_ninios(mascotas)
    assert type(estadistica) == dict
    
def test_generar_estadistica_razas_perro_incorrecto():
    """Test 4: intento fallido de generar el segundo tipo de informe estadístico
        puesto que no hay mascotas disponibles para realizar el análisis."""
    with pytest.raises(PetsNotFound):
        assert estd.generar_estadistica_razas_perro({})
        
def test_generar_estadistica_razas_perro_incorrecto2():
    """Test 5: intento fallido de generar el segundo tipo de informe estadístico
        por no pasar un diccionario."""
    with pytest.raises(PetsNotFound):
        assert estd.generar_estadistica_razas_perro(True)
        
def test_generar_estadistica_razas_perro_correcto():
    """Test 6: generar el segundo tipo de informe acerca de las razas de perro
        más sociables con niños y con otro tipo de mascotas."""
    mascota1 = {'id':'0', 'nombre':'Kira', 'tipo_animal':'dog', 'raza':'bulldog',
                'tamanio':'small', 'genero':'female', 'edad':'young', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'no', 'perros':'yes', 'ciudad':'Málaga', 'pais':'España'}
    mascota2 = {'id':'1', 'nombre':'Alem', 'tipo_animal':'dog', 'raza':'bulldog',
                'tamanio':'small', 'genero':'male', 'edad':'DNV', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Málaga', 'pais':'España'}
    mascota3 = {'id':'2', 'nombre':'Kobu', 'tipo_animal':'dog', 'raza':'Siberian Husky',
                'tamanio':'medium', 'genero':'male', 'edad':'adult', 'tipo_pelaje':'medium',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Granada', 'pais':'España'}
    mascota4 = {'id':'3', 'nombre':'Brayan', 'tipo_animal':'dog', 'raza':'Labrador',
                'tamanio':'DNV', 'genero':'male', 'edad':'adult', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'no', 'gatos':'no', 'perros':'yes', 'ciudad':'Sevilla', 'pais':'España'}
    mascota5 = {'id':'4', 'nombre':'Nora', 'tipo_animal':'dog', 'raza':'Labrador',
                'tamanio':'medium', 'genero':'female', 'edad':'senior', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'no', 'perros':'yes', 'ciudad':'Granada', 'pais':'España'}
    mascotas = {'0':mascota1, '1':mascota2, '2':mascota3, '3':mascota4, '4':mascota5}
    estadistica = estd.generar_estadistica_razas_perro(mascotas)
    assert type(estadistica) == dict

def test_generar_estadistica_tipos_mascotas_incorrecto():
    """Test 7: intento fallido de generar el tercer tipo de informe estadístico
        por no pasarle como argumento un diccionario con mascotas."""
    with pytest.raises(PetsNotFound):
        assert estd.generar_estadistica_tipos_mascotas({})
        
def test_generar_estadistica_tipos_mascotas_incorrecto2():
    """Test 8: intento fallido de generar el tercer tipo de informe estadístico
        por no pasarle como argumento un diccionario."""
    with pytest.raises(PetsNotFound):
        assert estd.generar_estadistica_tipos_mascotas("mascota")
        
def test_generar_estadistica_tipos_mascotas_correcto():
    """Test 9: generar el tercer tipo de informe acerca de las mascotas disponibles
        para la adopción así como su respectivo número de ejemplares."""
    mascota1 = {'id':'0', 'nombre':'Kira', 'tipo_animal':'cat', 'raza':'DNV',
                'tamanio':'small', 'genero':'female', 'edad':'young', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'no', 'perros':'yes', 'ciudad':'Málaga', 'pais':'España'}
    mascota2 = {'id':'1', 'nombre':'Alem', 'tipo_animal':'dog', 'raza':'bulldog',
                'tamanio':'small', 'genero':'male', 'edad':'DNV', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Málaga', 'pais':'España'}
    mascota3 = {'id':'2', 'nombre':'Kobu', 'tipo_animal':'dog', 'raza':'Siberian Husky',
                'tamanio':'medium', 'genero':'male', 'edad':'adult', 'tipo_pelaje':'medium',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Granada', 'pais':'España'}
    mascota4 = {'id':'3', 'nombre':'Brayan', 'tipo_animal':'cat', 'raza':'DNV',
                'tamanio':'DNV', 'genero':'male', 'edad':'adult', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'no', 'gatos':'no', 'perros':'yes', 'ciudad':'Sevilla', 'pais':'España'}
    mascota5 = {'id':'4', 'nombre':'Nora', 'tipo_animal':'dog', 'raza':'DNV',
                'tamanio':'medium', 'genero':'female', 'edad':'senior', 'tipo_pelaje':'DNV',
                'estado':'adoptable', 'ninios':'yes', 'gatos':'yes', 'perros':'yes', 'ciudad':'Granada', 'pais':'España'}
    mascotas = {'0':mascota1, '1':mascota2, '2':mascota3, '3':mascota4, '4':mascota5}
    estadistica = estd.generar_estadistica_tipos_mascotas(mascotas)
    assert type(estadistica) == dict
    
def test_obtener_estadistica_tipos_mascotas():
    """Test 10: obtener el informe estadístico acerca de las diferentes mascotas
        que se pueden adoptar de la base de datos."""
    informe = estd.obtener_estadistica_tipos_mascotas()
    assert type(informe) == dict
    
def test_obtener_estadistica_ninios():
    """Test 11: obtener el informe estadístico acerca de la relación entre los
        niños y las mascotas."""
    informe = estd.obtener_estadistica_ninios()
    assert type(informe) == dict
    
def test_obtener_estadistica_razas_perro():
    """Test 12: obtener el informe estadístico acerca de cuán sociable es cada
        raza de perro de la que haya datos."""
    informe = estd.obtener_estadistica_razas_perro()
    assert type(informe) == dict