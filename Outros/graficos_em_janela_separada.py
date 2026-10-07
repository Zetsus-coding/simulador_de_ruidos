# Ideia extra (não implementada): além de criar os gráficos em uma nova janela, permitir interagir com eles (zoom, pan, salvar como imagem etc.) 
# e também permitir que o usuário escolha quais gráficos ele quer ver (sinal, ruído, comparação e sinal filtrado) e em qual ordem eles serão exibidos.

# Imports das bibliotecas
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from processamento import gerar_sinais

# FUNÇÕES ----------------------------------------------------------------------------------------

# Função que atualiza a interface, adicionando ou removendo o campo da frequência de corte, dependendo de qual opção foi selecionada na combobox
def atualizar_interface(event=None):
    tipo_filtro = combo_filtro.get()

    if tipo_filtro in ["Passa-faixa", "Rejeita-faixa"]:
        frame_fc2.grid()
    else:
        frame_fc2.grid_remove()
#fim atualizar_interface

# Função que abre uma nova janela para o posicionamento dos gráficos
def abrir_janela_graficos(tempo, sinal, ruido, sinal_com_ruido):
    # Criação da janela secundária para os gráficos
    janela_graficos = tk.Toplevel(janela)
    janela_graficos.title("Gráficos da simulação")
    janela_graficos.geometry("1000x700")

    # Criação da figura e dos subplots (gráficos do sinal, ruído, comparação e sinal filtrado) do Matplotlib
    figura = Figure(figsize=(10, 7), dpi=100)
    grafico_sinal = figura.add_subplot(2, 2, 1)
    grafico_ruido = figura.add_subplot(2, 2, 2)
    grafico_entrada = figura.add_subplot(2, 2, 3)
    grafico_filtrado = figura.add_subplot(2, 2, 4)

    # Gráfico do sinal
    grafico_sinal.plot(tempo, sinal, color="blue", label="Sinal desejado")
    grafico_sinal.set_title("Sinal desejado")
    grafico_sinal.set_xlabel("Tempo (s)")
    grafico_sinal.set_ylabel("Amplitude V(t)")
    grafico_sinal.grid(True)
    grafico_sinal.legend()

    # Gráfico do ruído
    grafico_ruido.plot(tempo, ruido, color="red", label="Ruído")
    grafico_ruido.set_title("Ruído")
    grafico_ruido.set_xlabel("Tempo (s)")
    grafico_ruido.set_ylabel("Amplitude V(t)")
    grafico_ruido.grid(True)
    grafico_ruido.legend()

    # Gráfico do sinal desejado e sinal + ruído
    grafico_entrada.plot(tempo, sinal, color="blue", label="Sinal desejado")
    grafico_entrada.plot(tempo, sinal_com_ruido, color="red", label="Sinal + ruído")
    grafico_entrada.set_title("Antes da filtragem")
    grafico_entrada.set_xlabel("Tempo (s)")
    grafico_entrada.set_ylabel("Amplitude V(t)")
    grafico_entrada.grid(True)
    grafico_entrada.legend()

    # Gráfico reservado para o sinal após a filtragem
    grafico_filtrado.set_title("Após a filtragem")
    grafico_filtrado.set_xlabel("Tempo (s)")
    grafico_filtrado.set_ylabel("Amplitude V(t)")
    grafico_filtrado.grid(True)

    figura.tight_layout(pad=3.0) # Ajustando o layout da figura (para que os subplots não fiquem "colados" um no outro)

    # Criação do canvas (onde a figura será desenhada) e adição do canvas à janela dos gráficos
    canvas = FigureCanvasTkAgg(figura, master=janela_graficos)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    canvas.draw() # Desenhando a figura no canvas
#fim abrir_janela_graficos

