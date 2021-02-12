import keras
import json
import numpy as np
from keras import models
from keras import layers
from keras import optimizers

data = open('dados.txt', 'r')
for linha in data:
    data = linha
data = json.loads(data)
teste = open('treino.txt', 'r')
for linha in teste:
    teste = linha
teste = json.loads(teste)

dados = []
resp = []
jogos_treino = []
jogos_resultado = []

for jogo in range(len(data)):
    for rodada in range(len(data[jogo])):
        if data[jogo]['Resultado'] == 0:
            dados.append(data[jogo]['Rodadas'][rodada]['IAs'][0])
            resp.append(1)
            dados.append(data[jogo]['Rodadas'][rodada]['IAs'][1])
            resp.append(0)
        if data[jogo]['Resultado'] == 1:
            dados.append(data[jogo]['Rodadas'][rodada]['IAs'][0])
            resp.append(0)
            dados.append(data[jogo]['Rodadas'][rodada]['IAs'][1])
            resp.append(1)

for i in range(len(dados)):
    jogos_treino.append(dados[i])
    jogos_resultado.append(resp[i])

jogos_treino = np.array(jogos_treino)
jogos_resultado = np.array(jogos_resultado)

model = models.Sequential()
model.add(layers.Dense(90, activation='relu', input_shape=(91,)))
model.add(layers.Dense(45, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.summary()
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(jogos_treino, jogos_resultado, epochs=100, batch_size=128)

testes = []
respostas = []
jogos_teste = []
jogos_resul = []

for jogo in range(len(teste)):
    for rodada in range(len(teste[jogo])):
        if teste[jogo]['Resultado'] == 0:
            testes.append(teste[jogo]['Rodadas'][rodada]['IAs'][0])
            respostas.append(1)
            testes.append(teste[jogo]['Rodadas'][rodada]['IAs'][1])
            respostas.append(0)
        if teste[jogo]['Resultado'] == 1:
            testes.append(teste[jogo]['Rodadas'][rodada]['IAs'][0])
            respostas.append(0)
            testes.append(teste[jogo]['Rodadas'][rodada]['IAs'][1])
            respostas.append(1)

for i in range(len(testes)):
    jogos_teste.append(testes[i])
    jogos_resul.append(resp[i])

jogos_teste = np.array(jogos_teste)
jogos_resul = np.array(jogos_resul)

test_loss, test_acc = model.evaluate(jogos_teste, jogos_resul)
print('test_acc:', test_acc)

model.save("Domino.h5")