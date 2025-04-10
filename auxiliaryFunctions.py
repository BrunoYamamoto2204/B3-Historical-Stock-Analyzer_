from datetime import datetime, timedelta
import pandas as pd

import cores
import listaTicker


def converterData(data):
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    nova_string = data_obj.strftime("%Y-%m-%d")

    return nova_string


def filtrarDados(inicio, final):  #Tipo:datetime (y-m-d)
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    dados_filtrados = dados[(dados["Date"] >= inicio) & (dados["Date"] <= final)]

    return dados_filtrados


def lucro_maximo_minimo(inicio, final):  # y-m-d
    dados_filtrados = filtrarDados(inicio, final)

    lucro_acoes = {}
    maior_lucro_acao = {}
    menor_lucro_acao = {}

    for index, dia in dados_filtrados.iterrows():

        try:
            lucro = ((dia["Close"] - dia["Open"]) / dia["Open"]) * 100
        except ZeroDivisionError:
            lucro = 0

        if dia["Ticker"] not in lucro_acoes:  # Se for não tiver a ação registada ainda
            lucro_acoes[dia["Ticker"]] = {}
        lucro_acoes[dia["Ticker"]][str(dia["Date"].date())] = lucro

    for acao in listaTicker.TickerList():  #Passa por cada ação

        maior_lucro_acao[acao] = -100
        menor_lucro_acao[acao] = 100

        try:
            for lucro_dia in lucro_acoes[acao].values():  # Lucro de todos os dias de todas as ações
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


def fechamento_do_dia(inicio, final, ticker):
    dados = pd.read_csv("dados_acoes.csv")
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    inicio = datetime.strptime(inicio, "%Y-%m-%d")
    final = datetime.strptime(final, "%Y-%m-%d")

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
    dados_acao = dados_filtrados[dados_filtrados["Ticker"] == ticker]

    # Termina -1 para não exceder o index, como o dia atual tem o index + 1
    for index in range(len(dados_acao) - 1):
        dados_diaAnterior = dados_acao.iloc[index]["Close"]
        dados_diaAtual = dados_acao.iloc[index + 1]["Close"]

        dia_Anterior = dados_acao.iloc[index]["Date"]
        dia_Atual = dados_acao.iloc[index + 1]["Date"]

        dados_fechamento_anterior.append(float(dados_diaAnterior))
        dados_fechamento_atual.append(float(dados_diaAtual))

        # print(f"{dia_Anterior} - Fechamento do dia anterior: {dados_diaAnterior:.2f}")
        # print(f"{dia_Atual} - Fechamento do dia atual: {dados_diaAtual:.2f}")
        # print()

    return [dados_fechamento_anterior, dados_fechamento_atual]


# fechamento = fechamento_do_dia("2024-01-03","2025-04-09")
#
# print(f"Anterior: {fechamento[0]}")
# print(f"Atual {fechamento[1]}")