# Função que "pega" os dados dos campos de entrada, converte para float e armazena isso em suas respectivas variáveis
def aplicar_filtro():
    # O try/except serve para pegar os erros que poderam ocorrer e caso ocorram não parar o programa além de mostrar
    # além de mostrar uma mensagem de erro genérica (a mais detalhada ficaria no terminal)
    try:
        # Campos do sinal
        freq_sinal = float(entry_freq_sinal.get())
        amplitude_sinal = float(entry_amplit_sinal.get())

        # Campos do ruído
        freq_ruido = float(entry_freq_ruido.get())
        amplitude_ruido = float(entry_amplit_ruido.get())

        # Testes/debug dos campos de sinal e ruído
        # print(f"FS: {freq_sinal}; AS: {amplitude_sinal}; FR: {freq_ruido}; AR: {amplitude_ruido}")

        # O retorno da função gerar_sinal será armazenado nas seguintes variáveis (tempo, sinal, ruido, sinal_com_ruido)
        # Essa ordem é baseada na ordem do return de gerar_sinais
        tempo, sinal, ruido, sinal_com_ruido = gerar_sinais(freq_sinal, amplitude_sinal, freq_ruido, amplitude_ruido)

        # Testes/debug dos retornos da função gerar_sinais
        # print("Tempo:", tempo[:5])
        # print("Sinal:", sinal[:5])
        # print("Ruído:", ruido[:5])
        # print("Sinal + ruído:", sinal_com_ruido[:5])

        # Abre a janela separada para exibir os gráficos gerados
        abrir_janela_graficos(tempo, sinal, ruido, sinal_com_ruido)

    except ValueError as erro:
        print(erro)
        messagebox.showerror("ERRO", "Por favor, digite valores válidos")
#fim aplicar_filtro


# 1) JANELA PRINCIPAL ----------------------------------------------------------------------------------------

# Criação da janela principal (onde serão colocados os outros componentes como: labels, entries, frames etc.)
janela = tk.Tk()
janela.title("Simulador de ruídos eletrônicos")
janela.geometry("720x300")
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

# Frame principal para o posicionamento dos parâmetros de sinal, ruído e filtro
frame_parametros = tk.Frame(janela, borderwidth=0.5, relief="solid")
frame_parametros.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
frame_parametros.columnconfigure(0, weight=1, uniform="parametros")
frame_parametros.columnconfigure(2, weight=1, uniform="parametros")
frame_parametros.columnconfigure(4, weight=1, uniform="parametros")

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

# 3.4) Separador (linha vertical entre os frames de ruido e filtro)
separador_filtro = ttk.Separator(frame_parametros, orient="vertical")
separador_filtro.grid(row=0, column=3, sticky="ns", padx=10, pady=10)

# 4) FILTRO ----------------------------------------------------------------------------------------

# Frame para o posicionamento dos elementos relacionados ao filtro (tipo de filtro, frequência de 1 e 2 [fc1 e fc2])
frame_filtros = tk.Frame(frame_parametros)
frame_filtros.grid(row=0, column=4, sticky="nsew", padx=10, pady=10)

# Divisão do espaço do frame em 2 partes iguais (todas tem o mesmo peso)
frame_filtros.columnconfigure(0, weight=1)
frame_filtros.columnconfigure(1, weight=1)

# Label para os parâmetros do filtro 
label_filtros = tk.Label(frame_filtros, text="PARÂMETROS DO FILTRO")
label_filtros.grid(row=0, column=0, columnspan=2, pady=12)

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
frame_fc1.grid(row=2, column=0, pady=(5, 20))

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
frame_fc2.grid(row=2, column=1, pady=(5, 20))

# Label
label_fc2 = tk.Label(frame_fc2, text="fc2 (Hz): ")
label_fc2.grid(row=0, column=0, stick="ew")

# Entry
entry_fc2 = tk.Entry(frame_fc2, width=10)
entry_fc2.insert(0, "0")
entry_fc2.grid(row=0, column=1, stick="ew")

# 5) BOTÕES ----------------------------------------------------------------------------------------

# Frame para o posicionamento dos botões
frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=2, column=0, pady=15)

# Primeiro botão: aplicar filtro
botao_aplicar = ttk.Button(frame_botoes, text="APLICAR FILTRO", command=aplicar_filtro)
botao_aplicar.grid(row=0, column=0, padx=10)

# Segundo botão: limpar tela
botao_limpar = ttk.Button(frame_botoes, text="LIMPAR")
botao_limpar.grid(row=0, column=1, padx=10)

# INICIALIZAÇÃO ----------------------------------------------------------------------------------------

# Necessário chamar a função de atualizar a tela logo no "início", para esconder o campo do fc2 (já que a combobox começa na opção 'passa-baixa')
atualizar_interface()
janela.mainloop()
