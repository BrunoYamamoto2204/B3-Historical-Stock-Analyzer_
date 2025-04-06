import yfinance as yf
import pandas as pd
from time import time

inicio = time()
input("Escreva algo: ")
final = time()

tempo = final - inicio
print(f"{tempo:.2f}")
