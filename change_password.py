# -*- coding: utf-8 -*- 


# Importamos las librerías necesarias:
import MySQLdb
import sys

# Parametros variables de conexión base datos:
maquina = 'localhost'
usuario = 'root'
clave = 'root'
base_datos = 'ftpd'


# Recepción de los argumentos (nombre de usuario, opcion, clave nueva):
nombre_usuario = (sys.argv[1])
opcion = (sys.argv[2])
nueva_clave = (sys.argv[3])


if opcion == "-ftp":
	# Conexión a con la base de datos de MySQL:
	conexion_bd = MySQLdb.connect(host=maquina, user=usuario, passwd=clave, db=base_datos)
	# Consulta existencia de usuario:
	cursor = conexion_bd.cursor()
	coincidencia_usuario = select_username = "select username from usuarios where username='%s';" %nombre_usuario
	cursor.execute(coincidencia_usuario)
	resp_usuario = cursor.fetchone()
	if resp_usuario != None:
		cambiar_clave= "update usuarios set password=PASSWORD('%s') where username='%s';" % (nueva_clave, nombre_usuario)
		cursor.execute(cambiar_clave)
		recarga = "FLUSH PRIVILEGES;"
		cursor.execute(recarga)
		conexion_bd.commit()
		conexion_bd.close()
		print "La contraseña se ha cambiado satisfactoriamente"
	else:
		print "El usuario %s no existe en la base de datos, intentelo de nuevo" % nombre_usuario
		conexion_bd.close()	
		exit()
elif opcion == "-mysql":
	# Conexión a con la base de datos de MySQL:
	conexion_bd = MySQLdb.connect(host=maquina, user=usuario, passwd=clave, db=base_datos)
	cursor = conexion_bd.cursor()
	coincidencia_usuario = select_username = "select user from mysql.user where user='%s';" %nombre_usuario
	cursor.execute(coincidencia_usuario)
	resp_usuario = cursor.fetchone()
	if resp_usuario != None:
		cambiar_clave= "update mysql.user set password=PASSWORD('%s') where user='%s';" % (nueva_clave, nombre_usuario)
		cursor.execute(cambiar_clave)
		recarga = "FLUSH PRIVILEGES;"
		cursor.execute(recarga)
		conexion_bd.commit()
		conexion_bd.close()		
		print "La contraseña se ha cambiado satisfactoriamente"
	else:
		print "El usuario %s no existe en la base de datos, intentelo de nuevo" % nombre_usuario
		conexion_bd.close()
		exit()
else:
		print "la opción intorudcida no es correcta"
