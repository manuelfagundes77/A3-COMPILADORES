# ============================================================
# EXECUTOR — Execução do código intermediário da MiniLang
#
# Conceito:
#   O executor recebe o pseudo-assembly gerado pelo gerador
#   de código intermediário e executa as instruções em sequência.
#
#   Exemplo de pseudo-assembly:
#     LOAD 10
#     STORE x
#     LOAD x
#     ADD 5
#     STORE y
#     PRINT y
#
#   Instruções:
#     LOAD valor  → carrega um número ou variável no acumulador
#     ADD valor   → soma um valor ao acumulador
#     SUB valor   → subtrai um valor do acumulador
#     STORE var   → guarda o acumulador em uma variável
#     PRINT var   → imprime o valor de uma variável
#
#   Conceito teórico relacionado:
#     Máquina de Turing
#
#   A relação com a Máquina de Turing aparece porque o executor
#   processa as instruções uma por uma, de forma sequencial,
#   usando uma memória para armazenar os valores das variáveis.
# ============================================================

import sys
import os
import io
from contextlib import redirect_stdout

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def obter_valor(valor, memoria):
    """
    Obtém o valor real de um número ou de uma variável.

    Parâmetros:
        valor   → número ou nome de variável
        memoria → dicionário com os valores das variáveis

    Retorna:
        O valor inteiro correspondente.
    """
    if valor.isdigit():
        return int(valor)

    if valor in memoria:
        return memoria[valor]

    raise Exception(f"Erro de execução: variável '{valor}' não possui valor")


def executar_instrucao(instrucao, memoria, acumulador, saidas):
    """
    Executa uma única instrução do pseudo-assembly.

    Parâmetros:
        instrucao  → instrução atual
        memoria    → dicionário que guarda as variáveis
        acumulador → valor temporário usado nos cálculos
        saidas     → lista que guarda as saídas do PRINT

    Retorna:
        O novo valor do acumulador e a descrição do passo executado.
    """
    partes = instrucao.split()

    if len(partes) < 2:
        raise Exception(f"Erro de execução: instrução inválida '{instrucao}'")

    comando = partes[0]
    argumento = partes[1]

    if comando == "LOAD":
        acumulador = obter_valor(argumento, memoria)
        descricao = f"{instrucao:15} → acumulador = {acumulador}"

    elif comando == "ADD":
        valor = obter_valor(argumento, memoria)
        acumulador = acumulador + valor
        descricao = f"{instrucao:15} → acumulador = {acumulador}"

    elif comando == "SUB":
        valor = obter_valor(argumento, memoria)
        acumulador = acumulador - valor
        descricao = f"{instrucao:15} → acumulador = {acumulador}"

    elif comando == "STORE":
        memoria[argumento] = acumulador
        descricao = f"{instrucao:15} → memoria[{argumento}] = {acumulador}"

    elif comando == "PRINT":
        valor = obter_valor(argumento, memoria)
        saidas.append(valor)
        descricao = f"{instrucao:15} → imprime {valor}"

    else:
        raise Exception(f"Erro de execução: comando desconhecido '{comando}'")

    return acumulador, descricao


def executar(codigo_intermediario, verbose=False):
    """
    Função principal da execução.

    Parâmetros:
        codigo_intermediario → lista de instruções em pseudo-assembly
        verbose              → se True, mostra a execução passo a passo

    Retorna:
        A memória final com os valores das variáveis.
    """
    memoria = {}
    acumulador = 0
    saidas = []

    if verbose:
        print("=== EXECUÇÃO (MÁQUINA DE TURING) ===")

    for instrucao in codigo_intermediario:
        acumulador, descricao = executar_instrucao(
            instrucao,
            memoria,
            acumulador,
            saidas
        )

        if verbose:
            print(f"  {descricao}")

    if verbose:
        print("\n=== MEMÓRIA FINAL ===")
        print(f"Variáveis: {formatar_memoria(memoria)}")

        print("\n=== SAÍDA DO PROGRAMA ===")
        for saida in saidas:
            print(saida)

    return memoria


def formatar_memoria(memoria):
    """
    Formata a memória para exibição no terminal.

    Exemplo:
        {"x": 10, "y": 15}

    Saída:
        {x: 10, y: 15}
    """
    if not memoria:
        return "{}"

    itens = []

    for variavel, valor in memoria.items():
        itens.append(f"{variavel}: {valor}")

    return "{" + ", ".join(itens) + "}"


if __name__ == "__main__":
    from lexer.analisador_lexico import lexer
    from parser.analisador_sintatico import analisar_sintatico
    from semantico.analisador_semantico import semantico, variaveis_definidas
    from gerador.gerador import gerar_codigo

    programa_teste = [
        "x = 10",
        "y = x + 5",
        "z = y - 3",
        "print(z)"
    ]

    codigo_intermediario_completo = []

    variaveis_definidas.clear()

    print("=== EXECUTOR === \n")

    print("Código fonte:")
    for linha in programa_teste:
        print(f"  {linha}")

    try:
        for linha in programa_teste:
            tokens = lexer(linha)

            # O sintático é executado, mas a saída da pilha fica escondida
            # para a apresentação do executor ficar mais limpa.
            with redirect_stdout(io.StringIO()):
                analisar_sintatico(tokens)

            semantico(tokens)

            instrucoes = gerar_codigo(tokens)
            codigo_intermediario_completo.extend(instrucoes)

        print("\nCódigo intermediário:")
        for instrucao in codigo_intermediario_completo:
            print(f"  {instrucao}")

        print()
        executar(codigo_intermediario_completo, verbose=True)

    except Exception as e:
        print(e)