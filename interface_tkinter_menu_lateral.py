# Imports das bibliotecas
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from processamento import *

# FUNÇÕES ----------------------------------------------------------------------------------------

# Função que atualiza a interface, adicionando ou removendo o campo da frequência de corte, dependendo de qual opção foi selecionada na combobox
def atualizar_interface(event=None):
    tipo_filtro = combo_filtro.get()

    if tipo_filtro in ["Passa-faixa", "Rejeita-faixa"]:
        frame_fc2.grid()
    else:
        frame_fc2.grid_remove()
#fim atualizar_interface

# Função que lê ("pega") os valores dos campos de entrada e armazena em suas respectivas variáveis
def ler_entrada():

    # .replace(",", ".") -> Substitui vírgula por ponto, caso o usuário digite a vírgula na hora de digitar números decimais

    # Campos do sinal
    freq_sinal = float(entry_freq_sinal.get().replace(",", "."))
    amplitude_sinal = float(entry_amplit_sinal.get().replace(",", "."))
    
    # Campos do ruído
    freq_ruido = float(entry_freq_ruido.get().replace(",", "."))
    amplitude_ruido = float(entry_amplit_ruido.get().replace(",", "."))

    # Campos do filtro
    tipo_filtro = combo_filtro.get()
    fc1 = float(entry_fc1.get().replace(",", "."))

    fc2 = None # Inicializa a variável fc2 como None, caso não seja necessário ler o valor do campo fc2 (passa-baixa ou passa-alta)
    # Se o tipo de filtro for passa-faixa ou rejeita-faixa, então o campo fc2 terá seu valor lido e armazenado
    if tipo_filtro in ["Passa-faixa", "Rejeita-faixa"]: 
        fc2 = float(entry_fc2.get().replace(",", "."))

    return freq_sinal, amplitude_sinal, freq_ruido, amplitude_ruido, tipo_filtro, fc1, fc2
#fim ler_entrada

# Função que atualiza os gráficos com os novos dados (sinal desejado, ruído, sinal com ruído etc.)
def atualizar_grafico(tempo, sinal, ruido, sinal_com_ruido, sinal_filtrado, fs=1000, frequencias=None, magnitude_sem_filtro=None, magnitude_filtrada=None):
    # Limpa os gráficos antes de plotar os novos dados
    grafico_inicial.clear()
    grafico_final.clear()
    grafico_fft_inicial.clear()
    grafico_fft_final.clear()

    # Gráfico do sinal desejado + sinal com ruído
    grafico_inicial.plot(tempo, sinal_com_ruido, color="red", label="Sinal + ruído", alpha=0.6)
    grafico_inicial.plot(tempo, sinal, color="black", label="Sinal desejado", alpha=0.8)

    grafico_inicial.set_title("Antes da filtragem")
    grafico_inicial.set_xlabel("Tempo (s)")
    grafico_inicial.set_ylabel("Amplitude V(t)")
    grafico_inicial.legend()
    grafico_inicial.grid(True)

    # Gráfico do sinal desejado & sinal filtrado
    grafico_final.plot(tempo, sinal_filtrado, color="red", label="Sinal filtrado", alpha=0.7)
    grafico_final.plot(tempo, sinal, color="black", label="Sinal desejado", alpha=0.8)

    grafico_final.set_title("Depois da filtragem")
    grafico_final.set_xlabel("Tempo (s)")
    grafico_final.set_ylabel("Amplitude V(t)")
    grafico_final.legend()
    grafico_final.grid(True)

    # FFT do sinal antes da filtragem
    grafico_fft_inicial.plot(frequencias, magnitude_sem_filtro)
    grafico_fft_inicial.set_title("Espectro antes da filtragem")
    grafico_fft_inicial.set_xlabel("Frequência (Hz)")
    grafico_fft_inicial.set_ylabel("Magnitude")
    grafico_fft_inicial.grid(True)

    # FFT do sinal depois da filtragem
    grafico_fft_final.plot(frequencias, magnitude_filtrada)
    grafico_fft_final.set_title("Espectro depois da filtragem")
    grafico_fft_final.set_xlabel("Frequência (Hz)")
    grafico_fft_final.set_ylabel("Magnitude")
    grafico_fft_final.grid(True)

    figura.tight_layout(pad=2.5)
    canvas.draw()  # Atualiza o canvas (onde a figura é desenhada) com os novos gráficos
