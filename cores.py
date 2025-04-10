def amarelo(texto):
    return f"\033[33m{texto}\033[m"
def vermelho(texto):
    return f"\033[31m{texto}\033[m"
def verde(texto):
    return f"\033[32m{texto}\033[m"
def ciano(texto):
    return f"\033[36m{texto}\033[m"

def amarelo_bold(texto):
    return f"\033[1;33m{texto}\033[m"

def verde_bold(texto):
    return f"\033[1;32m{texto}\033[m"

def vermelho_bold(texto):
    return f"\033[1;31m{texto}\033[m"

def azul_bold(texto):
    return f"\033[1;34m{texto}\033[m"

def posivito_negativo(valor):
    if valor > 0:
        return f"\033[32m{valor}\033[m"
    elif valor < 0:
        return f"\033[31m{valor}\033[m"
    else:
        return f"\033[1m{valor}\033[m"