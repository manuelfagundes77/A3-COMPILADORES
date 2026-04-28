import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer.afd import (
    INICIO,
    LENDO_ID,
    LENDO_NUM,
    LENDO_OPERADOR,
    LENDO_PAREN,
    FIM,
    ERRO,
    transicao
)


def tipo_token(estado, valor):
    if estado == LENDO_ID:
        if valor == "print":
            return "PRINT"
        return "ID"

    elif estado == LENDO_NUM:
        return "NUM"

    elif estado == LENDO_OPERADOR:
        return "OP"

    elif estado == LENDO_PAREN:
        return "PAREN"

    return None


def lexer(codigo):
    tokens = []
    estado = INICIO
    valor = ""
    i = 0

    while i < len(codigo):
        caractere = codigo[i]
        proximo_estado = transicao(estado, caractere)

        if proximo_estado == FIM:
            tipo = tipo_token(estado, valor)

            if tipo and valor:
                tokens.append((tipo, valor))

            estado = INICIO
            valor = ""
            continue

        elif proximo_estado == ERRO:
            raise Exception(f"Erro léxico no caractere: '{caractere}'")

        else:
            estado = proximo_estado

            if estado != INICIO:
                valor += caractere

            i += 1

    if valor:
        tipo = tipo_token(estado, valor)

        if tipo:
            tokens.append((tipo, valor))

    return tokens


if __name__ == "__main__":
    while True:
        codigo = input("Digite o código: ")

        try:
            tokens = lexer(codigo)

            print("\nTokens:")
            for t in tokens:
                print(t)

        except Exception as e:
            print(e)

        continuar = input("\nContinuar? (s/n): ").lower()
        if continuar != "s":
            break