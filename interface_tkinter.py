# INCOMPLETO

# Imports das bibliotecas da interface
import tkinter as tk
from tkinter import ttk, messagebox

# Imports das outras bibliotecas (gráficos e cálculos)
import matplotlib as plt
import  numpy as np

# Criação da interface em Tkinter

# 1) Criação da janela principal
janela = tk.Tk()
janela.title("Simulador de ruídos eletrônicos") # 1. título da janela
janela.geometry("720x1000")                      # 2. tamanho inicial da janela
janela.option_add("*Font", "Arial 10")          # 3. fonte geral da janela (pode ser sobrescrita onde necessário)

# 2) Criação de frames + labels + campo de entrada de dados (entry)

janela.columnconfigure(0, weight=1) # Ajuste do espaço extra disponível na janela (como será distribuído entre as linhas/colunas do grid)

# Frame - Usado para separar melhor os elementos da interface em "caixas separadas" (ajudando no posicionamento dos elementos) 
frame_titulo = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_titulo.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
frame_titulo.columnconfigure(0, weight=1) # Ajuste do espaço extra disponível nesse frame (como será distribuído entre as linhas/colunas do grid)

# 2.1) "Titulo"

# Label - Titulo
label_titulo = tk.Label(
    frame_titulo,
    text= "SIMULADOR DE RUÍDOS",
    font=("Arial", 16, "bold", "underline")
)
label_titulo.grid(row=0, column=0, padx=5, pady=5)

# Frame - Usado para separar melhor os elementos da interface em "caixas separadas" (ajudando no posicionamento dos elementos) 
frame_parametros = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_parametros.grid(row=1, column=0, sticky="ew", pady=10, padx=10)

# 2.2) PARÂMETROS DE SINAL ----------------------------------------------------------------------------------------------------

# Label do "título" dos parâmetros do sinal
label_sinal = tk.Label (frame_parametros, text="PARÂMETROS DE SINAL")
label_sinal.grid(row=0, column=0, padx=5, pady=12, sticky="ew", columnspan=2)

# Label da frequência
label_freq_sinal = tk.Label (frame_parametros, text="Frequência (Hz): ")
label_freq_sinal.grid(row=1, column=0, padx=(15, 0), pady=8, sticky="e")

# Entry da frequência
entry_freq_sinal = tk.Entry(frame_parametros, width=15)
entry_freq_sinal.insert(0, "0")
entry_freq_sinal.grid(row=1, column=1, padx=5, pady=12, sticky="w")

# Label da amplitude
label_amplit_sinal = tk.Label (frame_parametros, text="Amplitude: ")
label_amplit_sinal.grid(row=2, column=0, padx=(15, 0), pady=(5, 20), sticky="e")

# Entry da amplitude
entry_amplit_sinal = tk.Entry(frame_parametros, width=15)
entry_amplit_sinal.insert(0, "0")
entry_amplit_sinal.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="w")

# 2.3) PARÂMETROS DE RUÍDO ----------------------------------------------------------------------------------------------------

# Label do "título" dos parâmetros do ruído
label_ruido = tk.Label (frame_parametros, text="PARÂMETROS DE RUÍDO")
label_ruido.grid(row=0, column=4, padx=5, pady=12, sticky="ew", columnspan=2)

# Label da frequência
label_freq_ruido = tk.Label (frame_parametros, text="Frequência (Hz): ")
label_freq_ruido.grid(row=1, column=4, padx=(15, 0), pady=8, sticky="e")

# Entry da frequência
entry_freq_ruido = tk.Entry(frame_parametros, width=15)
entry_freq_ruido.insert(0, "0")
entry_freq_ruido.grid(row=1, column=5, padx=5, pady=12, sticky="w")

# Label da amplitude
label_amplit_ruido = tk.Label (frame_parametros, text="Amplitude: ")
label_amplit_ruido.grid(row=2, column=4, padx=(15, 0), pady=(5, 20), sticky="e")

# Entry da amplitude
entry_amplit_ruido = tk.Entry(frame_parametros, width=15)
entry_amplit_ruido.insert(0, "0")
entry_amplit_ruido.grid(row=2, column=5, padx=5, pady=(5, 20), sticky="w")



janela.mainloop() # Deixa a janela em loop, ou seja: o programa continua rodando até a janela ser fechada