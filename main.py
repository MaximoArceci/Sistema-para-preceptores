from tkinter import *
from tkinter import ttk

"""   G U I   """

window = Tk()
window.title("Faltas 5to año 2022")

var_nombre = StringVar()
var_apellido = StringVar()
var_fecha = StringVar()
radio_state = IntVar()

mi_id = 0

#------ FUNCIONES ------

def radio_used():
    pass


def funcion_alta():
    global mi_id
    mi_id += 1
    tree.insert("", "end", text=str(mi_id), values=(var_nombre.get(), var_apellido.get(), var_fecha.get()))
    nombre_E.delete(0, END)
    apellido_E.delete(0, END)
    fecha_E.delete(0, END)
    nombre_E.focus()


def funcion_baja():
    global mi_id
    mi_id -= 1
    item = tree.focus()
    tree.delete(item)


#------ LABELS ------

nombre_L = Label(window, text="Nombre:")
nombre_L.grid(column=0, row=0, sticky=W)

apellido_L = Label(window, text="Apellido:")
apellido_L.grid(column=0, row=1, sticky=W)

fecha_L = Label(window, text="Fecha:")
fecha_L.grid(column=0, row=2, sticky=W)

#------ ENTRYS ------

nombre_E = Entry(window, textvariable=var_nombre)
nombre_E.grid(column=1, row=0, sticky=W)

apellido_E = Entry(window, textvariable=var_apellido)
apellido_E.grid(column=1, row=1, sticky=W)

fecha_E = Entry(window, textvariable=var_fecha)
fecha_E.grid(column=1, row=2, sticky=W)

#------ BUTTOMS ------

alta_B = Button(window, text="Guardar", command=funcion_alta)
alta_B.grid(column=0, columnspan=2, row=3)

baja_B = Button(window, text="eliminar", command=funcion_baja)
baja_B.grid(column=0, columnspan=2, row=4)

#------ RADIOSTATE ------
justificado_R = Radiobutton(text="Justificada", value=1, variable=radio_state, command=radio_used)
justificado_R.grid(column=0, row=5)

no_justificado_R = Radiobutton(text="No justificada", value=2, variable=radio_state, command=radio_used)
no_justificado_R.grid(column=0, row=6)
#------ TREEVIEW ------

tree = ttk.Treeview(window)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5")

tree.column("#0", width=25, minwidth=25, anchor=W)
tree.column("col1", width=80, minwidth=60, anchor=W)
tree.column("col2", width=80, minwidth=60, anchor=W)
tree.column("col3", width=80, minwidth=60, anchor=W)
tree.column("col4", width=80, minwidth=60, anchor=W)
tree.column("col5", width=80, minwidth=60, anchor=W)

tree.grid(column=0, row=7, columnspan=4)

window.mainloop()
