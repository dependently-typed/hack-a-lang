import Lox
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
            '(': lambda c: TokenType.LEFT_PAREN,
            ')': lambda c: TokenType.RIGHT_PAREN,
            '{': lambda c: TokenType.LEFT_BRACE,
            '}': lambda c: TokenType.RIGHT_BRACE,
            ',': lambda c: TokenType.COMMA,
            '.': lambda c: TokenType.DOT,
            '-': lambda c: TokenType.MINUS,
            '+': lambda c: TokenType.PLUS,
            ';': lambda c: TokenType.SEMICOLON,
            '*': lambda c: TokenType.STAR,
            # Conditial Symbols in different contexnts
            '!': lambda c: TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG,
            '=': lambda c: TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL,
            '<': lambda c: TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS,
            '>': lambda c: TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER,
            # White Spaces
            ' ': lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
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

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

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
        elif c == "\n":
            self.advanceLine()
        elif c == "/":
            self.slash()
        elif c == "\"":
            self.string()
        else:
            Lox.error(self.line, "Unexpected character")

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peekNext().isdigit(self.peekNext()):
            self.advance()
            while self.isdigit(self.peek()):
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

    def slash(self):
        if self.match('/'):
            while (self.peek() != '\n') and not self.isAtEnd():
                self.advance()
        elif self.match('*'):
            while not self.isAtEnd():
                if self.match('\n'):
                    self.line += 1
                elif self.match('*') and self.match('/'):
                    break
                else:
                    self.advance()
        else:
            self.addToken(TokenType.SLASH)


    def string(self):
        while (self.peek() != '"') and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isAtEnd():
            Lox.error(self.line, "Unterminated string.")
            return None
        self.advance()
        value = self.source[self.start+1:self.current-1]
        self.addToken(TokenType.STRING, value)

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
        self.current += 1
        return True

    def matchNext(self, expected):
        if self.isAtEnd():
            return False
        elif self.source[self.current+1] != expected:
            return False
        self.current += 1
        return True

