import datetime
from time import time
import pandas as pd
from datetime import datetime

import auxiliaryFunctions
import cores
import listaTicker

def filtrarAcoes(inicio, final, ordemDesejada, gain_desejado):
    pd.set_option('display.width', None) # Sem abreviação de colunas (Teste visualização de tabela)

    # Abrir o CSV | Desconsiderar fuso horário (algumas ações não tem)
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    inicio_datetime = datetime.strptime(inicio, "%Y-%m-%d")
    final_datetime = datetime.strptime(final, "%Y-%m-%d")

    # Lista de gain acima do desejado
    lista_gain = []

    # Filtra de todos as ações carregadas do CSV, qual está dentro do período
    dados_filtrados = dados[(dados["Date"] >= inicio_datetime) & (dados["Date"] <= final_datetime)]

    lucro_maximo = auxiliaryFunctions.lucro_maximo_minimo(inicio, final, dados)[0]
    lucro_minimo = auxiliaryFunctions.lucro_maximo_minimo(inicio, final, dados)[1]
    tempo_inicio = time()
    for index,ticker in enumerate(listaTicker.TickerList()): #Passa pelos tickers

        dados_ticker = dados_filtrados[dados_filtrados["Ticker"] == ticker]

        meio = int((50 - len(ticker)) / 2)
        print(f"{cores.azul_bold(f"{"-" * meio} {ticker} {"-" * meio}")}")

        data_inicio = dados_ticker["Date"].min().date()
        data_final = dados_ticker["Date"].max().date()
        maior_valor = dados_ticker["High"].max()
        menor_valor = dados_ticker["Low"].min()

        lucro_maximo_acao = lucro_maximo[ticker]
        lucro_minimo_acao = lucro_minimo[ticker]

        if not pd.isna(data_inicio) or not pd.isna(data_final): # Caso a data da ação seja NaT ou NaN, pula
            print(f"{index+1} - {cores.amarelo(f"({data_inicio} - {data_final})")}")
            print(f"Maior valor: {cores.verde_bold(f"R${maior_valor:.2f}")}")
            print(f"Menor valor: {cores.vermelho_bold(f"R${menor_valor:.2f}")}")
            print(f"{cores.ciano("\nMaior Lucro:")} {cores.verde(f"R${lucro_maximo_acao:.2f}%")}")
            print(f"{cores.ciano("Menor Lucro:")} {cores.vermelho(f"R${lucro_minimo_acao:.2f}%")}")

            gain = auxiliaryFunctions.calcularGain(ordemDesejada, inicio, final, ticker,dados)

            try:
                if gain >= gain_desejado:
                    gain_dic = {}
                    gain_dic[ticker] = gain
                    lista_gain.append(gain_dic)
            except:
                continue

        else:
            print("\033[31m[-]\033[m Sem dados disponíveis neste período")

    print()
    tempo_final = time()
    print(f"{cores.amarelo_bold("Tempo de espera")}: {tempo_final - tempo_inicio:.2f}s")

    return lista_gain

# filtrarAcoes("2025-01-03","2025-04-05", -2)
