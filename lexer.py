import ply.lex as lex

tokens = (
'ID',
'SEMICOLON',
'COLON',
'LBRACKET',
'RBRACKET',
'LSQBRACKET',
'RSQBRACKET',
'LPAREN',
'RPAREN',
'COMMA',
'DOT',
'AND',
'OR',
'NOT',
'LTHAN',
'GTHAN',
'EQUAL',
'DIFFERENT',
'ADD',
'SUB',
'MUL',
'DIV',
'CONST_FLOAT',
'CONST_INT',
'CONST_TEXT'
)

# General use reserved words
reserved = {
    'routine': 'ROUTINE',
    'int': 'INT',
    'float': 'FLOAT',
    'proc': 'PROC',
    'begin': 'BEGIN',
    'repeat': 'REPEAT',
    'if': 'IF',
    'else': 'ELSE',
    'void': 'VOID'
}

# Special reserved words
special_reserved = {
    'mean': 'MEAN',
    'median': 'MEDIAN',
    'mode': 'MODE',
    'std': 'STD',
    'kurt': 'KURT',
    'plot': 'PLOT',
    'dplot': 'DPLOT',
    'var': 'VAR',
    'sim': 'SIM',
    'corr': 'CORR',
    'df': 'DF',
    'dfread': 'DFREAD',
    '~(_8^(I)': '~(_8^(I)',
    '###( 8^ |)': '###( 8^ |)'
}

tokens += list(reserved.values()) + list(special_reserved.values())

t_ID = r'[A-Za-z_][A-Za-z0-9_]*'
t_SEMICOLON = r';'
t_COLON = r':'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_LTHAN = r'\<'
t_GTHAN = r'\>'
t_EQUAL = r'=='
t_DIFFERENT = r'\<\>'
t_ADD = r'\+'
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_CONST_FLOAT = r'\d*\.\d+'
t_CONST_INT = r'\d+'
t_CONST_TEXT = r'\"(\"\"|[^\"$])*\"'

t_ignore = ' \t'

lexer = lex.lex()