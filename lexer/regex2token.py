from lexer.token.token_type import TokenType
import re


def compile_regex2token():
    regex2token_compiled = {}
    for regex in regex2token:
        regex_compiled = re.compile(regex)
        regex2token_compiled[regex_compiled] = regex2token[regex]
    return regex2token_compiled


regex2token = {
    r'\n': TokenType.T_IGNORE,
    r'[ \t]+': TokenType.T_IGNORE,
    r'double(?![\w\d])': TokenType.T_DOUBLE,
    r'int(?![\w\d])': TokenType.T_INT,
    r'char(?![\w\d])': TokenType.T_CHAR,
    r'bool(?![\w\d])': TokenType.T_BOOL,
    r'string(?![\w\d])': TokenType.T_STRING,
    r'if(?![\w\d])': TokenType.T_IF,
    r'else(?![\w\d])': TokenType.T_ELSE,
    r'true(?![\w\d])': TokenType.T_TRUE,
    r'false(?![\w\d])': TokenType.T_FALSE,
    r'function(?![\w\d])': TokenType.T_FUNCTION,
    r'void(?![\w\d])': TokenType.T_VOID,
    r'return(?![\w\d])': TokenType.T_RETURN,
    r'phys(?![\w\d])': TokenType.T_PHYS,
    r'unit(?![\w\d])': TokenType.T_UNIT,
    r'while(?![\w\d])': TokenType.T_WHILE,
    r'or(?![\w\d])': TokenType.T_OR,
    r'and(?![\w\d])': TokenType.T_AND,
    r'not(?![\w\d])': TokenType.T_NOT,
    r'->': TokenType.T_ARROW,
    r',': TokenType.T_COMMA,
    r'\{': TokenType.T_LBRACKET,
    r'\}': TokenType.T_RBRACKET,
    r'\.': TokenType.T_DOT,
    r'==': TokenType.T_EQ,
    r'=': TokenType.T_ASSIGN,
    r'\(': TokenType.T_LPARENT,
    r'\)': TokenType.T_RPARENT,
    r';': TokenType.T_SEMICOLON,
    r'\:': TokenType.T_COLON,
    r'\+': TokenType.T_PLUS,
    r'-': TokenType.T_MINUS,
    r'\*': TokenType.T_MUL,
    r'/': TokenType.T_DIV,
    r'<=': TokenType.T_LESS_OR_EQ,
    r'>=': TokenType.T_GREATER_OR_EQ,
    r'<': TokenType.T_LESS,
    r'>': TokenType.T_GREATER,
    r'!=': TokenType.T_NOT_EQ,
    r'DONE': TokenType.T_EOT,
    # Changed 'unit' structure from initial documentation. Now it looks like |n/s*s|
    r'\|((([A-Za-z]*\*)*[A-Za-z]+)|[A-Za-z]*)\/((([A-Za-z]*\*)*[A-Za-z]+)|[A-Za-z]*)\|': TokenType.VT_UNIT,
    # VT_PHYS will be implemented in the Parser part.
    r'\d+\.\d+(?![\w])': TokenType.VT_DOUBLE,
    r'(0|[1-9]\d*)(?![\w])': TokenType.VT_INT,
    r'\'.\'(?![\w\d])': TokenType.VT_CHAR,
    r'\".*\"(?![\w\d])': TokenType.VT_STRING,
    r'[a-zA-Z_][a-zA-Z0-9_]*': TokenType.VT_ID
}
