# Imports
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

# FUNÇÕES ----------------------------------------------------------------------------------------
def atualizar_interface(event=None):
    tipo_filtro = combo_filtro.get()

    if tipo_filtro in ["Passa-faixa", "Rejeita-faixa"]:
        frame_fc2.grid()
    else:
        frame_fc2.grid_remove()

# JANELA PRINCIPAL ----------------------------------------------------------------------------------------
janela = tk.Tk()
janela.title("Simulador de ruídos eletrônicos")
janela.geometry("720x720")
janela.option_add("*Font", "Arial 10")
janela.columnconfigure(0, weight=1)

# TÍTULO ----------------------------------------------------------------------------------------
frame_titulo = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
frame_titulo.columnconfigure(0, weight=1)

label_titulo = tk.Label(
    frame_titulo,
    text="SIMULADOR DE RUÍDOS",
    font=("Arial", 16, "bold", "underline")
)
label_titulo.grid(row=0, column=0, padx=5, pady=5)

# PARÂMETROS ----------------------------------------------------------------------------------------
frame_parametros = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_parametros.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
frame_parametros.columnconfigure(0, weight=1)
frame_parametros.columnconfigure(2, weight=1)

# Parâmetros do sinal
frame_sinal = tk.Frame(frame_parametros)
frame_sinal.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_sinal.columnconfigure(0, weight=1)
frame_sinal.columnconfigure(1, weight=1)

label_sinal = tk.Label(frame_sinal, text="PARÂMETROS DO SINAL")
label_sinal.grid(row=0, column=0, columnspan=2, padx=5, pady=12)

label_freq_sinal = tk.Label(frame_sinal, text="Frequência (Hz): ")
label_freq_sinal.grid(row=1, column=0, padx=5, pady=8, sticky="e")

entry_freq_sinal = tk.Entry(frame_sinal, width=15)
entry_freq_sinal.insert(0, "0")
entry_freq_sinal.grid(row=1, column=1, padx=5, pady=8, sticky="w")

label_amplit_sinal = tk.Label(frame_sinal, text="Amplitude: ")
label_amplit_sinal.grid(row=2, column=0, padx=5, pady=(5, 20), sticky="e")

entry_amplit_sinal = tk.Entry(frame_sinal, width=15)
entry_amplit_sinal.insert(0, "0")
entry_amplit_sinal.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="w")

# Separador
separador = ttk.Separator(frame_parametros, orient="vertical")
separador.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

# Parâmetros do ruído

frame_ruido = tk.Frame(frame_parametros)
frame_ruido.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
frame_ruido.columnconfigure(0, weight=1)
frame_ruido.columnconfigure(1, weight=1)

label_ruido = tk.Label(frame_ruido, text="PARÂMETROS DO RUÍDO")
label_ruido.grid(row=0, column=0, columnspan=2, padx=5, pady=12)

label_freq_ruido = tk.Label(frame_ruido, text="Frequência (Hz): ")
label_freq_ruido.grid(row=1, column=0, padx=5, pady=8, sticky="e")

entry_freq_ruido = tk.Entry(frame_ruido, width=15)
entry_freq_ruido.insert(0, "0")
entry_freq_ruido.grid(row=1, column=1, padx=5, pady=8, sticky="w")

label_amplit_ruido = tk.Label(frame_ruido, text="Amplitude: ")
label_amplit_ruido.grid(row=2, column=0, padx=5, pady=(5, 20), sticky="e")

entry_amplit_ruido = tk.Entry(frame_ruido, width=15)
entry_amplit_ruido.insert(0, "0")
entry_amplit_ruido.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="w")

# FILTRO ----------------------------------------------------------------------------------------

# Frame
frame_filtros = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_filtros.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

# Divisão do espaço do frame em 3 partes iguais (já que todas tem o mesmo peso)
frame_filtros.columnconfigure(0, weight=1)
frame_filtros.columnconfigure(1, weight=1)
frame_filtros.columnconfigure(2, weight=1)

label_filtros = tk.Label(frame_filtros, text="PARÂMETROS DO FILTRO")
label_filtros.grid(row=0, column=0, columnspan=3, pady=12)

# Combobox
frame_tipo_filtro = tk.Frame(frame_filtros)
frame_tipo_filtro.grid(row=1, column=0, pady=(5, 20))

label_tipo_filtro = tk.Label(frame_tipo_filtro, text="Tipo: ")
label_tipo_filtro.grid(row=0, column=0)

combo_filtro = ttk.Combobox(
    frame_tipo_filtro,
    values=["Passa-baixa", "Passa-alta", "Passa-faixa", "Rejeita-faixa"],
    state="readonly",
    width=15
)
combo_filtro.grid(row=0, column=1)
combo_filtro.set("Passa-baixa")
combo_filtro.bind("<<ComboboxSelected>>", atualizar_interface)

# Frequência de corte 1 (fc1)
frame_fc1 = tk.Frame(frame_filtros)
frame_fc1.grid(row=1, column=1, pady=(5, 20))

label_fc1 = tk.Label(frame_fc1, text="fc1 (Hz): ")
label_fc1.grid(row=0, column=0, stick="ew")

entry_fc1 = tk.Entry(frame_fc1, width=10)
entry_fc1.insert(0, "0")
entry_fc1.grid(row=0, column=1, stick="ew")

# Frequência de corte 2 (fc2)
frame_fc2 = tk.Frame(frame_filtros)
frame_fc2.grid(row=1, column=2, pady=(5, 20))

label_fc2 = tk.Label(frame_fc2, text="fc2 (Hz): ")
label_fc2.grid(row=0, column=0, stick="ew")

entry_fc2 = tk.Entry(frame_fc2, width=10)
entry_fc2.insert(0, "0")
entry_fc2.grid(row=0, column=1, stick="ew")

# BOTÕES ----------------------------------------------------------------------------------------
frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=3, column=0, pady=15)

# Aplicar filtro
botao_aplicar = ttk.Button(frame_botoes, text="APLICAR FILTRO")
botao_aplicar.grid(row=0, column=0, padx=10)

# Limpar tela
botao_limpar = ttk.Button(frame_botoes, text="LIMPAR")
botao_limpar.grid(row=0, column=1, padx=10)

# INICIALIZAÇÃO ----------------------------------------------------------------------------------------
atualizar_interface()
janela.mainloop()