// 1611617

grammar MP;

@lexer::header {
from parser.lexererr import *
}

options{
    language=Python3;
}

program
    : manydecl EOF
    ;

manydecl
    : decl manydecl
    | decl
    ;

decl
    : var_decl
    | func_decl
    | proc_decl
    ;

var_decl
    : VAR varlist
    ;

varlist
    : var SEMI varlist
    | var SEMI
    ;

var
    : idenlist COLON mptype
    ;

idenlist
    : IDENT COMMA idenlist
    | IDENT
    ;

mptype
    : primitive_type
    | compound_type
    ;

primitive_type
    : INTEGER
    | REAL
    | BOOLEAN
    | STRING
    ;

compound_type
    : ARRAY array_value OF primitive_type
    ;

array_value
    : LB MINUS? NUM_INT DOUBLE_DOT MINUS? NUM_INT RB
    ;

func_decl
    : FUNCTION IDENT LR param_list? RR COLON mptype SEMI var_decl* compound_statement
    ;

param_list
    : var SEMI param_list
    | var
    ;

proc_decl
    : PROCEDURE IDENT LR param_list? RR SEMI var_decl* compound_statement
    ;

expression
    : expression (AND THEN | OR ELSE) expression_lv1
    | expression_lv1
    ;

expression_lv1
    : expression_lv2 (EQUAL | NOT_EQUAL | LT | LE | GE | GT) expression_lv2
    | expression_lv2
    ;

expression_lv2
    : expression_lv2 (PLUS | MINUS | OR) expression_lv3
    | expression_lv3
    ;

expression_lv3
    : expression_lv3 (STAR | SLASH | DIV | MOD | AND) expression_lv4
    | expression_lv4
    ;

expression_lv4
    : (NOT | MINUS) expression_lv4
    | index_expression
    ;

index_expression
    : index_expression LB expression RB
    | factor
    ;

invocation_expression
    : LR call_param? RR
    ;

factor
    : LR expression RR
    | literal
    | IDENT
    | IDENT invocation_expression
    ;

statement
    : normal_statement SEMI
    | structured_statement
    ;

structured_statement
    : if_statement
    | for_statement
    | compound_statement
    | with_statement
    | while_statement
    ;

normal_statement
    : assignment_statement
    | break_statement
    | continue_statement
    | return_statement
    | call_statement
    ;

assignment_statement
    : assignment_lhs_list expression
    ;

assignment_lhs_list
    : lhs ASSIGN assignment_lhs_list
    | lhs ASSIGN
    ;

lhs
    : index_expression
    | IDENT
    ;

if_statement
    : IF expression THEN statement (ELSE statement)?
    ;

while_statement
    : WHILE expression DO statement
    ;

for_statement
    : FOR IDENT ASSIGN expression (TO | DOWNTO) expression DO statement
    ;

break_statement
    : BREAK
    ;

continue_statement
    : CONTINUE
    ;

return_statement
    : RETURN expression?
    ;

compound_statement
    : BEGIN statement* END
    ;

with_statement
    : WITH varlist DO statement
    ;

call_statement
    : IDENT LR call_param? RR
    ;

call_param
    : expression COMMA call_param
    | expression
    ;

empty
    :
    ;

fragment A
    : ('A' | 'a')
    ;

fragment B
    : ('B' | 'b')
    ;

fragment C
    : ('C' | 'c')
    ;

fragment D
    : ('D' | 'd')
    ;

fragment E
    : ('E' | 'e')
    ;

fragment F
    : ('F' | 'f')
    ;

fragment G
    : ('G' | 'g')
    ;

fragment H
    : ('H' | 'h')
    ;

fragment I
    : ('I' | 'i')
    ;

fragment J
    : ('J' | 'j')
    ;

fragment K
    : ('K' | 'k')
    ;

fragment L
    : ('L' | 'l')
    ;

fragment M
    : ('M' | 'm')
    ;

fragment N
    : ('N' | 'n')
    ;

fragment O
    : ('O' | 'o')
    ;

fragment P
    : ('P' | 'p')
    ;

fragment Q
    : ('Q' | 'q')
    ;

