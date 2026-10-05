# Imports
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

# FUNÇÕES ----------------------------------------------------------------------------------------

# Função que atualiza a interface, adicionando ou removendo o campo da frequência de corte, dependendo de qual opção foi selecionada na combobox
def atualizar_interface(event=None):
    tipo_filtro = combo_filtro.get()

    if tipo_filtro in ["Passa-faixa", "Rejeita-faixa"]:
        frame_fc2.grid()
    else:
        frame_fc2.grid_remove()

# 1) JANELA PRINCIPAL ----------------------------------------------------------------------------------------

# Criação da janela principal (onde serão colocados os outros componentes como: labels, entries, frames etc.)
janela = tk.Tk()
janela.title("Simulador de ruídos eletrônicos")
janela.geometry("720x720")
janela.option_add("*Font", "Arial 10")
janela.columnconfigure(0, weight=1)

# 2) TÍTULO ----------------------------------------------------------------------------------------

# Frame para o posicionamento da label do "título" do programa
frame_titulo = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
frame_titulo.columnconfigure(0, weight=1)

# Criação da label do "título" do programa
label_titulo = tk.Label(
    frame_titulo,
    text="SIMULADOR DE RUÍDOS",
    font=("Arial", 16, "bold", "underline")
)
label_titulo.grid(row=0, column=0, padx=5, pady=5)

# 3) PARÂMETROS ----------------------------------------------------------------------------------------

# Frame principal para o posicionamento dos parâmetros de sinal e ruído
frame_parametros = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_parametros.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
frame_parametros.columnconfigure(0, weight=1)
frame_parametros.columnconfigure(2, weight=1)

# 3.1) Parâmetros do sinal

# Frame para o posicionamentos dos elementos dos parâmetros de sinal
frame_sinal = tk.Frame(frame_parametros)
frame_sinal.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_sinal.columnconfigure(0, weight=1)
frame_sinal.columnconfigure(1, weight=1)

# Label para os parâmetros de sinal 
label_sinal = tk.Label(frame_sinal, text="PARÂMETROS DO SINAL")
label_sinal.grid(row=0, column=0, columnspan=2, padx=5, pady=12)

# Label para o primeiro campo de entrada (frequência do sinal)
label_freq_sinal = tk.Label(frame_sinal, text="Frequência (Hz): ")
label_freq_sinal.grid(row=1, column=0, padx=5, pady=8, sticky="e")

# Entry (campo de entrada) para a frequência do sinal
entry_freq_sinal = tk.Entry(frame_sinal, width=15)
entry_freq_sinal.insert(0, "0")
entry_freq_sinal.grid(row=1, column=1, padx=5, pady=8, sticky="w")

# Label para o segundo campo de entrada (amplitude do sinal)
label_amplit_sinal = tk.Label(frame_sinal, text="Amplitude: ")
label_amplit_sinal.grid(row=2, column=0, padx=5, pady=(5, 20), sticky="e")

# Entry (campo de entrada) para a amplitude do sinal
entry_amplit_sinal = tk.Entry(frame_sinal, width=15)
entry_amplit_sinal.insert(0, "0")
entry_amplit_sinal.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="w")

# 3.2) Separador (linha vertical entre os frames de sinal e ruido)
separador = ttk.Separator(frame_parametros, orient="vertical")
separador.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

# 3.3) Parâmetros do ruído

# Frame para o posicionamentos dos elementos dos parâmetros de ruído
frame_ruido = tk.Frame(frame_parametros)
frame_ruido.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
frame_ruido.columnconfigure(0, weight=1)
frame_ruido.columnconfigure(1, weight=1)

# Label para os parâmetros de ruído 
label_ruido = tk.Label(frame_ruido, text="PARÂMETROS DO RUÍDO")
label_ruido.grid(row=0, column=0, columnspan=2, padx=5, pady=12)

