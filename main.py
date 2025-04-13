import auxiliaryFunctions
import cores
import createCSV
import manageData
# import createCSV
import auxiliaryFunctions as af
import pandas as pd

print(cores.azul_bold("=")*58)
print(cores.azul_bold("=")*10, cores.laranja("ANALISADOR DE HISTÓRICOS DE AÇÕES B3"), cores.azul_bold("=")*10)
print(cores.azul_bold("=")*58)

dados = pd.read_csv("dados_acoes.csv")
dados["Date"] = pd.to_datetime(dados["Date"]).dt.tz_localize(None)
dados_filtrados = dados[dados["Ticker"] == "ITSA4.SA"]

while True:
    data_min = af.converter_data_tradicional(min(dados_filtrados["Date"]))
    data_max = af.converter_data_tradicional(max(dados_filtrados["Date"]))

    print()
    print(cores.amarelo("-") * 20, cores.amarelo("Menu"), cores.amarelo("-") * 20)

    print(f"{cores.amarelo_bold("Datas disponíveis:")} {cores.ciano(f"{data_min}")} até {cores.ciano(f"{data_max}")}\n")

    print(cores.ciano("[ 1 ]") + " - Carregar outras datas")
    print(cores.ciano("[ 2 ]") + " - Analisar ações")
    print(cores.ciano("[ 3 ]") + " - Sair")
    resposta = af.reposta()

    if resposta == 1:
        print()
        print(cores.amarelo("-")*20, cores.amarelo("Carregar novas datas"), cores.amarelo("-")*20)
        createCSV.criarCSV()

    if resposta == 2:
        print()
        print(cores.amarelo("-")*20, cores.amarelo("Análise de operações"), cores.amarelo("-")*20)
        print((f"|| Média {cores.amarelo_bold(f"(15s a 30s)")} - Varia pelo tamanho do período ||\n"))

        inicio = af.converterData("Início")
        final = af.converterData("Final")
        ordem = af.numValido("Ordem de compra(%)")
        gain_esperado = af.numValido("Gaind desejado(%)")

        gains_acao = manageData.filtrarAcoes(inicio, final, ordem, gain_esperado)

        print(cores.ciano("\nAções filtradas:"))
        gains_ordem = sorted(gains_acao, key=lambda d: list(d.values())[0], reverse=True)
        for ticker in gains_ordem:
            for nome, valor in ticker.items():
                print(f"{cores.amarelo(f"{nome}")} - {cores.azul_bold(f"{valor}")}%")

        while True:
            print("-" * 40)
            print(cores.amarelo("\n|| APERTAR ") + cores.azul_bold("ENTER ") + cores.amarelo("PARA SAIR||"))
            conferir_acao = input(("Verficar ação (Nome.SA): "))

            if conferir_acao == "":
                break
            else:
                auxiliaryFunctions.calcularGain(ordem, inicio, final, conferir_acao, dados)

                print()
                print(cores.amarelo("-") * 20, cores.amarelo("Procurar ações"), cores.amarelo("-") * 20)

    if resposta == 3:
        print()
        print(cores.vermelho("-") * 20, cores.vermelho("Saiu da aplicação"), cores.vermelho("-") * 20)
        break
