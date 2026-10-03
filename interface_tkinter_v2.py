# INCOMPLETO

# Imports das bibliotecas da interface
import tkinter as tk
from tkinter import ttk, messagebox

# Imports das outras bibliotecas (gráficos e cálculos)
import matplotlib.pyplot as plt
import numpy as np

# Criação/definição de função para atualizar interface quando o passa/rejeita faixa é selecionado
def atualizar_interface(event=None):

    tipo_filtro = combo_filtro.get()

    if tipo_filtro in ["Passa-faixa", "Rejeita-faixa"]:
        label_fc2.grid()
        entry_fc2.grid()

    else:
        label_fc2.grid_remove()
        entry_fc2.grid_remove()

# Criação da interface em Tkinter

# 1) Criação da janela principal
janela = tk.Tk()
janela.title("Simulador de ruídos eletrônicos")   # 1. título da janela
janela.geometry("720x720")                       # 2. tamanho inicial da janela
janela.option_add("*Font", "Arial 10")            # 3. fonte geral da janela

# Faz a coluna principal da janela ocupar o espaço disponível
janela.columnconfigure(0, weight=1)

# 2) TÍTULO PRINCIPAL ----------------------------------------------------------------

# Frame do título da janela
frame_titulo = tk.Frame(
    janela,
    borderwidth=0.5,
    relief="solid"
)

frame_titulo.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=10,
    padx=10
)

# Faz a coluna do frame (frame_titulo) ocupar todo o espaço restante disponível
frame_titulo.columnconfigure(0, weight=1)

# Label do título
label_titulo = tk.Label(
    frame_titulo,
    text="SIMULADOR DE RUÍDOS",
    font=("Arial", 16, "bold", "underline")
)

label_titulo.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

# 3) PARÂMETROS

# Frame geral para os parâmetros
frame_parametros = tk.Frame(
    janela,
    borderwidth=0.5,
    relief="solid"
)

frame_parametros.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=10,
    padx=10
)

# As colunas 0 e 2 recebem igualmente o espaço disponível
frame_parametros.columnconfigure(0, weight=1)
frame_parametros.columnconfigure(2, weight=1)

# 3.1) FRAME DOS PARÂMETROS DO SINAL ----------------------------------------------------------------

frame_sinal = tk.Frame(frame_parametros)

frame_sinal.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)

# Divide o frame em duas colunas de mesmo peso
frame_sinal.columnconfigure(0, weight=1)
frame_sinal.columnconfigure(1, weight=1)

# Título dos parâmetros do sinal
label_sinal = tk.Label(
    frame_sinal,
    text="PARÂMETROS DO SINAL"
)

label_sinal.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=5,
    pady=12
)

# Label da frequência do sinal
label_freq_sinal = tk.Label(
    frame_sinal,
    text="Frequência (Hz): "
)

label_freq_sinal.grid(
    row=1,
    column=0,
    padx=5,
    pady=8,
    sticky="e"
)

# Entry da frequência do sinal
entry_freq_sinal = tk.Entry(
    frame_sinal,
    width=15
)

entry_freq_sinal.insert(0, "0")

entry_freq_sinal.grid(
    row=1,
    column=1,
    padx=5,
    pady=8,
    sticky="w"
)

# Label da amplitude do sinal
label_amplit_sinal = tk.Label(
    frame_sinal,
    text="Amplitude: "
)

label_amplit_sinal.grid(
    row=2,
    column=0,
    padx=5,
    pady=(5, 20),
    sticky="e"
)

# Entry da amplitude do sinal
entry_amplit_sinal = tk.Entry(
    frame_sinal,
    width=15
)

entry_amplit_sinal.insert(0, "0")

entry_amplit_sinal.grid(
    row=2,
    column=1,
    padx=5,
    pady=(5, 20),
    sticky="w"
)

# 3.2) SEPARADOR (SINAL | RUIDO) ----------------------------------------------------------------

separador = ttk.Separator(
    frame_parametros,
    orient="vertical"
)

separador.grid(
    row=0,
    column=1,
    sticky="ns",
    padx=10,
    pady=10
)

# 3.3) FRAME DOS PARÂMETROS DO RUÍDO ----------------------------------------------------------------

frame_ruido = tk.Frame(frame_parametros)

frame_ruido.grid(
    row=0,
    column=2,
    sticky="nsew",
    padx=10,
    pady=10
)

# Divide o frame em duas colunas de mesmo peso
frame_ruido.columnconfigure(0, weight=1)
frame_ruido.columnconfigure(1, weight=1)

