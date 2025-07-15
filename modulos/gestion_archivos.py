import hashlib

# --- Constantes de Archivos ---
RUTA_NINJAS = 'datos/ninjas.txt'
RUTA_HABILIDADES = 'datos/habilidades_ninja.txt'
RUTA_USUARIOS = 'datos/usuarios.txt'
RUTA_COMBATES = 'datos/combates.txt'

# --- Funciones de Carga de Datos ---

def cargar_ninjas():
    """Carga los ninjas desde ninjas.txt a una lista de diccionarios."""
    ninjas = []
    try:
        with open(RUTA_NINJAS, 'r') as f:
            for linea in f:
                if linea.strip():
                    partes = linea.strip().split(',')
                    ninjas.append({
                        'id': int(partes[0]),
                        'nombre': partes[1],
                        'fuerza': int(partes[2]),
                        'agilidad': int(partes[3]),
                        'resistencia': int(partes[4]),
                        'victorias': int(partes[5])
                    })
    except FileNotFoundError:
        print(f"ERROR: El archivo {RUTA_NINJAS} no fue encontrado.")
    return ninjas

def cargar_habilidades():
    """Carga las habilidades desde habilidades_ninja.txt a un diccionario."""
    habilidades = {}
    try:
        with open(RUTA_HABILIDADES, 'r') as f:
            for linea in f:
                if linea.strip():
                    partes = linea.strip().split(',')
                    id_ninja = int(partes[0])
                    habilidades[id_ninja] = partes[1:]
    except FileNotFoundError:
        print(f"ERROR: El archivo {RUTA_HABILIDADES} no fue encontrado.")
    return habilidades

def cargar_usuarios():
    """Carga los usuarios desde usuarios.txt."""
    usuarios = []
    try:
        with open(RUTA_USUARIOS, 'r') as f:
            for linea in f:
                if linea.strip():
                    partes = linea.strip().split(',')
                    usuarios.append({'usuario': partes[4], 'contrasena': partes[5]})
    except FileNotFoundError:
        open(RUTA_USUARIOS, 'w').close() # Crea el archivo si no existe
    return usuarios

# --- Funciones de Guardado de Datos ---

def guardar_ninjas(ninjas):
    """Guarda la lista de ninjas actualizada en ninjas.txt."""
    with open(RUTA_NINJAS, 'w') as f:
        for ninja in ninjas:
            linea = f"{ninja['id']},{ninja['nombre']},{ninja['fuerza']},{ninja['agilidad']},{ninja['resistencia']},{ninja['victorias']}\n"
            f.write(linea)

def guardar_nuevo_usuario(nombre, apellido, id_user, edad, usuario, contrasena):
    """Guarda un nuevo usuario en usuarios.txt hasheando la contraseña."""
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
    with open(RUTA_USUARIOS, 'a') as f:
        linea = f"{nombre},{apellido},{id_user},{edad},{usuario},{hash_contrasena}\n"
        f.write(linea)

def registrar_combate(ganador, perdedor, fecha):
    """Registra el resultado de un combate en combates.txt."""
    with open(RUTA_COMBATES, 'a') as f:
        linea = f"{ganador} vs {perdedor} – Ganador: {ganador} – Fecha: {fecha}\n"
        f.write(linea)