# ­*­ coding: utf­8 ­*­
import os
import sys
import MySQLdb


# Parametros variables de conexión base datos:
maquina = 'localhost'
usuario = 'root'
clave = 'root'
base_datos = 'ftpd'


# Recepción de argumento (dominio):
nombre_dominio=(sys.argv[1])


# Conexión a con la base de datos de MySQL:
conexion_bd = MySQLdb.connect(host=maquina, user=usuario, passwd=clave, db=base_datos)


# Consulta existencia del dominio en de la base de datos:
cursor = conexion_bd.cursor()
select_usuario = "select username from usuarios where dominio='%s';" %nombre_dominio
cursor.execute(select_usuario)
resp_usuario = cursor.fetchone()
if resp_usuario == None:
        print "El dominio introducido no existe, por favor vuelva a intentarlo"
        exit()
else:
        print "Se procederá a borrar la cuenta perteneciente al dominio%s" %nombre_dominio

	resp_usuario2 = str(resp_usuario)
	nombre_my = 'my'+resp_usuario2
	respuesta_usuario = resp_usuario[0]


        # Borramos los sitios en Apache del usuario y reiniciamos el servicio:
        os.system("a2dissite %s > /dev/null" % nombre_dominio)
        os.system("a2dissite mysql.%s > /dev/null" % nombre_dominio)
        os.system("rm -r -f /etc/apache2/sites-available/www.%s"%nombre_dominio)
        os.system("rm -r -f /etc/apache2/sites-available/mysql.%s"%nombre_dominio)
        os.system("service apache2 restart>/dev/null")


        # Eliminamos los registros de DNS:
        os.system("rm -r -f /etc/bind/db.%s" %nombre_dominio)
        #os.system("sed '/zone " + '"%s"'% nombre_dominio + "/,/};/d' /etc/bind/named.conf.local > portapapeles")
        #os.system("mv portapapales /etc/bind/named.conf.local")
        os.system("sed '/zone " + '"%s"'% nombre_dominio + "/,/};/d' /etc/bind/named.conf.local > porta")
        os.system("mv porta /etc/bind/named.conf.local")


        # Eliminamos el usuario mysql y su base de datos:
        drop_bd=" drop database %s;" % respuesta_usuario
        cursor.execute(drop_bd)
        revocar=" revoke all on *.* from my%s@localhost;" % respuesta_usuario
        cursor.execute(revocar)
        drop_user = " drop user my%s@localhost" % respuesta_usuario
        cursor.execute(drop_user)
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        conexion_bd.commit()

        # Eliminamos el usuario virtual:
        baja_usuario = "delete from usuarios where dominio='%s';" %nombre_dominio
        cursor.execute(baja_usuario)
        basereload = "FLUSH PRIVILEGES;"
        cursor.execute(basereload)
        conexion_bd.commit()
        conexion_bd.close()


        # Eliminamos el directorio del usuario.
        os.system("rm -r -f /srv/www/%s" %nombre_dominio)

        # Mostramos un mensaje informativo de que la operación se ha realizado con exito:
        print "El usuario %s y su dominio %s han sido borrado con exito" %(respuesta_usuario, nombre_dominio)

