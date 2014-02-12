# -*- coding: utf-8 -*- 

# Importamos las librerías necesarias:
import os
import sys
import MySQLdb

# Recepción de argumentos (nombre usuario y dominio):
nombre_usuario =(sys.argv[1])
nombre_dominio =(sys.argv[2])

# Conexión base de datos
conexion_bd = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ftpd")
# Consulta existencia de usuario:
cursor = conexion_bd.cursor()
select_username = "select username from usuarios where username='%s';" %nombre_usuario
cursor.execute(select_username)
resp_username = cursor.fetchone()
if resp_username != None:
	print "El nombre de usuario %s ya existe, por favor pruebe con otro" %nombre_usuario
	#exit()
else:
	print "El usuario introducido no esta registrado puede regisrarse como %s" %nombre_usuario
# Consulta existencia de dominio:
select_dominio = "select dominio from usuarios where dominio='%s';" %nombre_dominio
cursor.execute(select_dominio)
resp_dominio = cursor.fetchone()
if resp_dominio != None:
	print "El nombre de dominio %s ya existe, por favor pruebe con otro" %nombre_dominio
	#exit()
else:
	print "El dominio introducido no esta registrado puede registrarlo como %s" %nombre_dominio
