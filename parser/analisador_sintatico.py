import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from parser.pilha import Pilha
from lexer.analisador_lexico import lexer


def analisar_sintatico(tokens):
    pilha = Pilha()
    i = 0

    if len(tokens) == 0:
        raise Exception("Erro sintático: código vazio")

    if tokens[0][0] == "ID":
        pilha.empilhar("ATRIB")

    elif tokens[0][0] == "PRINT":
        pilha.empilhar("PRINT")

    else:
        raise Exception("Erro sintático: instrução inválida")

    while not pilha.vazia():
        topo = pilha.desempilhar()

        if topo == "ATRIB":
            pilha.empilhar("EXPR")
            pilha.empilhar("=")
            pilha.empilhar("ID")

        elif topo == "PRINT":
            pilha.empilhar(")")
            pilha.empilhar("ID")
            pilha.empilhar("(")
            pilha.empilhar("print")

        elif topo == "EXPR":
            if i < len(tokens) and tokens[i][0] in ("ID", "NUM"):
                pilha.empilhar("RESTO")
                pilha.empilhar("VALOR")
            else:
                raise Exception("Erro sintático: expressão inválida")

        elif topo == "RESTO":
            if i < len(tokens) and tokens[i][0] == "OP" and tokens[i][1] in ("+", "-"):
                operador = tokens[i][1]
                pilha.empilhar("VALOR")
                pilha.empilhar(operador)

        elif topo == "VALOR":
            if i < len(tokens) and tokens[i][0] in ("ID", "NUM"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado ID ou NUM")

        elif topo == "ID":
            if i < len(tokens) and tokens[i][0] == "ID":
                i += 1
            else:
                raise Exception("Erro sintático: esperado ID")

        elif topo == "=":
            if i < len(tokens) and tokens[i] == ("OP", "="):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '='")

        elif topo == "+":
            if i < len(tokens) and tokens[i] == ("OP", "+"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '+'")

        elif topo == "-":
            if i < len(tokens) and tokens[i] == ("OP", "-"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '-'")

        elif topo == "print":
            if i < len(tokens) and tokens[i][0] == "PRINT":
                i += 1
            else:
                raise Exception("Erro sintático: esperado print")

        elif topo == "(":
            if i < len(tokens) and tokens[i] == ("PAREN", "("):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '('")

        elif topo == ")":
            if i < len(tokens) and tokens[i] == ("PAREN", ")"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado ')'")

        else:
            raise Exception(f"Símbolo desconhecido na pilha: {topo}")

    if i != len(tokens):
        raise Exception("Erro sintático: tokens extras")

    return True


if __name__ == "__main__":
    while True:
        codigo = input("Digite o código: ")

        try:
            tokens = lexer(codigo)

            print("\nTokens:")
            for t in tokens:
                print(t)

            resultado = analisar_sintatico(tokens)
            print("\nSintático:", "OK" if resultado else "Erro")

        except Exception as e:
            print(e)

        continuar = input("\nContinuar? (s/n): ").lower()
        if continuar != "s":
            break