import pyodbc
import reportlab
import metodos
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def main():
    try:
        # Configura los parámetros de conexión
        server = 'LAPTOP-8S1SSGCK\\SQLEXPRESS' 
        database = 'tutoriasBD'
        username = 'sa'  
        password = '1234'  
        driver = '{ODBC Driver 17 for SQL Server}'

        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        # Conexión a la base de datos
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")

        cursor = conn.cursor()

        while True:
            metodos.mostrar_menu()
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                metodos.opcion1(cursor, conn)
            elif opcion == 2:
                metodos.opcion2(cursor)
            elif opcion == 3:
                metodos.opcion3(cursor,conn)
            elif opcion == 4:
                metodos.opcion4(cursor,conn)
            elif opcion == 5:
                metodos.opcion5(cursor)
            elif opcion == 6:
                metodos.opcion6(cursor)
            elif opcion == 7:
                metodos.opcion7(cursor,conn)
                print('Saliendo del sistema...')
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
                
            # Solo se ejecuta conn.commit() si la opción seleccionada no es 12
            conn.commit()

        # Cierra el cursor y la conexión después de salir del bucle
        cursor.close()
        conn.close()

    except pyodbc.Error as e:
        print(f"Error al conectar con la base de datos: {e}")

if __name__ == "__main__":
    main()
# # Configura los parámetros de conexión
# server = 'LAPTOP-8S1SSGCK\\SQLEXPRESS'  # Cambia esto por el nombre de tu servidor
# database = 'tutoriasBD'
# username = 'sa'  # Cambia esto por tu nombre de usuario
# password = '1234'  # Cambia esto por tu contraseña
# driver = '{ODBC Driver 17 for SQL Server}'

# conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# try:
#     conn = pyodbc.connect(conn_str)
#     print("Conexión exitosa")
# except Exception as e:
#     print("Error al conectar a la base de datos:", e)
#     exit()

# # Crear un cursor
# cursor = conn.cursor()

# # Ejecutar una consulta de prueba
# # try:
# #     cursor.execute('SELECT * FROM Usuarios')  # Cambia esto por una consulta válida en tu base de datos
# #     for row in cursor:
# #         print(row)
# # except Exception as e:
# #     print("Error al ejecutar la consulta:", e)

# # Cerrar la conexión
# conn.close()