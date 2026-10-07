import numpy as np

# Função para geração do sinal e ruído
def gerar_sinais(freq_sinal, amplitude_sinal, freq_ruido, amplitude_ruido, fs=1000, duracao=2):

    # Verificando se a amplitude do ruído não é maior que a do sinal
    if amplitude_ruido > amplitude_sinal:
        raise ValueError("Para esta simulação, a amplitude do ruído não pode ser superior a do sinal principal")

    # Tempo (cria uma lista que representará o tempo entre 0 e 2 [var. duracao],
    # com x pontos/valores por segundo, dependendo do fs)
    tempo = np.arange(0, duracao, 1 / fs)

    # Sinal principal/desejado
    sinal = amplitude_sinal * np.sin(2 * np.pi * freq_sinal * tempo)

    # Sinal do ruído
    ruido = amplitude_ruido * np.sin(2 * np.pi * freq_ruido * tempo)

    # Sinal combinado (sinal + ruído)
    sinal_com_ruido = sinal + ruido

    return tempo, sinal, ruido, sinal_com_ruido
#fim gerar_sinais


# Função para calcular a magnitude normalizada de um espectro gerado com rfft
def calcular_magnitude(espectro, quantidade_amostras):
    magnitude = np.abs(espectro) / quantidade_amostras

    # Como o rfft retorna apenas as frequências não negativas, as componentes positivas
    # precisam ser multiplicadas por 2 para representar a amplitude do sinal original.
    # A componente de 0 Hz nunca é duplicada. Se a quantidade de amostras for par,
    # a última posição corresponde à frequência de Nyquist e também não é duplicada.
    if quantidade_amostras % 2 == 0:
        magnitude[1:-1] *= 2
    else:
        magnitude[1:] *= 2

    return magnitude
#fim calcular_magnitude


# Função para validar uma frequência de corte
def validar_frequencia_corte(fc, fs):
    if fc <= 0:
        raise ValueError("A frequência de corte deve ser maior que zero")

    if fc >= fs / 2:
        raise ValueError("A frequência de corte deve ser menor que a frequência de Nyquist (fs/2)")
#fim validar_frequencia_corte

# Filtro passa-baixa de primeira ordem aplicado no domínio da frequência
def filtro_passa_baixa(sinal_entrada, fc, fs=1000):

    # Chama a função para validar a frequência de corte
    validar_frequencia_corte(fc, fs)

    # Transformada de Fourier do sinal de entrada (domínio do tempo para o da frequência)
    espectro = np.fft.rfft(sinal_entrada)

    # Vetor de frequências correspondentes ao espectro
    frequencias = np.fft.rfftfreq(len(sinal_entrada), d=1 / fs)

    # Resposta em frequência do filtro passa-baixa RC de primeira ordem
    # H(f) = 1 / (1 + j*(f/fc))
    # Em f = fc: H(fc) = 0.5 - 0.5j e |H(fc)| = aproximadamente 0.707
    resposta_filtro = 1 / (1 + 1j * (frequencias / fc))

    # Aplicação do filtro no espectro: Y(f) = X(f) * H(f)
    espectro_filtrado = espectro * resposta_filtro

    # Transformada Inversa de Fourier (domínio da frequência para o do tempo)
    sinal_filtrado = np.fft.irfft(espectro_filtrado, n=len(sinal_entrada))

    # Magnitudes utilizadas nos gráficos de frequência
    magnitude_sem_filtro = calcular_magnitude(espectro, len(sinal_entrada))
    magnitude_filtrada = calcular_magnitude(espectro_filtrado, len(sinal_entrada))

    return sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada
#fim filtro_passa_baixa


# Filtro passa-alta de primeira ordem aplicado no domínio da frequência
def filtro_passa_alta(sinal_entrada, fc, fs=1000):

    # Chama a função para validar a frequência de corte
    validar_frequencia_corte(fc, fs)

    # Transformada de Fourier e vetor de frequências
    espectro = np.fft.rfft(sinal_entrada)
    frequencias = np.fft.rfftfreq(len(sinal_entrada), d=1 / fs)

    # Resposta em frequência do filtro passa-alta RC de primeira ordem
    # H(f) = j*(f/fc) / (1 + j*(f/fc))
    # Em 0 Hz o ganho é 0; em f = fc o módulo é aproximadamente 0.707;
    # para frequências muito maiores que fc o ganho se aproxima de 1.
    proporcao = frequencias / fc
    resposta_filtro = (1j * proporcao) / (1 + 1j * proporcao)

    # Aplicação do filtro no espectro
    espectro_filtrado = espectro * resposta_filtro

    # Retorno para o domínio do tempo
    sinal_filtrado = np.fft.irfft(espectro_filtrado, n=len(sinal_entrada))

    # Magnitudes utilizadas nos gráficos de frequência
    magnitude_sem_filtro = calcular_magnitude(espectro, len(sinal_entrada))
    magnitude_filtrada = calcular_magnitude(espectro_filtrado, len(sinal_entrada))

    return sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada
