import sqlite3

def log(origem, tempo):
	conn = sqlite3.connect('log.db')
	cursor = conn.cursor()
	#soma com 1 para evitar numeros com notacao cientifica
	cursor.execute("INSERT INTO logs(origem,tempo) VALUES ('{}','{}')".format(str(origem), (float(tempo)+1)))
	conn.commit()
	conn.close()