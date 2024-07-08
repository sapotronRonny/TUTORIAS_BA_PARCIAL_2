import pyodbc
import index
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape   
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import re

def limpiar_pantalla():
    # Clear screen command based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')
        
    
    
def mostrar_menu():
    print("\nMenu de Opciones:")
    print("1. Agregar usuario")
    print("2. Mostrar usuarios")
    print("3. Modificar usuarios")
    print("4. eliminar usuario")
    print("5. Generacion de disparadores de Auditoria")
    print("6. Logs")
    print("7. SALIR")



# CREAR USUARIOS

def opcion1(cursor,conn):
    limpiar_pantalla()
    print("Agregar Nuevo Usuario")
    nombre_usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    correo_electronico = input("Correo electrónico: ")

    try:
        cursor.execute("INSERT INTO Usuarios (nombre_usuario, contraseña, correo_electronico) VALUES (?, ?, ?)",
                       (nombre_usuario, contraseña, correo_electronico))
        conn.commit()
        print("Usuario agregado exitosamente.")
    except pyodbc.Error as e:
        print(f"Error al agregar usuario: {e}")
    index.main()


# MOSTRAR USUARIOS

def opcion2(cursor):
    limpiar_pantalla()
    print("Lista de Usuarios")
    try:
        cursor.execute("SELECT id_usuario, nombre_usuario, correo_electronico FROM Usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            for usuario in usuarios:
                print(f"ID: {usuario.id_usuario}, Usuario: {usuario.nombre_usuario}, Correo: {usuario.correo_electronico}")
        else:
            print("No hay usuarios en la base de datos.")
    except pyodbc.Error as e:
        print(f"Error al recuperar usuarios: {e}")
    input("\nPresione Enter para continuar...")
    index.main()
    
    
   # BLOQUE DE MODIFICACION DE USUARIOS.
    # MODIFICAR NOMBRE DE USUARIO
def modificar_nombre(cursor, conn, id_usuario):
    limpiar_pantalla()
    nuevo_nombre = input("Nuevo nombre de usuario: ")
    try:
        cursor.execute("UPDATE Usuarios SET nombre_usuario = ? WHERE id_usuario = ?", (nuevo_nombre, id_usuario))
        conn.commit()
        if cursor.rowcount > 0:
            print("Nombre de usuario modificado exitosamente.")
        else:
            print("Usuario no encontrado.")
    except pyodbc.Error as e:
        print(f"Error al modificar nombre de usuario: {e}")
    input("\nPresione Enter para continuar...")

# MODIFICAR CONTRASEÑA DE USUARIO
def modificar_contraseña(cursor, conn, id_usuario):
    limpiar_pantalla()
    nueva_contraseña = input("Nueva contraseña: ")
    try:
        cursor.execute("UPDATE Usuarios SET contraseña = ? WHERE id_usuario = ?", (nueva_contraseña, id_usuario))
        conn.commit()
        if cursor.rowcount > 0:
            print("Contraseña modificada exitosamente.")
        else:
            print("Usuario no encontrado.")
    except pyodbc.Error as e:
        print(f"Error al modificar contraseña: {e}")
    input("\nPresione Enter para continuar...")

# MODIFICAR USUARIO
def opcion3(cursor, conn):
    limpiar_pantalla()
    print("Lista de Usuarios")
    cursor.execute("SELECT id_usuario, nombre_usuario, correo_electronico FROM Usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        for usuario in usuarios:
            print(f"ID: {usuario.id_usuario}, Usuario: {usuario.nombre_usuario}, Correo: {usuario.correo_electronico}")
    else:
        print("No hay usuarios en la base de datos.")
        input("\nPresione Enter para continuar...")
        return
    
    id_usuario = input("\nID de usuario a modificar (o 'C' para cancelar): ")

    if id_usuario.upper() == 'C':
        print("Operación cancelada.")
        input("\nPresione Enter para continuar...")
        return
    
    while True:
        limpiar_pantalla()
        print("Opciones de modificación:")
        print("1. Modificar nombre de usuario")
        print("2. Modificar contraseña de usuario")
        print("3. Cancelar")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            modificar_nombre(cursor, conn, id_usuario)
            break
        elif opcion == '2':
            modificar_contraseña(cursor, conn, id_usuario)
            break
        elif opcion == '3':
            print("Operación cancelada.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    
    input("\nPresione Enter para continuar...")    


# ELIMINAR USUARIO

def opcion4(cursor, conn):
    limpiar_pantalla()
    print("Lista de Usuarios")
    cursor.execute("SELECT id_usuario, nombre_usuario, correo_electronico FROM Usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
            for usuario in usuarios:
                print(f"ID: {usuario.id_usuario}, Usuario: {usuario.nombre_usuario}, Correo: {usuario.correo_electronico}")
    else:
            print("No hay usuarios en la base de datos.")
    
    print("Eliminar Usuario")
    id_usuario = input("ID de usuario a eliminar (o 'C' para cancelar): ")
    
    if id_usuario.upper() == 'C':
        print("Operación cancelada.")
        input("\nPresione Enter para continuar...")
        return

    try:
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Usuario eliminado exitosamente.")
        else:
            print("Usuario no encontrado.")
    except pyodbc.Error as e:
        print(f"Error al eliminar usuario: {e}")
    index.main()
    
    
    
def obtener_columnas_tabla(cursor, tabla):
    cursor.execute(f"SHOW COLUMNS FROM {tabla}")
    columnas = cursor.fetchall()
    nombres_columnas = [columna[0] for columna in columnas]
    return nombres_columnas


def obtener_columnas_tabla(cursor, tabla):
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabla}'")
    return [row[0] for row in cursor.fetchall()]

def crear_funcion_trigger(cursor, tabla):
    columnas = obtener_columnas_tabla(cursor, tabla)

    insert_values = ", ".join([f"'{columna}', inserted.{columna}" for columna in columnas])
    update_values = ", ".join([f"'{columna}', deleted.{columna}, '{columna}', inserted.{columna}" for columna in columnas])
    delete_values = ", ".join([f"'{columna}', deleted.{columna}" for columna in columnas])

    funcion_insert_sqlserver = f"""
    CREATE TRIGGER audit_{tabla}_after_insert
    ON {tabla}
    AFTER INSERT
    AS
    BEGIN
        INSERT INTO auditoria (nombre_tabla, usuario_db, accion, descripcion_cambios)
        SELECT '{tabla}', SYSTEM_USER, 'INSERT', (
            SELECT {insert_values}
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )
        FROM inserted;
    END;
    """

    funcion_update_sqlserver = f"""
    CREATE TRIGGER audit_{tabla}_after_update
    ON {tabla}
    AFTER UPDATE
    AS
    BEGIN
        INSERT INTO auditoria (nombre_tabla, usuario_db, accion, descripcion_cambios)
        SELECT '{tabla}', SYSTEM_USER, 'UPDATE', (
            SELECT {update_values}
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )
        FROM inserted
        INNER JOIN deleted ON inserted.id = deleted.id; -- Suponiendo que 'id' es la clave primaria
    END;
    """

    funcion_delete_sqlserver = f"""
    CREATE TRIGGER audit_{tabla}_after_delete
    ON {tabla}
    AFTER DELETE
    AS
    BEGIN
        INSERT INTO auditoria (nombre_tabla, usuario_db, accion, descripcion_cambios)
        SELECT '{tabla}', SYSTEM_USER, 'DELETE', (
            SELECT {delete_values}
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )
        FROM deleted;
    END;
    """

    try:
        cursor.execute(funcion_insert_sqlserver)
        cursor.commit()
    except pyodbc.Error as err:
        print(f"Error al ejecutar el disparador INSERT para {tabla}: {err}")

    try:
        cursor.execute(funcion_update_sqlserver)
        cursor.commit()
    except pyodbc.Error as err:
        print(f"Error al ejecutar el disparador UPDATE para {tabla}: {err}")

    try:
        cursor.execute(funcion_delete_sqlserver)
        cursor.commit()
    except pyodbc.Error as err:
        print(f"Error al ejecutar el disparador DELETE para {tabla}: {err}")

    return funcion_insert_sqlserver, funcion_update_sqlserver, funcion_delete_sqlserver



def opcion5(cursor):
    print("Ejecutando Opción 5...")

    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tablas = cursor.fetchall()

    print("\nTablas disponibles en la base de datos:")
    for idx, tabla in enumerate(tablas):
        print(f"{idx + 1}. {tabla[0]}")

    seleccion = input("\nSeleccione las tablas para auditar (separadas por coma, o 'all' para todas): ")

    if seleccion.lower() == 'all':
        tablas_seleccionadas = [tabla[0] for tabla in tablas]
    else:
        try:
            indices = map(int, seleccion.split(','))
            tablas_seleccionadas = [tablas[idx - 1][0] for idx in indices]
        except ValueError:
            print("Selección inválida. Por favor, use números separados por comas.")
            return

    with open("auditoria_triggers.sql", "w", encoding="utf-8") as sql_file:
        for tabla in tablas_seleccionadas:
            if tabla.lower() != 'auditoria':
                funciones_sql = crear_funcion_trigger(cursor, tabla)
                for funcion_sql in funciones_sql:
                    sql_file.write(funcion_sql)
                    sql_file.write("\n\n")  # Separador entre funciones

    print("\nDisparadores de auditoría creados exitosamente y guardados en 'auditoria_triggers.sql'.")
    





def obtener_logs(cursor, usuario, fecha_inicio, fecha_fin):
    query = f"""
    SELECT fecha_hora, log_entry
    FROM logs
    WHERE usuario = ?
      AND fecha_hora BETWEEN ? AND ?
    """
    cursor.execute(query, (usuario, fecha_inicio, fecha_fin))
    return [{'fecha_hora': row[0], 'linea': row[1]} for row in cursor.fetchall()]

def generar_pdf(logs, usuario, fecha_inicio, fecha_fin):
    pdf_filename = f'reporte_logs_{usuario}_{fecha_inicio.replace(":", "-").replace(" ", "_")}_a_{fecha_fin.replace(":", "-").replace(" ", "_")}.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        name='CustomStyle',
        fontSize=9,
        leading=10,
        spaceAfter=4,
        wordWrap='CJK'
    )
    date_time_style = ParagraphStyle(
        name='DateTimeStyle',
        fontSize=9,
        leading=10,
        spaceAfter=4,
        wordWrap='CJK',
        alignment=1
    )
    elements = []

    title = f"Reporte: Logs de SQL Server\nUsuario: {usuario}\nDesde: {fecha_inicio}\nHasta: {fecha_fin}"
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))

    col_widths = [100, 500]
    data = [["Fecha y Hora", "Log Entry"]]

    for log in logs:
        data.append([
            Paragraph(str(log['fecha_hora']), date_time_style),
            Paragraph(log['linea'], custom_style)
        ])

    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.cyan),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    elements.append(table)
    doc.build(elements)
    print(f"PDF generado exitosamente en '{pdf_filename}'")
    
