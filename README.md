# PopOut - Connect 4 com MCTS e ID3

Projeto desenvolvido no âmbito da disciplina de Inteligência Artificial.

O objetivo do projeto é implementar o jogo **PopOut**, uma variação do Connect 4 tradicional, e aplicar algoritmos de pesquisa e aprendizagem para tomada de decisão durante o jogo.

Neste projeto foram implementados:

- Jogo PopOut em modo texto;
- Modo USER vs USER;
- Modo USER vs IA;
- IA baseada em Monte Carlo Tree Search;
- Geração de datasets a partir de simulações com MCTS;
- Algoritmo ID3 treinado com os datasets gerados;
- Comparação entre ID3 e MCTS.

---

## Regras do jogo

O jogo utiliza um tabuleiro de **6 linhas por 7 colunas**.

Cada jogador pode realizar dois tipos de jogada:

### Drop

O jogador coloca uma peça numa coluna.

A peça cai para a posição livre mais baixa da coluna escolhida.

Exemplo:

```text
drop 4
```

### Pop

O jogador remove a peça inferior de uma coluna, desde que essa peça pertença ao próprio jogador.

Quando isso acontece, as peças acima descem uma posição.

Exemplo:

```text
pop 2
```

---

## Condições de vitória e empate

Um jogador vence quando consegue formar uma sequência de 4 peças:

- na horizontal;
- na vertical;
- na diagonal principal;
- na diagonal secundária.

Também foram implementadas regras específicas do PopOut:

- se um movimento `pop` criar quatro em linha para ambos os jogadores, vence o jogador que fez o `pop`;
- se o mesmo estado do tabuleiro se repetir 3 vezes, o jogo termina em empate;
- se não houver movimentos possíveis, o jogo termina em empate.

---

## Estrutura do projeto

A estrutura organizada do projeto é:

```text
AI_PROJECT/
│
├── Notebook.ipynb
├── README.md
│
└── Project/
    │
    ├── PopOut.py
    ├── MCTS.py
    ├── ID3.py
    │
    └── Data/
        ├── dataset_popout_100.csv
        ├── dataset_popout_3000.csv
        ├── dataset_popout_5000.csv
        └── iris.csv
```

---

## Descrição dos arquivos

### `PopOut.py`

Arquivo principal do projeto.

Contém:

- implementação do tabuleiro;
- regras do jogo;
- validação de jogadas;
- deteção de vitórias e empates;
- menu principal;
- modo USER vs USER;
- modo USER vs IA;
- geração de datasets com MCTS;
- função de comparação entre ID3 e MCTS.

---

### `MCTS.py`

Contém a implementação do algoritmo **Monte Carlo Tree Search**.

O MCTS utiliza:

- seleção com UCT;
- expansão de nós;
- simulação aleatória de partidas;
- retropropagação dos resultados;
- reaproveitamento parcial da árvore entre jogadas através da função `update_root`.

As opções disponíveis no menu do jogo incluem:

- MCTS com 100 iterações;
- MCTS com 3000 iterações;
- MCTS com 5000 iterações.

---

### `ID3.py`

Contém a implementação do algoritmo **ID3**.

O ID3 é treinado com os datasets gerados pelas simulações do MCTS.

O dataset é lido em formato CSV, onde cada linha contém:

- o estado do tabuleiro;
- a melhor jogada escolhida pelo MCTS.

Cada tabuleiro 6x7 é transformado numa lista com 42 atributos, representando cada posição do tabuleiro.

---

### `Notebook.ipynb`

Notebook utilizado para testes, experiências, análise de resultados e apoio ao relatório.

O notebook pode ser mantido fora da pasta `Project`, enquanto os códigos principais ficam dentro da pasta `Project`.

---

## Datasets

Os datasets foram gerados automaticamente através de partidas simuladas entre duas IAs MCTS.

Atualmente existem datasets gerados com diferentes números de iterações:

```text
dataset_popout_100.csv
dataset_popout_3000.csv
dataset_popout_5000.csv
```

O dataset principal utilizado para treinar o ID3 é:

```text
dataset_popout_3000.csv
```

Também foi gerado um dataset com MCTS 5000 iterações para testes e comparação no relatório.

---

## Como executar o jogo

A partir da pasta principal do projeto, entre na pasta `Project`:

```bash
cd Project
```

Execute o arquivo principal:

```bash
python PopOut.py
```

O menu inicial apresenta as opções:

```text
PopOut
1- USER vs USER
2- USER vs IA
```

Ao escolher `USER vs IA`, é apresentado um segundo menu:

```text
Escolha a IA:
1- MCTS 100 iterações
2- MCTS 3000 iterações
3- MCTS 5000 iterações
4- ID3 treinado com dataset_popout_3000.csv
```

---

## Como jogar

Durante a partida, o jogador deve escrever o tipo de movimento e a coluna.

Exemplos:

```text
drop 4
```

```text
pop 2
```

As colunas são numeradas de 1 a 7.

Internamente, o programa converte a coluna para índice de 0 a 6.

---

## Como gerar um dataset

No final do arquivo `PopOut.py`, é possível alterar o bloco principal para gerar novos datasets.

Exemplo:

```python
if __name__ == "__main__":
    game = PopOutGame()
    game.generate_dataset(num_games=200, iterations=3000)
```

Esse comando gera ou atualiza o arquivo:

