## Explorando o Jogo da Vida: Uma Abordagem Prática para Programação e Sistemas Distribuídos ##

**Objetivo**
Este repositório tem como objetivo explorar e demonstrar o Jogo da Vida de Conway como um modelo para compreender conceitos fundamentais de Sistemas Distribuídos. O projeto apresenta:

1. Uma implementação prática do Jogo da Vida de Conway, demonstrando suas regras e comportamentos emergentes.

2. Um artigo detalhado explicando:
* Os fundamentos e regras do autômato celular
* A história e importância do Jogo da Vida na computação
* Padrões comuns e suas evoluções
* Análise das propriedades emergentes do sistema


3. Correlação com Sistemas Distribuídos, explorando:
* Paralelismo natural do jogo (cada célula pode ser processada independentemente)
* Comunicação entre componentes (interação entre células vizinhas)
* Sincronização de estados (atualizações simultâneas das gerações)
* Tolerância a falhas (o sistema continua funcionando mesmo com células "mortas")
* Escalabilidade (o tabuleiro pode crescer mantendo as mesmas regras)
* Comportamento emergente em sistemas complexos


4. Implementações práticas demonstrando:
* Versão sequencial do jogo
* Versão paralela/distribuída
* Análise comparativa de performance
* Visualização do comportamento do sistema


Este projeto serve como uma ponte entre a teoria e a prática, usando um exemplo clássico e visualmente intuitivo para demonstrar conceitos complexos de sistemas distribuídos.

# **Pré-requisitos**
* Python 3.x
* VSCode (recomendado)
* Git

## **Como rodar o jogo da vida na sua máquina**

OBS.: Recomenda-se usar a IDE VSCode para melhor experiência de desenvolvimento.
1. **Clonar o repositório**
   Clonar o repositório no VSCode, escolha sua pasta destino e execute o comando abaixo no terminal:
    ```
    git clone https://github.com/Edugon0/Game-of-life-conway.git
    ```
  
2. **Instalar dependências necessarias para rodar o jogo**
* instalar biblioteca Numpy
   ```
    pip install numpy
   ```
* instalar biblioteca Matplotlib
   ```
    pip install matplotlib
   ```
3. **Executar o projeto**
   ```
    python index.py
   ```

# **Estrutura do Projeto**
 ```
.
├── README.md
├── index.py
└── Jogo da Vida.mp4
└── Explorando o Jogo da Vida_ Uma Abordagem Prática para Programação e Sistemas Distribuídos.docx.pdf
 ```
## **Colaboradores**

* Ana Beatriz M. Soares
* Camille Vitoria S. Andrade
* Eduardo Victor de O. Gonçalves
