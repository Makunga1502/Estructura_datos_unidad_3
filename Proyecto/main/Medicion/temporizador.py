import time

def medir_tiempo(funcion, *args, repeticiones=5):
    tiempos = []

    for _ in range(repeticiones):
        inicio = time.perf_counter_ns()
        funcion(*args)
        fin = time.perf_counter_ns()
        tiempos.append(fin - inicio)

    return sum(tiempos) / len(tiempos)
