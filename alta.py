# -*- coding: utf-8 -*- 

# Importamos las librerías necesarias:
import os
import sys
import MySQLdb

# Recepción de argumentos (nombre usuario y dominio):
nombre_usuario = sys.argv[1]
nombre_dominio = sys.arg[2]

# Conexión base de datos
conexion_bd = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftpd")
cursor = base.cursor()

