# main/Medicion/motor.py

from main.Medicion.generador import generar_datos
from main.Medicion.temporizador import medir_tiempo
from Busqueda import Binaria
from Estructuras_Lineales import Pila, Cola


def medir_ordenamiento(algoritmo, n, escenario, repeticiones=5):
    datos = generar_datos(n, escenario)
    return medir_tiempo(algoritmo, datos.copy(), repeticiones=repeticiones)


def medir_busqueda(algoritmo, n, escenario, repeticiones=5):
    datos = generar_datos(n, escenario)

    # Binaria requiere arreglo ordenado
    if algoritmo == Binaria:
        datos.sort()

    objetivo = datos[len(datos) // 2]
    return medir_tiempo(algoritmo, datos, objetivo, repeticiones=repeticiones)


def medir_estructuras(tipo, n, repeticiones=5):
    if tipo == "pila":
        pila = Pila()
        return medir_tiempo(_test_pila, pila, n, repeticiones=repeticiones)

    if tipo == "cola":
        cola = Cola()
        return medir_tiempo(_test_cola, cola, n, repeticiones=repeticiones)

    raise ValueError("Tipo inválido. Usa 'pila' o 'cola'.")


def _test_pila(pila, n):
    for i in range(n):
        pila.push(i)
    for _ in range(n):
        pila.pop()


def _test_cola(cola, n):
    for i in range(n):
        cola.enqueue(i)
    for _ in range(n):
        cola.dequeue()
