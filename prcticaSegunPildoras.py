from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

root=Tk()

def infoAdicional():
    messagebox.showinfo("Aplicacion para empaquetado","Aplicacion para empaquetado de Christian")


def avisoLicencia():
    messagebox.showwarning("Licencia","Producto bajo licencia de Christian")

def salirAplicacion():
    valor=messagebox.askquestion("Salir","Deseas salir de la aplicacion?")

    if valor=="yes":
        root.destroy()

def cerrarDocumento():
    valor=messagebox.askretrycancel("Reintentar","No es posible cerrar. Documento bloqueado")

    if valor==False:
        root.destroy()

def abreFichero():
    fichero=filedialog.askopenfilename(title="Abrir", initialdir="D:")

    print(fichero)

def crearBase():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       Nombre TEXT,
                       Apellidos TEXT,
                       Contrasenya TEXT,
                       Direccion text,
                       Comentarios text)''')
    conn.commit()
    conn.close()
    messagebox.showinfo("Base de datos", "Base de datos creada exitosamente.")

def insertar_registro():
    texto1 = nombreEntry.get()
    texto2 = apellidoEntry.get()
    texto3 = contraseñaEntry.get()
    texto4 = direccionEntry.get()
    texto5 = comentariotexto.get("1.0","end-1c")


    if texto1 and texto2 and texto3 and texto4 :
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO registros (Nombre, Apellidos, Contrasenya, Direccion, Comentarios) VALUES (?, ?,?,?,?)',
        (texto1, texto2, texto3, texto4, texto5))
        conn.commit()
        conn.close()
        messagebox.showinfo("Insertar", "Registro insertado exitosamente.")
        limpiar_campos()

    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")



def leerBase():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()
    conn.close()

    if registros:
        resultado = "\n".join([f"ID: {reg[0]} - {reg[1]}, {reg[2]}, {reg[3]}, {reg[4]}, {reg[5]}" for reg in registros])
        messagebox.showinfo("Registros", resultado)
    else:
        messagebox.showinfo("Registros", "No hay registros en la base de datos.")



def actualizarBase():
    id_registro = idEntry.get()
    texto1 = nombreEntry.get()
    texto2 = apellidoEntry.get()
    texto3 = contraseñaEntry.get()
    texto4 = direccionEntry.get()
    texto5 = comentariotexto.get()

    if id_registro and texto1 and texto2 and texto3 and texto4 and texto5:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE registros SET Nombre = ?, Apellidos = ?, Contrasenya = ?, Direccion = ? , Comentarios = ?  WHERE id = ?',
        (texto1, texto2, texto3, texto4, texto5, id_registro))
        conn.commit()
        conn.close()
        messagebox.showinfo("Actualizar", "Registro actualizado exitosamente.")
        limpiar_campos()
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")



def borrarBase():
    id_registro = idEntry.get()

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

def limpiar_campos():
    miId.set("")
    miNombre.set("")
    miApellido.set("")
    miContrasenya.set("")
    miDireccion.set("")
    comentariotexto.delete(1.0, END)


#Button(root, text="Abrir fichero", command=abreFichero).pack()

root.title("Paractica Pildoras")

barraMenu=Menu(root)
root.config(menu=barraMenu,width=300,height=300)

bbddMenu=Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Crear BBDD", command=crearBase)
bbddMenu.add_command(label="Nuevo archivo", command=abreFichero)
bbddMenu.add_command(label="Guardar")
bbddMenu.add_separator()
bbddMenu.add_command(label="Cerrar", command=cerrarDocumento)
bbddMenu.add_command(label="Salir", command=salirAplicacion)


borrarMenu=Menu(barraMenu,tearoff=0)
borrarMenu.add_command(label="Limpiar", command=limpiar_campos)
borrarMenu.add_command(label="Copiar")
borrarMenu.add_command(label="Cortar")
borrarMenu.add_command(label="Pegar")


crudMenu=Menu(barraMenu,tearoff=0)
crudMenu.add_command(label="Created", command=insertar_registro)
crudMenu.add_command(label="Read", command=leerBase)
crudMenu.add_command(label="Update", command=actualizarBase)
crudMenu.add_command(label="Delete", command=borrarBase)



ayudaMenu=Menu(barraMenu,tearoff=0)
ayudaMenu.add_command(label="Licencia",command=avisoLicencia)
ayudaMenu.add_command(label="Acerca de",command=infoAdicional)



barraMenu.add_cascade(label="BBDD",menu=bbddMenu)
barraMenu.add_cascade(label="Borrar",menu=borrarMenu)
barraMenu.add_cascade(label="CRUD",menu=crudMenu)
barraMenu.add_cascade(label="Ayuda",menu=ayudaMenu)

miFrame=Frame(root,width=500,height=400)
miFrame.pack()

miId=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miContrasenya=StringVar()
miDireccion=StringVar()



#para utilizar imagenes tkinter usa png y gif, y tienes que especificar la ruta si no esta en el mismo directorio
#miImagen=PhotoImage(file="imagenes-png.png")
#miImagen.Label(miFrame, image=miImagen)
idEntry=Entry(miFrame,textvariable=miId)
idEntry.grid(row=0,column=1,padx=10)
idLabel=Label(miFrame, text="Id: ")
idLabel.grid(row=0,column=0,sticky="e")
nombreEntry=Entry(miFrame, textvariable=miNombre)
nombreEntry.grid(row=1,column=1,padx=10)
nombreEntry.config(fg="red")
nombreEntry.config(fg="red", justify="right")
nombreLabel=Label(miFrame, text="Nombre: ")
nombreLabel.grid(row=1,column=0,sticky="e")
contraseñaEntry=Entry(miFrame,textvariable=miContrasenya)
contraseñaEntry.grid(row=3,column=1)
contraseñaLabel=Label(miFrame, text="contraseña: ")
contraseñaLabel.grid(row=3,column=0,sticky="e")
contraseñaEntry.config(show="*")
apellidoEntry=Entry(miFrame,textvariable=miApellido)
apellidoEntry.grid(row=2,column=1,padx=10)
apellidoLabel=Label(miFrame, text="Apellido: ")
apellidoLabel.grid(row=2,column=0,sticky="e")
direccionEntry=Entry(miFrame,textvariable=miDireccion)
direccionEntry.grid(row=4,column=1)
direccionLabel=Label(miFrame, text="Direccion: ")
direccionLabel.grid(row=4,column=0,sticky="e")

#vamos a introducir texto largo y botones
comentarioLabel=Label(miFrame, text="comentarios: ")
comentarioLabel.grid(row=5,column=0,sticky="e")
comentariotexto=Text(miFrame, width=30,height=7)
comentariotexto.grid(row=5,column=1)
barralateral=Scrollbar(miFrame, command=comentariotexto.yview)#barra lateral para subir y bajar por un texto largo
barralateral.grid(row=4,column=2,sticky="nsew")
barralateral.grid(row=5,column=2,sticky="nsew")
comentariotexto.config(yscrollcommand=barralateral.set)
#agregar boton, y agregar instrucciones
def codigoBoton():
    minombre.set("Christian")
#para obtener informacion(get)

miFrame1=Frame(root)
miFrame1.pack()

botonCrear=Button(miFrame1, text="Create",command=insertar_registro)
botonCrear.grid(row=0,column=0,sticky="e")

botonLeer=Button(miFrame1, text="Read",command=leerBase)
botonLeer.grid(row=0,column=1,sticky="e")

botonActualizar=Button(miFrame1, text="Update",command=actualizarBase)
botonActualizar.grid(row=0,column=2,sticky="e")

botonEliminar=Button(miFrame1, text="Delete",command=borrarBase)
botonEliminar.grid(row=0,column=3,sticky="e")

botonLimpiar=Button(miFrame1, text="Limpiar",command=limpiar_campos)
botonLimpiar.grid(row=0,column=4,sticky="e")


root.mainloop()