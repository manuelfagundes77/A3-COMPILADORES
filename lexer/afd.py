INICIO = "INICIO"
LENDO_ID = "LENDO_ID"
LENDO_NUM = "LENDO_NUM"
LENDO_OPERADOR = "LENDO_OPERADOR"
LENDO_PAREN = "LENDO_PAREN"
FIM = "FIM"
ERRO = "ERRO"

CATEGORIA_LETRA = "letra"
CATEGORIA_DIGITO = "digito"
CATEGORIA_OPERADOR = "operador"
CATEGORIA_PAREN = "paren"
CATEGORIA_ESPACO = "espaco"
CATEGORIA_OUTRO = "outro"


tabela_de_transicao = {
    INICIO: {
        CATEGORIA_LETRA: LENDO_ID,
        CATEGORIA_DIGITO: LENDO_NUM,
        CATEGORIA_OPERADOR: LENDO_OPERADOR,
        CATEGORIA_PAREN: LENDO_PAREN,
        CATEGORIA_ESPACO: INICIO,
        CATEGORIA_OUTRO: ERRO,
    },

    LENDO_ID: {
        CATEGORIA_LETRA: LENDO_ID,
        CATEGORIA_DIGITO: LENDO_ID,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN: FIM,
        CATEGORIA_ESPACO: FIM,
        CATEGORIA_OUTRO: FIM,
    },

    LENDO_NUM: {
        CATEGORIA_LETRA: ERRO,
        CATEGORIA_DIGITO: LENDO_NUM,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN: FIM,
        CATEGORIA_ESPACO: FIM,
        CATEGORIA_OUTRO: FIM,
    },

    LENDO_OPERADOR: {
        CATEGORIA_LETRA: FIM,
        CATEGORIA_DIGITO: FIM,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN: FIM,
        CATEGORIA_ESPACO: FIM,
        CATEGORIA_OUTRO: FIM,
    },

    LENDO_PAREN: {
        CATEGORIA_LETRA: FIM,
        CATEGORIA_DIGITO: FIM,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN: FIM,
        CATEGORIA_ESPACO: FIM,
        CATEGORIA_OUTRO: FIM,
    },
}


def classificar_caractere(caractere):
    if caractere.isalpha():
        return CATEGORIA_LETRA

    elif caractere.isdigit():
        return CATEGORIA_DIGITO

    elif caractere in ("+", "-", "="):
        return CATEGORIA_OPERADOR

    elif caractere in ("(", ")"):
        return CATEGORIA_PAREN

    elif caractere in (" ", "\t", "\n"):
        return CATEGORIA_ESPACO

    else:
        return CATEGORIA_OUTRO


def transicao(estado_atual, caractere_atual):
    categoria = classificar_caractere(caractere_atual)

    transicoes_do_estado = tabela_de_transicao.get(estado_atual, {})
    proximo_estado = transicoes_do_estado.get(categoria, ERRO)

    return proximo_estado