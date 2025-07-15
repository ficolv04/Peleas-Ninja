import random
import time
from datetime import datetime
from modulos.estructuras import ArbolBinario, Cola
from modulos.gestion_archivos import registrar_combate, guardar_ninjas

def construir_arbol_habilidades(id_ninja, habilidades_db):
    """Construye un árbol binario con las habilidades de un ninja."""
    arbol = ArbolBinario()
    if id_ninja in habilidades_db:
        for habilidad in habilidades_db[id_ninja]:
            arbol.insertar(habilidad)
    return arbol

def simular_combate_1v1(ninja1, ninja2, habilidades_db, lista_ninjas_completa):
    """Simula un combate uno a uno entre dos ninjas."""
    print(f"\n💥 ¡COMIENZA EL COMBATE: {ninja1['nombre']} vs {ninja2['nombre']}! 💥")
    
    arbol1 = construir_arbol_habilidades(ninja1['id'], habilidades_db)
    arbol2 = construir_arbol_habilidades(ninja2['id'], habilidades_db)

    # Fórmula simple de poder de combate
    poder1 = (ninja1['fuerza'] * 0.4) + (ninja1['agilidad'] * 0.4) + (ninja1['resistencia'] * 0.2)
    poder2 = (ninja2['fuerza'] * 0.4) + (ninja2['agilidad'] * 0.4) + (ninja2['resistencia'] * 0.2)
    
    # Simulación de turnos con estrategias basadas en recorridos
    for i in range(3):
        print(f"\n--- Turno {i+1} ---")
        time.sleep(1)
        
        # Estrategia Ninja 1
        if poder1 > poder2: # Si va ganando, usa preorden (ofensivo)
            estrategia1 = arbol1.preorden()
            print(f"{ninja1['nombre']} ataca con una estrategia ofensiva!")
        elif poder1 < poder2: # Si va perdiendo, usa postorden (defensivo)
            estrategia1 = arbol1.postorden()
            print(f"{ninja1['nombre']} usa una táctica defensiva!")
        else: # Empate, usa inorden (equilibrado)
            estrategia1 = arbol1.inorden()
            print(f"{ninja1['nombre']} mantiene una postura equilibrada.")
        
        if estrategia1:
            print(f"Técnica usada: {random.choice(estrategia1)}")
            poder1 += random.uniform(-2, 5) # Pequeño factor aleatorio

        # Estrategia Ninja 2
        if poder2 > poder1:
            estrategia2 = arbol2.preorden()
            print(f"{ninja2['nombre']} responde con una fuerte ofensiva!")
        else:
            estrategia2 = arbol2.inorden()
            print(f"{ninja2['nombre']} busca una apertura...")

        if estrategia2:
            print(f"Técnica usada: {random.choice(estrategia2)}")
            poder2 += random.uniform(-2, 5)
    
    time.sleep(1)
    print("\n--- ¡RESULTADO FINAL! ---")
    
    if poder1 > poder2:
        ganador = ninja1
        perdedor = ninja2
    else:
        ganador = ninja2
        perdedor = ninja1

    print(f"🏆 El ganador es: {ganador['nombre']} 🏆")

    # Actualizar victorias y guardar
    for n in lista_ninjas_completa:
        if n['id'] == ganador['id']:
            n['victorias'] += 1
            break
    
    guardar_ninjas(lista_ninjas_completa)
    registrar_combate(ganador['nombre'], perdedor['nombre'], datetime.now().strftime("%d/%m/%Y"))
    
    return ganador

def simular_torneo(ninjas, habilidades_db):
    """Simula un torneo completo de eliminación simple."""
    if len(ninjas) < 2:
        print("No hay suficientes ninjas para un torneo.")
        return

    # Clonamos y barajamos la lista para no afectar la original y tener torneos diferentes
    participantes = list(ninjas)
    random.shuffle(participantes)
    
    cola_torneo = Cola()
    for p in participantes:
        cola_torneo.encolar(p)
        
    ronda = 1
    while len(cola_torneo) > 1:
        print(f"\n\n--- RONDA {ronda} ---")
        combatientes_siguiente_ronda = Cola()
        
        while not cola_torneo.esta_vacia():
            # Sacamos dos combatientes
            ninja1 = cola_torneo.desencolar()
            if cola_torneo.esta_vacia(): # Si queda un número impar, pasa directo
                print(f"{ninja1['nombre']} pasa a la siguiente ronda sin combatir.")
                combatientes_siguiente_ronda.encolar(ninja1)
                break
            ninja2 = cola_torneo.desencolar()

            # Simular combate y el ganador avanza
            ganador_ronda = simular_combate_1v1(ninja1, ninja2, habilidades_db, ninjas)
            combatientes_siguiente_ronda.encolar(ganador_ronda)
            input("Presiona Enter para el siguiente combate...")

        cola_torneo = combatientes_siguiente_ronda
        ronda += 1
    
    campeon = cola_torneo.desencolar()
    print(f"\n\n👑 ¡¡¡EL CAMPEÓN DEL TORNEO ES {campeon['nombre']}!!! 👑")