class Pilha:
    def __init__(self):
        self.dados = []

    def empilhar(self, valor):
        self.dados.append(valor)

    def desempilhar(self):
        return self.dados.pop() if self.dados else None

    def topo(self):
        return self.dados[-1] if self.dados else None

    def vazia(self):
        return len(self.dados) == 0