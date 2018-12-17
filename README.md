# MP Compiler

From my Principle of Programming Languages assignment, I have created a compiler for the MP language. The assignment is divided to 4 phases, from Lexer and Parser, to AST generation to Static Checker and Jasmin Code generation.

The assignment code structure is quite ugly, so I re-organized the code, adding some more steps to make the code look nicer and compile a `*.mp` file to a `jar` file.

Given the mp file as follows:

```mp
// hello.mp
procedure main();
begin
    putString("Hello World");
end
```

Compile and run the file by issuing these commands:

```shell
python mpc.py hello.mp
java -jar hello.jar
```

More documentation is being built.


## Project Structure
```
.
├── mpc.py
├── tests
├── astgen
│   ├── ASTGeneration.py
│   ├── __init__.py
├── checker
│   ├── __init__.py
│   ├── StaticCheck.py
│   └── StaticError.py
├── codegen
│   ├── CodeGenerator.py
│   ├── CodeGenError.py
│   ├── Emitter.py
│   ├── Frame.py
│   ├── __init__.py
│   ├── MachineCode.py
├── external
│   ├── antrl4.jar
│   └── jasmin.jar
├── libs
│   ├── io.class
│   └── io.java
├── MP_specifications
│   ├── assignment1.pdf
│   ├── assignment2.pdf
│   ├── assignment3.pdf
│   ├── assignment4.pdf
│   └── MP.pdf
├── parser
│   ├── __init__.py
│   ├── lexererr.py
│   ├── MP.g4
│   ├── MP.interp
│   ├── MPLexer.interp
│   ├── MPLexer.py
│   ├── MPLexer.tokens
│   ├── MPParser.py
│   ├── MP.tokens
│   ├── MPVisitor.py
├── tools
│   ├── genANTLR4.py
│   ├── __init__.py
└── utils
    ├── AST.py
    ├── __init__.py
    ├── Utils.py
    └── Visitor.py
```
All files is categorized and put into their own folder, turning them to a module by using `__init__.py` and import them by using the syntax `from package.module import module`. This makes the code easier to read, easier to find code, rather than altering the system path. The files in parser are created by running antlr4 generator from the given `MP.g4` file. Import this module is a little hard, but an exception can be catch upon importing the module to generate the neccessary files and import the module afterward.

Most of the code is of my own teacher, Nguyen Hua Phung, I have no plan to refactor all this code as the architecture is just right. So all rights go to my teacher. The only thing I do is refactor part of the code and implement the algorithm.

Test folder is currently in manual testing. There will be a unit test to test functions in the future, maybe.


## Development

### TODO

+ Finish Array in CodeGen
+ Add unit test frame
+ Add magic???

### Magic

The specification for this language is a one-file compile, but I want to make it able to work in multiple files, maybe in so-far future I will try to make this possible. Also, why not make a language highlighter for this language?

