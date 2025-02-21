import random
import json
import ast

class Domino:
    def __init__(self):
        self.pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]

    # Começa o jogo 
    def start(self, qtd0, qtd1):
        # Setando váriaveis
        self.field = []
        self.hand0 = []
        self.hand1 = []
        self.edges = []
        self.rest = []
        self.aux = []
        self.backups = [0,0,0,0,0,0,0]
        self.biggest = [[],0,0]
        self.hasWinner = False
        self.round = 0
        # Emabaralha e distribui as peças 
        self.shuffle = random.sample(self.pieces, len(self.pieces))
        for _ in range(qtd0):
            self.hand0.append(self.shuffle[0])
            del self.shuffle[0]
        for _ in range(qtd1):
            self.hand1.append(self.shuffle[1])
            del self.shuffle[0]
        self.rest = self.shuffle
        # Coloca uma peça qualquer
        self.edges.append(self.hand0[0][0])
        self.edges.append(self.hand0[0][1])
        # Adiciona a nova peça no campo
        self.field.append(self.hand0[0])
        # Removendo a peça da mão
        del self.hand0[0]
        # Avança o turno
        self.round += 1

    # Valida a jogada
    def valid(self):
        # Verifica de quem é a vez
        if self.round%2 == 0:
            for i in range(len(self.hand0)):
                if self.hand0[i][0] in self.edges:
                    return True
                if self.hand0[i][1] in self.edges:
                    return True
        else:
            for i in range(len(self.hand1)):
                if self.hand1[i][0] in self.edges:
                    return True
                if self.hand1[i][1] in self.edges:
                    return True
        return False

    def data(self):
        return {
            'Turno': self.round,
            'Campo': self.field,
            'Bordas': self.edges,
            'Hands': [self.hand0, self.hand1],
            'IAs': [IA(domino.field, domino.edges, domino.hand0, domino.hand1), IA(domino.field, domino.edges, domino.hand1, domino.hand0)]
        }

    # Jogada
    def play(self):

        # Verificar se houve ganhador
        if len(self.hand0) == 0:
            self.hasWinner = True
            self.winner = 0
        elif len(self.hand1) == 0:
            self.hasWinner = True
            self.winner = 1
        else:
            # Verifica se o jogador tem jogadas válidas
            if self.valid():
                # Verifica o jogador da vez
                if self.round%2 == 0:
                    self.aux = []
                    self.backups = [0,0,0,0,0,0,0]
                    self.biggest = [[],0,0]
                    # Percorre a mão do jogador da vez
                    for i in range(len(self.hand0)):
                        # Verificando peças com mais backup
                        self.backups[self.hand0[i][0]] += 1
                        self.backups[self.hand0[i][1]] += 1

                        # Verificando possiveis jogadas
                        if self.edges[0] in self.hand0[i] or self.edges[1] in self.hand0[i]:
                            self.aux.append(self.hand0[i])
                    
                    if len(self.aux)>1:
                        for j in range(len(self.aux)):
                            # Métrica pra verificar maior backup
                            backup = (self.backups[self.aux[j][0]]+self.backups[self.aux[j][1]])
                            # Métrica pra verificar maior peça
                            biggest = self.aux[j][0] + self.aux[j][1]

                            # Se empatar no backup pegar a maior peça
                            if backup == self.biggest[1]:
                                if biggest > self.biggest[2]:
                                    self.biggest = [self.aux[j], backup, biggest]
                            elif backup > self.biggest[1]:
                                self.biggest = [self.aux[j], backup, biggest]
                        
                        for j in range(len(self.edges)):
                            if self.biggest[0][0] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.biggest[0][0]
                                # Adiciona a nova peça no campo
                                self.field.append(self.biggest[0])
                                # Remove a peça da mão
                                del self.hand0[self.hand0.index(self.biggest[0])]
                                # Avança o turno
                                self.round += 1
                                break
                            
                            if self.biggest[0][1] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.biggest[0][1]
                                # Adiciona a nova peça no campo
                                self.field.append(self.biggest[0])
                                # Remove a peça da mão
                                del self.hand0[self.hand0.index(self.biggest[0])]
                                # Avança o turno
                                self.round += 1
                                break
                    else:
                        for j in range(len(self.edges)):
                            if self.aux[0][0] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.aux[0][0]
                                # Adiciona a nova peça no campo
                                self.field.append(self.aux[0])
                                # Remove a peça da mão
                                del self.hand0[self.hand0.index(self.aux[0])]
                                # Avança o turno
                                self.round += 1
                                break
                            
                            if self.aux[0][1] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.aux[0][1]
                                # Adiciona a nova peça no campo
                                self.field.append(self.aux[0])
                                # Remove a peça da mão
                                del self.hand0[self.hand0.index(self.aux[0])]
                                # Avança o turno
                                self.round += 1
                                break
                            
                else:
                    self.aux = []
                    self.backups = [0,0,0,0,0,0,0]
                    self.biggest = [[],0,0]
                    # Percorre a mão do jogador da vez
                    for i in range(len(self.hand1)):
                        # Verificando peças com mais backup
                        self.backups[self.hand1[i][0]] += 1
                        self.backups[self.hand1[i][1]] += 1

                        # Verificando possiveis jogadas
                        if self.edges[0] in self.hand1[i] or self.edges[1] in self.hand1[i]:
                            self.aux.append(self.hand1[i])

                    for ii in range(len(self.field)):
                        self.backups[self.field[ii][0]] += 1
                        self.backups[self.field[ii][1]] += 1

                    
                    if len(self.aux)>1:
                        for j in range(len(self.aux)):
                            # Métrica pra verificar maior backup
                            backup = (self.backups[self.aux[j][0]]+self.backups[self.aux[j][1]])
                            # Métrica pra verificar maior peça
                            biggest = self.aux[j][0] + self.aux[j][1]

                            # Se empatar no backup pegar a maior peça
                            if backup == self.biggest[1]:
                                if biggest > self.biggest[2]:
                                    self.biggest = [self.aux[j], backup, biggest]
                            elif backup > self.biggest[1]:
                                self.biggest = [self.aux[j], backup, biggest]
                        
                        for j in range(len(self.edges)):
                            if self.biggest[0][0] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.biggest[0][0]
                                # Adiciona a nova peça no campo
                                self.field.append(self.biggest[0])
                                # Remove a peça da mão
                                del self.hand1[self.hand1.index(self.biggest[0])]
                                # Avança o turno
                                self.round += 1
                                break
                            
                            if self.biggest[0][1] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.biggest[0][1]
                                # Adiciona a nova peça no campo
                                self.field.append(self.biggest[0])
                                # Remove a peça da mão
                                del self.hand1[self.hand1.index(self.biggest[0])]
                                # Avança o turno
                                self.round += 1
                                break
                    else:
                        for j in range(len(self.edges)):
                            if self.aux[0][0] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.aux[0][0]
                                # Adiciona a nova peça no campo
                                self.field.append(self.aux[0])
                                # Remove a peça da mão
                                del self.hand1[self.hand1.index(self.aux[0])]
                                # Avança o turno
                                self.round += 1
                                break
                            
                            if self.aux[0][1] == self.edges[j]:
                                # Substitui a borda antiga pela nova
                                self.edges[j] = self.aux[0][1]
                                # Adiciona a nova peça no campo
                                self.field.append(self.aux[0])
                                # Remove a peça da mão
                                del self.hand1[self.hand1.index(self.aux[0])]
                                # Avança o turno
                                self.round += 1
                                break
            
            # Caso não haja jogadas válidas
            else:
                # Verifica o jogador da vez
                if self.round%2 == 0:
                    # Verifica se ainda há resto pra pegar
                    if len(self.rest) == 0:
                        self.hasWinner = True
                        self.winner = 1
                    else:
                        # Adiciona uma peça do resto à mão
                        self.hand0.append(self.rest[0])
                        del self.rest[0]
                else:
                    # Verifica se ainda há resto pra pegar
                    if len(self.rest) == 0:
                        self.hasWinner = True
                        self.winner = 0
                    else:
                        # Adiciona uma peça do resto à mão
                        self.hand1.append(self.rest[0])
                        del self.rest[0]


