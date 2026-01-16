import random

def generar_datos(n, escenario):
    if escenario == "MC":  # Mejor Caso
        return list(range(n))
    elif escenario == "PC":  # Peor Caso
        return list(range(n, 0, -1))
    else:  # Caso Promedio
        datos = list(range(n))
        random.shuffle(datos)
        return datos
