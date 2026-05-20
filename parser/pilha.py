# ============================================================
# PILHA — Estrutura de Dados do PDA (Autômato de Pilha)
#
# Conceito:
#   A pilha é uma estrutura de dados LIFO (Last In, First Out)
#   que armazena símbolos durante a análise sintática. No contexto
#   de um PDA (Pushdown Automaton), a pilha permite ao autômato
#   "lembrar" de informações sobre a estrutura do código enquanto
#   o processa sequencialmente.
#
#   Operações fundamentais:
#     - empilhar (push): adiciona um elemento no topo
#     - desempilhar (pop): remove e retorna o elemento do topo
#     - topo: consulta o elemento do topo sem remover
#     - vazia: verifica se a pilha está vazia
#
#   O histórico registra cada operação para demonstrar visualmente
#   o funcionamento do PDA durante a análise sintática.
#
# Exemplo de uso no parser:
#   pilha.empilhar("EXPR")     → Pilha: [EXPR]
#   pilha.empilhar("ID")       → Pilha: [EXPR, ID]
#   pilha.desempilhar()        → Pilha: [EXPR]
# ============================================================


class Pilha:
    """
    Implementação de uma pilha com registro de histórico.
    
    A pilha mantém uma lista de dados (self.dados) e um histórico
    (self.historico) que registra cada operação realizada junto com
    o estado da pilha após a operação.
    """
    
    def __init__(self):
        """
        Inicializa a pilha vazia.
        
        Atributos:
            dados     → lista que armazena os elementos da pilha
            historico → lista que registra cada operação realizada
        """
        self.dados = []
        self.historico = []
    
    def empilhar(self, valor):
        """
        Adiciona um elemento no topo da pilha (operação PUSH).
        
        Parâmetros:
            valor → elemento a ser empilhado
        """
        self.dados.append(valor)
        # Registra a operação no histórico com uma cópia do estado atual
        self.historico.append(f"PUSH {valor:10} → Pilha: {self.dados.copy()}")
    
    def desempilhar(self):
        """
        Remove e retorna o elemento do topo da pilha (operação POP).
        
        Retorna:
            o elemento que estava no topo, ou None se a pilha estiver vazia
        """
        if self.dados:
            valor = self.dados.pop()
            # Registra a operação no histórico com o estado após o POP
            self.historico.append(f"POP  {valor:10} → Pilha: {self.dados.copy()}")
            return valor
        return None
    
    def topo(self):
        """
        Retorna o elemento no topo da pilha sem removê-lo.
        
        Retorna:
            o elemento do topo, ou None se a pilha estiver vazia
        """
        return self.dados[-1] if self.dados else None
    
    def vazia(self):
        """
        Verifica se a pilha está vazia.
        
        Retorna:
            True se a pilha não contém elementos, False caso contrário
        """
        return len(self.dados) == 0
    
    def mostrar_historico(self):
        """
        Exibe no terminal todas as operações registradas no histórico.
        
        """
        print("\n=== HISTÓRICO DA PILHA (PDA) ===")
        for operacao in self.historico:
            print(f"  {operacao}")
        print("================================\n")
    
    def limpar_historico(self):
        """
        Limpa o histórico de operações.
        """
        self.historico = []