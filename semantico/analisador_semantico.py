# ============================================================
# ANALISADOR SEMÂNTICO — Verificação de significado da MiniLang
#
# Conceito:
#   O analisador semântico verifica se o código, além de estar
#   escrito corretamente, também faz sentido.
#
#   Exemplo:
#     x = 10       → válido, cria a variável x
#     y = x + 5    → válido, se x já foi criada
#     z = a + 2    → inválido, se a ainda não foi criada
#     print(y)     → válido, se y já foi criada
#
#   Enquanto o analisador sintático verifica a ORDEM dos tokens,
#   o analisador semântico verifica o USO correto das variáveis.
#
#   Conceito teórico relacionado:
#     Linguagem Sensível ao Contexto (CSL)
#
#   Isso acontece porque o significado depende do contexto anterior:
#   uma variável só pode ser usada se já foi declarada/criada antes.
# ============================================================

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer.analisador_lexico import lexer
from parser.analisador_sintatico import analisar_sintatico


# Tabela de símbolos:
# Guarda as variáveis que já foram criadas durante a análise.
variaveis_definidas = set()


def registrar_variavel(nome_variavel):
    """
    Registra uma variável na tabela de símbolos.

    Parâmetros:
        nome_variavel → nome da variável que será criada
    """
    variaveis_definidas.add(nome_variavel)


def verificar_variavel_definida(nome_variavel):
    """
    Verifica se uma variável já foi criada antes de ser usada.

    Parâmetros:
        nome_variavel → nome da variável que será verificada

    Lança erro se a variável ainda não existir.
    """
    if nome_variavel not in variaveis_definidas:
        raise Exception(f"Erro semântico: variável '{nome_variavel}' não foi definida")


def verificar_atribuicao(tokens):
    """
    Verifica semanticamente uma atribuição.

    Exemplo:
        x = 10
        y = x + 5

    Regras:
        - A variável do lado esquerdo será registrada.
        - Variáveis usadas do lado direito precisam existir antes.
    """
    variavel_recebe = tokens[0][1]

    # Percorre os tokens depois do '='
    for tipo, valor in tokens[2:]:
        if tipo == "ID":
            verificar_variavel_definida(valor)

    registrar_variavel(variavel_recebe)


def verificar_print(tokens):
    """
    Verifica semanticamente o comando print.

    Exemplo:
        print(x)

    Regra:
        - A variável usada dentro do print precisa existir antes.
    """
    for tipo, valor in tokens:
        if tipo == "ID":
            verificar_variavel_definida(valor)


def semantico(tokens):
    """
    Função principal da análise semântica.

    Parâmetros:
        tokens → lista de tokens retornada pelo analisador léxico

    Retorna:
        True se a análise semântica estiver correta.
    """
    if len(tokens) == 0:
        raise Exception("Erro semântico: código vazio")

    if tokens[0][0] == "ID":
        verificar_atribuicao(tokens)

    elif tokens[0][0] == "PRINT":
        verificar_print(tokens)

    else:
        raise Exception("Erro semântico: instrução inválida")

    return True


if __name__ == "__main__":
    testes = [
        {
            "nome": "Teste 1 — Correto: variável usando outra já definida",
            "codigos": [
                "x = 5",
                "y = x + 2",
                "print(y)"
            ]
        },
        {
            "nome": "Teste 2 — Errado: variável w não foi definida",
            "codigos": [
                "x = 5",
                "y = x + w",
                "print(y)"
            ]
        },
        {
            "nome": "Teste 3 — Errado: print usando variável não definida",
            "codigos": [
                "print(w)"
            ]
        },
        {
            "nome": "Teste 4 — Correto: expressão com vários valores",
            "codigos": [
                "x =  3 + 2",
                "y = 2 + x",
                "z = x + y + 10",
                "print(z)"
            ]
        },
        {
            "nome": "Teste 5 — Errado: variável z usada antes de existir",
            "codigos": [
                "x = 10",
                "y = z + 1",
                "print(y)"
            ]
        }
    ]

    for teste in testes:
        print("\n========================================")
        print(teste["nome"])
        print("========================================")

        # Cada teste começa com a tabela de símbolos vazia
        variaveis_definidas.clear()

        for codigo in teste["codigos"]:
            print(f"\nCódigo: {codigo}")

            try:
                tokens = lexer(codigo)

                # Aqui o sintático ainda é chamado para garantir
                # que a estrutura do código está correta,
                # mas o foco da saída será apenas o semântico.
                analisar_sintatico(tokens)

                semantico(tokens)

                print("Semântico: OK")
                print("Variáveis definidas:", variaveis_definidas)

            except Exception as e:
                print("Semântico:", e)
                print("Variáveis definidas:", variaveis_definidas)
                print("Teste interrompido por erro.")
                break