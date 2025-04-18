from datetime import datetime, timedelta
import pandas as pd

import cores
import listaTicker


def reposta():
    while True:
        try:
            r = int(input("Escolha: "))

            if 1 <= r <= 3:
                return r
            else:
                print(cores.vermelho_bold("Reposta inválida! Digite 1 ou 2.\n"))
        except:
            print(cores.vermelho_bold("Reposta inválida! Digite 1 ou 2.\n"))

def numValido(texto):
    while True:
        try:
            r = float(input(f"{texto}: ").replace(",","."))
            return r

        except:
            print(cores.vermelho_bold("Reposta inválida! Apenas números.\n"))

def converterData(texto): #string %d/%m/%Y
    while True:
        try:
            data = input(f"{texto}{cores.amarelo(f"(dd/mm/YYYY)")}: ")
            data_obj = datetime.strptime(data, "%d/%m/%Y")
            nova_string = data_obj.strftime("%Y-%m-%d")

            return nova_string
        except:
            print(cores.vermelho("Data inválida! Digite novamente!\n"))



def converter_data_tradicional(data): #datetime %Y-%m-%d
    nova_string = data.strftime("%d/%m/%Y")

    return nova_string

def filtrarDados(inicio, final, dados):  #Tipo:datetime (y-m-d)
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    dados_filtrados = dados[(dados["Date"] >= inicio) & (dados["Date"] <= final)]

    return dados_filtrados


def lucro_maximo_minimo(inicio, final, dados):  # y-m-d
    dados_filtrados = filtrarDados(inicio, final, dados)

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


def voltar_um_dia_util(data_datetime, ticker, dados):
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


def fechamento_do_dia(inicio, final, ticker, dados): # string "%Y-%m-%d"
    dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)

    inicio = datetime.strptime(inicio, "%Y-%m-%d")
    final = datetime.strptime(final, "%Y-%m-%d")

    # Volta no dia anterior da bolsa (sem FDS e feriados)
    inicio_dia_anterior = voltar_um_dia_util(inicio, "ITSA4.SA", dados)

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

def calcularGain(ordemDesejada, inicio, final, acao, dados): #Tipo:string (y-m-d)
    # Converter para datetime
    inicio_datetime = datetime.strptime(inicio, "%Y-%m-%d")
    final_datetime = datetime.strptime(final, "%Y-%m-%d")

    # Filtrar por data e ticker
    dados_filtrados = filtrarDados(inicio_datetime, final_datetime, dados)
    dados_acao = dados_filtrados[dados_filtrados["Ticker"] == acao]

    # Fechamento do dia atual e anterior
    fechamento = fechamento_do_dia(inicio, final, acao, dados)
    fechamento_anterior = fechamento[0]
    fechamento_atual = fechamento[1]

    # Variáveis p/ calculos de estatísticos de gain
    qntd_gain = 0  # Comprou mais baixo vendeu mais alto [+]
    qntd_loss = 0  # Comprou mais alto vendeu mais baixo [-]
    qtnd_total = 0  # Total, compraram por gainDesejado ou pela abertura

    registro_trades = []  # Verificar maior e menor gain
    gain_acumulado = 0  # somar os gains

    # Percorre todos os dias do período
    for index in range(len(fechamento_atual)):
        # print(f"Data: {dados_acao.iloc[index]["Date"]}")
        # print(f"Fechamento ontem: {fechamento_anterior[index]:.2f}")
        # print(f"Fechamento do dia: {fechamento_atual[index]:.2f}")
        # print(f"Abertura de hoje: {dados_acao.iloc[index]["Open"]:.2f}")
        # print(f"Máxima: {dados_acao.iloc[index]["High"]:.2f}")
        # print(f"Minima: {dados_acao.iloc[index]["Low"]:.2f}")

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
                qntd_loss += 1

        # Compra pela ordem
        elif var_minima < ordemDesejada:  #Se ordem estiver maior que a mínima, compra pela ordem
            qtnd_total += 1
            registro_trades.append(var_fechamento - ordemDesejada)

            if var_fechamento >= ordemDesejada:  # Vendeu com fechamento maior do que a compra na ordem [+]
                qntd_gain += 1
                gain_acumulado += var_fechamento - ordemDesejada

            else:  # Vendeu com fechamento menor do que a compra na ordem [-]
                qntd_loss += 1

        # print(f"\nVariação fechamento: {var_fechamento:.2f}%")
        # print(f"Variação abertura: {var_abertura:.2f}%")
        # print(f"Variação Max: {var_maxima:.2f}%")
        # print(f"Variação Min: {var_minima:.2f}%")
        # print("-" * 40)

    # Caso não tenha sido realizado trade
    if qtnd_total == 0:
        print(cores.amarelo(f"Nenhum trade para o ticker {acao} foi realizado no período de {inicio} até {final}.\n"))
        return

    # Caso não tenha gain em nenhum trade
    if qntd_gain == 0:
        print(cores.amarelo(f"Nenhum Gain trade para o ticker {acao} realizado no período de {inicio} até {final}.\n"))
        return

    # Calculo dos resultados
    loss_porcentagem = round((qntd_loss / qtnd_total) * 100, 2)
    gain_porcentagem = round((qntd_gain / qtnd_total) * 100, 2)

    min_gain = round(min(registro_trades), 2)
    max_gain = round(max(registro_trades), 2)

    ganho_medio = round((gain_acumulado / qntd_gain), 2)  # gain_acumulado / qntd_gain
    gain_acumulado = round(gain_acumulado, 2)

    print(cores.ciano(f"\n-- ||Trades|| --"))
    print(f"Total trades: {cores.azul_bold(f"{qtnd_total}")}")
    print(f"Gain trades: {cores.verde(f"{qntd_gain}")}")
    print(f"Loss trades: {cores.vermelho(f"{qntd_loss}")}\n")

    print(cores.ciano(f"-- ||Gain-Loss|| --"))
    print(f"Loss porcentagem: {cores.vermelho(f"{loss_porcentagem}%")}")
    print(f"Gain porcentagem: {cores.verde(f"{gain_porcentagem}%")}\n")

    print(cores.ciano(f"-- ||Mix-Max|| --"))
    print(f"Min Gain: {cores.vermelho(f"{min_gain}%")}")
    print(f"Max Gain: {cores.verde(f"{max_gain}%")}\n")

    print(cores.ciano(f"-- ||Média|| --"))
    print(f"Gain acumulado: {cores.azul_bold(f"{gain_acumulado}%")}")
    print(f"Ganho médio: {cores.azul_bold(f"{ganho_medio}%")}\n")

    return gain_porcentagem

# calcularGain(-2, "2024-01-03", "2025-04-04", "ITSA4.SA")
