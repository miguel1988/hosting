# -*- coding: utf-8 -*- 


# Importamos las librerías necesarias:
import MySQLdb



# Parametros variables de conexión base datos:
maquina = 'localhost'
usuario = 'root'
clave = 'root'
base_datos = 'ftpd'


# Recepción de argumentos(dominio):
nombre_usuario = (sys.argv[1])
nueva_clave = (sys.argv[1])


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
	conexion_bd.close()
	print "El usuario %s no existe en la base de datos, intentelo de nuevo" % nombre_usuario
	
