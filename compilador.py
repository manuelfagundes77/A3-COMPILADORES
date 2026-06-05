# ============================================================
# COMPILADOR — Integração de todas as etapas da MiniLang
#
# Conceito:
#   Orquestra todas as etapas do compilador em sequência:
#   Léxico → Sintático → Semântico → Gerador → Executor
#
#   Cada linha do código fonte passa pelas 4 primeiras etapas.
#   O código intermediário de todas as linhas é acumulado e
#   enviado ao executor apenas no final.
#
#   Exemplo:
#     Entrada:
#       x = 10
#       y = x + 5
#       print(y)
#
#     Fluxo:
#       Linha 1 → tokens → válido → semântico → LOAD 10 / STORE x
#       Linha 2 → tokens → válido → semântico → LOAD x / ADD 5 / STORE y
#       Linha 3 → tokens → válido → semântico → PRINT y
#       Executor roda tudo → imprime 15
# ============================================================

import io
import sys
import os
from contextlib import redirect_stdout

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer.analisador_lexico import lexer
from parser.analisador_sintatico import analisar_sintatico
from semantico.analisador_semantico import semantico, variaveis_definidas
from gerador.gerador import gerar_codigo
from executor.executor import executar


def compilar(codigo_fonte, verbose=False):
    """
    Compila e executa um programa MiniLang.

    Parâmetros:
        codigo_fonte → string com o código completo (pode ter várias linhas)
        verbose      → se True, mostra detalhes de cada etapa

    Retorna:
        A memória final com os valores das variáveis.
    """

    # Reseta a tabela de símbolos do semântico antes de compilar
    variaveis_definidas.clear()

    # Separa o código em linhas e ignora linhas vazias
    linhas = [linha.strip() for linha in codigo_fonte.strip().split("\n") if linha.strip()]

    codigo_intermediario_completo = []

    print("=== COMPILADOR MINILANG ===\n")

    # -------------------------------------------------------
    # Etapa 1 — Mostra o código fonte recebido
    # -------------------------------------------------------
    print("=== CÓDIGO FONTE ===")
    for linha in linhas:
        print(f"  {linha}")

    print()

    # -------------------------------------------------------
    # Etapas 2, 3, 4, 5 — Processa linha por linha
    # -------------------------------------------------------
    for numero_linha, linha in enumerate(linhas, start=1):

        if verbose:
            print(f"--- Linha {numero_linha}: {linha} ---")

        # Etapa 2: Análise Léxica — gera tokens via AFD
        tokens = lexer(linha)

        if verbose:
            print(f"  Tokens: {tokens}")

        # Etapa 3: Análise Sintática — valida estrutura via PDA
        # A saída da pilha é suprimida para manter o terminal limpo
        with redirect_stdout(io.StringIO()):
            analisar_sintatico(tokens)

        if verbose:
            print(f"  Sintático: OK")

        # Etapa 4: Análise Semântica — verifica variáveis via CSL
        semantico(tokens)

        if verbose:
            print(f"  Semântico: OK")
            print(f"  Variáveis definidas: {variaveis_definidas}")

        # Etapa 5: Geração de código intermediário
        instrucoes = gerar_codigo(tokens)
        codigo_intermediario_completo.extend(instrucoes)

        if verbose:
            print(f"  Código gerado: {instrucoes}")

        if verbose:
            print()

    # -------------------------------------------------------
    # Etapa 6 — Mostra o código intermediário completo
    # -------------------------------------------------------
    print("=== CÓDIGO INTERMEDIÁRIO ===")
    for instrucao in codigo_intermediario_completo:
        print(f"  {instrucao}")

    print()

    # -------------------------------------------------------
    # Etapa 7 — Executa o código intermediário (Máquina de Turing)
    # -------------------------------------------------------
    memoria_final = executar(codigo_intermediario_completo, verbose=True)

    return memoria_final


if __name__ == "__main__":
    testes = [
        {
            "nome": "Teste 1 — Exemplo básico do professor",
            "codigo": """
x = 10
y = x + 5
print(y)
"""
        },
        {
            "nome": "Teste 2 — Múltiplas variáveis e prints",
            "codigo": """
x = 10
y = x + 5
z = y - 3
print(y)
print(z)
"""
        },
        {
            "nome": "Teste 3 — Erro semântico: variável não definida",
            "codigo": """
x = 10
y = w + 5
print(y)
"""
        },
        {
            "nome": "Teste 4 — Erro sintático: estrutura inválida",
            "codigo": """
x 10 = +
"""
        },
    ]

    for teste in testes:
        print("\n========================================")
        print(teste["nome"])
        print("========================================\n")

        try:
            compilar(teste["codigo"])
        except Exception as erro:
            print(f"Erro: {erro}")