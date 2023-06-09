from client.interfaz import mostrar_menu_inicio, mostrar_menu_gestion ,menu_inicio_sesion, menu_registro, solicitar_dato

from model.recopilarDatos import RecopilarDatos
from model.empleado import Empleado
from model.conexion import Conexion
from model.usuario import validar_credenciales, registrar_usuario

def agregar_empleado():
    formulario = RecopilarDatos()

    info_personal =formulario.recoger_informacion_personal()
    info_laboral = formulario.recoger_informacion_laboral()
    contacto_emergencia = formulario.recoger_contacto_emergencia()
    carga_familiar = formulario.recoger_carga_familiar()

    nuevo_empleado = Empleado(info_personal, info_laboral, contacto_emergencia, carga_familiar)
    nuevo_empleado.ingresar_informacion()
    nuevo_empleado.mostrar_informacion()

def crear_perfil():
    formulario = RecopilarDatos()

    usuario_datos, id_empleado, rut_empleado = formulario.recoger_informacion_usuario()
    usuario_datos.ingresar_perfil(id_empleado, rut_empleado)

def actualizar_empleado():
    formulario = RecopilarDatos()

    rut = solicitar_dato("Introduce el RUT del empleado a actualizar: ")
    id_filtrado, _= Empleado.obtener_id(rut)

    if id_filtrado is not None:

        empleado = Empleado.obtener_empleado(id_filtrado)

        print(empleado)

        nombre, rut, sexo, direccion, telefono = formulario.recoger_nueva_informacion_personal()

        # Verificar si se proporcionó un valor para cada campo y actualizar solo los campos no vacíos
        if nombre != "":
            empleado.info_personal.nombre = nombre
        if rut != "":
            empleado.info_personal.rut = rut
        if sexo != "":
            empleado.info_personal.sexo = sexo
        if direccion != "":
            empleado.info_personal.direccion = direccion
        if telefono != "":
            empleado.info_personal.telefono = telefono

        empleado.actualizar_informacion_personal(id_filtrado)

def gestion_empleados():
    while True:
        mostrar_menu_gestion()
        opcion = solicitar_dato("Escoge una opcion: ")
        menu_opciones = {
            "1": Empleado.mostrar_lista_empleados,
            "2": agregar_empleado,
            "3": lambda: None,
            "4": actualizar_empleado,
            "5": crear_perfil,
            "6": lambda: False
        }

        if opcion in menu_opciones:
            continuar = menu_opciones[opcion]()
            if continuar is False:
                print("Se ha cerrado correctamente.")
                break
        else:
            print("\nOpcion no valida. Por favor, intentalo de nuevo.")

def main():
    conexion = Conexion()
    conexion.crear_tablas()
    conexion.cerrar_conexion()

    while True:
        mostrar_menu_inicio()
        opcion = solicitar_dato("Escoge una opcion: ")

        try:
            if opcion == "1":
                nombre_usuario, clave = menu_inicio_sesion()
                if nombre_usuario is None or clave is None:
                    continue
                valido, tipo_perfil= validar_credenciales(nombre_usuario, clave)
                if valido:
                    if tipo_perfil == "administrador":
                        gestion_empleados()
                    elif tipo_perfil == "normal":
                        print("Tu tipo de perfil es normal, estamos trabajando para implementar tu menu.")

            elif opcion == "2":
                nombre_usuario, rut_empleado, clave, clave_repetida, tipo_perfil = menu_registro()
                if nombre_usuario is None:
                    continue
                resultado = registrar_usuario(nombre_usuario, rut_empleado, clave, clave_repetida, tipo_perfil)
                print(resultado)

            elif opcion == "3":
                print("\nGracias por utilizar nuestro software.")
                break
            else:
                print("\nOpcion no valida. Por favor, intentalo de nuevo.")

        except Exception as error:
            print(f"No se ha podido ingresar correctamente: {error}")


    # app.mainloop()
    # app = Ventana()

if __name__ == '__main__':
    main()