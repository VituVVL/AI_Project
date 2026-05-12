import csv
import ast
import math
from collections import Counter


def carregar_dados(filename):
    # Lê o CSV e converte a string do tabuleiro numa lista de 42 atributos.

    X = [] # guarda os tabuleiros (cada um com 42 posições)
    y = [] # guarda as melhores jogadas
    
    print(f"A ler o ficheiro {filename}...")
    
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader) # Saltar o cabeçalho
        
        for linha in reader:
            if not linha: continue
            
            
            board_matriz = ast.literal_eval(linha[0])
            best_move = linha[1]
            
            # "Achatar" a matriz 6x7 numa única lista de 42 elementos
            board_achatado = []
            for row in board_matriz:
                board_achatado.extend(row)
                
            X.append(board_achatado)
            y.append(best_move)
            
    print(f"Total de exemplos: {len(X)}")
    return X, y

def calcular_entropia(labels):
    #Calcula a impureza/entropia de um conjunto de decisões.

    total_exemplos = len(labels)
    if total_exemplos == 0:
        return 0.0
    
    # Conta quantas vezes cada jogada aparece na lista
    contagem = Counter(labels)
    entropia = 0.0
    
    for jogada, quantidade in contagem.items():
        probabilidade = quantidade / total_exemplos
        # Fórmula da Entropia
        entropia -= probabilidade * math.log2(probabilidade)
        
    return entropia

def ganho_informacao(x, y, indice):
    entropia_base = calcular_entropia(y)

    subconjuntos = {}
    for i in range(len(x)):
        valor_da_casa = x[i][indice]
        if valor_da_casa not in subconjuntos:
            subconjuntos[valor_da_casa] = []
        subconjuntos[valor_da_casa].append(y[i])
    
    entropia_nova = 0.0
    total_exemplos = len(y)

    for valor_da_casa, jogadas in subconjuntos.items():
        peso = len(jogadas) / total_exemplos
        entropia_nova += peso * calcular_entropia(jogadas)

    return entropia_base - entropia_nova

def construir_arvore(x, y, atributos):
    #Contrutor da arvore passo a passo

    # todas as jogadas neste ramo forem iguais, devolvemos essa jogada (Folha Pura)
    if len(set(y)) == 1:
        return y[0]
    
    # já não houver mais casas para testar, devolvemos a jogada mais comum
    if len(atributos) == 0:
        return Counter(y).most_common(1)[0][0]
    
    # escolher a melhor pergunta
    melhor_ganho = -1
    melhor_atributo = None

    for atributo in atributos:
        ganho = ganho_informacao(x, y, atributo)
        if ganho > melhor_ganho:
            melhor_ganho = ganho
            melhor_atributo = atributo

    # se nenhuma pergunta melhorar a informação, devolvemos a jogada mais comum
    if melhor_ganho == 0:
        return Counter(y).most_common(1)[0][0]
    
    # criar o no da arvore
    arvore = {melhor_atributo: {}}

    # remover o atributo escolhido para não voltarmos a perguntar sobre a mesma casa
    novos_atributos = atributos.copy()
    novos_atributos.remove(melhor_atributo)

    # descobrir que valores ('X', 'O', '-') existem nesta casa no nosso dataset
    valores_nesta_casa = set([x[i][melhor_atributo] for i in range(len(x))])

    for valor in valores_nesta_casa:
        x_sub = []
        y_sub = []

        for i in range(len(x)):
            if x[i][melhor_atributo] == valor:
                x_sub.append(x[i])
                y_sub.append(y[i])
            
        arvore[melhor_atributo][valor] = construir_arvore(x_sub, y_sub, novos_atributos)
    
    return arvore

# Colocar a IA a jogar
def prever_jogada(arvore, estado_tabuleiro):
    if not isinstance(arvore ,dict):
        return arvore
    
    pergunta_casa = list(arvore.keys())[0]

    valor_no_tabuleiro = estado_tabuleiro[pergunta_casa]

    if valor_no_tabuleiro in arvore[pergunta_casa]:
        proximo_no = arvore[pergunta_casa][valor_no_tabuleiro]
        return prever_jogada(proximo_no, estado_tabuleiro)
    else:
        #Cair num cenário que a árvore nunca viu na vida
        ramo_seg = list(arvore[pergunta_casa].keys())[0]
        proximo_no = arvore[pergunta_casa][ramo_seg]
        return prever_jogada(proximo_no, estado_tabuleiro)
    

class ID3Jogador:
    def __init__(self, arvore_treinada):
        self.arvore = arvore_treinada

    def search(self, game_state):
        board_achatado = []
        for row in game_state.board:
            board_achatado.extend(row)

        jogada_str = prever_jogada(self.arvore, board_achatado)

        partes = jogada_str.split()
        move_type = partes[0]
        coluna = int(partes[1])

        return (move_type, coluna)


if __name__ == "__main__":
    import time
    # 1. Carregar os Dados
    X_dados, y_jogadas = carregar_dados("dataset_popout_3000.csv")
    
    # O nosso tabuleiro tem 42 posições (0 a 41)
    atributos = list(range(42))
    
    tempo_inicio = time.time()
    
    # 2. Treinar a Árvore Mágica
    minha_arvore_id3 = construir_arvore(X_dados, y_jogadas, atributos)
    
    tempo_fim = time.time()
    
    print(f"Tempo: {tempo_fim - tempo_inicio:.2f} segundos!")
    print(f"Raiz da árvore (A primeira pergunta que a IA faz): A casa {list(minha_arvore_id3.keys())[0]}")