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

Potential exercises:
- Implement lexing
  - keyword
  - operator
  - variable
  - floating point number
- Regexes

## Part 3: Parsing

Potential exercises:
- Implement Pratt parsing (operator precedence)

## Part 4: AST evaluator

## Part 5: Bytecode

## Part 6: Optimization

## Part 7: To infinity and beyond

