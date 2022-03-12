# hack-a-lang 0001

This tutorial will give you a taste of what its like to implement your own
programming language from scratch. It is based of the book "Crafting
Interpreters" by Bob Nystrom. We will be working on a subset of the Lox
programming language. The tutorial is structured as a series of exercises. We
won't be developing everything from scratch. Rather, we'll be filling in some
of the more important parts of the implementation. We decided to go this route
to save time and ignore some of the more ceremonius details.

## Getting started

You will need Python >= 3.6 installed.

1. Clone the repository

```
git clone https://github.com/dependently-typed/hack-a-lang.git
cd hack-a-lang
```

2. Checkout the `0001` branch

```
git checkout -b 0001
```

## Directory Layout

```
|_ soln/        # reference implementation
|_ lox/         # this is where you'll be working on your implementation
|_ tools/       # build tooling
|_ README.md    # the tutorial you are currently reading
```

## Part 1: Getting to know Lox

Before we try to complete an implementation of Lox in the `lox/` folder, we
must learn about Lox itself. We will do this by writing some Lox code and
trying it out.

[Reading: Chapter 3 - The Lox Language](https://craftinginterpreters.com/the-lox-language.html)

### Exercises

1. Write a Lox program that computes the nth Fibonacci number.
2. Can you write a program to check if a string is a palindrome? What features did you use/are missing?

You can run your program by using the provided reference implementation of Lox.

```
python3 -m soln <file containing your program>
```

## Part 2: Lexing

The Lexer/Scanner takes the raw input stream of characters and tokenizes it.
This will help the parser establish the relationship between each token.
Basically we are going through the characters in a loop while classifying each
character/string by comparing it to our list of special tokens or categories through
a lot of conditional statements.


### Exercises

1. Implement the `scanTokens` function in `Scanner.py`
2. Implement the `identifier` function in `Scanner.py`

### Relevant files

```
Scanner.py      # The actual lexer that tokenizes the character source
Token.py        # The token class
TokenTypes.py   # The different types of special tokens
```

### Bonus

1. TODO

## Part 3: Parsing

The Parser takes the tokenized version of the source from the Lexer and then 
creates an Abstract Syntax Tree (AST) based on the grammar rules of the language.
There are different rules for expressions and statements, which are certain configurations
of tokens that come together to statements that can later be evaluated by the interpreter.

### Exercises

1. Implement the `block` function in `Parser.py`
2. Implement the `andOperator` and `comparison` function in `Parser.py`
3. Implement the `forStatement` function in `Parser.py`

### Relevant files

```
Parser.py     # The actual parser that takes the tokenized string and generates the AST
Expr.py       # The expression class for representing simple expressions
Stmt.py       # The statement class for representing compound statements
```

### Bonus

1. TODO
2. TODO

## Part 4: AST evaluator

The AST evaluator/Interpreter takes the generated AST and performs all of the actions needed
in the code from evaluating arithmetic expressions to recursive function calls. The Interpreter
has to deal with evaluating expressions and statements, executing bits of code, and managing the
changing states of the environment. 

### Exercises

1. Implement the `get` function in `Environment.py`
2. Implement the `executeBlock` function in `Interpreter.py`
3. Implement the `visitIf` and `visitWhile` function in `Interpreter.py`

### Relevant files

```
Interpreter.py      # The intepreter that will execute the parsed code
Environment.py      # The environment at runtime, handles defined variables and more
LoxCallable.py      # Originally and interface for LoxFunction
LoxFunction.py      # File needed for handling environment changes
RuntimeError.py     # Custom RuntimeError class
Return.py           # Custom Return class
```

### Bonus

1. Remove our implementation of functions and try to implement them yourself.
2. We omitted implementing the OOP features of Lox. Take a shot at that. You
   can find more details in the Crafting Interpreters book.

## Interlude

This concludes the parts you'll be implementing during the workshop. The
remaining sections are long-form and will take a fair bit of time to implement.
We're providing this so that you can apply the concepts we talked about on your
own after hack-a-lang. Feel free to use the dependently-typed Discord to ask
questions.

## Part 5: Bytecode

### Exercises

In this series of exercises we will add bytecode interpreter support for Lox.

1. First, we need to learn about the Lox bytecode instructions. This will take some time to get through. You'll need to skim chapters 14 to 25 of the Crafting Interpreters book. Remember to carefully observe the purpose of each instruction.
2. Encode the bytecode instructions in Python. You can do this any way you prefer (using classes, enums, dictionaries, tuples). For the full set of instructions you need to look at https://github.com/munificent/craftinginterpreters/blob/master/c/chunk.h
3. Write a function that takes an AST and outputs bytecode. Start small. You can do this by supporting only a subset of the AST. Only then move on to more complex nodes like functions and closures.