def calcularGain(ordemDesejada, inicio, final, acao):
    # Converter para datetime
    inicio_datetime = datetime.strptime(inicio, "%Y-%m-%d")
    final_datetime = datetime.strptime(final, "%Y-%m-%d")

    # Filtrar por data e ticker
    dados_filtrados = filtrarDados(inicio_datetime, final_datetime)
    dados_acao = dados_filtrados[dados_filtrados["Ticker"] == acao]

    # Fechamento do dia atual e anterior
    fechamento = fechamento_do_dia(inicio, final, acao)
    fechamento_anterior = fechamento[0]
    fechamento_atual = fechamento[1]

    # Variáveis p/ calculos de estatísticos de gain
    qntd_gain = 0  # Comprou mais baixo vendeu mais alto [+]
    qtnd_loss = 0  # Comprou mais alto vendeu mais baixo [-]
    qtnd_total = 0  # Total, compraram por gainDesejado ou pela abertura

    registro_trades = []  # Verificar maior e menor gain
    gain_acumulado = 0  # somar os gains

    # Percorre todos os dias do período
    for index in range(len(fechamento_atual)):
        print(f"Data: {dados_acao.iloc[index]["Date"]}")
        print(f"Fechamento ontem: {fechamento_anterior[index]:.2f}")
        print(f"Fechamento do dia: {fechamento_atual[index]:.2f}")
        print(f"Abertura de hoje: {dados_acao.iloc[index]["Open"]:.2f}")
        print(f"Máxima: {dados_acao.iloc[index]["High"]:.2f}")
        print(f"Minima: {dados_acao.iloc[index]["Low"]:.2f}")

        var_fechamento = (fechamento_atual[index] / fechamento_anterior[index] - 1) * 100
        var_abertura = (dados_acao.iloc[index]["Open"] / fechamento_anterior[index] - 1) * 100
        var_maxima = (dados_acao.iloc[index]["High"] / fechamento_anterior[index] - 1) * 100
        var_minima = (dados_acao.iloc[index]["Low"] / fechamento_anterior[index] - 1) * 100

        # Compra pela abertura
        if var_abertura < ordemDesejada:  #Se a abertura for menor que a ordem, compra pela abertura
            qtnd_total += 1
            registro_trades.append(var_fechamento - var_abertura)

            if var_fechamento >= var_abertura:  #Vendeu com fechamento maior do que a compra na abertura [+]
                qntd_gain += 1
                gain_acumulado += var_fechamento - var_abertura

            else:  #Vendeu com fechamento menor do que a compra abertura [-]
                qtnd_loss += 1

        # Compra pela ordem
        elif var_minima < ordemDesejada:  #Se ordem estiver maior que a mínima, compra pela ordem
            qtnd_total += 1
            registro_trades.append(var_fechamento - ordemDesejada)

            if var_fechamento >= ordemDesejada:  # Vendeu com fechamento maior do que a compra na ordem [+]
                qntd_gain += 1
                gain_acumulado += var_fechamento - ordemDesejada

            else:  # Vendeu com fechamento menor do que a compra na ordem [-]
                qtnd_loss += 1

        print(f"\nVariação fechamento: {var_fechamento:.2f}%")
        print(f"Variação abertura: {var_abertura:.2f}%")
        print(f"Variação Max: {var_maxima:.2f}%")
        print(f"Variação Min: {var_minima:.2f}%")

        print()
        print(f"Total trades: {qtnd_total}")
        print(f"Gain trades: {qntd_gain}")
        print(f"Loss trades: {qtnd_loss}")
        print("-" * 40)
        print()

    # Calculo dos resultados
    loss_porcentagem = round((qtnd_loss / qtnd_total) * 100, 2)
    gain_porcentagem = round((qntd_gain / qtnd_total) * 100, 2)

    min_gain = round(min(registro_trades), 2)
    max_gain = round(max(registro_trades), 2)

    ganho_medio = round((gain_acumulado / qntd_gain), 2)  # gain_acumulado / qntd_gain
    gain_acumulado = round(gain_acumulado, 2)

    print(cores.amarelo("Resultados:\n"))

    print(cores.ciano(f"-- ||Gain-Loss|| --"))
    print(f"Loss porcentagem: {cores.vermelho(f"{loss_porcentagem}%")}")
    print(f"Gain porcentagem: {cores.verde(f"{gain_porcentagem}%")}\n")

    print(cores.ciano(f"-- ||Mix-Max|| --"))
    print(f"Min Gain: {cores.vermelho(f"{min_gain}%")}")
    print(f"Max Gain: {cores.verde(f"{max_gain}%")}\n")

    print(cores.ciano(f"-- ||Média|| --"))
    print(f"Gain acumulado: {cores.azul_bold(f"{gain_acumulado}%")}\n")
    print(f"Ganho médio: {cores.azul_bold(f"{ganho_medio}%")}\n")


calcularGain(-2.1, "2024-03-07", "2025-04-02", "KLBN11.SA")
