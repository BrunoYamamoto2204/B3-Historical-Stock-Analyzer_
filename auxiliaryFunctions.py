from datetime import datetime
import pandas as pd
import listaTicker

def converterData(data):
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    nova_string = data_obj.strftime("%Y-%m-%d")

    return nova_string

def lucro_maximo_minimo(inicio, final):
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    inicio = datetime.strptime(inicio, "%Y-%m-%d")
    final = datetime.strptime(final, "%Y-%m-%d")

    dados_filtrados = dados[(dados["Date"] >= inicio) & (dados["Date"] <= final)]

    lucro_acoes = {}
    maior_lucro_acao = {}
    menor_lucro_acao = {}

    for index,dia in dados_filtrados.iterrows():

        try:
            lucro = ((dia["Close"] - dia["Open"]) / dia["Open"]) * 100
        except ZeroDivisionError:
            lucro = 0

        if dia["Ticker"] not in lucro_acoes: # Se for não tiver a ação registada ainda
            lucro_acoes[dia["Ticker"]] = {}
        lucro_acoes[dia["Ticker"]][str(dia["Date"].date())] = lucro

    for acao in listaTicker.TickerList(): #Passa por cada ação

        maior_lucro_acao[acao] = -100
        menor_lucro_acao[acao] = 100

        try:
            for lucro_dia in lucro_acoes[acao].values(): # Lucro de todos os dias de todas as ações
                if lucro_dia > maior_lucro_acao[acao]:
                    maior_lucro_acao[acao] = lucro_dia
                if lucro_dia < menor_lucro_acao[acao]:
                    menor_lucro_acao[acao] = lucro_dia
        except:
            continue

    return [maior_lucro_acao, menor_lucro_acao]

# print(lucro_maximo_minimo("2025-01-01", "2025-04-05")[0]["ITSA4.SA"])
# print(lucro_maximo_minimo("2025-01-01", "2025-04-05")[1]["ITSA4.SA"])