fragment R
    : ('R' | 'r')
    ;

fragment S
    : ('S' | 's')
    ;

fragment T
    : ('T' | 't')
    ;

fragment U
    : ('U' | 'u')
    ;

fragment V
    : ('V' | 'v')
    ;

fragment W
    : ('W' | 'w')
    ;

fragment X
    : ('X' | 'x')
    ;

fragment Y
    : ('Y' | 'y')
    ;

fragment Z
    : ('Z' | 'z')
    ;

literal
    : number
    | BOOL_LIT
    | STRING_LITERAL
    ;

STRING_LITERAL
    : UNCLOSE_STRING '"'
    {self.text = self.text[1:-1]}
    ;

UNCLOSE_STRING
    : '"' ('\\' [btrnf\\'"] | ~[\b\t\r\n\f\\'"])*
    {raise UncloseString(self.text[1:])}
    ;

ILLEGAL_ESCAPE
    : UNCLOSE_STRING '\\' ~[btnfr"'\\]
    {raise IllegalEscape(self.text[1:])}
    ;

fragment ESCAPE_STRING
    : '\\b'
    | '\\f'
    | '\\r'
    | '\\n'
    | '\\t'
    | '\\\''
    | '\\"'
    | '\\\\'
    ;

number
    : NUM_INT
    | NUM_REAL
    ;

NUM_INT
    : [0-9]+
    ;

NUM_REAL
    : [0-9]+ '.' [0-9]* EXPONENT?
    | '.' [0-9]+ EXPONENT?
    | [0-9]+ EXPONENT
    ;

BOOL_LIT
    : TRUE
    | FALSE
    ;

fragment EXPONENT
    : ('e' | 'E') '-'? ('0' .. '9')+
    ;


LCURLY
   : '{'
   ;

RCURLY
   : '}'
   ;

LR
    : '('
    ;

RR
    : ')'
    ;

LB
    : '['
    ;

RB
    : ']'
    ;

SEMI
    : ';'
    ;

DOUBLE_DOT
    : '..'
    ;

COMMA
    : ','
    ;

COLON
    : ':'
    ;

BREAK
    : B R E A K
    ;

CONTINUE
    : C O N T I N U E
    ;

FOR
    : F O R
    ;

TO
    : T O
    ;

DOWNTO
    : D O W N T O
    ;

DO
    : D O
    ;

IF
    : I F
    ;

THEN
    : T H E N
    ;

ELSE
    : E L S E
    ;

RETURN
    : R E T U R N
    ;

WHILE
    : W H I L E
    ;

BEGIN
    : B E G I N
    ;

END
    : E N D
    ;

FUNCTION
    : F U N C T I O N
    ;

PROCEDURE
    : P R O C E D U R E
    ;

VAR
    : V A R
    ;

TRUE
    : T R U E
    ;

FALSE
    : F A L S E
    ;

ARRAY
    : A R R A Y
    ;

OF
    : O F
    ;

REAL
    : R E A L
    ;

BOOLEAN
    : B O O L E A N
    ;

INTEGER
    : I N T E G E R
    ;

STRING
    : S T R I N G
    ;

NOT
    : N O T
    ;

AND
    : A N D
    ;

OR
    : O R
    ;

DIV
    : D I V
    ;

MOD
    : M O D
    ;

WITH
    : W I T H
    ;

PLUS
    : '+'
    ;

MINUS
    : '-'
    ;

STAR
    : '*'
    ;

SLASH
    : '/'
    ;

EQUAL
    : '='
    ;

NOT_EQUAL
    : '<>'
    ;

LT
    : '<'
    ;

LE
    : '<='
    ;

GE
    : '>='
    ;

GT
    : '>'
    ;

ASSIGN
    : ':='
    ;

IDENT
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

COMMENT_3
    : '//' .*? '\r'* '\n'+ -> skip
    ;

WS
    : [ \t\r\n] -> skip
    ; // skip spaces, tabs

COMMENT_1
    : '(*' .*? '*)' -> skip
    ;

COMMENT_2
    : '{' .*? '}' -> skip
    ;

ERROR_CHAR
    : .
    {raise ErrorToken(self.text)}
    ;