#fim atualizar_grafico

# Essa função chama a função ler_entrada() para pegar os valores dos campos de entrada, chama a função gerar_sinais() para gerar 
# o sinal e o ruído, e então plota os gráficos do sinal desejado e do sinal com ruído
def aplicar_filtro():
    # O try/except serve para pegar os erros que poderam ocorrer e caso ocorram não parar o programa além de mostrar
    # além de mostrar uma mensagem de erro genérica (a mais detalhada ficaria no terminal)
    try:

        # Pegando os valores dos campos de entrada e armazenando em suas respectivas variáveis (através da função ler_entrada())
        freq_sinal, amplitude_sinal, freq_ruido, amplitude_ruido, tipo_filtro, fc1, fc2 = ler_entrada()
        
        # Testes/debug dos campos de sinal e ruído
        # print(f"FS: {freq_sinal}; AS: {amplitude_sinal}; FR: {freq_ruido}; AR: {amplitude_ruido}")

        fs = 1000

        # O retorno da função gerar_sinal será armazenado nas seguintes variáveis (tempo, sinal, ruido, sinal_com_ruido)
        # Essa ordem é baseada na ordem do return de gerar_sinais
        tempo, sinal, ruido, sinal_com_ruido = gerar_sinais(freq_sinal, amplitude_sinal, freq_ruido, amplitude_ruido, fs=fs)

        # Chama a função do filtro correspondente ao tipo de filtro selecionado na combobox
        if tipo_filtro == "Passa-baixa":
            sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada = filtro_passa_baixa(sinal_com_ruido, fc1, fs=fs)
        
        elif tipo_filtro == "Passa-alta":
            sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada = filtro_passa_alta(sinal_com_ruido, fc1)

        elif tipo_filtro == "Passa-faixa":
            sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada = filtro_passa_faixa(sinal_com_ruido, fc1, fc2)

        elif tipo_filtro == "Rejeita-faixa":
            sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada = filtro_rejeita_faixa(sinal_com_ruido, fc1, fc2)
            
        else:
            raise ValueError("Este tipo de filtro ainda não foi implementado")

        # Testes/debug dos retornos da função gerar_sinais (limita cada um aos primeiros 5 valores, para não poluir o terminal)
        # print("Tempo:", tempo[:5])
        # print("Sinal:", sinal[:5])
        # print("Ruído:", ruido[:5])
        # print("Sinal + ruído:", sinal_com_ruido[:5])

        # Chamando a função para atualizar os gráficos
        atualizar_grafico(tempo, sinal, ruido, sinal_com_ruido, sinal_filtrado, fs, frequencias, magnitude_sem_filtro, magnitude_filtrada)

    except ValueError as erro:
        print(erro)
        messagebox.showerror("ERRO", "Por favor, digite valores válidos")
#fim aplicar_filtro

# 1) JANELA PRINCIPAL ----------------------------------------------------------------------------------------

# Criação da janela principal (onde serão colocados os outros componentes como: labels, entries, frames etc.)
janela = tk.Tk()
janela.title("Simulador de ruídos eletrônicos")
janela.geometry("1400x850")
janela.minsize(1100, 700)
janela.option_add("*Font", "Arial 10")

# A janela principal fica dividida em duas colunas: menu lateral e área dos gráficos
janela.columnconfigure(0, weight=0)
janela.columnconfigure(1, weight=1)
janela.rowconfigure(0, weight=1)

# 2) MENU LATERAL ----------------------------------------------------------------------------------------

# Frame principal do menu lateral
frame_menu = tk.Frame(janela, borderwidth=0.5, relief="solid", width=320)
frame_menu.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)
frame_menu.grid_propagate(False)
frame_menu.columnconfigure(0, weight=1)

# Frame para o posicionamento da label do "título" do programa
frame_titulo = tk.Frame(frame_menu)
frame_titulo.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
frame_titulo.columnconfigure(0, weight=1)

