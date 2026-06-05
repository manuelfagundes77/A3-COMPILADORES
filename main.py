# ============================================================
# MAIN — Ponto de entrada do compilador MiniLang
#
# Uso:
#   python main.py
#
# O compilador lê o arquivo programa.ml na mesma pasta.
#
# Exemplo de programa.ml:
#   x = 10
#   y = x + 5
#   print(y)
# ============================================================

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compilador import compilar

# Arquivo de entrada do compilador
ARQUIVO_PROGRAMA = "programa.ml"


def ler_arquivo():
    """
    Lê o conteúdo do arquivo programa.ml.

    Retorna:
        O conteúdo do arquivo como string.
    """
    if not os.path.exists(ARQUIVO_PROGRAMA):
        raise Exception(f"Arquivo '{ARQUIVO_PROGRAMA}' não encontrado")

    with open(ARQUIVO_PROGRAMA, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def main():
    """
    Função principal — lê o programa.ml e compila.
    """
    try:
        codigo_fonte = ler_arquivo()
        compilar(codigo_fonte)

    except Exception as erro:
        print(f"\nErro: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()