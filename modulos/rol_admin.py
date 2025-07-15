import os
from modulos.gestion_archivos import cargar_ninjas, guardar_ninjas

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_admin():
    """Muestra el menú de administrador y gestiona sus opciones."""
    ninjas = cargar_ninjas()

    while True:
        limpiar_pantalla()
        print("--- MENÚ DE ADMINISTRADOR ---")
        print("1. Agregar nuevo ninja")
        print("2. Listar todos los ninjas")
        print("3. Actualizar atributos de un ninja")
        print("4. Eliminar un ninja")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_ninja(ninjas)
            guardar_ninjas(ninjas)
        elif opcion == '2':
            listar_ninjas(ninjas)
        elif opcion == '3':
            actualizar_ninja(ninjas)
            guardar_ninjas(ninjas)
        elif opcion == '4':
            eliminar_ninja(ninjas)
            guardar_ninjas(ninjas)
        elif opcion == '5':
            print("Guardando cambios y saliendo...")
            break
        else:
            print("Opción no válida.")
        input("\nPresiona Enter para continuar...")

def agregar_ninja(ninjas):
    """Agrega un nuevo ninja a la lista."""
    print("\n--- Agregar Nuevo Ninja ---")
    try:
        # ID automático basado en el último ninja
        nuevo_id = max(n['id'] for n in ninjas) + 1 if ninjas else 1
        nombre = input("Nombre del ninja: ")
        fuerza = int(input("Fuerza (1-100): "))
        agilidad = int(input("Agilidad (1-100): "))
        resistencia = int(input("Resistencia (1-100): "))
        
        nuevo_ninja = {
            'id': nuevo_id,
            'nombre': nombre,
            'fuerza': fuerza,
            'agilidad': agilidad,
            'resistencia': resistencia,
            'victorias': 0
        }
        ninjas.append(nuevo_ninja)
        print(f"\n¡Ninja '{nombre}' agregado con éxito!")
    except ValueError:
        print("Error: Fuerza, agilidad y resistencia deben ser números enteros.")

def listar_ninjas(ninjas):
    """Muestra una lista de todos los ninjas."""
    print("\n--- Listado de Ninjas ---")
    if not ninjas:
        print("No hay ninjas registrados.")
        return
        
    # Ordena por ID para mostrar
    ninjas_ordenados = sorted(ninjas, key=lambda x: x['id'])
    for n in ninjas_ordenados:
        print(f"ID: {n['id']} | Nombre: {n['nombre']} | F:{n['fuerza']} A:{n['agilidad']} R:{n['resistencia']} | Victorias: {n['victorias']}")

def buscar_ninja_por_id(ninjas, id_buscado):
    """Busca un ninja por su ID (búsqueda lineal)."""
    for ninja in ninjas:
        if ninja['id'] == id_buscado:
            return ninja
    return None

def actualizar_ninja(ninjas):
    """Actualiza los datos de un ninja existente."""
    print("\n--- Actualizar Ninja ---")
    listar_ninjas(ninjas)
    try:
        id_actualizar = int(input("\nIngrese el ID del ninja a actualizar: "))
        ninja = buscar_ninja_por_id(ninjas, id_actualizar)

        if ninja:
            print(f"Actualizando a {ninja['nombre']}. Deje en blanco para no cambiar un valor.")
            
            nuevo_nombre = input(f"Nuevo nombre ({ninja['nombre']}): ")
            if nuevo_nombre: ninja['nombre'] = nuevo_nombre

            nueva_fuerza = input(f"Nueva fuerza ({ninja['fuerza']}): ")
            if nueva_fuerza: ninja['fuerza'] = int(nueva_fuerza)
            
            nueva_agilidad = input(f"Nueva agilidad ({ninja['agilidad']}): ")
            if nueva_agilidad: ninja['agilidad'] = int(nueva_agilidad)
            
            nueva_resistencia = input(f"Nueva resistencia ({ninja['resistencia']}): ")
            if nueva_resistencia: ninja['resistencia'] = int(nueva_resistencia)

            print("¡Ninja actualizado con éxito!")
        else:
            print("ID de ninja no encontrado.")
    except ValueError:
        print("Error: El ID debe ser un número.")

def eliminar_ninja(ninjas):
    """Elimina un ninja de la lista."""
    print("\n--- Eliminar Ninja ---")
    listar_ninjas(ninjas)
    try:
        id_eliminar = int(input("\nIngrese el ID del ninja a eliminar: "))
        ninja = buscar_ninja_por_id(ninjas, id_eliminar)

        if ninja:
            confirmacion = input(f"¿Está seguro de que desea eliminar a {ninja['nombre']}? (s/n): ").lower()
            if confirmacion == 's':
                ninjas.remove(ninja)
                print("¡Ninja eliminado con éxito!")
            else:
                print("Operación cancelada.")
        else:
            print("ID de ninja no encontrado.")
    except ValueError:
        print("Error: El ID debe ser un número.")