import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from CTkTable import CTkTable

def conectar_bd():
    #Establece la conexión con la base de datos MySQL.
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password='', # Contraseña de tu base de datos MySQL
            database="hospital.1.1" # Nombre correcto de tu base de datos
            )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Base de datos", f"Error al conectar con la base de datos: {err}")
        return None
#datos de doctor a insertar

def insertar_doctor(datos_doctor):
    #Inserta un nuevo doctor en la tabla 'doctor'
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        
        consulta_sql = "INSERT INTO doctor (CodigoDoc, Nombre_Doc, Apellido_Paterno, Apellido_Materno, Especialidad, Telefono, Cedula_Profesional, Correo, Direccion, Fecha_Nacimiento, Tipo_Sangre, Genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(consulta_sql, datos_doctor)
            conexion.commit()
            listar_doctores() # Actualizar la tabla
            messagebox.showinfo("Éxito", "Doctor registrado con éxito")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al insertar doctor: {err}")
        finally:
            cursor.close()
            conexion.close()

def listar_doctores():
    """Obtiene y muestra la lista de doctores en la tabla CTkTable."""
    conexion = conectar_bd()
    # Si la conexión falla al inicio, no mostramos error, solo la tabla vacía.
    if not (conexion and conexion.is_connected()):
        tabla.update_values([["Error de conexión", "", "", "", "", "", ""]])
        return
    else:
        cursor = conexion.cursor()
        consulta_sql = "SELECT CodigoDoc, Nombre_Doc, Apellido_Paterno, Apellido_Materno, Especialidad, Telefono, Correo FROM doctor"
        
        try:
            cursor.execute(consulta_sql)
            registros = cursor.fetchall()
            
            # Encabezados de la nueva tabla de doctores
            cabecera = ["Código", "Nombre", "Paterno", "Materno", "Especialidad", "Teléfono", "Correo"]
            totalregistros = [cabecera] + list(registros)

            # Limpiar el frame antes de dibujar la nueva tabla
            for widget in listadodocs_frame.winfo_children():
                widget.destroy()

            tabla = CTkTable(listadodocs_frame, values=totalregistros, header_color="red")
            tabla.pack(expand=True, fill="both", padx=5, pady=5, side="bottom")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener doctores: {err}")
        finally:
            cursor.close()
            conexion.close()

def guardar():
    """Recoge los datos de los campos de entrada e invoca la función de inserción."""
    # Renombrar las variables para que reflejen los campos del doctor
    datos_doctor = (
        detalle_codigo.get(),
        detalle_nombre.get(),
        detalle_paterno.get(),
        detalle_materno.get(),
        detalle_especialidad.get(),
        detalle_telefono.get(),
        detalle_cedula.get(),
        detalle_correo.get(),
        detalle_direccion.get(),
        detalle_fecha_nacimiento.get(),
        combo_tipo_sangre.get(),
        combo_genero.get()
    )
    
    # Validar que todos los campos estén llenos
    if all(datos_doctor):
        insertar_doctor(datos_doctor)
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

def limpiar_campos():
    """Limpia todos los campos de entrada del formulario."""
    detalle_codigo.delete(0, 'end')
    detalle_nombre.delete(0, 'end')
    detalle_paterno.delete(0, 'end')
    detalle_materno.delete(0, 'end')
    detalle_especialidad.delete(0, 'end')
    detalle_telefono.delete(0, 'end')
    detalle_cedula.delete(0, 'end')
    detalle_correo.delete(0, 'end')
    detalle_direccion.delete(0, 'end')
    detalle_fecha_nacimiento.delete(0, 'end')
    combo_tipo_sangre.set(tipos_sangre[0])
    combo_genero.set(generos[0])
    detalle_codigo.focus() # Pone el cursor en el primer campo


# Renombrar la ventana
Ventana_Doctor = ctk.CTk(fg_color="black")
Ventana_Doctor.title("Registro de Doctores")
Ventana_Doctor.geometry("950x800")

# Frame Título
frame_titulo = ctk.CTkFrame(Ventana_Doctor, fg_color="#1858d7", corner_radius=10)
frame_titulo.pack(padx=5, pady=5, side='top', fill="x")
titulo = ctk.CTkLabel(frame_titulo, text="REGISTRO DE DOCTORES", text_color="white")
titulo.pack(padx=5, pady=5, side='top')

# Frame Contenedor   detalles y botones 
frame_contenedor = ctk.CTkFrame(Ventana_Doctor)
frame_contenedor.pack(padx=10, pady=10, side='top', fill="x")

# Frame Detalle (Campos de Entrada)
frame_detalle = ctk.CTkFrame(frame_contenedor, fg_color="#18d725", corner_radius=10)
frame_detalle.pack(padx=10, pady=10, side='left', fill="both", expand=True)
frame_detalle.grid_columnconfigure((0, 1), weight=1) # Columnas se expanden

