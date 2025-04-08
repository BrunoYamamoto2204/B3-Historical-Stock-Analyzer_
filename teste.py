import yfinance as yf
import pandas as pd
frase = "jonson é jonson bem jonson"
palavras = len(frase.split())

letras = 0
palavras_repetidas = {}
for c in range(len(frase)):
    if frase[c] != " ":
        letras += 1

for p in frase.split():
    if not p in palavras_repetidas:
        palavras_repetidas[p] = 1
    else:
        palavras_repetidas[p] += 1

print(f"Caracteres: {letras}")
print(f"Palavras: {palavras}")

print(f"Contagem de palavras:")
for palavra,qntd in palavras_repetidas.items():
    print(f'    "{palavra}" apareceu {qntd} vezes')

