# 📈 B3-Historical-Stock-Analyzer

Ferramenta em Python para análise de ações da **B3 (Bolsa de Valores Brasileira)** com dados históricos personalizados via [**yfinance**](https://pypi.org/project/yfinance/). Ideal para investidores e entusiastas que desejam obter insights detalhados sobre o desempenho de ativos em períodos específicos.

---

## ⚙️ Funcionalidades

- 🔍 Busca cotações históricas com base em **períodos personalizados**
- 📡 Integração com a API **yfinance**
- 📊 Exibe **estatísticas detalhadas** do desempenho da ação
- 📁 Permite análise **separada por ação**
- 🎯 Define parâmetros como:
  - Porcentagem de ordem de compra
  - Porcentagem de ganho (gain) desejado

---

## ⌨️ Inputs do Usuário

O programa solicitará as seguintes informações:

- 📅 Data inicial e final do período de análise  
- 💰 Porcentagem de **ordem de compra**  
- 📈 Porcentagem de **gain** desejado

---

## 🧾 Resultados Gerados (Output)

Após a análise, o programa retorna:

- 💹 Lucro **máximo** e **mínimo** no período
- 📈 Ganho **máximo**, **mínimo** e **médio**
- 🔁 Quantidade de **trades realizados**
- 📉 Resultado total de **ganhos e perdas**

---

## 🧩 Tecnologias Utilizadas

- 📌 **Linguagem**: Python  
- 📚 **Bibliotecas**:
  - `yfinance`
  - `json`
  - `pandas`
  - `datetime`
  - `time`

---

## 📝 Observações

- A ferramenta é voltada para fins educacionais e informativos.
- Os dados são coletados em tempo real via a API pública do Yahoo Finance.
- É recomendável validar os dados antes de tomar qualquer decisão de investimento.
