# ============================================================
# ANALISADOR SINTÁTICO — Parser da MiniLang
#
# Conceito:
#   O analisador sintático verifica se a sequência de tokens
#   obedece às regras gramaticais da linguagem MiniLang.
#
#   Nesta versão:
#     - A atribuição é validada por regras sintáticas diretas
#     - O comando print é validado usando pilha (PDA)
#
#   Gramática simplificada da MiniLang:
#
#     ATRIBUICAO → ID = EXPRESSAO
#     EXPRESSAO  → VALOR (OP VALOR)*
#     VALOR      → ID | NUM
#     OP         → + | -
#
#     PRINT      → print ( ID )
#
#   Exemplos aceitos:
#     x = 4
#     x = 4 + 6
#     x = y
#     x = y + 6
#     x = y + z + 5
#     print(x)
#
#   Conceitos:
#     - Gramática Livre de Contexto: regras da linguagem
#     - PDA: usado na validação do print com pilha
# ============================================================

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from parser.pilha import Pilha
from lexer.analisador_lexico import lexer


# ------------------------------------------------------------
# DICIONÁRIO DE REGRAS SINTÁTICAS
# ------------------------------------------------------------
#  as regras principais da linguagem.
#
# A atribuição segue:
#   ID = VALOR (OP VALOR)*
#
# Ou seja:
#   começa com ID
#   depois precisa ter =
#   depois precisa ter um valor
#   depois pode repetir operador + valor
# ------------------------------------------------------------

regras_sintaticas = {
    "ATRIBUICAO": {
        "inicio": ["ID", "="],
        "valores": ["ID", "NUM"],
        "operadores": ["+", "-"],
        "formato": "ID = VALOR (OP VALOR)*"
    },

    "PRINT": {
        "formato": ["PRINT", "(", "ID", ")"],
        "usa_pilha": True
    }
}


def eh_valor(token):
    """
    Verifica se o token é um valor válido para expressão.

    VALOR pode ser:
        ID  → variável
        NUM → número
    """
    tipo, valor = token
    return tipo in regras_sintaticas["ATRIBUICAO"]["valores"]


def eh_operador_matematico(token):
    """
    Verifica se o token é operador matemático aceito.

    Operadores aceitos:
        +
        -
    """
    tipo, valor = token

    return (
        tipo == "OP"
        and valor in regras_sintaticas["ATRIBUICAO"]["operadores"]
    )


def validar_expressao(tokens_expressao):
    """
    Valida a expressão depois do sinal de igual.

    Formato aceito:
        VALOR
        VALOR OP VALOR
        VALOR OP VALOR OP VALOR ...

    Exemplos válidos:
        4
        y
        4 + 6
        y + 6
        y + z + 5

    Exemplos inválidos:
        + 4
        y +
        y + + 6
    """
    if len(tokens_expressao) == 0:
        raise Exception("Erro sintático: expressão vazia após '='")

    esperando_valor = True

    for token in tokens_expressao:
        if esperando_valor:
            if eh_valor(token):
                esperando_valor = False
            else:
                raise Exception("Erro sintático: esperado ID ou NUM na expressão")

        else:
            if eh_operador_matematico(token):
                esperando_valor = True
            else:
                raise Exception("Erro sintático: esperado operador '+' ou '-'")

    if esperando_valor:
        raise Exception("Erro sintático: expressão não pode terminar com operador")


def validar_atribuicao(tokens):
    """
    Valida uma atribuição.

    Formato esperado:
        ID = EXPRESSAO

    Exemplos:
        x = 4
        x = 4 + 6
        x = y
        x = y + 6
        x = y + z + 5
    """
    if len(tokens) < 3:
        raise Exception("Erro sintático: atribuição incompleta")

    if tokens[0][0] != "ID":
        raise Exception("Erro sintático: atribuição deve começar com ID")

    if tokens[1] != ("OP", "="):
        raise Exception("Erro sintático: esperado '=' após o ID")

    tokens_expressao = tokens[2:]

    validar_expressao(tokens_expressao)


def analisar_print_com_pilha(tokens):
    """
    Valida o comando print usando pilha.

    Formato esperado:
        print ( ID )

    Exemplo:
        print(x)

    Aqui a pilha demonstra o funcionamento de um PDA.
    """
    pilha = Pilha()
    i = 0

    pilha.empilhar("PRINT")

    while not pilha.vazia():
        topo = pilha.desempilhar()

        if topo == "PRINT":
            pilha.empilhar(")")
            pilha.empilhar("ID")
            pilha.empilhar("(")
            pilha.empilhar("print")

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

        elif topo == "ID":
            if i < len(tokens) and tokens[i][0] == "ID":
                i += 1
            else:
                raise Exception("Erro sintático: esperado ID dentro do print")

        elif topo == ")":
            if i < len(tokens) and tokens[i] == ("PAREN", ")"):
                i += 1
            else:
                raise Exception("Erro sintático: esperado ')'")

        else:
            raise Exception(f"Símbolo desconhecido na pilha: {topo}")

    if i != len(tokens):
        raise Exception("Erro sintático: tokens extras após o print")

    pilha.mostrar_historico()


def analisar_sintatico(tokens):
    """
    Função principal da análise sintática.

    Ela identifica se a instrução é:
        - atribuição
        - print

    Depois chama a validação correta.
    """
    if len(tokens) == 0:
        raise Exception("Erro sintático: código vazio")

    if tokens[0][0] == "ID":
        validar_atribuicao(tokens)

    elif tokens[0][0] == "PRINT":
        analisar_print_com_pilha(tokens)

    else:
        raise Exception("Erro sintático: instrução inválida")

    return True


if __name__ == "__main__":
    testes = [
        {
            "nome": "Teste 1 — Correto: atribuição simples",
            "codigo": "x = 10"
        },
        {
            "nome": "Teste 6 — Errado: expressão termina com operador",
            "codigo": "x = 10 +"
        },
        {
            "nome": "Teste 7 — Errado: comando inválido com parêntese",
            "codigo": "pint(x)"
        },
    ]
 
    print("=== ANALISADOR SINTÁTICO (PDA) ===\n")
 
    for teste in testes:
        print("========================================")
        print(teste["nome"])
        print("========================================")
        print(f"Código: {teste['codigo']}")
 
        try:
            tokens = lexer(teste["codigo"])
            print(f"Tokens: {tokens}")
            analisar_sintatico(tokens)
            print("Sintático: OK")
 
        except Exception as e:
            print(f"Sintático: {e}")
 
        print()
 