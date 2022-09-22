from tkinter import *
from tkinter import ttk
import re
from tkinter import messagebox
import sqlite3

""" PATRONES REGEX """
nombreApellido_patron = "[a-zA-ZáéíóúÁÉÍÓÚ ]+"
numeros_patron = "[\d]+"


def conectar_base():
    con = sqlite3.connect("alumnos.db")
    return con


def empezar_programa():
    create_table()
    dni_E.delete(0, END)
    faltas_E.delete(0, END)
    justificadas_E.delete(0, END)
    nombre_E.focus()
    if len(seleccionar(conectar_base())) > 0:
        actualizar_tree()
    else:
        pass


"""  FUNCIONES SQL """


def seleccionar(conection):
    cursor = conection.cursor()
    sql = "SELECT * FROM alumnos_5b"
    cursor.execute(sql)

    rows = cursor.fetchall()
    return rows


def actualizar_tree():
    ordenada = sorted(seleccionar(conectar_base()), key=lambda dni: dni[2])
    for record in tree.get_children():
        tree.delete(record)
    for row in ordenada:
        tree.insert("", "end", text="", values=(row[0], row[1], row[2], row[3], row[4]))


def create_table():
    conection = conectar_base()
    cursor = conection.cursor()
    sql = "CREATE TABLE IF NOT EXISTS alumnos_5b(id integrer PRIMARY KEY, nombre text, apellido text, faltas integrer," \
          " justificadas integrer)"
    cursor.execute(sql)
    conection.commit()


def alta(conection, data):
    cursor = conection.cursor()
    sql = "INSERT INTO alumnos_5b(id, nombre, apellido, faltas, justificadas) VALUES (?, ?, ?, ?, ?);"
    try:
        cursor.execute(sql, data)
    except:
        create_table()
        cursor.execute(sql, data)
    conection.commit()
    actualizar_tree()


def actualizar(conection, data):
    cursor = conection.cursor()
    sql = "UPDATE alumnos_5b SET id = ?, nombre = ?, apellido = ?, faltas = ?, justificadas = ?  WHERE id = ?"
    cursor.execute(sql, data)
    conection.commit()
    actualizar_tree()


"""funciones command"""


def alta_alumno():
    if len(var_nombre.get()) == 0 or len(var_apellido.get()) == 0 or len(dni_E.get()) == 0 or \
            len(faltas_E.get()) == 0 or len(justificadas_E.get()) == 0:
        messagebox.showwarning(title="¡Importante!", message="Al dar un alta ningún campo puede estar vacío.")
    elif re.search(nombreApellido_patron, var_apellido.get()).span()[1] == len(var_apellido.get()) and \
            re.search(nombreApellido_patron, var_nombre.get()).span()[1] == len(var_nombre.get()) and \
            re.search(numeros_patron, str(dni_E.get())).span()[1] == len(dni_E.get()) and \
            re.search(numeros_patron, str(faltas_E.get())).span()[1] == len(faltas_E.get()) and \
            re.search(numeros_patron, str(justificadas_E.get())).span()[1] == len(justificadas_E.get()):
        mensaje = messagebox.askyesno(title="Alta de alumno", message=f"¿Agregar a la tabla a {var_nombre.get()} "
                                                                      f"{var_apellido.get()}?\n\nDNI: {var_dni.get()}"
                                                                      f"\nFaltas: {var_faltas.get()}\nJustificadas: "
                                                                      f"{justificadas_E.get()}")
        if mensaje:
            data = (var_dni.get(), var_nombre.get(), var_apellido.get(), var_faltas.get(), var_justificadas.get())
            alta(conection=conectar_base(), data=data)
            nombre_E.delete(0, END)
            apellido_E.delete(0, END)
            dni_E.delete(0, END)
            faltas_E.delete(0, END)
            justificadas_E.delete(0, END)
            nombre_E.focus()
        else:
            pass
    else:
        messagebox.showerror(title="Advertencia!",
                             message="Campos no validos! DNI, FALTAS y JUSTIFICADAS solo pueden ser"
                                     " numeros. NOMBRE y APELLIDO solo letras.")