# Criação da label do "título" do programa
label_titulo = tk.Label(
    frame_titulo,
    text="SIMULADOR DE RUÍDOS",
    font=("Arial", 16, "bold", "underline")
)
label_titulo.grid(row=0, column=0, padx=5, pady=5)

# 3) PARÂMETROS ----------------------------------------------------------------------------------------

# Frame principal para o posicionamento dos parâmetros de sinal, ruído e filtro
frame_parametros = tk.Frame(frame_menu)
frame_parametros.grid(row=1, column=0, sticky="new", padx=10, pady=5)
frame_parametros.columnconfigure(0, weight=1)

# 3.1) Parâmetros do sinal

# Frame para o posicionamentos dos elementos dos parâmetros de sinal
frame_sinal = tk.Frame(frame_parametros)
frame_sinal.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
frame_sinal.columnconfigure(0, weight=1)
frame_sinal.columnconfigure(1, weight=1)

# Label para os parâmetros de sinal 
label_sinal = tk.Label(frame_sinal, text="PARÂMETROS DO SINAL", font=("Arial", 10, "bold"))
label_sinal.grid(row=0, column=0, columnspan=2, padx=5, pady=8)

# Label para o primeiro campo de entrada (frequência do sinal)
label_freq_sinal = tk.Label(frame_sinal, text="Frequência (Hz): ")
label_freq_sinal.grid(row=1, column=0, padx=5, pady=5, sticky="e")

# Entry (campo de entrada) para a frequência do sinal
entry_freq_sinal = tk.Entry(frame_sinal, width=12)
entry_freq_sinal.insert(0, "0")
entry_freq_sinal.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Label para o segundo campo de entrada (amplitude do sinal)
label_amplit_sinal = tk.Label(frame_sinal, text="Amplitude: ")
label_amplit_sinal.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Entry (campo de entrada) para a amplitude do sinal
entry_amplit_sinal = tk.Entry(frame_sinal, width=12)
entry_amplit_sinal.insert(0, "0")
entry_amplit_sinal.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# 3.2) Separador (linha horizontal entre os frames de sinal e ruido)
separador = ttk.Separator(frame_parametros, orient="horizontal")
separador.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

# 3.3) Parâmetros do ruído

# Frame para o posicionamentos dos elementos dos parâmetros de ruído
frame_ruido = tk.Frame(frame_parametros)
frame_ruido.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
frame_ruido.columnconfigure(0, weight=1)
frame_ruido.columnconfigure(1, weight=1)

# Label para os parâmetros do ruído 
label_ruido = tk.Label(frame_ruido, text="PARÂMETROS DO RUÍDO", font=("Arial", 10, "bold"))
label_ruido.grid(row=0, column=0, columnspan=2, padx=5, pady=8)

# Label para o primeiro campo de entrada (frequência do ruído)
label_freq_ruido = tk.Label(frame_ruido, text="Frequência (Hz): ")
label_freq_ruido.grid(row=1, column=0, padx=5, pady=5, sticky="e")

# Entry (campo de entrada) para a frequência do ruído
entry_freq_ruido = tk.Entry(frame_ruido, width=12)
entry_freq_ruido.insert(0, "0")
entry_freq_ruido.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Label para o segundo campo de entrada (amplitude do ruído)
label_amplit_ruido = tk.Label(frame_ruido, text="Amplitude: ")
label_amplit_ruido.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Entry (campo de entrada) para a amplitude do ruído
entry_amplit_ruido = tk.Entry(frame_ruido, width=12)
entry_amplit_ruido.insert(0, "0")
entry_amplit_ruido.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# 3.4) Separador (linha horizontal entre os frames de ruido e filtro)
separador_filtro = ttk.Separator(frame_parametros, orient="horizontal")
separador_filtro.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

# 4) FILTRO ----------------------------------------------------------------------------------------

# Frame para o posicionamento dos elementos relacionados ao filtro (tipo de filtro, frequência de 1 e 2 [fc1 e fc2])
frame_filtros = tk.Frame(frame_parametros)
frame_filtros.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

