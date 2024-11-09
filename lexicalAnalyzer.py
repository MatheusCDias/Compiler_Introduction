import re

# Analisador Léxico

keywords = ['if', 'else', 'while', 'return'] # Palavras chave
operadores = ['+', '-', '*', '/', '=', '=='] # Operadores

# Função para identificar tokens (lexemas)
def chk_tokens(codigo):
    tokens = [] # Lista de tokens encontrados
    padroes_tokens = [
        ('NUM', r'\d+(\.\d*)?'), # Números
        ('ID', r'[A-Za-z]+'), # Variáveis
        ('OP', r'[+\-*/=]==?'), # Operadores
        ('SKIP', r'[ \t]+'), # Espaços em branco ou \t
        ('MISMATCH', r'.') # Caracteres perdidos (não identificados)
    ]
    
    # Gera a string com a expressão regular completa
    token_regex = '|' .join('(?P<%s>%s)' % par for par in padroes_tokens)
    
    # Vai buscar por todos os padrões encontrados no código e fazer uma iteração
    for iterador in re.finditer(token_regex, codigo):
        tipo = iterador.lastgroup
        valor = iterador.group()
        if tipo == 'NUM' or tipo == 'ID' or tipo == 'OP':
            tokens.append([tipo, valor])
        elif tipo == 'SKIP':
            continue
        else:
            raise RuntimeError(f'Caracter inexperado: {valor}')
    
    return tokens

def verifica_se_eh_numero(texto):
    padrao = re.compile(r'\d+(\.\d*)?')
    # \d: tipo de máscara que representa um dígito
    if padrao.search(texto):
        return True
    else:
        return False

print(verifica_se_eh_numero('O valor é 100.23'))

# Para casa: Estudar expressões regulares com Python
# Abrir o arquivo de códigos
def lerCodigo():
    with open ('codigo.txt', 'r') as arquivo:
        codigo = arquivo.read()


codigo = lerCodigo()

chk_tokens(codigo)