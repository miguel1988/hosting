# -*- coding: utf-8 -*- 

import os
import sys
import MySQLdb

nombre_usuario=(sys.argv[1])
nombre_subdominio=(sys.argv[2])

maquina = 'localhost'
usuario = 'root'
clave = 'root'
base_datos = 'ftpd'

conexion_bd = MySQLdb.connect(host=maquina, user=usuario, passwd=clave, db=base_datos)
cursor = conexion_bd.cursor()
select_dominio = "select dominio from usuarios where username='%s';" % (nombre_usuario)
cursor.execute(select_dominio)
resp_dominio = cursor.fetchone()
if resp_dominio == None:
	print "El nombre de usuario %s no existe, por favor pruebe con otro" %nombre_usuario
	exit()
else:
    resp2=str(resp_dominio)
    resp3=resp2[2:-3]      
    os.system("mkdir /srv/www/%s/subdominio" % (resp3))
    os.system("mkdir /srv/www/%s/subdominio/%s" % (resp3,nombre_subdominio))
    os.system("cp -f index.html /srv/www/%s/subdominio/%s/index.html" %(resp3,nombre_subdominio))
    
    subdo=open("p_virtualhost","r")
    linea=subdo.read()
    subdo.close()
	
    resp2=str(resp_dominio)
    resp3=resp2[2:-3]    

    linea=linea.replace("@serv_na@","%s.%s" % (nombre_subdominio,resp3))
    linea=linea.replace("@doc_root@","%s/subdominio/%s"% (resp3,nombre_subdominio))
    subdo=open("/etc/apache2/sites-available/subdominio.%s" % resp3,"w")
    subdo.write(linea)
    subdo.close()

    os.system("a2ensite subdominio.%s" % resp3)
    os.system("service apache2 restart >/dev/null ")

    directa = open("/var/cache/bind/db.%s" % resp3,"a")
    directa.write("%s  CNAME servidor\n" % nombre_subdominio)
    directa.close()
    os.system("service bind9 restart >/dev/null ") 
    os.system("chmod -R 777 /srv/www/%s/" % (resp3)
