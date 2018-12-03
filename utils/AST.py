from abc import ABC, abstractmethod, ABCMeta
# from Visitor import Visitor

# cheated = True
cheated = False


class AST(ABC):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @abstractmethod
    def accept(self, v, param):
        return v.visit(self, param)


class Type(AST):
    __metaclass__ = ABCMeta
    pass


class IntType(Type):
    global cheated

    def __str__(self):
        if not cheated:
            return "IntType"
        else:
            return "IntType()"

    def accept(self, v, param):
        return v.visitIntType(self, param)


class FloatType(Type):
    global cheated

    def __str__(self):
        if not cheated:
            return "FloatType"
        else:
            return "FloatType()"

    def accept(self, v, param):
        return v.visitFloatType(self, param)


class BoolType(Type):
    global cheated

    def __str__(self):
        if not cheated:
            return "BoolType"
        else:
            return "BoolType()"

    def accept(self, v, param):
        return v.visitBoolType(self, param)


class StringType(Type):
    global cheated

    def __str__(self):
        if not cheated:
            return "StringType"
        else:
            return "StringType()"

    def accept(self, v, param):
        return v.visitStringType(self, param)


class ArrayType(Type):
    global cheated
    # lower:int
    # upper:int
    # eleType:Type

    def __init__(self, lower, upper, eleType):
        self.lower = lower
        self.upper = upper
        self.eleType = eleType

    def __str__(self):
        return "ArrayType(" + str(self.lower) + "," + \
            str(self.upper) + "," + str(self.eleType) + ")"

    def accept(self, v, param):
        return v.visitArrayType(self, param)


class VoidType(Type):
    global cheated

    def __str__(self):
        return "VoidType()"

    def accept(self, v, param):
        return v.visitVoidType(self, param)


class Program(AST):
    global cheated
    # decl:list(Decl)

    def __init__(self, decl):
        self.decl = decl

    def __str__(self):
        return "Program([" + ','.join(str(i) for i in self.decl) + "])"

    def accept(self, v, param):
        return v.visitProgram(self, param)


class Decl(AST):
    __metaclass__ = ABCMeta
    pass


class VarDecl(Decl):
    global cheated
    # variable:Id
    # varType: Type

    def __init__(self, variable, varType):
        self.variable = variable
        self.varType = varType

    def __str__(self):
        return "VarDecl(" + str(self.variable) + "," + str(self.varType) + ")"

    def accept(self, v, param):
        return v.visitVarDecl(self, param)


class FuncDecl(Decl):
    global cheated
    # name: Id
    # param: list(VarDecl)
    # returnType: Type => VoidType for Procedure
    # local:list(VarDecl)
    # body: list(Stmt)

    def __init__(self, name, param, local, body, returnType=VoidType()):
        self.name = name
        self.param = param
        self.returnType = returnType
        self.local = local
        self.body = body

    def __str__(self):
        if not cheated:
            return "FuncDecl(" + str(self.name) + ",[" + \
                ','.join(str(i) for i in self.param) + "]," + \
                str(self.returnType) + ",[" + \
                ','.join(str(i) for i in self.local) + "],[" + \
                ','.join(str(i) for i in self.body) + "])"
        else:
            return "FuncDecl(" + str(self.name) + ",[" + \
                ','.join(str(i) for i in self.param) + "],[" + \
                ','.join(str(i) for i in self.local) + "],[" + \
                ','.join(str(i) for i in self.body) + "]," + \
                str(self.returnType) + ")"

    def accept(self, v, param):
        return v.visitFuncDecl(self, param)


class Stmt(AST):
    __metaclass__ = ABCMeta
    pass


class Assign(Stmt):
    global cheated
    # lhs:Expr
    # exp:Expr

    def __init__(self, lhs, exp):
        self.lhs = lhs
        self.exp = exp

    def __str__(self):
        if not cheated:
            return "AssignStmt(" + str(self.lhs) + "," + str(self.exp) + ")"
        else:
            return "Assign(" + str(self.lhs) + "," + str(self.exp) + ")"

    def accept(self, v, param):
        return v.visitAssign(self, param)


class If(Stmt):
    global cheated
    # expr:Expr
    # thenStmt:list(Stmt)
    # elseStmt:list(Stmt)

    def __init__(self, expr, thenStmt, elseStmt=[]):
        self.expr = expr
        self.thenStmt = thenStmt
        self.elseStmt = elseStmt

    def __str__(self):
        return "If(" + str(self.expr) + ",[" + \
            ','.join(str(i) for i in self.thenStmt) + "],[" + \
            ','.join(str(i) for i in self.elseStmt) + "])"

    def accept(self, v, param):
        return v.visitIf(self, param)


class While(Stmt):
    global cheated
    # sl:list(Stmt)
    # exp: Expr

    def __init__(self, exp, sl):
        self.sl = sl
        self.exp = exp

    def __str__(self):
        return "While(" + str(self.exp) + \
            ",[" + ','.join(str(i) for i in self.sl) + "])"

    def accept(self, v, param):
        return v.visitWhile(self, param)


class For(Stmt):
    global cheated
    # id:Id
    # expr1,expr2:Expr
    # loop:list(Stmt)
    # up:Boolean #True => increase; False => decrease

    def __init__(self, id, expr1, expr2, up, loop):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2
        self.up = up
        self.loop = loop

    def __str__(self):
        if not cheated:
            return "For(" + str(self.id) + ","\
                + str(self.expr1) + "," \
                + str(self.expr2) + ","\
                + str(self.up) + ',[' \
                + ','.join(str(i) for i in self.loop) + "])"
        else:
            return "For(" + str(self.id) + ","\
                + str(self.expr1) + "," \
                + str(self.expr2) + ","\
                + str(self.up) + ',[' \
                + ','.join(str(i) for i in self.loop) + "])"

    def accept(self, v, param):
        return v.visitFor(self, param)


