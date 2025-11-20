import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Paloma32"
)

print(mydb)


mycursor = mydb.cursor()

# Creamos la base de datos
mycursor.execute("CREATE DATABASE IF NOT EXISTS farmacias_valencia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
mycursor.execute("USE farmacias_valencia")

# Creamos la tabla de farmacias
mycursor.execute("""
CREATE TABLE IF NOT EXISTS farmacias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255),
    codigo_postal VARCHAR(20),
    municipio VARCHAR(100),
    telefono VARCHAR(50),
    latitud DECIMAL(10, 7),
    longitud DECIMAL(10, 7)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")

# Insertamos algunos datos de ejemplo
farmacias = [
    ("Farmacia San Vicente", "Calle San Vicente Mártir, 100", "46007", "Valencia", "963000000", 39.468, -0.376),
    ("Farmacia La Torre", "Avenida de la Torre, 25", "46020", "Valencia", "963111111", 39.492, -0.365),
    ("Farmacia El Carmen", "Plaza del Carmen, 3", "46003", "Valencia", "963222222", 39.471, -0.378)
]

sql = "INSERT INTO farmacias (nombre, direccion, codigo_postal, municipio, telefono, latitud, longitud) VALUES (%s, %s, %s, %s, %s, %s, %s)"
mycursor.executemany(sql, farmacias)

mydb.commit()

print(mycursor.rowcount, "farmacias insertadas.")

# Consultamos para verificar
mycursor.execute("SELECT * FROM farmacias")
for fila in mycursor.fetchall():
    print(fila)

mycursor.close()
mydb.close()
