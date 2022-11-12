import mysql.connector
from mysql.connector import Error
try:
	connection=mysql.connector.connect(host='localhost',port='3308',database='gamemate',user='root',password='Tito1497.')
	if connection.is_connected():
			db_Info=connection.get_server_info()
			print("Conectado a la versión del servidor MySQL", db_Info)
			cursor=connection.cursor()
			cursor.execute("select database();")
			record=cursor.fetchone()
			print("Estas conectado a la base de datos:", record)
except Error as e:
	print ("Error al conectarse a MySQL", e)
finally:
	if connection.is_connected():
		cursor.close()
		connection.close()
		print("La conexión MySQL está cerrada")

