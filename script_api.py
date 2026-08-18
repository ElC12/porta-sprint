import requests
import sqlite3
from datetime import datetime as datatime

print("=== AUTOMATIZACIÓN DE DATOS - DIGITAL CORE PRO ===")

url = "https://api.exchangerate-api.com/v4/latest/USD"
response = requests.get(url)

if response.status_code == 200:
	data = response.json()
	tasa_pen = data["rates"]["PEN"]
	fecha = datatime.now().strftime("%Y-%m-%d %H:%M:%S")
	print(f"[{fecha}] Tipo de cambio USD a PEN: S/ {tasa_pen}")
	
	conn = sqlite3.connect("monitoreo_divisas.db")
	cursor= conn.cursor()
	cursor.execute(''' 
		CREATE TABLE IF NOT EXISTS historial_dolar ( 
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			fecha TEXT,
			precio_soles REAL)''')

	cursor.execute("INSERT INTO historial_dolar ( fecha, precio_soles) VALUES(?,?)",(fecha, tasa_pen))
	conn.commit()
	print("Datos guardados exitosamente en la base de datos SQL.")
	
	cursor.execute("SELECT *FROM historial_dolar")
	registros = cursor.fetchall()
	print("\n Historial en SQL:")
	
	for r in registros:
		print(f"ID: {r[0]} | Fecha: {r[1]} | USD/PEN: S/ {r[2]}")
	conn.close()
else:
     print("Error al conectar en la API")
