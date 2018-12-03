# MP Compiler

From my Principle of Programming Languages assignment, I have created a compiler for the MP language. The assignment phase is divided to 4 phases, from doing Lexer, Parser, AST generation to Static Checker and Jasmin Code generation.

The assignment code structure is quite ugle, so I re-organized the code, adding some more steps to make the code look nicer and compile a \*.mp file to a jar file.

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


## Notes

Because I was having serious deadlines at the end of the semester, I drop on working on ArrayCell, which will be added later.

Because the lexer and parser are given by the famous `ANTLR4` engine, there should exists a path to antlr4.jar on the environment variable `ANTLR_LIB` or else, the program will use the antlr4 file in the external folder.

Before running `mpc.py`, you must be sure that you have generate neccessary files from ANTLR4.
```shell
python genANTRL4.py
```