def baja_alumno():
    conection = conectar_base()
    # item = tree.focus()
    cursor = conection.cursor()
    if len(tree.selection()) > 0:
        if messagebox.askyesno(title="Baja de alumno.",
                               message="Está seguro de eliminar al/los alumno/s seleccionados?"):
            for item in tree.selection():
                data = (tree.item(item)["values"][0],)
                sql = "DELETE FROM alumnos_5b WHERE id = ?;"
                cursor.execute(sql, data)
                conection.commit()
            actualizar_tree()
    else:
        messagebox.showinfo(title="Importante!", message="Seleccione un alumno para eliminar.")


def sumar_ausencia():
    con = conectar_base()
    # item = tree.focus()
    # print(tree.item(item))
    cursor = con.cursor()
    for item in tree.selection():
        data = (int(tree.item(item)["values"][3]) + 1, tree.item(item)["values"][0])
        sql = "UPDATE alumnos_5b SET faltas = ? WHERE id = ?"
        cursor.execute(sql, data)
        con.commit()
    actualizar_tree()


def sumar_ausencia_justificada():
    con = conectar_base()
    # item = tree.focus()
    cursor = con.cursor()
    for item in tree.selection():
        data = (
            int(tree.item(item)["values"][3]) + 1, int(tree.item(item)["values"][4]) + 1, tree.item(item)["values"][0])
        sql = "UPDATE alumnos_5b SET faltas = ?, justificadas = ? WHERE id = ?"
        cursor.execute(sql, data)
        con.commit()
    actualizar_tree()


def modificar_alumno():
    item = tree.focus()
    if item != "":
        if len(var_nombre.get()) == 0 or len(var_apellido.get()) == 0 or len(dni_E.get()) == 0 or \
                len(faltas_E.get()) == 0 or len(justificadas_E.get()) == 0:
            messagebox.showwarning(title="¡Importante!", message="Ningún campo puede estar vacío.")
        elif re.search(nombreApellido_patron, var_apellido.get()).span()[1] == len(var_apellido.get()) and \
                re.search(nombreApellido_patron, var_nombre.get()).span()[1] == len(var_nombre.get()) and \
                re.search(numeros_patron, str(dni_E.get())).span()[1] == len(dni_E.get()) and \
                re.search(numeros_patron, str(faltas_E.get())).span()[1] == len(faltas_E.get()) and \
                re.search(numeros_patron, str(justificadas_E.get())).span()[1] == len(justificadas_E.get()):
            mensaje = messagebox.askyesno(title="Modificar alumno", message=f"¿Agregar a la tabla"
                                                                            f" a {var_nombre.get()} "
                                                                            f"{var_apellido.get()}?\n\nDNI: {var_dni.get()}"
                                                                            f"\nFaltas: {var_faltas.get()}\nJustificadas: "
                                                                            f"{justificadas_E.get()}")
            if mensaje:
                data = (var_dni.get(), var_nombre.get(), var_apellido.get(), var_faltas.get(), var_justificadas.get(),
                        int(tree.item(item)["values"][0]))
                actualizar(conectar_base(), data)
                nombre_E.delete(0, END)
                apellido_E.delete(0, END)
                dni_E.delete(0, END)
                faltas_E.delete(0, END)
                justificadas_E.delete(0, END)
                nombre_E.focus()
        else:
            messagebox.showerror(title="Advertencia!",
                                 message="Campos no validos! DNI, FALTAS y JUSTIFICADAS solo pueden ser"
                                         " numeros. NOMBRE y APELLIDO solo letras.")
    else:
        messagebox.showinfo(title="Importante!", message="Seleccione un alumno a modificar.")


"""   G U I   """

window = Tk()
window.configure(padx=20, pady=20)
window.minsize(770, 610)
window.title("Máximo Álvarez Python Inicial ------- ´SISTEMA DE FALTAS´")

var_nombre = StringVar()
var_apellido = StringVar()
var_dni = IntVar()
var_faltas = IntVar()
var_justificadas = IntVar()
# var_justificada = IntVar()

# ------ LABELS ------

