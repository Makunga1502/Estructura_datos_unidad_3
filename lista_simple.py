

class Nodo:
    def __init__(self, dato: int):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
 
    def __init__(self):
        self.cabeza = None

    def insertar_al_inicio(self, nuevo_dato: int):
       
        nuevo_nodo = Nodo(nuevo_dato)
        nuevo_nodo.siguiente = self.cabeza

        self.cabeza = nuevo_nodo
        print(f"Insertando a inicio {nuevo_dato}")

    def insertar_al_final(self, nuevo_dato: int):
        nuevo_nodo = Nodo(nuevo_dato)

    
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            print(f"Insertando al final (Lista vacia) {nuevo_dato}")
            return

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente

      
        actual.siguiente = nuevo_nodo
        print(f"Insertando al final {nuevo_dato}")

    def imprimir_lista(self):
        actual = self.cabeza
        print("Lista simple")

        while actual is not None:
            print(f"{actual.dato}->")
            actual = actual.siguiente

        print("Null")


def main():
    lista = ListaEnlazada()
    lista.insertar_al_inicio(3)
    lista.insertar_al_inicio(2)
    lista.insertar_al_inicio(1)

    lista.insertar_al_final(4)
    lista.insertar_al_final(5)

    lista.imprimir_lista()


if __name__ == "__main__":
    main()