# Divisão do espaço do frame em 2 partes iguais (todas tem o mesmo peso)
frame_filtros.columnconfigure(0, weight=1)
frame_filtros.columnconfigure(1, weight=1)

# Label para os parâmetros do filtro 
label_filtros = tk.Label(frame_filtros, text="PARÂMETROS DO FILTRO", font=("Arial", 10, "bold"))
label_filtros.grid(row=0, column=0, columnspan=2, pady=8)

# Combobox
frame_tipo_filtro = tk.Frame(frame_filtros)
frame_tipo_filtro.grid(row=1, column=0, columnspan=2, pady=5)

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
frame_fc1.grid(row=2, column=0, columnspan=2, pady=5)

# Label
label_fc1 = tk.Label(frame_fc1, text="fc1 (Hz): ")
label_fc1.grid(row=0, column=0, sticky="e")

# Entry
entry_fc1 = tk.Entry(frame_fc1, width=10)
entry_fc1.insert(0, "0")
entry_fc1.grid(row=0, column=1, sticky="w")

# Frequência de corte 2 (fc2)
# Frame
frame_fc2 = tk.Frame(frame_filtros)
frame_fc2.grid(row=3, column=0, columnspan=2, pady=5)

# Label
label_fc2 = tk.Label(frame_fc2, text="fc2 (Hz): ")
label_fc2.grid(row=0, column=0, sticky="e")

# Entry
entry_fc2 = tk.Entry(frame_fc2, width=10)
entry_fc2.insert(0, "0")
entry_fc2.grid(row=0, column=1, sticky="w")

# 5) BOTÕES ----------------------------------------------------------------------------------------

# Frame para o posicionamento dos botões
frame_botoes = tk.Frame(frame_menu)
frame_botoes.grid(row=2, column=0, sticky="ew", padx=10, pady=15)
frame_botoes.columnconfigure(0, weight=1)

# Primeiro botão: aplicar filtro
botao_aplicar = ttk.Button(frame_botoes, text="APLICAR FILTRO", command=aplicar_filtro)
botao_aplicar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

# Segundo botão: limpar tela
botao_limpar = ttk.Button(frame_botoes, text="LIMPAR")
botao_limpar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

# 6) GRÁFICOS (figure e canvas) -----------------------------------------------------------------------------------------------------

# Frame para o posicionamento da seção dos gráficos
frame_graficos = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_graficos.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

frame_graficos.columnconfigure(0, weight=1) # Fazendo com que o espaço restante da coluna (column) [do frame_graficos] seja ocupado/utilizado
frame_graficos.rowconfigure(0, weight=1) # Fazendo com que o espaço restante da linha (row) [do frame_graficos] seja ocupado/utilizado

# Criação da figura e dos 4 subplots: 2 no domínio do tempo e 2 no domínio da frequência
figura = Figure(figsize=(11, 8), dpi=100)
grafico_inicial = figura.add_subplot(2, 2, 1)
grafico_final = figura.add_subplot(2, 2, 2)
grafico_fft_inicial = figura.add_subplot(2, 2, 3)
grafico_fft_final = figura.add_subplot(2, 2, 4)
figura.tight_layout(pad=2.5) # Ajustando o layout da figura (para que os subplots não fiquem "colados" um no outro)

# Títulos dos gráficos/subplots
grafico_inicial.set_title("Antes da filtragem")
grafico_final.set_title("Depois da filtragem")
grafico_fft_inicial.set_title("Espectro antes da filtragem")
grafico_fft_final.set_title("Espectro depois da filtragem")

# Criação do canvas (onde a figura será desenhada) e adição do canvas ao frame_graficos
canvas = FigureCanvasTkAgg(figura, master=frame_graficos)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew") # Transformando em um widget e definindo a posição do canvas (no frame_graficos)

canvas.draw() # Desenhando a figura no canvas

# INICIALIZAÇÃO ----------------------------------------------------------------------------------------

# Necessário chamar a função de atualizar a tela logo no "início", para esconder o campo do fc2 (já que a combobox começa na opção 'passa-baixa')
atualizar_interface()
janela.mainloop()