# Título dos parâmetros do ruído
label_ruido = tk.Label(
    frame_ruido,
    text="PARÂMETROS DO RUÍDO"
)

label_ruido.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=5,
    pady=12
)

# Label da frequência do ruído
label_freq_ruido = tk.Label(
    frame_ruido,
    text="Frequência (Hz): "
)

label_freq_ruido.grid(
    row=1,
    column=0,
    padx=5,
    pady=8,
    sticky="e"
)

# Entry da frequência do ruído
entry_freq_ruido = tk.Entry(
    frame_ruido,
    width=15
)

entry_freq_ruido.insert(0, "0")

entry_freq_ruido.grid(
    row=1,
    column=1,
    padx=5,
    pady=8,
    sticky="w"
)

# Label da amplitude do ruído
label_amplit_ruido = tk.Label(
    frame_ruido,
    text="Amplitude: "
)

label_amplit_ruido.grid(
    row=2,
    column=0,
    padx=5,
    pady=(5, 20),
    sticky="e"
)

# Entry da amplitude do ruído
entry_amplit_ruido = tk.Entry(
    frame_ruido,
    width=15
)

entry_amplit_ruido.insert(0, "0")

entry_amplit_ruido.grid(
    row=2,
    column=1,
    padx=5,
    pady=(5, 20),
    sticky="w"
)

# 4) SELEÇÃO DO FILTRO (Combobox) -------------------------------------------------------------------------

frame_filtros = tk.Frame(
    janela,
    borderwidth=0.5,
    relief="solid"
)

frame_filtros.grid(
    row=2,
    column=0,
    sticky="ew",
    pady=10,
    padx=10
)

frame_filtros.columnconfigure(0, weight=1)
frame_filtros.columnconfigure(1, weight=1)


# Título da seção
label_filtros = tk.Label(
    frame_filtros,
    text="PARÂMETROS DO FILTRO"
)

label_filtros.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=12
)


# Tipo de filtro
label_tipo_filtro = tk.Label(
    frame_filtros,
    text="Tipo de filtro: "
)

label_tipo_filtro.grid(
    row=1,
    column=0,
    padx=5,
    pady=8,
    sticky="e"
)


combo_filtro = ttk.Combobox(
    frame_filtros,
    values=[
        "Passa-baixa",
        "Passa-alta",
        "Passa-faixa",
        "Rejeita-faixa"
    ],
    state="readonly",
    width=15
)

combo_filtro.grid(
    row=1,
    column=1,
    padx=5,
    pady=8,
    sticky="w"
)

combo_filtro.set("Passa-baixa")

combo_filtro.bind(
    "<<ComboboxSelected>>",
    atualizar_interface
)

# 4.1) FREQUÊNCIAS DE CORTE

# Frequência de corte 1 (fc1)
label_fc1 = tk.Label(
    frame_filtros,
    text="Frequência de corte 1 (Hz): "
)

label_fc1.grid(
    row=2,
    column=0,
    padx=5,
    pady=8,
    sticky="e"
)


entry_fc1 = tk.Entry(
    frame_filtros,
    width=15
)

entry_fc1.insert(0, "0")

entry_fc1.grid(
    row=2,
    column=1,
    padx=5,
    pady=8,
    sticky="w"
)

# Frequência de corte 2
label_fc2 = tk.Label(
    frame_filtros,
    text="Frequência de corte 2 (Hz): "
)

label_fc2.grid(
    row=3,
    column=0,
    padx=5,
    pady=(8, 20),
    sticky="e"
)


entry_fc2 = tk.Entry(
    frame_filtros,
    width=15
)

entry_fc2.insert(0, "0")

entry_fc2.grid(
    row=3,
    column=1,
    padx=5,
    pady=(8, 20),
    sticky="w"
)

# 5) BOTÕES -------------------------------------------------------------------------

frame_botoes = tk.Frame(janela)

frame_botoes.grid(
    row=3,
    column=0,
    pady=15
)


botao_aplicar = ttk.Button(
    frame_botoes,
    text="APLICAR FILTRO"
)

botao_aplicar.grid(
    row=0,
    column=0,
    padx=10
)


botao_limpar = ttk.Button(
    frame_botoes,
    text="LIMPAR"
)

botao_limpar.grid(
    row=0,
    column=1,
    padx=10
)

atualizar_interface() # Esconde o 2nd campo logo quando a aplicação inicia (já que o filtro "pré-selecionado" é o passa-baixa)

# Mantém a janela em execução (sem isso a janela abre e fecha [mas é tão rápido que não dá para reparar])
janela.mainloop()