#fim filtro_passa_alta

# Filtro passa-faixa aplicado no domínio da frequência
def filtro_passa_faixa(sinal_entrada, fc1, fc2, fs=1000):

    # Chama a função para validar as frequências de corte 1 e 2
    validar_frequencia_corte(fc1, fs)
    validar_frequencia_corte(fc2, fs)

    if fc1 >= fc2:
        raise ValueError("fc1 deve ser menor que fc2")

    # Transformada de Fourier e vetor de frequências
    espectro = np.fft.rfft(sinal_entrada)
    frequencias = np.fft.rfftfreq(len(sinal_entrada), d=1 / fs)

    # O passa-faixa é formado pela combinação de:
    # 1) um passa-alta com frequência de corte fc1;
    # 2) um passa-baixa com frequência de corte fc2.
    proporcao_alta = frequencias / fc1
    resposta_passa_alta = (1j * proporcao_alta) / (1 + 1j * proporcao_alta)

    resposta_passa_baixa = 1 / (1 + 1j * (frequencias / fc2))

    # A resposta total é a multiplicação das duas respostas.
    # Frequências abaixo de fc1 e acima de fc2 são progressivamente atenuadas.
    resposta_filtro = resposta_passa_alta * resposta_passa_baixa

    # Aplicação do filtro no espectro
    espectro_filtrado = espectro * resposta_filtro

    # Retorno para o domínio do tempo
    sinal_filtrado = np.fft.irfft(espectro_filtrado, n=len(sinal_entrada))

    # Magnitudes utilizadas nos gráficos de frequência
    magnitude_sem_filtro = calcular_magnitude(espectro, len(sinal_entrada))
    magnitude_filtrada = calcular_magnitude(espectro_filtrado, len(sinal_entrada))

    return sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada
#fim filtro_passa_faixa

# Filtro rejeita-faixa aplicado no domínio da frequência
def filtro_rejeita_faixa(sinal_entrada, fc1, fc2, fs=1000):

    # Chama a função para validar as frequências de corte 1 e 2
    validar_frequencia_corte(fc1, fs)
    validar_frequencia_corte(fc2, fs)

    if fc1 >= fc2:
        raise ValueError("fc1 deve ser menor que fc2")

    # Transformada de Fourier e vetor de frequências
    espectro = np.fft.rfft(sinal_entrada)
    frequencias = np.fft.rfftfreq(len(sinal_entrada), d=1 / fs)

    # O rejeita-faixa combina duas regiões de passagem:
    # 1) passa-baixa com corte em fc1 -> preserva principalmente as frequências baixas;
    # 2) passa-alta com corte em fc2 -> preserva principalmente as frequências altas.
    resposta_passa_baixa = 1 / (1 + 1j * (frequencias / fc1))

    proporcao_alta = frequencias / fc2
    resposta_passa_alta = (1j * proporcao_alta) / (1 + 1j * proporcao_alta)

    # Soma das duas respostas para preservar as regiões abaixo de fc1 e acima de fc2,
    # atenuando progressivamente a faixa entre as duas frequências de corte.
    resposta_filtro = resposta_passa_baixa + resposta_passa_alta

    # Aplicação do filtro no espectro
    espectro_filtrado = espectro * resposta_filtro

    # Retorno para o domínio do tempo
    sinal_filtrado = np.fft.irfft(espectro_filtrado, n=len(sinal_entrada))

    # Magnitudes utilizadas nos gráficos de frequência
    magnitude_sem_filtro = calcular_magnitude(espectro, len(sinal_entrada))
    magnitude_filtrada = calcular_magnitude(espectro_filtrado, len(sinal_entrada))

    return sinal_filtrado, frequencias, magnitude_sem_filtro, magnitude_filtrada
#fim filtro_rejeita_faixa


# TESTES/DEBUG ----------------------------------------------------------------------------------------------------------------
# if __name__ == "__main__":
#     tempo, sinal, ruido, sinal_com_ruido = gerar_sinais(5, 1, 50, 0.4)
#
#     sinal_filtrado, frequencias, magnitude_antes, magnitude_depois = filtro_passa_baixa(
#         sinal_com_ruido,
#         10
#     )
#
#     print("Tempo:", tempo[:5])
#     print("Sinal:", sinal[:5])
#     print("Ruído:", ruido[:5])
#     print("Sinal + ruído:", sinal_com_ruido[:5])
#     print("Sinal filtrado:", sinal_filtrado[:5])
