from TokenType import TokenType
from Token import Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        
        # Dictionary of characters and lambdas that return a single character token
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
        
    """
    Main loop for scanner. Loop and call scanToken() until you reach the end of file.
    Note:
        - Don't implement the whole scanning logic here. Implement scanToken() first 
          and call that in the loop.
        - This function should return self.tokens
        - Try to think of what the variables start and current 
        - Make sure to add end of file (EOF) token before you return self.tokens
    """
    def scanTokens(self):
        # Your code goes here! Change the return to appropriate value
        return None
     
    """
    Scanner function responsible for one token
    Note: 
        - Use advance() to get the current character. Go ahead and implement advance() 
        - Case 1: Check if the current character is a single character token, defined in 
          self.tokenStrings.
          
        ** For below cases, try to think what the first character should be to match the token **
        - Case 2: tokenize numbers          -> number()
        - Case 3: tokenize identifers       -> identifier()
        - Case 4: tokenize newlines         -> advanceLine()
        - Case 5: tokenize slashes          -> slash()
        - Case 6: tokenize strings literals -> string()
    """
    def scanToken(self):
         # Your code goes here! Change the return to appropriate value
        return None
    
    """
    Parse a number from source input
    Notes:
        - Note both int and floats are numbers
        - Note that you have these helper functions! 
            - peek(), peekNext(), addToken(), advance():        Instance functions
            - c.isDigit():      Python built-in function
    """
    def number(self):
         # Your code goes here! Change the return to appropriate value
        return None
    """
    Parse an identifer, aka variables
    Notes:
        - Make sure to check if the variables are keywords!
        - If it is a keyword, you should add keywords to tokens, not identifiers
        - Useful functions
            - Instance functions:   peek(), addToken(), advance()
            - Python built-in:      isalnum()
    """
    def identifier(self):
         # Your code goes here! Change the return to appropriate value
        return None

    
    """
    Slash is special because both division and comments use / as the first char
    Notes: 
        - Comments aren't tokens, so just increment pointers without adding to tokens
        - BONUS! Try if you can add block comments! (e.g. /* \n */)
        - Make sure to add the slash token if it's not a comment
    """
    def slash(self):
         # Your code goes here! Change the return to appropriate value
        return None

    """
    Parse string literals, which are wrapped around quotes
    Notes:
        - Lox allows multiline string literals that are wrapped around quotes ("")
        - Make sure to increment line instance variable if the string has a newline
        - No need for explicit error handling, but think about how you should handle 
          unterminated strings
    """
    def string(self):
        # Your code goes here! Change the return to appropriate value
        return None

    """
    Return the next character without incrementing self.current
    Notes: 
        - note that self.current could have already been incremented by advance()
          so it might not be necessary to increment here (depending on ur implementation)
        - It's a good idea to check if the next char is the end of file
    """
    def peek(self):
        # Your code goes here! Change the return to appropriate value
        return None

    """
    peek() on steroids, it returns the next, next character
    Notes: 
        - Also check for EOF!
    """
    def peekNext(self):
        # Your code goes here! Change the return to appropriate value
        return None

    """
    Check if current is at the end of the source string
    Notes: 
        - None
    """
    def isAtEnd(self):
        # Your code goes here! Change the return to appropriate value
        return None

    """
    Increment current and return character at current - 1
    Notes: 
        - None
    """
    def advance(self):
        # Your code goes here! Change the return to appropriate value
        return None

    
    """
    Increment self.line(). This is useful for error handling but we will not
    cover that due to time constraint. You should still implement this because
    Token constructors expect linenumbers
    Notes: 
        - None
    """
    def advanceLine(self):
        # Your code goes here! Change the return to appropriate value
        return None

    """
    Add the token to self.tokens list
    Notes: 
        - Use the pointers (start, current) to get token substring
        - Check Token.py to see what args Token constructor takes
    """
    def addToken(self, tokenType, literal=None):
        # Your code goes here! Change the return to appropriate value
        return None

    """
    Check if the next character matches the expected character
    Notes:
        - match() should increment the current pointer
        - As usual, think of what you should do when current is at the end of the file
    """
    def match(self, expected):
        # Your code goes here! Change the return to appropriate value
        return None
    
    """
    match() on steroids. Return true if the next, next character is the expected character
    Notes:
        - matchNext() should increment the current pointer
    """
    def matchNext(self, expected):
        # Your code goes here! Change the return to appropriate value
        return None
