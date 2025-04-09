from datetime import datetime, timedelta
import pandas as pd

import cores
import listaTicker

def converterData(data):
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    nova_string = data_obj.strftime("%Y-%m-%d")

    return nova_string

def filtrarDados(inicio, final):
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    inicio = datetime.strptime(inicio, "%Y-%m-%d")
    final = datetime.strptime(final, "%Y-%m-%d")

    dados_filtrados = dados[(dados["Date"] >= inicio) & (dados["Date"] <= final)]

    return dados_filtrados


def lucro_maximo_minimo(inicio, final):
    dados_filtrados = filtrarDados(inicio, final)

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


def voltar_um_dia_util(data_datetime, ticker):
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    dados_acao = dados[dados["Ticker"] == ticker]
    dias_uteis = set(dados_acao["Date"].dt.date)

    menor_data = min(dias_uteis)

    while True:
        data_datetime -= timedelta(days=1)

        if data_datetime.date() < menor_data:
            print(f"{cores.vermelho("*Não há dados anteriores a essa data.\n")}")
            return False
        if data_datetime.date() in dias_uteis:
            return data_datetime


def fechamento_do_dia(inicio, final):
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    inicio = datetime.strptime(converterData(inicio), "%Y-%m-%d")
    final = datetime.strptime(converterData(final), "%Y-%m-%d")

    # Volta no dia anterior da bolsa (sem FDS e feriados)
    inicio_dia_anterior = voltar_um_dia_util(inicio, "ITSA4.SA")

    # Se não tiver dia anterior no csv, usa o inicio fornecido, se não considera um dia menos
    if not inicio_dia_anterior:
        dados_filtrados = dados[(dados["Date"] >= inicio) & (dados["Date"] <= final)]
    else:
        dados_filtrados = dados[(dados["Date"] >= inicio_dia_anterior) & (dados["Date"] <= final)]

    dados_fechamento_atual = []
    dados_fechamento_anterior = []

    # Filtrar as datas (poderia ser qualquer ticker, pois todas tem a mesma data) | Começar a tabela do index 0
    dados_acao = dados_filtrados[dados_filtrados["Ticker"] == "ITSA4.SA"]

    for index in range(len(dados_acao) - 1):
        dados_diaAnterior = dados_acao.iloc[index]["Close"]
        dados_diaAtual = dados_acao.iloc[index + 1]["Close"]

        dia_Anterior = dados_acao.iloc[index]["Date"]
        dia_Atual = dados_acao.iloc[index + 1]["Date"]

        dados_fechamento_anterior.append(float(dados_diaAnterior))
        dados_fechamento_atual.append(float(dados_diaAtual))

        print(f"{dia_Anterior} - Fechamento do dia anterior: {dados_diaAnterior:.2f}")
        print(f"{dia_Atual} - Fechamento do dia atual: {dados_diaAtual:.2f}")
        print()

    return [dados_fechamento_anterior, dados_fechamento_atual]


fechamento = fechamento_do_dia("02/01/2024","09/04/2025")

print(f"Anterior: {fechamento[0]}")
print(f"Atual {fechamento[1]}")
