# main/Resultados/registro.py
import csv
import os
from datetime import datetime

DEFAULT_CSV_PATH = os.path.join("resultados", "resultados.csv")

HEADERS = [
    "timestamp",
    "modulo",
    "algoritmo",
    "n",
    "escenario",
    "repeticiones",
    "tiempo_prom_ns",
]

def guardar_resultado(modulo, algoritmo, n, escenario, repeticiones, tiempo_ns, csv_path=DEFAULT_CSV_PATH):
    # Crea carpeta /resultados si no existe (en la raíz del proyecto)
    carpeta = os.path.dirname(csv_path)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    existe = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not existe:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "modulo": modulo,
            "algoritmo": algoritmo,
            "n": int(n),
            "escenario": escenario,
            "repeticiones": int(repeticiones),
            "tiempo_prom_ns": float(tiempo_ns),
        })
