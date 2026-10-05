# Sugestão do gepeto para um "sistema" de tooltips quando passar o mouse em cima dos elementos (o tkinter não tem opção própria)
import tkinter as tk
from tkinter import ttk


def adicionar_tooltip(elemento, texto):
    tooltip = None

    def mostrar(event=None):
        nonlocal tooltip

        x = elemento.winfo_rootx() + 20
        y = elemento.winfo_rooty() + elemento.winfo_height() + 5

        tooltip = tk.Toplevel(elemento)
        tooltip.overrideredirect(True)
        tooltip.geometry(f"+{x}+{y}")

        label_tooltip = tk.Label(
            tooltip,
            text=texto,
            borderwidth=1,
            relief="solid",
            padx=6,
            pady=3
        )

        label_tooltip.pack()

    def esconder(event=None):
        nonlocal tooltip

        if tooltip is not None:
            tooltip.destroy()
            tooltip = None

    elemento.bind("<Enter>", mostrar, add="+")
    elemento.bind("<Leave>", esconder, add="+")


# -------------------------------------------------------
# INTERFACE
# -------------------------------------------------------

janela = tk.Tk()
janela.title("Exemplo de tooltip")
janela.geometry("400x200")


label_fc1 = tk.Label(
    janela,
    text="Frequência de corte (Hz):"
)
label_fc1.grid(row=0, column=0, padx=10, pady=30)


entry_fc1 = tk.Entry(
    janela,
    width=15
)
entry_fc1.insert(0, "10")
entry_fc1.grid(row=0, column=1, padx=10, pady=30)


adicionar_tooltip(
    label_fc1,
    "Define a frequência de corte do filtro."
)

adicionar_tooltip(
    entry_fc1,
    "Digite a frequência de corte em Hz."
)


janela.mainloop()