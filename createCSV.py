import yfinance as yf
import pandas as pd
import auxiliaryFunctions
from time import time
from listaTicker import TickerList
import cores

inicio = auxiliaryFunctions.converterData(input("Início (dd/mm/YYYY): "))
final = auxiliaryFunctions.converterData(input("Final (dd/mm/YYYY): "))

print(f"{cores.amarelo("Carregando ações (2min)...")}")

acoes = TickerList()
dados_acoes = {} # Armazerna a tabela dos dados de cada ação

inicioTempo = time()

for acao in acoes:
    ticker = yf.Ticker(acao)
    dados = ticker.history(start=inicio, end=final)
    dados = dados[["Low","High","Volume","Open","Close"]]

    if not dados.empty:
        dados["Ticker"] = acao
        dados_acoes[acao] = dados
    else:
        print(f"Nenhum dado encontrado para {acao}")
        continue

todos_dados = pd.concat(dados_acoes.values())
todos_dados.to_csv("dados_acoes.csv")

fim_tempo = time()
tempo = fim_tempo - inicioTempo

print(f"{tempo:.2f}s")