```text
Project/Data/dataset_popout_3000.csv
```

Também é possível gerar datasets com outro número de iterações:

```python
game.generate_dataset(num_games=300, iterations=5000)
```

Nesse caso, o arquivo gerado será:

```text
Project/Data/dataset_popout_5000.csv
```

---

## Como treinar o ID3

O ID3 pode ser executado diretamente pelo arquivo `ID3.py`.

Na pasta `Project`, execute:

```bash
python ID3.py
```

O programa carrega o dataset:

```text
Project/Data/dataset_popout_3000.csv
```

Depois constrói a árvore de decisão com base nos estados do tabuleiro e nas jogadas escolhidas pelo MCTS.

---

## Comparação ID3 vs MCTS

O arquivo `PopOut.py` contém uma função chamada `idvsmc`.

Ela coloca o ID3 a jogar contra o MCTS.

Exemplo de utilização:

```python
if __name__ == "__main__":
    idvsmc(num_games=5)
```

Nesse teste:

- o ID3 joga com `X`;
- o MCTS joga com `O`;
- são contabilizadas vitórias do ID3, vitórias do MCTS e empates.

---

## Algoritmo MCTS

O algoritmo **Monte Carlo Tree Search** foi utilizado para escolher jogadas através de simulações.

O funcionamento geral do MCTS segue quatro etapas:

1. **Seleção**  
   A árvore é percorrida utilizando a fórmula UCT, que equilibra exploração e aproveitamento.

2. **Expansão**  
   Uma jogada ainda não explorada é escolhida e adicionada à árvore como novo nó.

3. **Simulação**  
   A partir do novo estado, o jogo é simulado com jogadas aleatórias até chegar a uma vitória ou empate.

4. **Retropropagação**  
   O resultado da simulação é propagado de volta pelos nós visitados, atualizando visitas e vitórias.

A fórmula UCT é usada para escolher os nós mais promissores durante a fase de seleção.

---

## Algoritmo ID3

O algoritmo **ID3** foi utilizado para construir uma árvore de decisão a partir dos exemplos gerados pelo MCTS.

Cada exemplo do dataset contém:

- uma configuração do tabuleiro;
- a jogada escolhida pelo MCTS para aquele estado.

O tabuleiro é transformado numa lista com 42 atributos, um para cada posição do tabuleiro.

Durante a construção da árvore, o ID3 utiliza:

- entropia;
- ganho de informação;
- escolha do melhor atributo para divisão dos dados.

A árvore treinada passa a ser usada como uma IA capaz de prever jogadas com base no estado atual do tabuleiro.

---

## Otimização da verificação de vitória

Inicialmente, a verificação de vitória era feita separadamente para cada jogador através da função `check_winner_for`.

Depois, essa lógica foi otimizada com a função `get_winners`, que percorre o tabuleiro uma única vez e identifica se houve vitória de `X`, de `O` ou de ambos.

Essa alteração não modificou as regras do jogo.

A equivalência entre a versão antiga e a nova foi testada através de simulações automáticas, comparando os resultados das duas abordagens em múltiplos estados de jogo.

A otimização reduziu significativamente o tempo gasto na verificação de estados terminais durante as simulações do MCTS.

---

## Observações sobre desempenho

O MCTS é o componente mais pesado do projeto, principalmente quando são utilizadas muitas iterações.

Uma partida com MCTS 3000 ou 5000 iterações pode demorar mais tempo, pois cada jogada executa milhares de simulações.

Durante os testes, também foi utilizada uma opção com MCTS 100 iterações para permitir partidas mais rápidas.

A geração dos datasets também pode demorar, porque cada partida simulada envolve múltiplas chamadas ao MCTS.

---

## Requisitos

O projeto foi desenvolvido em Python.

As principais bibliotecas utilizadas pertencem à biblioteca padrão:

- `csv`
- `os`
- `time`
- `math`
- `random`
- `ast`
- `collections`

O notebook pode utilizar bibliotecas adicionais para análise e visualização, como:

- `matplotlib`

---

## Como executar o notebook

O notebook pode ficar fora da pasta `Project`.

Caso seja necessário importar os arquivos do projeto a partir do notebook, pode ser usado o seguinte código no início do notebook:

```python
import sys
from pathlib import Path

ROOT_DIR = Path.cwd()
PROJECT_DIR = ROOT_DIR / "Project"

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import Project.ID3 as ID3
```

Os datasets devem ser acessados dentro da pasta:

```text
Project/Data/
```

---

## Estado atual do projeto

O projeto contém:

- jogo PopOut funcional;
- modo USER vs USER;
- modo USER vs IA;
- IA MCTS funcional;
- IA ID3 funcional;
- geração de datasets;
- menu com diferentes opções de IA;
- comparação entre ID3 e MCTS;
- estrutura organizada com datasets separados na pasta `Data`.

---

## Autores
- [Sérgio Gomes Pinto](https://github.com/SergioGP12) (up202309160)
- [Francisco Ribeiro](https://github.com/Kyuri-beiro) (up202304757)
- [Victor de Vargas Lopes](https://github.com/vituvvl) (up202400863)

Projeto desenvolvido no âmbito da disciplina de Inteligência Artificial, nas licenciaturas de Ciência dos Computadores(CC) e Inteligência Artificial e Ciência de Dados(IACD) da Universidade do Porto.