import tkinter as tk
from tkinter import ttk, messagebox

from Ordenamiento import Burbuja, QuikSort
from Busqueda import Secuencial, Binaria
from main.Medicion.motor import medir_ordenamiento, medir_busqueda, medir_estructuras
from main.Resultados.registro import guardar_resultado
from main.Resultados.graficas import abrir_ventana_graficas



# ---------------- Ventana principal ----------------
root = tk.Tk()
root.title("Análisis de Rendimiento Algorítmico")
root.geometry("520x420")
root.resizable(False, False)


# ---------------- Variables ----------------
modulo_var = tk.StringVar(value="Ordenamiento")
algoritmo_var = tk.StringVar()
escenario_var = tk.StringVar(value="CP")

n_var = tk.StringVar()
rep_var = tk.StringVar(value="5")


# ---------------- Funciones ----------------
def actualizar_algoritmos(*args):
    combo_algoritmo.set("")
    combo_algoritmo["values"] = []
    
    m = modulo_var.get().strip()

    m_norm = m.lower().replace("ú", "u").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")

    if "orden" in m_norm:
        combo_algoritmo["values"] = ["Burbuja", "QuikSort"]
        algoritmo_var.set("Burbuja")
    elif "busqu" in m_norm:
        combo_algoritmo["values"] = ["Secuencial", "Binaria"]
        algoritmo_var.set("Secuencial")
    else:
        combo_algoritmo["values"] = ["Pila", "Cola"]
        algoritmo_var.set("Pila")


def ejecutar():
    tk.Button(root, text="ver graficas", command=lambda: abrir_ventana_graficas(root),
              bg="#444", fg="white", font=("Arial", 11, "bold"),
              width=20).pack(pady=5)
    try:
        n = int(n_var.get())
        rep = int(rep_var.get())
        escenario = escenario_var.get()
    except ValueError:
        messagebox.showerror("Error", "N y repeticiones deben ser números enteros.")
        return

    if n <= 0 or rep <= 0:
        messagebox.showerror("Error", "N y repeticiones deben ser mayores que 0.")
        return

    modulo = modulo_var.get()
    algoritmo = algoritmo_var.get()

    try:
        if modulo == "Ordenamiento":
            func = Burbuja if algoritmo == "Burbuja" else QuikSort
            tiempo = medir_ordenamiento(func, n, escenario, rep)

        elif modulo == "Búsqueda":
            func = Secuencial if algoritmo == "Secuencial" else Binaria
            tiempo = medir_busqueda(func, n, escenario, rep)

        else:
            tipo = "pila" if algoritmo == "Pila" else "cola"
            tiempo = medir_estructuras(tipo, n, rep)

        lbl_resultado.config(
            text=f"Tiempo promedio:\n{tiempo:.2f} ns",
            fg="green"
        )

        guardar_resultado(modulo=modulo, algoritmo=algoritmo, n=n,
                          escenario=escenario if modulo != "Pila/Cola" else "NA",
                          repeticiones=rep, tiempo_ns=tiempo)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- UI ----------------
tk.Label(root, text="Análisis de Rendimiento Algorítmico",
         font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Módulo:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
combo_modulo = ttk.Combobox(frame, textvariable=modulo_var, state="readonly",
                            values=["Ordenamiento", "Búsqueda", "Pila / Cola"])
combo_modulo.grid(row=0, column=1)
combo_modulo.bind("<<ComboboxSelected>>", actualizar_algoritmos)

tk.Label(frame, text="Algoritmo:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
combo_algoritmo = ttk.Combobox(frame, textvariable=algoritmo_var, state="readonly")
combo_algoritmo.grid(row=1, column=1)

tk.Label(frame, text="Escenario:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
combo_escenario = ttk.Combobox(frame, textvariable=escenario_var, state="readonly",
                              values=["MC", "CP", "PC"])
combo_escenario.grid(row=2, column=1)

tk.Label(frame, text="Tamaño N:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
tk.Entry(frame, textvariable=n_var).grid(row=3, column=1)

tk.Label(frame, text="Repeticiones:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
tk.Entry(frame, textvariable=rep_var).grid(row=4, column=1)

tk.Button(root, text="Ejecutar prueba", command=ejecutar,
          bg="#2c7be5", fg="white", font=("Arial", 11, "bold"),
          width=20).pack(pady=15)

lbl_resultado = tk.Label(root, text="Tiempo promedio:\n—",
                         font=("Arial", 13), fg="blue")
lbl_resultado.pack(pady=10)

tk.Label(root, text="Proyecto Final – Estructura de Datos",
         font=("Arial", 9)).pack(side="bottom", pady=5)


actualizar_algoritmos()
root.mainloop()
