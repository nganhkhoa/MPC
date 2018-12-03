import os
import subprocess


ANTLR_JAR = os.environ.get('ANTLR_LIB')
JASMIN_JAR = './external/jasmin.jar'

if ANTLR_JAR is None:
    # fall back, not recommended
    ANTLR_JAR = './external/antrl4.jar'


def generate():
    files_from_antlr4 = [
        'MP.interp',
        'MPLexer.interp',
        'MPLexer.py',
        'MPLexer.tokens',
        'MPParser.py',
        'MP.tokens',
        'MPVisitor.py'
    ]
    if all(list(map(os.path.isfile, files_from_antlr4))):
        return
    gen_antlr_class_cmd = [
        "java",
        "-jar",
        ANTLR_JAR,
        "-no-listener",
        "-visitor",
        "parser/MP.g4"
    ]
    subprocess.run(gen_antlr_class_cmd)


if __name__ == '__main__':
    generate()
