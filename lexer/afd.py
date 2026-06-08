# Q — conjunto de estados do autômato
INICIO         = "INICIO"
LENDO_ID       = "LENDO_ID"
LENDO_NUM      = "LENDO_NUM"
LENDO_OPERADOR = "LENDO_OPERADOR"
LENDO_PAREN    = "LENDO_PAREN"
FIM            = "FIM"   # F — estado de aceitação
ERRO           = "ERRO"

# Σ — alfabeto (categorias de caracteres)
CATEGORIA_LETRA    = "letra"
CATEGORIA_DIGITO   = "digito"
CATEGORIA_OPERADOR = "operador"
CATEGORIA_PAREN    = "paren"
CATEGORIA_ESPACO   = "espaco"
CATEGORIA_OUTRO    = "outro"


# δ — função de transição (este dicionário É o autômato)
# Leitura: tabela[estado_atual][categoria] = proximo_estado
# q0 — estado inicial é INICIO
tabela_de_transicao = {

    # Em INICIO decidimos qual token está começando
    INICIO: {
        CATEGORIA_LETRA:    LENDO_ID,
        CATEGORIA_DIGITO:   LENDO_NUM,
        CATEGORIA_OPERADOR: LENDO_OPERADOR,
        CATEGORIA_PAREN:    LENDO_PAREN,
        CATEGORIA_ESPACO:   INICIO,   # espaço em INICIO é ignorado
        CATEGORIA_OUTRO:    ERRO,
    },

    # Em LENDO_ID continuamos enquanto for letra ou dígito
    LENDO_ID: {
        CATEGORIA_LETRA:    LENDO_ID,
        CATEGORIA_DIGITO:   LENDO_ID,
        CATEGORIA_OPERADOR: FIM,      # qualquer outro caractere encerra o token
        CATEGORIA_PAREN:    FIM,
        CATEGORIA_ESPACO:   FIM,
        CATEGORIA_OUTRO:    FIM,
    },

    # Em LENDO_NUM continuamos enquanto for dígito
    LENDO_NUM: {
        CATEGORIA_LETRA:    ERRO,     # letra após número é inválido ex: 10x
        CATEGORIA_DIGITO:   LENDO_NUM,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN:    FIM,
        CATEGORIA_ESPACO:   FIM,
        CATEGORIA_OUTRO:    FIM,
    },

    # Operadores são sempre um único caractere → qualquer coisa encerra
    LENDO_OPERADOR: {
        CATEGORIA_LETRA:    FIM,
        CATEGORIA_DIGITO:   FIM,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN:    FIM,
        CATEGORIA_ESPACO:   FIM,
        CATEGORIA_OUTRO:    FIM,
    },

    # Parênteses também são sempre um único caractere
    LENDO_PAREN: {
        CATEGORIA_LETRA:    FIM,
        CATEGORIA_DIGITO:   FIM,
        CATEGORIA_OPERADOR: FIM,
        CATEGORIA_PAREN:    FIM,
        CATEGORIA_ESPACO:   FIM,
        CATEGORIA_OUTRO:    FIM,
    },
}


def classificar_caractere(caractere):
    # Mapeia o caractere real para uma categoria do alfabeto Σ
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
    # Consulta a tabela δ e retorna o próximo estado
    categoria = classificar_caractere(caractere_atual)
    transicoes_do_estado = tabela_de_transicao.get(estado_atual, {})
    proximo_estado = transicoes_do_estado.get(categoria, ERRO)
    return proximo_estado