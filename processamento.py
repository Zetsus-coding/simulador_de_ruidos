import numpy as np

# Função para geração do sinal e ruído
def gerar_sinais(freq_sinal, amplitude_sinal, freq_ruido, amplitude_ruido, fs=1000, duracao=2):

    # Verificando se a amplitude do ruído não é maior que a do sinal
    if amplitude_ruido > amplitude_sinal:
        raise ValueError ("Para esta simulação, a amplitude do ruído não pode ser superior a do sinal principal")

    # Tempo (Cria uma lista que representará o tempo entre 0 e 2 [var. duracao] (com x pontos/valores por seg. - depende do fs))
    tempo = np.arange(0, duracao, 1/fs)
    #print(tempo[:5])

    # Sinal principal/desejado
    sinal = amplitude_sinal * np.sin(2 * np.pi * freq_sinal * tempo)

    # Sinal do ruído
    ruido = amplitude_ruido * np.sin(2 * np.pi * freq_ruido * tempo)

    # Sinal combinado (sinal + ruido)
    sinal_com_ruido = sinal + ruido

    return tempo, sinal, ruido, sinal_com_ruido
#fim gerar_sinais


# TESTES ----------------------------------------------------------------------------------------------------------------
# if __name__ == "__main__":
#     tempo, sinal, ruido, sinal_com_ruido = gerar_sinais(
#         5,
#         1,
#         50,
#         0.4
#     )

#     print("Tempo:", tempo[:5])
#     print("Sinal:", sinal[:5])
#     print("Ruído:", ruido[:5])
#     print("Sinal + ruído:", sinal_com_ruido[:5])
