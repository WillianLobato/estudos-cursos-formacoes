"""
2. Noções básicas de Python
1 2 3 4 5 6 7 8
Tipos de dados básicos
Em Python, os tipos de dados básicos são as categorias nas quais podemos classificar os valores que utilizamos em nossos programas. Compreender os diferentes tipos de dados é fundamental para trabalhar com variáveis e realizar operações em Python. Os tipos de dados básicos incluem:

Inteiros (int)
Os números inteiros são aqueles que não têm parte decimal. Em Python, são representados simplesmente escrevendo o número sem aspas nem pontos decimais. Por exemplo:
"""

idade = 25
quantidade = 100


"""
Flutuantes (float)
Os números flutuantes, também conhecidos como números de ponto flutuante, são aqueles que têm uma parte decimal. Em Python, são representados utilizando um ponto para separar a parte inteira da parte decimal. Por exemplo:
"""
preço = 9.99
altura = 1.75

"""
Cadeias de texto (strings)
As cadeias de texto, ou simplesmente cadeias, são sequências de caracteres encerradas entre aspas simples ('...') ou duplas ("..."). São utilizadas para representar texto em Python. Por exemplo:
"""
nome = "Juan"
mensagem = "¡Hola, mundo!"

"""
Você pode incluir caracteres especiais nas cadeias utilizando o caractere de escape \. Por exemplo, para incluir aspas dentro de uma cadeia, você pode usar \' ou \". Também pode utilizar a notação de tripla aspa para criar cadeias de várias linhas.

Booleanos
Os valores booleanos representam os valores de verdade: True (verdadeiro) e False (falso). São comumente utilizados em expressões condicionais e operações lógicas. Por exemplo:
"""
é_maior_de_idade = True
tem_desconto = False


'''
Regras para nomear variáveis
Ao nomear variáveis em Python, é importante seguir algumas regras para manter um código legível e evitar erros:

Os nomes das variáveis só podem conter letras (a-z, A-Z), números (0-9) e sublinhados (_). Não podem começar com um número.

O Python diferencia maiúsculas de minúsculas, então nome e Nome são variáveis diferentes.

Não se pode usar palavras-chave reservadas do Python como nomes de variáveis (por exemplo, if, else, for, while, etc.).

Recomenda-se usar nomes descritivos para as variáveis, que indiquem claramente seu propósito: nome, idade, total_vendas, etc.

Seguindo essas regras, alguns exemplos de nomes de variáveis válidos são:
'''
idade = 10
nome_completo = 10
total_vendas = 10
_contador = 10

'''E alguns exemplos de nomes de variáveis inválidos são:'''

1idade   # Começa com um número
nome-completo   # Usa um hífen em vez de um sublinhado
if   # Palavra-chave reservada do Python

'''
Tenha em mente
Escolher nomes descritivos para suas variáveis facilita a leitura e compreensão do código, tanto para você quanto para outros desenvolvedores que possam trabalhar no mesmo projeto.
'''
