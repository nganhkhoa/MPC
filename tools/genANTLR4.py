import os
import subprocess


ANTLR_JAR = os.environ.get('ANTLR_LIB')

if ANTLR_JAR is None:
    # fall back, not recommended
    ANTLR_JAR = '../external/antrl4.jar'

files_from_antlr4 = [
    'parser/MP.interp',
    'parser/MPLexer.interp',
    'parser/MPLexer.py',
    'parser/MPLexer.tokens',
    'parser/MPParser.py',
    'parser/MP.tokens',
    'parser/MPVisitor.py'
]


def generate():
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


def regenerate():
    for f in files_from_antlr4:
        os.remove(f)
    generate()
