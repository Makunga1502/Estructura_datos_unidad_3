# main/Resultados/graficas.py
import os
import csv
from collections import defaultdict

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

DEFAULT_CSV_PATH = os.path.join("resultados", "resultados.csv")


def _leer_csv(csv_path=DEFAULT_CSV_PATH):
    if not os.path.exists(csv_path):
        return []

    filas = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Tipos
            row["n"] = int(row["n"])
            row["repeticiones"] = int(row["repeticiones"])
            row["tiempo_prom_ns"] = float(row["tiempo_prom_ns"])
            filas.append(row)
    return filas


def _promedio_por_grupo(filas, keys):
    # Promedia tiempos por grupo de llaves
    acum = defaultdict(list)
    for r in filas:
        k = tuple(r[key] for key in keys)
        acum[k].append(r["tiempo_prom_ns"])
    prom = {k: sum(v) / len(v) for k, v in acum.items()}
    return prom


def _limpiar_fig(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def abrir_ventana_graficas(parent, csv_path=DEFAULT_CSV_PATH):
    filas = _leer_csv(csv_path)

    if not filas:
        messagebox.showwarning(
            "Sin datos",
            "Aún no hay resultados guardados.\n\nEjecuta pruebas para generar el CSV y luego vuelve aquí."
        )
        return

    win = tk.Toplevel(parent)
    win.title("Gráficas - Rendimiento Algorítmico")
    win.geometry("860x560")
    win.resizable(True, True)

    notebook = ttk.Notebook(win)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- TAB 1: Comparación de escenarios para N fijo (ordenamiento) ----------------
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Escenarios (N fijo)")

    controls1 = ttk.Frame(tab1)
    controls1.pack(fill="x", pady=5)

    ttk.Label(controls1, text="N fijo (ej. 10000):").pack(side="left")
    n_entry = ttk.Entry(controls1, width=12)
    n_entry.pack(side="left", padx=8)

    ttk.Label(controls1, text="Algoritmo O(n²):").pack(side="left")
    algo1 = ttk.Combobox(controls1, state="readonly", width=12)
    algo1.pack(side="left", padx=6)

    ttk.Label(controls1, text="Algoritmo O(n log n):").pack(side="left")
    algo2 = ttk.Combobox(controls1, state="readonly", width=12)
    algo2.pack(side="left", padx=6)

    frame_plot1 = ttk.Frame(tab1)
    frame_plot1.pack(fill="both", expand=True)

    # Opciones de algoritmos disponibles en el CSV (solo ordenamiento)
    algos_orden = sorted({r["algoritmo"] for r in filas if r["modulo"] == "Ordenamiento"})
    # defaults
    algo1["values"] = algos_orden
    algo2["values"] = algos_orden
    if "Burbuja" in algos_orden:
        algo1.set("Burbuja")
    elif algos_orden:
        algo1.set(algos_orden[0])

    if "QuickSort" in algos_orden:
        algo2.set("QuickSort")
    elif len(algos_orden) > 1:
        algo2.set(algos_orden[1])
    elif algos_orden:
        algo2.set(algos_orden[0])

    def plot_escenarios():
        try:
            n_fijo = int(n_entry.get())
        except ValueError:
            messagebox.showerror("Error", "N fijo debe ser entero.")
            return

        a1 = algo1.get().strip()
        a2 = algo2.get().strip()
        if not a1 or not a2:
            messagebox.showerror("Error", "Selecciona 2 algoritmos.")
            return

        # Filtrar solo ordenamiento y ese N
        sub = [r for r in filas if r["modulo"] == "Ordenamiento" and r["n"] == n_fijo and r["algoritmo"] in (a1, a2)]
        if not sub:
            messagebox.showwarning("Sin datos", f"No hay datos de ordenamiento para N={n_fijo}.")
            return

        # Promedio por (algoritmo, escenario)
        prom = _promedio_por_grupo(sub, ["algoritmo", "escenario"])

        escenarios = ["MC", "CP", "PC"]
        y1 = [prom.get((a1, e), None) for e in escenarios]
        y2 = [prom.get((a2, e), None) for e in escenarios]

        if all(v is None for v in y1) and all(v is None for v in y2):
            messagebox.showwarning("Sin datos", "Faltan combinaciones (MC/CP/PC) para graficar.")
            return

        _limpiar_fig(frame_plot1)

        fig = Figure(figsize=(7.8, 4.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(f"Comparación de escenarios (N={n_fijo})")
        ax.set_xlabel("Escenario")
        ax.set_ylabel("Tiempo promedio (ns)")

        # Convertir None → no plottear puntos
        x = list(range(len(escenarios)))
        ax.plot(x, [v if v is not None else float("nan") for v in y1], marker="o", label=a1)
        ax.plot(x, [v if v is not None else float("nan") for v in y2], marker="o", label=a2)

        ax.set_xticks(x)
        ax.set_xticklabels(escenarios)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame_plot1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, frame_plot1)
        toolbar.update()

    ttk.Button(controls1, text="Graficar", command=plot_escenarios).pack(side="left", padx=10)

    # ---------------- TAB 2: Escalabilidad (ordenamiento) ----------------
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Escalabilidad (N crece)")

    controls2 = ttk.Frame(tab2)
    controls2.pack(fill="x", pady=5)

    ttk.Label(controls2, text="Escenario:").pack(side="left")
    escenario_cb = ttk.Combobox(controls2, state="readonly", width=6, values=["MC", "CP", "PC"])
    escenario_cb.pack(side="left", padx=8)
    escenario_cb.set("CP")

    ttk.Label(controls2, text="Algoritmo O(n²):").pack(side="left")
    s_algo1 = ttk.Combobox(controls2, state="readonly", width=12, values=algos_orden)
    s_algo1.pack(side="left", padx=6)

    ttk.Label(controls2, text="Algoritmo O(n log n):").pack(side="left")
    s_algo2 = ttk.Combobox(controls2, state="readonly", width=12, values=algos_orden)
    s_algo2.pack(side="left", padx=6)

    if algo1.get():
        s_algo1.set(algo1.get())
    if algo2.get():
        s_algo2.set(algo2.get())

    frame_plot2 = ttk.Frame(tab2)
    frame_plot2.pack(fill="both", expand=True)

    def plot_escalabilidad():
        esc = escenario_cb.get().strip()
        a1 = s_algo1.get().strip()
        a2 = s_algo2.get().strip()
        if not esc or not a1 or not a2:
            messagebox.showerror("Error", "Selecciona escenario y 2 algoritmos.")
            return

        sub = [r for r in filas if r["modulo"] == "Ordenamiento" and r["escenario"] == esc and r["algoritmo"] in (a1, a2)]
        if not sub:
            messagebox.showwarning("Sin datos", f"No hay datos de ordenamiento en escenario {esc}.")
            return

        # Promedio por (algoritmo, n)
        prom = _promedio_por_grupo(sub, ["algoritmo", "n"])

        # Conjuntos N disponibles
        ns = sorted({r["n"] for r in sub})
        y1 = [prom.get((a1, n), None) for n in ns]
        y2 = [prom.get((a2, n), None) for n in ns]

        if all(v is None for v in y1) and all(v is None for v in y2):
            messagebox.showwarning("Sin datos", "No hay puntos suficientes para graficar.")
            return

        _limpiar_fig(frame_plot2)

        fig = Figure(figsize=(7.8, 4.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(f"Escalabilidad en {esc} (Ordenamiento)")
        ax.set_xlabel("Tamaño N")
        ax.set_ylabel("Tiempo promedio (ns)")

        ax.plot(ns, [v if v is not None else float("nan") for v in y1], marker="o", label=a1)
        ax.plot(ns, [v if v is not None else float("nan") for v in y2], marker="o", label=a2)

        ax.legend()
        ax.grid(True, linestyle="--", linewidth=0.5)

        canvas = FigureCanvasTkAgg(fig, master=frame_plot2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, frame_plot2)
        toolbar.update()

    ttk.Button(controls2, text="Graficar", command=plot_escalabilidad).pack(side="left", padx=10)

    # Tip: valores sugeridos
    ttk.Label(tab2, text="Tip: corre pruebas con N = 10^3, 10^4, 10^5, 10^6 para ver una curva clara.").pack(pady=6)

    # Default N fijo sugerido
    n_entry.insert(0, "10000")
