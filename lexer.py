import ply.lex as lex

tokens = [
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
    'ASSIGN',
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
]

reserved = {
    # General use reserved words
    'routine': 'ROUTINE',
    'globals': 'GLOBALS',
    'locals': 'LOCALS',
    'var': 'VAR',
    'procedures': 'PROCEDURES',
    'instructions': 'INSTRUCTIONS',
    'int': 'INT',
    'float': 'FLOAT',
    'write': 'WRITE',
    'read': 'READ',
    'proc': 'PROC',
    'begin': 'BEGIN',
    'repeat': 'REPEAT',
    'if': 'IF',
    'else': 'ELSE',
    'void': 'VOID',
    'return': 'RETURN',
    'and': 'AND',
    'or': 'OR',

    # Special reserved words
    'df': 'DF',
    'mean': 'MEAN',
    'median': 'MEDIAN',
    'mode': 'MODE',
    'std': 'STD',
    'kurtosis': 'KURTOSIS',
    'plot': 'PLOT',
    'dplot': 'DPLOT',
    'variance': 'VARIANCE',
    'simmetry': 'SIMMETRY',
    'correlation': 'CORRELATION',
    'dfread': 'DFREAD',
    '~(_8^(I)': 'HOMERO',
    '###(_8^ |)': 'MARGE'
}

tokens += list(reserved.values())

t_SEMICOLON = r';'
t_COLON = r':'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_ASSIGN = r'='
t_LTHAN = r'\<'
t_GTHAN = r'\>'
t_EQUAL = r'=='
t_DIFFERENT = r'\<\>'
t_ADD = r'\+'
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_CONST_FLOAT = r'-?\d*\.\d+'
t_CONST_INT = r'-?\d+'
t_CONST_TEXT = r'\"(\"\"|[^\"$])*\"'

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.skip(1)


lexer = lex.lex()
