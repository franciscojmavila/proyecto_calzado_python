import numpy as np
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

datos = declarative_base()

class Ventas(datos):
    __ventas__ = 'ventas'
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    producto_id = Column(Integer)
    pais = Column(String)
    genero = Column(String)
    talle = Column(String)
    precio = Column(String)

def read_db():
    engine = create_engine('sqlite:///ventas_calzados.db')
    conn = engine.connect()
    query = conn.execute("SELECT * FROM ventas")
    
    paises = []
    generos = []
    talles = []
    precios = []

    for row in query:
        paises.append(row.pais)
        generos.append(row.genero)
        talles.append(row.talle)
        precios.append(float(row.precio.replace('$', '')))
    
    paises = np.array(paises)
    generos = np.array(generos)
    talles = np.array(talles)
    precios = np.array(precios)

    conn.close()
    
    return paises, generos, talles, precios

def obtener_paises_unicos(paises):
    return np.unique(paises)

def obtener_ventas_por_pais(paises_objetivo, paises, precios):
    ventas_por_pais = {}
    for pais in paises_objetivo:
        ventas_por_pais[pais] = np.sum(precios[paises == pais])
    return ventas_por_pais

def obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles):
    calzado_mas_vendido_por_pais = {}
    for pais in paises_objetivo:
        talles_pais = talles[paises == pais]
        unique_talles, counts = np.unique(talles_pais, return_counts=True)
        calzado_mas_vendido_por_pais[pais] = unique_talles[np.argmax(counts)]
    return calzado_mas_vendido_por_pais

def obtener_ventas_por_genero_pais(paises_objetivo, genero_objetivo, paises, generos):
    ventas_por_genero_pais = {}
    for pais in paises_objetivo:
        ventas_por_genero_pais[pais] = np.sum((paises == pais) & (generos == genero_objetivo))
    return ventas_por_genero_pais

if __name__ == "__main__":
    paises, generos, talles, precios = read_db()
    
    print("Países únicos:", obtener_paises_unicos(paises))

    paises_objetivo = ["Canada", "Germany"]
    print("Ventas por país:", obtener_ventas_por_pais(paises_objetivo, paises, precios))

    print("Calzado más vendido por país:", obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles))
    
    genero_objetivo = "Female"
    print("Ventas por género y país:", obtener_ventas_por_genero_pais(paises_objetivo, genero_objetivo, paises, generos))