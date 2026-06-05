# ============================================================
# GERADOR DE CÓDIGO INTERMEDIÁRIO
#
# Conceito:
#   Converte os tokens da MiniLang em pseudo-assembly, uma
#   representação intermediária mais próxima da linguagem de máquina.
#
#   Exemplo:
#     Código: x = 10 + 5
#     Pseudo-assembly:
#       LOAD 10
#       ADD 5
#       STORE x
#
#   Instruções do pseudo-assembly:
#     LOAD valor  → carrega um número ou variável no acumulador
#     STORE var   → guarda o acumulador em uma variável
#     ADD valor   → soma ao acumulador
#     SUB valor   → subtrai do acumulador
#     PRINT var   → imprime o valor de uma variável
#
#   O executor (Máquina de Turing) processará essas instruções
#   sequencialmente para produzir o resultado final.
# ============================================================

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def gerar_atribuicao(tokens):
    """
    Gera código para atribuição: x = 10 + 5
    
    Estratégia:
      1. LOAD primeiro valor
      2. Para cada operador: ADD/SUB próximo valor
      3. STORE no destino
    """
    codigo = []
    variavel_destino = tokens[0][1]
    
    # tokens[0] = ID, tokens[1] = '=', tokens[2:] = expressão
    expressao = tokens[2:]
    
    # Carrega o primeiro valor
    tipo, valor = expressao[0]
    codigo.append(f"LOAD {valor}")
    
    # Processa operadores e valores seguintes
    i = 1
    while i < len(expressao):
        if expressao[i][0] == "OP":
            operador = expressao[i][1]
            
            # Próximo valor
            i += 1
            tipo, valor = expressao[i]
            
            if operador == "+":
                codigo.append(f"ADD {valor}")
            elif operador == "-":
                codigo.append(f"SUB {valor}")
        
        i += 1
    
    # Guarda o resultado
    codigo.append(f"STORE {variavel_destino}")
    
    return codigo


def gerar_print(tokens):
    """
    Gera código para print: print(x)
    
    Estratégia:
      PRINT var
    """
    codigo = []
    
    # Procura o ID dentro do print
    for tipo, valor in tokens:
        if tipo == "ID":
            codigo.append(f"PRINT {valor}")
            break
    
    return codigo


def gerar_codigo(tokens):
    """
    Função principal da geração de código.
    
    Recebe tokens e retorna lista de instruções em pseudo-assembly.
    """
    if len(tokens) == 0:
        return []
    
    if tokens[0][0] == "ID":
        return gerar_atribuicao(tokens)
    
    elif tokens[0][0] == "PRINT":
        return gerar_print(tokens)
    
    else:
        raise Exception("Erro no gerador: instrução desconhecida")


if __name__ == "__main__":
    from lexer.analisador_lexico import lexer
    
    testes = [
        "x = 10",
        "y = x + 5",
        "z = y - 3",
        "print(z)"
    ]
    
    print("=== GERADOR DE CÓDIGO INTERMEDIÁRIO ===\n")
    
    for codigo_fonte in testes:
        print(f"Código: {codigo_fonte}")
        
        tokens = lexer(codigo_fonte)
        print(f"Tokens: {tokens}")
        
        codigo_intermediario = gerar_codigo(tokens)
        print("Pseudo-assembly:")
        for instrucao in codigo_intermediario:
            print(f"  {instrucao}")
        
        print()