# Traduz o estado do jogo para um array com dados binarios
def IA(field, edges, player, enemy):
    pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]
    field_ia = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    edges_ia = [0, 0, 0, 0, 0, 0, 0]
    player_ia = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    enemy_ia = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Preenche com 1 cada peça presente no campo
    for piece in field:
        field_ia[pieces.index(piece)] = 1
    # Preenche as peças na mão
    for piece in player:
        player_ia[pieces.index(piece)] = 1
    # Preenche a quantidade de peças do oponente
    for i in range(len(enemy)):
        enemy_ia[i] = 1
    edges_ia[edges[0]-1] = 1
    edges_ia[edges[1]-1] = 1
    # 28 possíveis peças pro campo + 28 possíveis peças pra mão + 28 possíveis quantidades de peças do oponente + 6 possíveis valores na borda
    return field_ia + player_ia + enemy_ia + edges_ia

def save(game):
    arquivo = open("teste.txt","a")
    game = json.dumps(game)
    arquivo.write(game)
    arquivo.close()

domino = Domino()

for ii in range(100):
    data = []
    # Quantidade de peças na mão de cada jogador
    qtd0 = 3
    qtd1 = 3
    # Início do jogo
    domino.start(qtd0,qtd1)
    # Variável que armazena as rodadas
    rodadas = ''
    while True:
        # Verifica se alguém ganhou
        if domino.hasWinner:
            break

        # Armazenando as informações da rodada
        rodadas += str(domino.data()) + ','
        domino.play()

    # Armazenando as informações do jogo
    jogo = {
        'Jogo': ii,
        'Resultado': domino.winner,
        'Rodadas': ast.literal_eval(rodadas[:-1])
    }
    if domino.winner == 0:
        qtd1 += 1
    else:
        qtd0 += 1
    data.append(jogo)
    save(data)