import os
import getpass
import re
from modulos.gestion_archivos import (
    cargar_ninjas, cargar_habilidades, cargar_usuarios, 
    guardar_nuevo_usuario
)
from modulos.combate import simular_combate_1v1, construir_arbol_habilidades, simular_torneo
import hashlib

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def quick_sort(lista, clave='victorias'):
    """Algoritmo QuickSort para ordenar ninjas por una clave."""
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[len(lista) // 2]
        menores = [x for x in lista if x[clave] > pivot[clave]]
        iguales = [x for x in lista if x[clave] == pivot[clave] and x != pivot]
        mayores = [x for x in lista if x[clave] < pivot[clave]]
        return quick_sort(menores, clave) + [pivot] + iguales + quick_sort(mayores, clave)

def menu_jugador():
    """Muestra el menú principal para el jugador."""
    ninjas = cargar_ninjas()
    habilidades = cargar_habilidades()
    usuario_actual = None

    while True:
        limpiar_pantalla()
        print(f"--- MENÚ DE JUGADOR --- (Usuario: {usuario_actual or 'Ninguno'})")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        if usuario_actual:
            print("3. Simular Combate 1 vs 1")
            print("4. Simular Torneo Completo")
            print("5. Ver Ranking de Victorias")
            print("6. Ver Árbol de Habilidades de un Ninja")
            print("7. Cerrar Sesión")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            if not usuario_actual:
                usuario_actual = iniciar_sesion()
            else:
                print("Ya hay una sesión iniciada.")
        elif opcion == '3' and usuario_actual:
            menu_combate_1v1(ninjas, habilidades)
        elif opcion == '4' and usuario_actual:
            simular_torneo(ninjas, habilidades)
        elif opcion == '5' and usuario_actual:
            mostrar_ranking(ninjas)
        elif opcion == '6' and usuario_actual:
            ver_arbol_habilidades(ninjas, habilidades)
        elif opcion == '7' and usuario_actual:
            usuario_actual = None
            print("Sesión cerrada con éxito.")
        elif opcion == '8':
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción no válida o requiere iniciar sesión.")
        
        input("\nPresiona Enter para continuar...")


def registrar_usuario():
    """Registra un nuevo jugador."""
    print("\n--- Registro de Nuevo Jugador ---")
    nombre = input("Nombres: ")
    apellido = input("Apellidos: ")
    id_user = input("Identificación: ")
    edad = input("Edad: ")
    usuario = input("Correo electrónico (será tu usuario, ej: nombre.apellido@gmail.com): ")
    
    # Validar contraseña segura
    while True:
        contrasena = getpass.getpass("Contraseña (mín 8 carac, 1 mayús, 1 núm): ")
        if len(contrasena) >= 8 and re.search(r'[A-Z]', contrasena) and re.search(r'[0-9]', contrasena):
            break
        else:
            print("La contraseña no es segura. Inténtalo de nuevo.")

    try:
        guardar_nuevo_usuario(nombre, apellido, id_user, edad, usuario, contrasena)
        print("\n¡Usuario registrado con éxito!")
    except Exception as e:
        print(f"Error al registrar: {e}")

def iniciar_sesion():
    """Autentica a un usuario."""
    print("\n--- Iniciar Sesión ---")
    usuario = input("Usuario (email): ")
    contrasena = getpass.getpass("Contraseña: ")
    
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
    
    usuarios_db = cargar_usuarios()
    for user in usuarios_db:
        if user['usuario'] == usuario and user['contrasena'] == hash_contrasena:
            print("\n¡Inicio de sesión exitoso!")
            return usuario
    
    print("\nUsuario o contraseña incorrectos.")
    return None

def menu_combate_1v1(ninjas, habilidades):
    """Menú para seleccionar ninjas para un combate 1 vs 1."""
    print("\n--- Seleccionar Combatientes ---")
    for n in ninjas:
        print(f"ID: {n['id']} - {n['nombre']}")
    
    try:
        id1 = int(input("ID del primer ninja: "))
        id2 = int(input("ID del segundo ninja: "))

        ninja1 = next((n for n in ninjas if n['id'] == id1), None)
        ninja2 = next((n for n in ninjas if n['id'] == id2), None)

        if ninja1 and ninja2 and id1 != id2:
            simular_combate_1v1(ninja1, ninja2, habilidades, ninjas)
        else:
            print("IDs no válidos o iguales. Inténtalo de nuevo.")
    except ValueError:
        print("Error: El ID debe ser un número.")

def mostrar_ranking(ninjas):
    """Muestra el ranking de ninjas ordenado por victorias."""
    print("\n--- Ranking de Victorias ---")
    # Usamos Quicksort para ordenar por victorias
    ninjas_ordenados = quick_sort(ninjas, 'victorias')
    for i, n in enumerate(ninjas_ordenados, 1):
        print(f"#{i} {n['nombre']} - {n['victorias']} victorias")

def ver_arbol_habilidades(ninjas, habilidades):
    """Muestra el árbol de habilidades de un ninja."""
    print("\n--- Ver Árbol de Habilidades ---")
    for n in ninjas:
        print(f"ID: {n['id']} - {n['nombre']}")
    
    try:
        id_ninja = int(input("ID del ninja para ver sus habilidades: "))
        ninja = next((n for n in ninjas if n['id'] == id_ninja), None)

        if ninja:
            arbol = construir_arbol_habilidades(ninja['id'], habilidades)
            if not arbol.raiz:
                print(f"{ninja['nombre']} no tiene habilidades registradas.")
                return

            print(f"\nEstrategias de {ninja['nombre']}:")
            print(f"Ofensiva (Preorden): {arbol.preorden()}")
            print(f"Equilibrada (Inorden): {arbol.inorden()}")
            print(f"Defensiva (Postorden): {arbol.postorden()}")
        else:
            print("ID no válido.")
    except ValueError:
        print("Error: El ID debe ser un número.")