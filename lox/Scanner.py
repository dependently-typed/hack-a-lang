from TokenType import TokenType
from Token import Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokenStrings = {
            # Paranthesis and Symbols
            '(': lambda f: TokenType.LEFT_PAREN,
            ')': lambda f: TokenType.RIGHT_PAREN,
            '{': lambda f: TokenType.LEFT_BRACE,
            '}': lambda f: TokenType.RIGHT_BRACE,
            ',': lambda f: TokenType.COMMA,
            '.': lambda f: TokenType.DOT,
            '-': lambda f: TokenType.MINUS,
            '+': lambda f: TokenType.PLUS,
            ';': lambda f: TokenType.SEMICOLON,
            '*': lambda f: TokenType.STAR,
            # We need lambda for these statements since they work as switch cases
            '!': lambda f: TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG,
            '=': lambda f: TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL,
            '<': lambda f: TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS,
            '>': lambda f: TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER,
            # White Spaces
            ' ': lambda f: None,
            '\r': lambda f: None,
            '\t': lambda f: None,
            # New Line
            '\n': lambda f: self.advanceLine(),
        }
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }

    def scanToken(self):
        c = self.advance()
        if c in self.tokenStrings:
            c = self.tokenStrings[c](c)
            if c is not None:
                self.addToken(c)
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == "-":
            self.identifier()

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peekNext().isdigit(self.peekNext()):
            self.advance()
            while self.isdigit(self._peek()):
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        text = self.source[self.start:self.current]
        if text not in self.keywords:
            self.addToken(TokenType.IDENTIFIER)
        else:
            self.addToken(self.keywords[text])

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if (self.current + 1) >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def isAtEnd(self):
        return (self.current >= len(self.source))

    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def advanceLine(self):
        self.line += 1

    def addToken(self, tokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))


    def match(self, expected):
        if self.isAtEnd():
            return False
        elif self.source[self.current] != expected:
            return False
        else:
            self.current += 1
            return True