# --- Columna 1 ---
ctk.CTkLabel(frame_detalle, text="CÓDIGO DE DOCTOR", text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
detalle_codigo = ctk.CTkEntry(frame_detalle, placeholder_text="Ej: DOC001")
detalle_codigo.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="NOMBRE(S)", text_color="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
detalle_nombre = ctk.CTkEntry(frame_detalle, placeholder_text="Nombre del doctor")
detalle_nombre.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="APELLIDO PATERNO", text_color="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
detalle_paterno = ctk.CTkEntry(frame_detalle, placeholder_text="Apellido paterno")
detalle_paterno.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="APELLIDO MATERNO", text_color="white").grid(row=6, column=0, padx=10, pady=5, sticky="w")
detalle_materno = ctk.CTkEntry(frame_detalle, placeholder_text="Apellido materno")
detalle_materno.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="ESPECIALIDAD", text_color="white").grid(row=8, column=0, padx=10, pady=5, sticky="w")
detalle_especialidad = ctk.CTkEntry(frame_detalle, placeholder_text="Ej: Cardiología")
detalle_especialidad.grid(row=9, column=0, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="TELÉFONO", text_color="white").grid(row=10, column=0, padx=10, pady=5, sticky="w")
detalle_telefono = ctk.CTkEntry(frame_detalle, placeholder_text="Número de teléfono")
detalle_telefono.grid(row=11, column=0, padx=10, pady=5, sticky="ew")

# --- Columna 2 ---
ctk.CTkLabel(frame_detalle, text="CÉDULA PROFESIONAL", text_color="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
detalle_cedula = ctk.CTkEntry(frame_detalle, placeholder_text="Cédula profesional")
detalle_cedula.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="CORREO ELECTRÓNICO", text_color="white").grid(row=2, column=1, padx=10, pady=5, sticky="w")
detalle_correo = ctk.CTkEntry(frame_detalle, placeholder_text="ejemplo@correo.com")
detalle_correo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="DIRECCIÓN", text_color="white").grid(row=4, column=1, padx=10, pady=5, sticky="w")
detalle_direccion = ctk.CTkEntry(frame_detalle, placeholder_text="Dirección completa")
detalle_direccion.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="FECHA DE NACIMIENTO", text_color="white").grid(row=6, column=1, padx=10, pady=5, sticky="w")
detalle_fecha_nacimiento = ctk.CTkEntry(frame_detalle, placeholder_text="AAAA-MM-DD")
detalle_fecha_nacimiento.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

ctk.CTkLabel(frame_detalle, text="TIPO DE SANGRE", text_color="white").grid(row=8, column=1, padx=10, pady=5, sticky="w")
tipos_sangre = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
combo_tipo_sangre = ctk.CTkComboBox(frame_detalle, values=tipos_sangre)
combo_tipo_sangre.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
combo_tipo_sangre.set(tipos_sangre[0]) 

ctk.CTkLabel(frame_detalle, text="GÉNERO", text_color="white").grid(row=10, column=1, padx=10, pady=5, sticky="w")
generos = ["Masculino", "Femenino", "Otro"]
combo_genero = ctk.CTkComboBox(frame_detalle, values=generos)
combo_genero.grid(row=11, column=1, padx=10, pady=5, sticky="ew")
combo_genero.set(generos[0]) 






# Frame Botones
frame_botones = ctk.CTkFrame(frame_contenedor, fg_color="#d718aa", corner_radius=10)
frame_botones.pack(padx=10, pady=10, side="right", fill="y")

# Botones con comandos asignados
boton_guardar = ctk.CTkButton(frame_botones, text="INSERTAR", fg_color="green", text_color="white", command=guardar)
boton_guardar.pack(padx=10, pady=15, side='top')

boton_actualizar_lista = ctk.CTkButton(frame_botones, text="ACTUALIZAR LISTA", fg_color="black", text_color="white", command=listar_doctores)
boton_actualizar_lista.pack(padx=10, pady=15, side='top')

boton_cancelar = ctk.CTkButton(frame_botones, text="CANCELAR", fg_color="orange", text_color="white", command=limpiar_campos)
boton_cancelar.pack(padx=10, pady=15, side='top') 
boton_modificar = ctk.CTkButton(frame_botones, text="MODIFICAR", fg_color="black", text_color="white")
boton_modificar.pack(padx=10, pady=15, side='top')
boton_eliminar = ctk.CTkButton(frame_botones, text="ELIMINAR", fg_color="black", text_color="white")
boton_eliminar.pack(padx=10, pady=15, side='top')

# Frame para la Tabla de Doctores
listadodocs_frame = ctk.CTkFrame(Ventana_Doctor, fg_color="red")
listadodocs_frame.pack(pady=10, padx=10, fill="both", expand=True, side='bottom')

listar_doctores()

Ventana_Doctor.mainloop()