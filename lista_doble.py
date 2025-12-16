
class NodoDoble:
    def __init__(self, dato: int):
        self.dato = dato
        self.siguiente = None
        self.previo = None


class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None  

    def insertar_al_final(self, dato: int):
        nuevo = NodoDoble(dato)

        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
            return

        self.cola.siguiente = nuevo
        nuevo.previo = self.cola
        self.cola = nuevo

    def imprimir_hacia_adelante(self):
        actual = self.cabeza
        while actual is not None:
            print(f"{actual.dato}<->")
            actual = actual.siguiente
        print("null")

    def imprimir_hacia_atras(self):
        actual = self.cola
        while actual is not None:
            print(f"{actual.dato}<->")
            actual = actual.previo
        print("null")


if __name__ == "__main__":
    lista = ListaDoblementeEnlazada()
    for x in [1, 2, 3, 4, 5]:
        lista.insertar_al_final(x)

    print("Recorremos hacia adelante")
    lista.imprimir_hacia_adelante()

    print("Recorremos hacia atras")
    lista.imprimir_hacia_atras()
