import sys
import os
import subprocess

from antlr4 import FileStream, CommonTokenStream  # Token
from antlr4.error.ErrorListener import ConsoleErrorListener  # ErrorListener

try:
    from parser.MPLexer import MPLexer as Lexer
    from parser.MPParser import MPParser as Parser
    from astgen.ASTGeneration import ASTGeneration
    from checker.StaticCheck import StaticChecker
    from codegen.CodeGenerator import CodeGenerator
except ModuleNotFoundError:
    print('Generate ANTLR4 first')
    print('python genANTLR4.py')
    exit(1)


ANTLR_JAR = os.environ.get('ANTLR_LIB')
JASMIN_JAR = './external/jasmin.jar'

if ANTLR_JAR is None:
    # fall back, not recommended
    ANTLR_JAR = './external/antrl4.jar'


class SyntaxException(Exception):
    def __init__(self, msg):
        self.message = msg


class NewErrorListener(ConsoleErrorListener):
    INSTANCE = None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxException(
            "Error on line " +
            str(line) +
            " col " +
            str(column) +
            ": " +
            offendingSymbol.text)


def compile(inputfile):
    lexer = Lexer(FileStream(inputfile))
    tokens = CommonTokenStream(lexer)
    try:
        # listener = TestParser.createErrorListener()
        listener = NewErrorListener().INSTANCE
        parser = Parser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(listener)
        tree = parser.program()
    except SyntaxException as f:
        msg = f.message.split(':')[0].split(' ')
        line = int(msg[3])
        col = int(msg[5])
        error_line = open(inputfile).read()
        error_line = error_line.split('\n')[line - 1]
        print(error_line)
        print('~' * (col) + '^')
        print(f.message)
        raise f
    asttree = ASTGeneration().visit(tree)

    checker = StaticChecker(asttree)
    checker.check()

    path = os.path.dirname(inputfile)
    filename = os.path.basename(inputfile).split('.')[0]
    codeGen = CodeGenerator()
    codeGen.gen(asttree, path, filename)

    subprocess.call(
        # "java  -jar " + JASMIN_JAR + " " + path + "/MPClass.j",
        "java -jar {} {}/{}.j -d {}".format(JASMIN_JAR, path, filename, path),
        shell=True,
        stderr=subprocess.STDOUT
    )

    with open('{}/io.class'.format(path), 'wb') as iofile:
        iofile.write(open('libs/io.class', 'rb').read())

    subprocess.call(
        # 'jar cvfm {}/{}.jar {}/manifest.mf {} {}.class'.format(
        'jar cvfe {0}.jar {0} io.class {0}.class'.format(
            filename
        ),
        cwd=path,
        shell=True,
        stderr=subprocess.STDOUT
    )

    os.remove('{}/{}.j'.format(path, filename))
    os.remove('{}/{}.class'.format(path, filename))
    os.remove('{}/io.class'.format(path))


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        exit(1)

    try:
        print("Compiling {}".format(os.path.relpath(argv[1])))
        compile(argv[1])
    except BaseException as e:
        print(e)
        exit(1)
    print("Compiled successfully")
