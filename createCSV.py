import yfinance as yf
import pandas as pd
import auxiliaryFunctions
from time import time
from listaTicker import TickerList
import cores

def criarCSV():
    inicio = auxiliaryFunctions.converter_data_createCSV_dia_anterior()
    final = auxiliaryFunctions.converter_data_createCSV_dia_seguinte()

    print(f"{cores.amarelo("Carregando ações (2min)...")}")

    acoes = TickerList()
    inicioTempo = time()

    tickers_str = " ".join(acoes)
    dados_brutos = yf.download(
        tickers=tickers_str,
        start=inicio,
        end=final,
        group_by="ticker",
        threads=True # Permite a realização de várias consultas ao mesmo tempo
    )

    dados_acoes = [] # Armazerna a tabela dos dados de cada ação

    for acao in acoes:
        try:
            dados = dados_brutos[acao].copy() # Cópia da linha da tabela
            if not dados.empty:
                dados["Ticker"] = acao
                dados = dados[["Low","High","Volume","Open","Close", "Ticker"]]
                dados_acoes.append(dados)
            else:
                print(f"Nenhum dado encontrado para {acao}")
                continue

        except KeyError: # Caso não exista o ticker
            print(f"Nenhum dado encontrado para {acao}")
            continue


    todos_dados = pd.concat(dados_acoes)
    todos_dados.to_csv("dados_acoes.csv")

    fim_tempo = time()
    tempo = fim_tempo - inicioTempo

    print(f"\nDuração da consulta{tempo:.2f}s")