def obtener_usuarios(cursor):
    cursor.execute("SELECT name FROM sys.sql_logins WHERE type_desc = 'SQL_LOGIN';")
    return [usuario[0] for usuario in cursor.fetchall()]

def validar_fechas(fecha_inicio, fecha_fin, cursor):
    try:
        cursor.execute("DECLARE @fecha_inicio NVARCHAR(19) = ?; "
                       "DECLARE @fecha_fin NVARCHAR(19) = ?; "
                       "SELECT TRY_CAST(@fecha_inicio AS DATETIME) AS fecha_inicio, TRY_CAST(@fecha_fin AS DATETIME) AS fecha_fin;",
                       fecha_inicio, fecha_fin)
        row = cursor.fetchone()
        if row and row.fecha_inicio is not None and row.fecha_fin is not None:
            return True
        else:
            print("Formato de fecha y hora incorrecto. Por favor, use el formato 'YYYY-MM-DD HH:MM:SS'.")
            return False
    except pyodbc.Error as e:
        print(f"Error al validar fechas: {e}")
        return False

import re

def leer_logs_en_rango(log_directory, fecha_inicio, fecha_fin, usuario, cursor):
    logs_combinados = []
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M:%S")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Formato de fecha y hora incorrecto.")
        return []

    log_files = sorted(os.listdir(log_directory))
    for log_file in log_files:
        if not log_file.endswith('.log'):
            continue

        log_path = os.path.join(log_directory, log_file)
        if os.path.getsize(log_path) > 0:
            with open(log_path, 'rb') as file:
                raw_data = file.read()
                try:
                    decoded_data = raw_data.decode('utf-8')
                except UnicodeDecodeError:
                    decoded_data = raw_data.decode('utf-8', errors='replace')

                for line in decoded_data.splitlines():
                    match = re.match(
                        r"(?P<fecha_hora>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",  # Ajustar según el formato de tu log
                        line
                    )
                    if match:
                        log_fecha = datetime.strptime(match.group("fecha_hora"), "%Y-%m-%d %H:%M:%S")
                        if fecha_inicio_dt <= log_fecha <= fecha_fin_dt:
                            log_entry = {
                                'fecha_hora': log_fecha.strftime("%Y-%m-%d %H:%M:%S"),
                                'linea': line
                            }
                            logs_combinados.append(log_entry)
    return logs_combinados

