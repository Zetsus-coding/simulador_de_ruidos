# Simulador de Ruídos Eletrônicos e Filtros Digitais

Projeto desenvolvido em Python para simular um sinal senoidal, adicionar uma interferência também senoidal e observar o efeito de diferentes filtros sobre o sinal resultante.

O programa possui uma interface gráfica feita com **Tkinter** e utiliza **NumPy** para gerar e processar os sinais e **Matplotlib** para exibir os gráficos.

## Objetivo

O objetivo do projeto é visualizar, de forma simples, como filtros podem atenuar determinadas componentes de frequência de um sinal.

O usuário informa:

- frequência e amplitude do sinal desejado;
- frequência e amplitude da interferência;
- tipo de filtro;
- frequência de corte (`fc1` e, quando necessário, `fc2`).

A partir desses valores, o programa gera o sinal, aplica o filtro escolhido e compara o resultado antes e depois da filtragem.

> Neste projeto, o termo **ruído** representa uma interferência senoidal simulada. Portanto, não se trata de um ruído aleatório.

## Filtros disponíveis

O programa possui quatro tipos de filtro:

### Passa-baixa

Preserva principalmente as frequências abaixo da frequência de corte e atenua progressivamente as frequências mais altas.

### Passa-alta

Preserva principalmente as frequências acima da frequência de corte e atenua progressivamente as frequências mais baixas.

### Passa-faixa

Utiliza duas frequências de corte e preserva principalmente as componentes localizadas entre `fc1` e `fc2`.

### Rejeita-faixa

Utiliza duas frequências de corte e atenua principalmente as componentes localizadas entre `fc1` e `fc2`, preservando as regiões abaixo e acima dessa faixa.

## Como o processamento funciona

O processamento dos filtros é feito no domínio da frequência.

De forma resumida, o fluxo é:

```text
Sinal + interferência
        ↓
      rFFT
        ↓
Espectro X(f)
        ↓
Aplicação da resposta do filtro H(f)
        ↓
Y(f) = X(f) · H(f)
        ↓
     irFFT
        ↓
Sinal filtrado
```

A função `np.fft.rfft()` converte o sinal do domínio do tempo para o domínio da frequência. Em seguida, cada componente do espectro é multiplicada pela resposta do filtro correspondente.

Depois da filtragem, `np.fft.irfft()` reconstrói o sinal no domínio do tempo.

Os filtros utilizam respostas de primeira ordem, com atenuação gradual em vez de um corte instantâneo.

## Exemplo de teste

Um exemplo simples para visualizar o comportamento do programa é:

```text
Sinal desejado:
Frequência = 5 Hz
Amplitude = 1 V

Interferência:
Frequência = 50 Hz
Amplitude = 0,7 V

Filtro passa-baixa:
fc = 10 Hz
```

Nesse caso, o filtro tende a preservar mais a componente de `5 Hz` e reduzir a componente de `50 Hz`.

O mesmo conjunto de sinais pode ser utilizado para comparar o comportamento dos outros filtros.

## Estrutura do projeto

```text
projeto/
│
├── interface_tkinter.py
├── processamento.py
└── README.md
```

### `interface_tkinter.py`

Responsável pela interface gráfica do programa. Nela são criados:

- janela principal;
- campos de entrada;
- seleção do tipo de filtro;
- botões;
- gráficos.

A interface também lê os valores informados pelo usuário e chama as funções presentes no arquivo de processamento.

### `processamento.py`

Responsável pelos cálculos do projeto. Contém as funções de:

- geração do sinal e da interferência;
- cálculo da FFT;
- cálculo da magnitude do espectro;
- validação das frequências de corte;
- aplicação dos quatro filtros;
- reconstrução do sinal após a filtragem.

## Tecnologias utilizadas

- **Python 3**
- **Tkinter** — interface gráfica
- **NumPy** — geração dos sinais, FFT e cálculos numéricos
- **Matplotlib** — geração dos gráficos

## Requisitos

É necessário ter Python instalado e as bibliotecas NumPy e Matplotlib.

Instalação das dependências:

```bash
python -m pip install numpy matplotlib
```

O Tkinter normalmente já acompanha a instalação padrão do Python no Windows.

## Como executar

1. Baixe ou clone o projeto.
2. Certifique-se de que `interface_tkinter.py` e `processamento.py` estejam na mesma pasta.
3. Instale as dependências, caso ainda não estejam instaladas.
4. Execute o arquivo da interface:

```bash
python interface_tkinter.py
```

5. Informe os parâmetros do sinal, da interferência e do filtro.
6. Clique em **APLICAR FILTRO**.

## Observações

A frequência de amostragem padrão utilizada no projeto é de `1000 Hz`.

Por esse motivo, as frequências de corte devem permanecer abaixo da frequência de Nyquist:

```text
fs / 2 = 500 Hz
```

Para os filtros passa-faixa e rejeita-faixa também deve ser respeitada a condição:

```text
fc1 < fc2
```

Os filtros não alteram a frequência original de uma componente. Eles modificam principalmente sua amplitude e sua fase, de acordo com a resposta do filtro.

## Possíveis melhorias futuras

Algumas melhorias que podem ser adicionadas futuramente são:

- exibição do espectro de frequência antes e depois da filtragem;
- reorganização da interface com menu lateral;
- inclusão de outros tipos de ruído;
- comparação entre diferentes ordens de filtros;
- exibição numérica da atenuação de cada componente de frequência.

## Contexto

Projeto desenvolvido como atividade acadêmica de Engenharia, com foco em programação aplicada, processamento de sinais e compreensão do funcionamento de filtros digitais.
