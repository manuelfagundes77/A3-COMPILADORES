# ============================================================
# ANALISADOR SINTÁTICO — Parser com PDA (Autômato de Pilha)
#
# Conceito:
#   O analisador sintático verifica se a sequência de tokens
#   obedece às regras gramaticais da linguagem MiniLang. Utiliza
#   um PDA (Pushdown Automaton) — autômato com pilha — para
#   processar a estrutura hierárquica do código.
#
#   Gramática da MiniLang:
#     PROGRAM → STMT
#     STMT    → ID = EXPR | print(ID)
#     EXPR    → VALOR RESTO
#     RESTO   → OP VALOR RESTO | ε (vazio)
#     VALOR   → ID | NUM
#     OP      → + | -
#
#   A pilha guarda símbolos não-terminais (EXPR, STMT, etc.) e
#   terminais (ID, =, etc.) que ainda precisam ser processados.
#
# Exemplo para "x = 10":
#   Pilha inicial: [ATRIB]
#   Expande ATRIB → [ID, =, EXPR]
#   Consome ID    → [=, EXPR]
#   Consome =     → [EXPR]
#   Expande EXPR  → [VALOR, RESTO]
#   Consome NUM   → [RESTO]
#   RESTO vazio   → []
#   ✓ Aceito
# ============================================================

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from parser.pilha import Pilha
from lexer.analisador_lexico import lexer


def analisar_sintatico(tokens):
    """
    Analisa a estrutura sintática dos tokens usando um PDA.
    
    Parâmetros:
        tokens → lista de tuplas (tipo, valor) retornada pelo lexer
    
    Retorna:
        True se a estrutura é válida, lança exceção se inválida
    """
    pilha = Pilha()
    i = 0  # índice do token atual sendo processado

    # Verifica se o código não está vazio
    if len(tokens) == 0:
        raise Exception("Erro sintático: código vazio")

    # -----------------------------------------------------------
    # VALIDAÇÃO: Se o primeiro token é ID seguido de '(',
    # só aceita se for o comando 'print'
    # Exemplo: pint(x) → erro, abc(y) → erro
    # -----------------------------------------------------------
    if tokens[0][0] == "ID" and len(tokens) > 1 and tokens[1] == ("PAREN", "("):
        raise Exception(f"Erro sintático: '{tokens[0][1]}' não é um comando válido. Apenas 'print' pode usar parênteses")

    # Identifica o tipo de instrução pelo primeiro token
    # e empilha o símbolo inicial correspondente
    if tokens[0][0] == "ID":
        pilha.empilhar("ATRIB")  # é uma atribuição: x = ...

    elif tokens[0][0] == "PRINT":
        pilha.empilhar("PRINT")  # é um print: print(...)

    else:
        raise Exception("Erro sintático: instrução inválida")

    # Loop principal: processa a pilha até ela esvaziar
    while not pilha.vazia():
        topo = pilha.desempilhar()

        # -----------------------------------------------------------
        # Produção: ATRIB → ID = EXPR
        # Quando encontra ATRIB na pilha, expande para os símbolos
        # que compõem uma atribuição
        # -----------------------------------------------------------
        if topo == "ATRIB":
            pilha.empilhar("EXPR")
            pilha.empilhar("=")
            pilha.empilhar("ID")

        # -----------------------------------------------------------
        # Produção: PRINT → print ( ID )
        # Empilha os símbolos na ordem inversa (por ser pilha)
        # -----------------------------------------------------------
        elif topo == "PRINT":
            pilha.empilhar(")")
            pilha.empilhar("ID")
            pilha.empilhar("(")
            pilha.empilhar("print")

        # -----------------------------------------------------------
        # Produção: EXPR → VALOR RESTO
        # Uma expressão começa com um valor (ID ou NUM)
        # -----------------------------------------------------------
        elif topo == "EXPR":
            if i < len(tokens) and tokens[i][0] in ("ID", "NUM"):
                pilha.empilhar("RESTO")
                pilha.empilhar("VALOR")
            else:
                raise Exception("Erro sintático: expressão inválida")

        # -----------------------------------------------------------
        # Produção: RESTO → OP VALOR | ε (vazio)
        # Após um valor, pode vir um operador + outro valor, ou nada
        # -----------------------------------------------------------
        elif topo == "RESTO":
            if i < len(tokens) and tokens[i][0] == "OP" and tokens[i][1] in ("+", "-"):
                operador = tokens[i][1]
                pilha.empilhar("VALOR")
                pilha.empilhar(operador)
            # Se não tem operador, RESTO é vazio (produção ε) — não faz nada

        # -----------------------------------------------------------
        # Terminal: VALOR → ID | NUM
        # Consome um token ID ou NUM da entrada
        # -----------------------------------------------------------
        elif topo == "VALOR":
            if i < len(tokens) and tokens[i][0] in ("ID", "NUM"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado ID ou NUM")

        # -----------------------------------------------------------
        # Terminal: ID
        # Consome um token ID da entrada
        # -----------------------------------------------------------
        elif topo == "ID":
            if i < len(tokens) and tokens[i][0] == "ID":
                i += 1
            else:
                raise Exception("Erro sintático: esperado ID")

        # -----------------------------------------------------------
        # Terminal: =
        # Consome o operador de atribuição
        # -----------------------------------------------------------
        elif topo == "=":
            if i < len(tokens) and tokens[i] == ("OP", "="):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '='")

        # -----------------------------------------------------------
        # Terminal: +
        # Consome o operador de adição
        # -----------------------------------------------------------
        elif topo == "+":
            if i < len(tokens) and tokens[i] == ("OP", "+"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '+'")

        # -----------------------------------------------------------
        # Terminal: -
        # Consome o operador de subtração
        # -----------------------------------------------------------
        elif topo == "-":
            if i < len(tokens) and tokens[i] == ("OP", "-"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '-'")

        # -----------------------------------------------------------
        # Terminal: print
        # Consome a palavra-chave print
        # -----------------------------------------------------------
        elif topo == "print":
            if i < len(tokens) and tokens[i][0] == "PRINT":
                i += 1
            else:
                raise Exception("Erro sintático: esperado print")

        # -----------------------------------------------------------
        # Terminal: (
        # Consome o parêntese de abertura
        # -----------------------------------------------------------
        elif topo == "(":
            if i < len(tokens) and tokens[i] == ("PAREN", "("):
                i += 1
            else:
                raise Exception("Erro sintático: esperado '('")

        # -----------------------------------------------------------
        # Terminal: )
        # Consome o parêntese de fechamento
        # -----------------------------------------------------------
        elif topo == ")":
            if i < len(tokens) and tokens[i] == ("PAREN", ")"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado ')'")

        else:
            raise Exception(f"Símbolo desconhecido na pilha: {topo}")

    # Verifica se todos os tokens foram consumidos
    if i != len(tokens):
        raise Exception("Erro sintático: tokens extras")

    # Mostra o histórico de operações da pilha (demonstra o PDA)
    pilha.mostrar_historico()

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