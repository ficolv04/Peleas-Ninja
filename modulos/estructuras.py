# Archivo: modulos/estructuras.py
from collections import deque

# --- Estructura para el Árbol de Habilidades ---

class NodoArbol:
    """Representa un nodo en el árbol binario de habilidades."""
    def __init__(self, habilidad):
        self.habilidad = habilidad
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    """Organiza las habilidades de un ninja en un árbol binario."""
    def __init__(self):
        self.raiz = None

    def insertar(self, habilidad):
        """Método público para insertar una nueva habilidad en el árbol."""
        if self.raiz is None:
            self.raiz = NodoArbol(habilidad)
        else:
            self._insertar_recursivo(self.raiz, habilidad)

    def _insertar_recursivo(self, nodo, habilidad):
        """Método privado para la inserción recursiva."""
        if habilidad < nodo.habilidad:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(habilidad)
            else:
                self._insertar_recursivo(nodo.izquierda, habilidad)
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(habilidad)
            else:
                self._insertar_recursivo(nodo.derecha, habilidad)

    # --- Métodos de Recorrido para Estrategias de Combate ---

    def preorden(self):
        """Recorrido Preorden (Ofensivo): Raíz -> Izquierda -> Derecha."""
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.habilidad)
            self._preorden_recursivo(nodo.izquierda, resultado)
            self._preorden_recursivo(nodo.derecha, resultado)

    def inorden(self):
        """Recorrido Inorden (Equilibrado): Izquierda -> Raíz -> Derecha."""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierda, resultado)
            resultado.append(nodo.habilidad)
            self._inorden_recursivo(nodo.derecha, resultado)

    def postorden(self):
        """Recorrido Postorden (Defensivo): Izquierda -> Derecha -> Raíz."""
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo, resultado):
        if nodo:
            self._postorden_recursivo(nodo.izquierda, resultado)
            self._postorden_recursivo(nodo.derecha, resultado)
            resultado.append(nodo.habilidad)


# --- Estructura para la Cola del Torneo ---

class Cola:
    """Representa la cola de ninjas para el torneo usando collections.deque."""
    def __init__(self):
        self.items = deque()

    def esta_vacia(self):
        """Verifica si la cola no tiene elementos."""
        return len(self.items) == 0

    def encolar(self, item):
        """Añade un ninja al final de la cola."""
        self.items.append(item)

    def desencolar(self):
        """Saca al primer ninja de la cola."""
        if not self.esta_vacia():
            return self.items.popleft()
        return None
    
    def __len__(self):
        """Permite usar len() para saber el tamaño de la cola."""
        return len(self.items)