# Label para o primeiro campo de entrada (frequência do ruído)
label_freq_ruido = tk.Label(frame_ruido, text="Frequência (Hz): ")
label_freq_ruido.grid(row=1, column=0, padx=5, pady=8, sticky="e")

# Entry (campo de entrada) para a frequência do ruído
entry_freq_ruido = tk.Entry(frame_ruido, width=15)
entry_freq_ruido.insert(0, "0")
entry_freq_ruido.grid(row=1, column=1, padx=5, pady=8, sticky="w")

# Label para o segundo campo de entrada (amplitude do ruído)
label_amplit_ruido = tk.Label(frame_ruido, text="Amplitude: ")
label_amplit_ruido.grid(row=2, column=0, padx=5, pady=(5, 20), sticky="e")

# Entry (campo de entrada) para a amplitude do ruído
entry_amplit_ruido = tk.Entry(frame_ruido, width=15)
entry_amplit_ruido.insert(0, "0")
entry_amplit_ruido.grid(row=2, column=1, padx=5, pady=(5, 20), sticky="w")

# 4) FILTRO ----------------------------------------------------------------------------------------

# Frame para o posicionamento dos elementos relacionados ao filtro (tipo de filtro, frequência de 1 e 2 [fc1 e fc2])
frame_filtros = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_filtros.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

# Divisão do espaço do frame em 3 partes iguais (todas tem o mesmo peso)
frame_filtros.columnconfigure(0, weight=1)
frame_filtros.columnconfigure(1, weight=1)
frame_filtros.columnconfigure(2, weight=1)

# Label para os parâmetros do filtro 
label_filtros = tk.Label(frame_filtros, text="PARÂMETROS DO FILTRO")
label_filtros.grid(row=0, column=0, columnspan=3, pady=12)

# Combobox
frame_tipo_filtro = tk.Frame(frame_filtros)
frame_tipo_filtro.grid(row=1, column=0, pady=(5, 20))

# Label para a combobox
label_tipo_filtro = tk.Label(frame_tipo_filtro, text="Tipo: ")
label_tipo_filtro.grid(row=0, column=0)

# Opções dentro da combobox
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
# Frame
frame_fc1 = tk.Frame(frame_filtros)
frame_fc1.grid(row=1, column=1, pady=(5, 20))

# Label
label_fc1 = tk.Label(frame_fc1, text="fc1 (Hz): ")
label_fc1.grid(row=0, column=0, stick="ew")

# Entry
entry_fc1 = tk.Entry(frame_fc1, width=10)
entry_fc1.insert(0, "0")
entry_fc1.grid(row=0, column=1, stick="ew")

# Frequência de corte 2 (fc2)
# Frame
frame_fc2 = tk.Frame(frame_filtros)
frame_fc2.grid(row=1, column=2, pady=(5, 20))

# Label
label_fc2 = tk.Label(frame_fc2, text="fc2 (Hz): ")
label_fc2.grid(row=0, column=0, stick="ew")

# Entry
entry_fc2 = tk.Entry(frame_fc2, width=10)
entry_fc2.insert(0, "0")
entry_fc2.grid(row=0, column=1, stick="ew")

# BOTÕES ----------------------------------------------------------------------------------------

# Frame para o posicionamento dos botões
frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=3, column=0, pady=15)

# Primeiro botão: aplicar filtro
botao_aplicar = ttk.Button(frame_botoes, text="APLICAR FILTRO")
botao_aplicar.grid(row=0, column=0, padx=10)

# Segundo botão: limpar tela
botao_limpar = ttk.Button(frame_botoes, text="LIMPAR")
botao_limpar.grid(row=0, column=1, padx=10)

# INICIALIZAÇÃO ----------------------------------------------------------------------------------------

# Necessário chamar a função de atualizar a tela logo no "início", para esconder o campo do fc2 (já que a combobox começa na opção 'passa-baixa')
atualizar_interface()
janela.mainloop()
