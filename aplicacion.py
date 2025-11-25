import tkinter as tk
from tkinter import messagebox
import sqlite3

# Función para crear la base de datos
def crear_base_datos():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        texto1 TEXT,
                        texto2 TEXT,
                        texto3 TEXT)''')
    conn.commit()
    conn.close()
    messagebox.showinfo("Base de datos", "Base de datos creada exitosamente.")

# Función para insertar un registro en la base de datos mediante consulta parametrizada
def insertar_registro():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    datos = entry_texto1.get(),entry_texto2.get(),entry_texto3.get()
    
  
    cursor.execute("INSERT INTO registros VALUES (NULL,?,?,?)",(datos))
                       
    conn.commit()
       
    messagebox.showinfo("Insertar", "Registro insertado exitosamente.")
    
# Función para leer todos los registros de la base de datos
def leer_registros():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()
    conn.close()

    if registros:
        resultado = "\n".join([f"ID: {reg[0]} - {reg[1]}, {reg[2]}, {reg[3]}" for reg in registros])
        messagebox.showinfo("Registros", resultado)
    else:
        messagebox.showinfo("Registros", "No hay registros en la base de datos.")

# Función para actualizar un registro
def actualizar_registro():
    id_registro = entry_id.get()
    texto1 = entry_texto1.get()
    texto2 = entry_texto2.get()
    texto3 = entry_texto3.get()

    if id_registro and texto1 and texto2 and texto3:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE registros SET texto1 = ?, texto2 = ?, texto3 = ? WHERE id = ?',
                       (texto1, texto2, texto3, id_registro))
        conn.commit()
        conn.close()
        messagebox.showinfo("Actualizar", "Registro actualizado exitosamente.")
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

# Función para borrar un registro
def borrar_registro():
    id_registro = entry_id.get()

    if id_registro:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM registros WHERE id = ?', (id_registro,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Borrar", "Registro borrado exitosamente.")
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un ID para borrar.")

# Limpiar los campos de entrada
def limpiar_campos():
    entry_texto1.delete(0, tk.END)
    entry_texto2.delete(0, tk.END)
    entry_texto3.delete(0, tk.END)

# Función para mostrar la información de la aplicación
def mostrar_info():
    messagebox.showinfo("Acerca de", "Aplicación de gestión de registros.\nDesarrollada en Python con Tkinter y SQLite.")

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Registros")

# Crear el menú
menu_bar = tk.Menu(root)

# Menú de opciones
opciones_menu = tk.Menu(menu_bar, tearoff=0)
opciones_menu.add_command(label="Salir", command=root.quit)
opciones_menu.add_command(label="Crear base de datos", command=crear_base_datos)
opciones_menu.add_command(label="Funcionalidades", command=lambda: mostrar_info())
menu_bar.add_cascade(label="Menú", menu=opciones_menu)

root.config(menu=menu_bar)

# Crear los cuadros de texto para introducir datos
label_id = tk.Label(root, text="ID (Autogenerado):")
label_id.pack()
entry_id = tk.Entry(root)
entry_id.pack()

label_texto1 = tk.Label(root, text="nombre:")
label_texto1.pack()
entry_texto1 = tk.Entry(root)
entry_texto1.pack()


label_texto2 = tk.Label(root, text="apellidos:")
label_texto2.pack()
entry_texto2 = tk.Entry(root)
entry_texto2.pack()

label_texto3 = tk.Label(root, text="contraseña:")
label_texto3.pack()
entry_texto3 = tk.Entry(root)
entry_texto3.pack()

# Crear botones para insertar, leer, actualizar y borrar
frame_botones = tk.Frame(root)
frame_botones.pack()

boton_insertar = tk.Button(frame_botones, text="Insertar", command=insertar_registro)
boton_insertar.grid(row=0, column=0, padx=5, pady=5)

boton_leer = tk.Button(frame_botones, text="Leer", command=leer_registros)
boton_leer.grid(row=0, column=1, padx=5, pady=5)

boton_actualizar = tk.Button(frame_botones, text="Actualizar", command=actualizar_registro)
boton_actualizar.grid(row=0, column=2, padx=5, pady=5)

boton_borrar = tk.Button(frame_botones, text="Borrar", command=borrar_registro)
boton_borrar.grid(row=0, column=3, padx=5, pady=5)

# Ejecutar la ventana principal
root.mainloop()
