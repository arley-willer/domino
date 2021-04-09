import keras
import json
import numpy as np
from keras import models
from keras.models import load_model

teste = open('treino.txt', 'r')
for linha in teste:
    teste = linha
teste = json.loads(teste)

model = load_model('domino.h5')
print(model)
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
    jogos_resul.append(respostas[i])

jogos_teste = np.array(jogos_teste)
jogos_resul = np.array(jogos_resul)

test_loss, test_acc = model.evaluate(jogos_teste, jogos_resul)
print('test_acc:', test_acc)
predictions = model.predict(jogos_teste)
print(predictions)