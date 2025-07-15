import os
from modulos.rol_admin import menu_admin
from modulos.rol_jugador import menu_jugador

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal que ejecuta el programa."""
    while True:
        limpiar_pantalla()
        print("  =====================================")
        print("  |                                   |")
        print("  |   BIENVENIDO AL TORNEO POLI-NINJA   |")
        print("  |                                   |")
        print("  =====================================")
        print("\n  Elige tu rol:")
        print("  1. Administrador")
        print("  2. Jugador")
        print("  3. Salir")
        
        opcion = input("\n  Seleccione una opción: ")

        if opcion == '1':
            # Aquí iría una contraseña de admin si se quisiera
            print("Accediendo al panel de Administrador...")
            menu_admin()
        elif opcion == '2':
            menu_jugador()
        elif opcion == '3':
            print("¡Hasta la próxima!")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()