class Break(Stmt):
    global cheated

    def __str__(self):
        if not cheated:
            return "Break"
        else:
            return "Break()"

    def accept(self, v, param):
        return v.visitBreak(self, param)


class Continue(Stmt):
    global cheated

    def __str__(self):
        if not cheated:
            return "Continue"
        else:
            return "Continue()"

    def accept(self, v, param):
        return v.visitContinue(self, param)


class Return(Stmt):
    global cheated
    # expr:Expr

    def __init__(self, expr=None):
        self.expr = expr

    def __str__(self):
        if not cheated:
            return "Return(" + ("None" if (self.expr is None)
                                else "Some(" + str(self.expr) + ")") + ")"
        else:
            return "Return()" if self.expr is None \
                else "Return(" + str(self.expr) + ")"

    def accept(self, v, param):
        return v.visitReturn(self, param)


class With(Stmt):
    global cheated
    # decl:list(VarDecl)
    # stmt:list(Stmt)

    def __init__(self, decl, stmt):
        self.decl = decl
        self.stmt = stmt

    def __str__(self):
        return "With([" + ','.join(str(i) for i in self.decl) + \
            "],[" + ','.join(str(i) for i in self.stmt) + "])"

    def accept(self, v, param):
        return v.visitWith(self, param)


class CallStmt(Stmt):
    global cheated
    # method:Id
    # param:list(Expr)

    def __init__(self, method, param):
        self.method = method
        self.param = param

    def __str__(self):
        return "CallStmt(" + str(self.method) + \
            ",[" + ','.join(str(i) for i in self.param) + "])"

    def accept(self, v, param):
        return v.visitCallStmt(self, param)


class Expr(AST):
    __metaclass__ = ABCMeta
    pass


class BinaryOp(Expr):
    global cheated
    # op:string: AND THEN => andthen; OR ELSE => orelse; other => keep it
    # left:Expr
    # right:Expr

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        if not cheated:
            return "BinaryOp(" + self.op + "," + str(self.left) + \
                "," + str(self.right) + ")"
        else:
            return "BinaryOp(\"" + self.op + "\"," + str(self.left) + \
                "," + str(self.right) + ")"

    def accept(self, v, param):
        return v.visitBinaryOp(self, param)


class UnaryOp(Expr):
    global cheated
    # op:string
    # body:Expr

    def __init__(self, op, body):
        self.op = op
        self.body = body

    def __str__(self):
        if not cheated:
            return "UnaryOp(" + self.op + "," + str(self.body) + ")"
        else:
            return "UnaryOp(\"" + self.op + "\"," + str(self.body) + ")"

    def accept(self, v, param):
        return v.visitUnaryOp(self, param)


class CallExpr(Expr):
    global cheated
    # method:Id
    # param:list(Expr)

    def __init__(self, method, param):
        self.method = method
        self.param = param

    def __str__(self):
        return "CallExpr(" + str(self.method) + \
            ",[" + ','.join(str(i) for i in self.param) + "])"

    def accept(self, v, param):
        return v.visitCallExpr(self, param)


class LHS(Expr):
    global cheated
    __metaclass__ = ABCMeta
    pass


class Id(LHS):
    global cheated
    # name:string

    def __init__(self, name):
        self.name = name

    def __str__(self):
        if not cheated:
            return "Id(" + self.name + ")"
        else:
            return "Id(\"" + self.name + "\")"

    def accept(self, v, param):
        return v.visitId(self, param)


class ArrayCell(LHS):
    global cheated
    # arr:Expr
    # idx:Expr

    def __init__(self, arr, idx):
        self.arr = arr
        self.idx = idx

    def __str__(self):
        return "ArrayCell(" + str(self.arr) + "," + str(self.idx) + ")"

    def accept(self, v, param):
        return v.visitArrayCell(self, param)


class Literal(Expr):
    global cheated
    __metaclass__ = ABCMeta
    pass


class IntLiteral(Literal):
    global cheated
    # value:int

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "IntLiteral(" + str(self.value) + ")"

    def accept(self, v, param):

        return v.visitIntLiteral(self, param)


class FloatLiteral(Literal):
    global cheated
    # value:float

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "FloatLiteral(" + str(self.value) + ")"

    def accept(self, v, param):
        return v.visitFloatLiteral(self, param)


class StringLiteral(Literal):
    global cheated
    # value:string

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if not cheated:
            return "StringLiteral(" + self.value + ")"
        else:
            return "StringLiteral(\"" + self.value + "\")"

    def accept(self, v, param):
        return v.visitStringLiteral(self, param)


class BooleanLiteral(Literal):
    global cheated
    # value:boolean

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "BooleanLiteral(" + str(self.value) + ")"

    def accept(self, v, param):
        return v.visitBooleanLiteral(self, param)


class ArrayPointerType(Type):
    def __init__(self, ctype):
        # cname: String
        self.eleType = ctype

    def __str__(self):
        return "ArrayPointerType({0})".format(
            str(self.eleType)
        )

    def accept(self, v, param):
        return None


class ClassType(Type):
    def __init__(self, cname):
        self.cname = cname

    def __str__(self):
        return "Class({0})".format(str(self.cname))

    def accept(self, v, param):
        return None
