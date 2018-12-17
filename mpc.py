import os
import subprocess
import click

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ConsoleErrorListener

from tools.genANTLR4 import generate, regenerate

try:
    # dynamic loading of ANTLR4 files
    from parser import MPLexer, MPParser  # type: ignore
except ImportError:
    generate()
    from parser import MPLexer, MPParser   # type: ignore

from astgen.ASTGeneration import ASTGeneration
from checker.StaticCheck import StaticChecker
from codegen.CodeGenerator import CodeGenerator

Lexer = MPLexer.MPLexer         # load from module
Parser = MPParser.MPParser      # load from module

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


def compile(inputfile, output):
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

    path = output
    filename = os.path.basename(inputfile).split('.')[0]
    jasmin_file = '{}/{}.j'.format(path, filename)
    codeGen = CodeGenerator()
    codeGen.gen(asttree, path, filename)

    subprocess.call(
        "java -jar {} {} -d {}".format(JASMIN_JAR, jasmin_file, path),
        shell=True,
        stderr=subprocess.STDOUT
    )

    with open('{}/io.class'.format(path), 'wb') as iofile:
        iofile.write(open('libs/io.class', 'rb').read())

    subprocess.call(
        'jar cvfe {0}.jar {0} io.class {0}.class'.format(
            filename
        ),
        cwd=path,
        shell=True,
        stderr=subprocess.STDOUT
    )

    os.remove(jasmin_file)
    os.remove('{}/{}.class'.format(path, filename))
    os.remove('{}/io.class'.format(path))


@click.command()
@click.argument('file')
@click.option(
    '--output', default='',
    help='Where the jar file will be after compile')
@click.option(
    '--regen', is_flag=True,
    help='Regenerate antlr4 files and exit'
)
def main(file, output, regen):
    if regen:
        regenerate()
        print("ANTLR4 files regenerate succesfully")
        return

    if output == '':
        output = os.path.dirname(file)
    else:
        # check if directory, create

        # if file path, then
        pass

    print("Compiling {}".format(os.path.relpath(file)))
    try:
        compile(file, output)
    except BaseException as e:
        print(e)
        exit(1)
    print("Compiled successfully")


if __name__ == "__main__":
    main()
