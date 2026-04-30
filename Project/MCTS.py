#Monte Carlo Tree Search
import math
import random

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state      #estado atual do jogo
        self.parent = parent    #nó pai
        self.move = move        #jogada que originou este estado

        self.children = []      #lista de nós filhos já expandidos
        self.wins = 0           #numero de vitorias a partir de este nó
        self.visits = 0         #numero de vezes que este no foi visitado
        self.untried_moves = state.get_legal_moves()

        if parent is not None:
            self.player_who_moved = parent.state.current_player
        else:
            self.player_who_moved = None

        #Guardamos as jogadas possiveis que ainda nao transformamos em filhos
        self.untried_moves = state.get_legal_moves()

    def uct_value(self, c_param=1.41):
        #Calcula o valor UCT do nó para decidir se devemos explorá-lo

        #Se o nó nunca foi visitado, damos prioridade maxima para o explorar
        if self.visits == 0:
            return float('inf')
        
        #Taxa de vitoria deste nó
        tx_v = self.wins / self.visits

        #Incentiva a explorar nós menos visitados face ao pai
        exp = c_param * math.sqrt(math.log(self.parent.visits) / self.visits)

        return tx_v + exp
    
    def add_child(self, child_state, move):
        #Cria um filho e junta-o à arvore
        child_node = Node(state=child_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child_node)
        return child_node
    
    def update(self, result):
        #Atualiza estatísticas após uma simulação
        self.visits +=1

        if result == self.player_who_moved:
            self.wins += 1
        elif result == 'DRAW':
            #Um empate é melhor do que derrota logo adicionamos 0.5
            self.wins += 0.5

class MCTS:
    def __init__(self, ai_player, iterations=10000):
        self.ai_player = ai_player      #Define se a IA está a jogar com 'X' ou 'O'
        self.iterations = iterations    #Quantos "jogos à sorte" vamos simular por jogada

    def search(self, initial_state):
        #Devolve a melhor jogada possível após realizar milhares de simulações

        #Nó raiz estado do tabuleiro exatamente como ele está agora
        root = Node(state=initial_state.clone())

        #O ciclo de simulações(limitado pelo iteration 1000)
        for _ in range(self.iterations):
            node = root
            state = initial_state.clone()   #Usamos um clone novo para podermos usar nas simulações

            #Descemos pela árvore já explorada usando a fórmula UCT
            while len(node.untried_moves) == 0 and len(node.children) > 0:
                node = max(node.children, key=lambda c: c.uct_value())
                state.apply_move(node.move[0], node.move[1])
                state.switch_player()  #Alternamos o jogador para refletir a mudança de estado

            #Se chegarmos a um no com jogadas por testar
            if len(node.untried_moves) > 0 and state.get_game_result() is None:
                #Escolhemos uma jogada à sorte que ainda nao testamos
                move = random.choice(node.untried_moves)
                state.apply_move(move[0], move[1])
                state.switch_player()  #Alternamos o jogador para refletir a mudança de estado
                #Criamos um filho novo na árvore
                node = node.add_child(state.clone(), move)
            
            #SIMULAÇÃO
            #Jogamos sempre à sorte até alguem ganhar ou empatar
            while state.get_game_result() is None:
                possible_moves = state.get_legal_moves()
                if not possible_moves:
                    break
                move = random.choice(possible_moves)
                state.apply_move(move[0], move[1])
                state.switch_player()  #Alternamos o jogador para refletir a mudança de estado
            
            #No fim da simulação vemos que ganhou
            result = state.get_game_result()

            while node is not None:
                node.update(result)
                node = node.parent
        
        #A jogada que escolhemos é do filho que foi visitado mais vezes
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move
