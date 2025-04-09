class Cola:
    def __init__(self, limite=None):
        # Inicializa la cola con un límite opcional.
        self.items = []
        self.limite = limite

    def agregar(self, item):
        # Agrega un elemento al final de la cola.
        if self.limite is None or len(self.items) < self.limite:
            self.items.append(item)
        else:
            raise Exception("Límite de cola alcanzado")

    def eliminar(self):
    
        # Elimina y retorna el primer elemento de la cola.
        if not self.esta_vacia():
            return self.items.pop(0)
        raise Exception("Cola vacía")

    def primero(self):
        # Retorna el primer elemento sin eliminarlo.
        if not self.esta_vacia():
            return self.items[0]
        return None

    def esta_vacia(self):
        # Verifica si la cola está vacía.
        return len(self.items) == 0

    def tamanio(self):
        #Retorna el número de elementos en la cola.
        return len(self.items)
