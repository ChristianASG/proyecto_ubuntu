from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import mysql.connector

root = Tk()

# ------------------- Funciones de info y salida -------------------
def infoAdicional():
    messagebox.showinfo("Aplicación Farmacias", "Aplicación para gestión de farmacias - Christian")

def avisoLicencia():
    messagebox.showwarning("Licencia", "Producto bajo licencia de Christian")

def salirAplicacion():
    valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicación?")
    if valor == "yes":
        root.destroy()

def cerrarDocumento():
    valor = messagebox.askretrycancel("Reintentar", "No es posible cerrar. Documento bloqueado")
    if valor == False:
        root.destroy()

def abreFichero():
    fichero = filedialog.askopenfilename(title="Abrir", initialdir="D:")
    print(fichero)

# ------------------- Conexión a MySQL -------------------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Paloma32",
        database="farmacias_valencia"
    )

# ------------------- Crear Base y Tabla -------------------
def crearBase():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Paloma32"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS farmacias_valencia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("USE farmacias_valencia")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmacias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            direccion VARCHAR(255),
            codigo_postal VARCHAR(20),
            municipio VARCHAR(100),
            telefono VARCHAR(50)
             )
        """)
        messagebox.showinfo("Base de datos", "Base de datos y tabla creadas exitosamente.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo crear la base de datos: {err}")

# ------------------- CRUD -------------------
def insertar_registro():
    conn = conectar()
    cursor = conn.cursor()
    sql = """INSERT INTO farmacias (nombre, direccion, codigo_postal, municipio, telefono)
             VALUES (%s, %s, %s, %s, %s)"""
    val = (
        miNombre.get(),
        miDireccion.get(),
        miCodigoPostal.get(),
        miMunicipio.get(),
        miTelefono.get()
    )
    cursor.execute(sql, val)
    conn.commit()
    messagebox.showinfo("BBDD", "Registro insertado con éxito")
    cursor.close()
    conn.close()

def leerBase():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farmacias WHERE id=%s", (miId.get(),))
    registros = cursor.fetchall()
    for f in registros:
        miId.set(f[0])
        miNombre.set(f[1])
        miDireccion.set(f[2])
        miCodigoPostal.set(f[3])
        miMunicipio.set(f[4])
        miTelefono.set(f[5])
        
    cursor.close()
    conn.close()

def actualizarBase():
    conn = conectar()
    cursor = conn.cursor()
    sql = """UPDATE farmacias SET nombre=%s, direccion=%s, codigo_postal=%s, municipio=%s,
             telefono=%s, WHERE id=%s"""
    val = (
        miNombre.get(),
        miDireccion.get(),
        miCodigoPostal.get(),
        miMunicipio.get(),
        miTelefono.get(),
        miId.get()
    )
    cursor.execute(sql, val)
    conn.commit()
    messagebox.showinfo("BBDD", "Registro actualizado con éxito")
    cursor.close()
    conn.close()

def borrarBase():
    id_registro = miId.get()
    if id_registro:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farmacias WHERE id=%s", (id_registro,))
        conn.commit()
        messagebox.showinfo("Borrar", "Registro borrado exitosamente.")
        limpiar_campos()
        cursor.close()
        conn.close()
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un ID para borrar.")

def limpiar_campos():
    miId.set("")
    miNombre.set("")
    miDireccion.set("")
    miCodigoPostal.set("")
    miMunicipio.set("")
    miTelefono.set("")
    

# ------------------- Cargar farmacias de ejemplo -------------------
def cargar_farmacias_ejemplo():
    farmacias = [
        ("Farmacia San Vicente", "Calle San Vicente Mártir, 100", "46007", "Valencia", "963000000"),
        ("Farmacia La Torre", "Avenida de la Torre, 25", "46020", "Valencia", "963111111"),
        ("Farmacia El Carmen", "Plaza del Carmen, 3", "46003", "Valencia", "963222222"),
        ("Farmacia Central", "Calle Central, 10", "46001", "Valencia", "963333333"),
        ("Farmacia Norte", "Avenida Norte, 45", "46015", "Valencia", "963444444")
    ]

    conn = conectar()
    cursor = conn.cursor()
    sql = """INSERT INTO farmacias (nombre, direccion, codigo_postal, municipio, telefono)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.executemany(sql, farmacias)
    conn.commit()
    messagebox.showinfo("BBDD", f"{cursor.rowcount} farmacias de ejemplo insertadas.")
    cursor.close()
    conn.close()


# ------------------- GUI -------------------
root.title("Gestión de Farmacias Valencia")

barraMenu = Menu(root)
root.config(menu=barraMenu, width=400, height=400)

bbddMenu = Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Crear BBDD", command=crearBase)
bbddMenu.add_command(label="Abrir archivo", command=abreFichero)
bbddMenu.add_separator()
bbddMenu.add_command(label="Cerrar", command=cerrarDocumento)
bbddMenu.add_command(label="Salir", command=salirAplicacion)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Create", command=insertar_registro)
crudMenu.add_command(label="Read", command=leerBase)
crudMenu.add_command(label="Update", command=actualizarBase)
crudMenu.add_command(label="Delete", command=borrarBase)

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Licencia", command=avisoLicencia)
ayudaMenu.add_command(label="Acerca de", command=infoAdicional)

barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

miFrame = Frame(root)
miFrame.pack()

# Variables
miId = StringVar()
miNombre = StringVar()
miDireccion = StringVar()
miCodigoPostal = StringVar()
miMunicipio = StringVar()
miTelefono = StringVar()


# Labels y Entrys
labels = ["ID","Nombre","Dirección","Código Postal","Municipio","Teléfono"]
variables = [miId, miNombre, miDireccion, miCodigoPostal, miMunicipio, miTelefono]

for i, (lab, var) in enumerate(zip(labels, variables)):
    Label(miFrame, text=lab).grid(row=i, column=0, sticky="e", padx=5, pady=3)
    Entry(miFrame, textvariable=var).grid(row=i, column=1, padx=5, pady=3)

# Botones CRUD
miFrame1 = Frame(root)
miFrame1.pack()

Button(miFrame1, text="Create", command=insertar_registro).grid(row=0,column=0)
Button(miFrame1, text="Read", command=leerBase).grid(row=0,column=1)
Button(miFrame1, text="Update", command=actualizarBase).grid(row=0,column=2)
Button(miFrame1, text="Delete", command=borrarBase).grid(row=0,column=3)
Button(miFrame1, text="Limpiar", command=limpiar_campos).grid(row=0,column=4)
Button(miFrame1, text="Cargar Ejemplo", command=cargar_farmacias_ejemplo).grid(row=0,column=5)





root.mainloop()