titulo_L = Label(window, text="Para agregar un alumno, complete los datos y aprete el boton ´AÑADIR ALUMNO´. \n\nPara "
                              "modificar la informacion de un alumno, selecciónelo y complete de nuevo sus datos. Luego precione el boton ´MODIFICAR ALUMNO\n´")
titulo_L.grid(column=0, row=0, columnspan=3, sticky=N)

nombre_L = Label(window, text="Nombre:")
nombre_L.grid(column=0, row=1, sticky=W)

apellido_L = Label(window, text="Apellido:")
apellido_L.grid(column=0, row=2, sticky=W)

dni_L = Label(window, text="DNI:")
dni_L.grid(column=0, row=3, sticky=W)

faltas_L = Label(window, text="Cantidad de faltas totales:")
faltas_L.grid(column=0, row=4, sticky=W)

justificadas_L = Label(window, text="Cantidad de faltas justificadas:")
justificadas_L.grid(column=0, row=5, sticky=W)

borrar_L = Label(window, text="\nPara eliminar un alumno, seleccionelo de la tabla y haga click en el boton"
                              " ´Eliminar alumno´\n")
borrar_L.grid(column=0, columnspan=3, row=6, sticky=N)

separador1_L = Label(window, text="_________________________________________________________________________________\n")
separador1_L.grid(column=0, columnspan=4, row=10, sticky=N)

separador2_L = Label(window, text="_________________________________________________________________________________\n")
separador2_L.grid(column=0, columnspan=4, row=8, sticky=N)

# ------ ENTRYS ------

nombre_E = Entry(window, textvariable=var_nombre, width=60)
nombre_E.grid(column=1, row=1, sticky=W)

apellido_E = Entry(window, textvariable=var_apellido, width=60)
apellido_E.grid(column=1, row=2, sticky=W)

dni_E = Entry(window, textvariable=var_dni, width=60)
dni_E.grid(column=1, row=3, sticky=W)

faltas_E = Entry(window, textvariable=var_faltas, width=60)
faltas_E.grid(column=1, row=4, sticky=W)

justificadas_E = Entry(window, textvariable=var_justificadas, width=60)
justificadas_E.grid(column=1, row=5, sticky=W)

# ------ BUTTOMS ------

alta_B = Button(window, text="Añadir alumno", command=alta_alumno)
alta_B.grid(column=0, row=7)

actualizar_B = Button(window, text="Modificar alumno", command=modificar_alumno)
actualizar_B.grid(column=2, row=7)

borrar_B = Button(window, text="Eliminar alumno", command=baja_alumno)
borrar_B.grid(column=1, row=7, sticky=N)

# ------ TREEVIEW ------

tree = ttk.Treeview(window)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5")

tree.column("#0", width=0, minwidth=0, anchor=W)
tree.column("col1", width=80, minwidth=60, anchor=CENTER)
tree.column("col2", width=80, minwidth=60, anchor=W)
tree.column("col3", width=80, minwidth=60, anchor=W)
tree.column("col4", width=80, minwidth=60, anchor=CENTER)
tree.column("col5", width=80, minwidth=60, anchor=CENTER)

tree.heading("#0", text="", anchor=CENTER)
tree.heading("col1", text="DNI", anchor=CENTER)
tree.heading("col2", text="NOMBRE", anchor=W)
tree.heading("col3", text="APELLIDO", anchor=W)
tree.heading("col4", text="FALTAS", anchor=CENTER)
tree.heading("col5", text="JUSTIFICADAS", anchor=CENTER)

tree.grid(column=0, row=9, columnspan=4)

# ------ botones de abajo ------

sumar_falta_B = Button(window, text="añadir falta injustificada", command=sumar_ausencia)
sumar_falta_B.grid(column=0, row=11)
sumar_falta_j_B = Button(window, text="añadir falta justificada", command=sumar_ausencia_justificada)
sumar_falta_j_B.grid(column=1, row=11)

# ------ TREEVIEW STYLE ------

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="silver",
                foreground="black",
                rowheight=25,
                fieldbackgorund="silver")
style.map("Treeview",
          background=[("selected", "red")])

empezar_programa()

window.mainloop()
