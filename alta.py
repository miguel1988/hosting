# -*- coding: utf-8 -*- 

# Importamos las librerías necesarias:
import os
import sys
import MySQLdb
import string

# Parametros variables de conexión base datos:
maquina = 'localhost'
usuario = 'root'
clave = 'root'
based_datos = 'ftpd'

# Recepción de argumentos (nombre usuario y dominio):
nombre_usuario =(sys.argv[1])
nombre_dominio =(sys.argv[2])

# Conexión a con la base de datos de MySQL:
conexion_bd = MySQLdb.connect(host=maquina, user=usuario, passwd=clave, db=base_datos)

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

# Generamos una contraseña de 8 digitos para el nuevo usuario:
from random import choice
def GenPasswd(n):
    return ''.join([choice(string.letters + string.digits) for i in range(n)])
contrasenia_bd = GenPasswd(8)
print "%s tu contraseña es %s" % (nombre_usuario, contrasenia_bd)

# Creamos la base de datos y le otorgamos los privilegios al nuevo usuario:
crea_db = "create database %s" %nombre_usuario
cursor.execute(crea_db)
otorgar_privilegios = "grant all privileges on %s.* to "% (nombre_usuario)+ " %s@localhost"% (nombre_usuario)+ " identified by "+"'%s'" % (contrasenia_bd)+";"
cursor.execute(otorgar_privilegios)
recargar_bd = "flush privileges;"
conexion_bd.commit()

# Creamos el directorio del nuevo usuario:
os.system("mkdir /srv/www/%s" %nombre_usuario)
os.system("cp index.html /srv/www/%s" %nombre_usuario/index.html)


# Editamos el fichero del virtualhost para el nuevo usuario:
vh=open("p_virtualhost","r")
texto_vh=vh.read()
vh.close()
texto_vh=texto_vh.replace("@serv_ad@","@%s.org"% nombre_dominio)
texto_vh=texto_vh.replace("@serv_na@","www.%s.org" % nombre_dominio)
texto_vh=texto_vh.replace("@doc_root@","%s"% nombre_dominio)
vh=open("/etc/apache2/sites-available/%s" % nombre_dominio,"w")
vh.write(texto_vh)
vh.close()


pma=open("p_myphpadmin","r")
texto_pma=pma.read()
pma.close()
texto_pma=texto_pma.replace"@serv_ad@","@%s.org" % nombre_dominio)
texto_pma=texto_pma.replace("@serv_na@","%s"% nombre_dominio)
pma=open("/etc/apache2/sites-available/phpmyadmin%s" % nombre_dominio,"w")
pma.write(texto_pma)
pma.close()
os.system("a2ensite phpmyadmin%s >/dev/null" % nombre_dominio)
os.system("a2ensite %s >/dev/null" % nombre_dominio)
os.system("service apache2 restart >/dev/null ")