def generar_pdf(logs, usuario, fecha_inicio, fecha_fin):
    pdf_filename = f'reporte_logs_{usuario}_{fecha_inicio.replace(":", "-").replace(" ", "_")}_a_{fecha_fin.replace(":", "-").replace(" ", "_")}.pdf'
    # Resto del código de generación del PDF omitido por simplicidad

def opcion6(cursor):
    print("Ejecutando Opción 6...")

    usuarios = obtener_usuarios(cursor)
    print("\nUsuarios disponibles:")
    for idx, usuario in enumerate(usuarios):
        print(f"{idx + 1}. {usuario}")

    seleccion_usuario = input("\nSeleccione un usuario (número): ")
    try:
        usuario = usuarios[int(seleccion_usuario) - 1]
    except (IndexError, ValueError):
        print("Selección de usuario inválida.")
        return

    while True:
        fecha_inicio = input("Ingrese la fecha y hora de inicio (YYYY-MM-DD HH:MM:SS): ")
        fecha_fin = input("Ingrese la fecha y hora de fin (YYYY-MM-DD HH:MM:SS): ")
        if validar_fechas(fecha_inicio, fecha_fin, cursor):
            break

    log_directory = r"C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Log"  # Ajustar la ruta al directorio de logs de SQL Server
    logs = leer_logs_en_rango(log_directory, fecha_inicio, fecha_fin, usuario, cursor)

    if not logs:
        print("No se encontraron registros para los criterios especificados.")
    else:
        print("\nContenido de los logs seleccionados:\n")
        for log in logs:
            print(f"{log['fecha_hora']} - {log['linea']}")

        pdf_filename = input("Ingrese el nombre del archivo PDF a generar: ") + ".pdf"
        generar_pdf(logs, usuario, fecha_inicio, fecha_fin)

