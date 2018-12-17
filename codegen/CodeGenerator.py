from utils.Utils import Utils
from utils.Visitor import BaseVisitor
from checker.StaticCheck import MType, Symbol
from utils.AST import (
    IntType,
    FloatType,
    BoolType,
    StringType,
    VoidType,
    FuncDecl,
    Assign,
    While,
    BinaryOp,
    Id,
    IntLiteral,
    ArrayPointerType,
    ClassType
)
from codegen.Emitter import Emitter
from codegen.Frame import Frame
from abc import ABC


class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [
            # from specification, section 7: Built-in Functions/Procedures
            Symbol(
                "getInt",
                MType([], IntType()),
                CName(self.libName)
            ),
            Symbol(
                "putInt",
                MType([IntType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putIntLn",
                MType([IntType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "getFloat",
                MType([], FloatType()),
                CName(self.libName)
            ),
            Symbol(
                "putFloat",
                MType([FloatType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putFloatLn",
                MType([FloatType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putBool",
                MType([BoolType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putBoolLn",
                MType([BoolType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putString",
                MType([StringType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putStringLn",
                MType([StringType()], VoidType()),
                CName(self.libName)
            ),
            Symbol(
                "putLn",
                MType([], VoidType()),
                CName(self.libName)
            )
        ]

    def gen(self, ast, dir_, name):
        # ast: AST
        # dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_, name)
        gc.visit(ast, None)  # visits Program


class SubBody():
    def __init__(self, frame, sym):
        # frame: Frame
        # sym: List[Symbol]

        self.frame = frame
        self.sym = sym
        self.gen = False
        self.isFor = False

    def __str__(self):
        return "SubBody({},{})".format(
            str(self.frame),
            ','.join([str(x) for x in self.sym])
        )


class Access():
    def __init__(self, frame, sym, **kwargs):
        # frame: Frame
        # sym: List[Symbol]
        # isLeft: Boolean
        # isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = kwargs.get('isLeft', False)
        self.isFirst = kwargs.get('isFirst', False)


class Val(ABC):
    pass


class Index(Val):
    def __init__(self, value):
        # value: Int

        self.value = value


class CName(Val):
    def __init__(self, value):
        # value: String

        self.value = value


class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_, name):
        '''
        astTree: AST
        env: List[Symbol]
        dir_: File
        '''

        self.astTree = astTree
        self.env = env[:]  # safety reason
        self.className = name
        self.path = dir_
        self.emit = Emitter(
            self.path + "/" + self.className + ".j")

        # import sys
        # print(astTree, file=sys.stderr)

    def genMETHOD(self, consdecl, o, frame):
        '''
        consdecl: FuncDecl
        o: SubBody,
        frame: Frame

        Submethod to generate code for body,
        most of this is given by teacher himself
        with slight modifications,
        add local variable code generation
        '''

        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and \
            len(consdecl.param) == 0 and \
            isinstance(consdecl.returnType, VoidType)

        if isInit:
            returnType = VoidType()
            methodName = '<init>'
        else:
            returnType = consdecl.returnType
            methodName = consdecl.name.name

        if isMain:
            intype = [ArrayPointerType(StringType())]
        else:
            intype = [v.varType for v in consdecl.param]

        mtype = MType(intype, returnType)

        self.emit.printout(
            self.emit.emitMETHOD(
                methodName,
                mtype,
                not isInit,
                frame
            ))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(
                self.emit.emitVAR(
                    frame.getNewIndex(),
                    "this",
                    ClassType(self.className),
                    frame.getStartLabel(),
                    frame.getEndLabel(),
                    frame
                ))
        if isMain:
            self.emit.printout(
                self.emit.emitVAR(
                    frame.getNewIndex(),
                    "args",
                    ArrayPointerType(StringType()),
                    frame.getStartLabel(),
                    frame.getEndLabel(),
                    frame
                ))

        # set up local variables
        if glenv is None:
            glenv = []
        local = []
        for p in consdecl.param:
            s = self.visit(
                p,
                SubBody(frame, local + glenv)
            )
            local = [s] + local
        for l in consdecl.local:
            s = self.visit(
                l,
                SubBody(frame, local + glenv)
            )
            local = [s] + local
        glenv = local + glenv

        body = consdecl.body
        self.emit.printout(
            self.emit.emitLABEL(
                frame.getStartLabel(),
                frame
            ))

        # Generate code for statements
        if isInit:
            self.emit.printout(
                self.emit.emitREADVAR(
                    "this",
                    ClassType(self.className),
                    0,
                    frame
                ))
            self.emit.printout(
                self.emit.emitINVOKESPECIAL(frame)
            )

        # visit statement
        list(map(lambda x:
                 self.visit(
                     x,
                     SubBody(frame, glenv)),
                 body
                 ))

        self.emit.printout(
            self.emit.emitLABEL(
                frame.getEndLabel(),
                frame
            ))
        '''
        prevents:
        LabelX:
        LabelY:
        end
        '''
        self.emit.printout(
            self.emit.emitRETURN(
                VoidType(),
                frame
            ))
        self.emit.printout(
            self.emit.emitENDMETHOD(frame)
        )
        frame.exitScope()

    def callBody(self, ast, ctxt):
        '''
        ast: CallExpr | CallStmt
        ctxt: SubBody if CallStmt
              Access if CallExpr
        => name, type if CallExpr

        CallExpr and CallStmt has similar routine,
        Except that CallExpr returns (name, type)
        of the function being called
        '''
        frame = ctxt.frame
        sym = ctxt.sym

        symbol, ctype = self.visit(  # visits Id
            ast.method,
            Access(frame, sym, isFirst=True)
        )
        cname = symbol.value
        params = ctype.partype

        in_ = ("", list())
        for i, arg in enumerate(ast.param):
            str1, typ1 = self.visit(
                arg,
                Access(frame, sym, isFirst=True)
            )
            if isinstance(typ1, Symbol):
                typ1 = typ1.mtype.rettype

            if not isinstance(typ1, type(params[i])):
                # foo(float) ==> foo(int)
                # others: Checker catches
                str1 += self.emit.emitI2F(frame)

            in_ = (in_[0] + str1, in_[1] + [typ1])

        # funcname = cname.value + '/' + ast.method.name
        funcname = cname.value + '/' + symbol.name
        code = ''
        code += in_[0]
        code += self.emit.emitINVOKESTATIC(
            funcname,
            ctype,
            frame
        )
        return code, symbol

    def visitProgram(self, ast, c):
        '''
        ast: Program
        c: Unknown
        => c
        '''

        self.emit.printout(
            self.emit.emitPROLOG(
                self.className,
                "java.lang.Object"
            ))
        e = SubBody(None, self.env)

        # generate global declare list
        for x in ast.decl:
            # returns Symbol on no Gen
            self.env += [self.visit(x, e)]

        e.gen = True
        for x in ast.decl:
            # recall that e = SubBody(None, self.env)
            # and e.sym = self.env as reference
            self.visit(x, e)

        # generate default constructor
        self.genMETHOD(
            FuncDecl(
                Id("<init>"),
                list(),
                list(),
                list(),
                None
            ),
            c,
            Frame("<init>", VoidType)
        )
        self.emit.emitEPILOG()
        return c

    def visitFuncDecl(self, ast, subbody):
        '''
        ast: FuncDecl
        subbody: SubBody
        => None if generate code
        => else Symbol
        '''

        if subbody.gen:
            # on gen
            frame = Frame(ast.name, ast.returnType)
            self.genMETHOD(
                ast,
                subbody.sym,
                frame
            )
        else:
            # on first scan to get global Symbol
            params = [v.varType for v in ast.param]
            return Symbol(
                ast.name.name,
                MType(params, ast.returnType),
                CName(self.className)
            )

    def visitVarDecl(self, ast, subbody):
        '''
        ast: VarDecl
        subbody: SubBody
        => Symbol(,,CName) for global VarDecl
        => Symbol(,,Index) for local VarDecl
        '''
        if subbody.gen:
            return
        if subbody.frame is None:
            # generate code for global var decl
            # returns Symbol with CName
            code = self.emit.emitATTRIBUTE(
                ast.variable.name,
                ast.varType,
                False,
                ''
            )
            self.emit.printout(code)
            return Symbol(
                ast.variable.name,
                ast.varType,
                CName(self.className)
            )
        else:
            # generate code for local var decl
            # returns Symbol with Index
            frame = subbody.frame
            idx = frame.getNewIndex()
            code = self.emit.emitVAR(
                idx,
                ast.variable.name,
                ast.varType,
                frame.getStartLabel(),
                frame.getEndLabel(),
                frame
            )
            self.emit.printout(code)
            return Symbol(
                ast.variable.name,
                ast.varType,
                Index(idx)
            )

    def visitBinaryOp(self, ast, param):
        '''
        ast: BinaryOp
        param: Access
        => code, type

        Rules:
            (/) --> Float/Int:Float/Int => Float
            (+,-,*) --> Float:Float/Int => Float
                    --> Float/Int:Float => Float
                    --> Int:Int         => Int
            (div,mod) --> Int:Int => Int
            (<,<=,=,>=,>,<>) --> Float:Float/Int => Bool
                             --> Float/Int:Float => Bool
                             --> Int:Int => Bool
            (and,or,andthen,orelse) --> Bool:Bool => Bool
        '''
        frame = param.frame
        sym = param.sym

        lhs, ltype = self.visit(
            ast.left,
            Access(frame, sym)
        )
        rhs, rtype = self.visit(
            ast.right,
            Access(frame, sym)
        )
        if isinstance(ltype, MType):
            ltype = ltype.rettype
        if isinstance(rtype, MType):
            rtype = rtype.rettype

        if (isinstance(ltype, type(rtype))):
            # because idiv returns int not float
            # while MP / returns float on all cases
            if ast.op == '/' and\
                    isinstance(ltype, IntType):
                lhs += self.emit.emitI2F(frame)
                rhs += self.emit.emitI2F(frame)
                intype = FloatType()
                rettype = FloatType()
            else:
                intype = ltype
                rettype = ltype
        else:
            # only Float:Int or Int:Float
            # I2F on Int
            if isinstance(ltype, IntType):
                lhs += self.emit.emitI2F(frame)
            if isinstance(rtype, IntType):
                rhs += self.emit.emitI2F(frame)
            intype = FloatType()
            rettype = FloatType()

        code = ''
        code += lhs
        code += rhs
        # self.emit.printout(lhs)  # push left
        # self.emit.printout(rhs)  # push right

        # generate code for each operator
        if ast.op in ('+', '-'):
            code += self.emit.emitADDOP(
                ast.op,
                intype,
                frame
            )
        elif ast.op in ('*', '/'):
            code += self.emit.emitMULOP(
                ast.op,
                intype,
                frame
            )
        elif ast.op in ('<', '<=', '=', '>=', '>', '<>'):
            code += self.emit.emitREOP(
                ast.op,
                intype,
                frame
            )
            rettype = BoolType()
        elif ast.op.lower() == 'div':
            code += self.emit.emitDIV(frame)
        elif ast.op.lower() == 'mod':
            code += self.emit.emitMOD(frame)
        elif ast.op.lower() == 'and':
            code += self.emit.emitANDOP(frame)
        elif ast.op.lower() == 'or':
            code += self.emit.emitOROP(frame)
        elif ast.op.lower() == 'andthen':
            code = ''
            falseLabel = frame.getNewLabel()
            endLabel = frame.getNewLabel()
            code += lhs
            code += self.emit.emitIFEQ(falseLabel, frame)
            code += rhs
            code += self.emit.emitIFEQ(falseLabel, frame)
            code += self.emit.emitPUSHICONST(1, frame)
            code += self.emit.emitGOTO(endLabel, frame)
            code += self.emit.emitLABEL(falseLabel, frame)
            code += self.emit.emitPUSHICONST(0, frame)
            code += self.emit.emitLABEL(endLabel, frame)
            rettype = BoolType()
        elif ast.op.lower() == 'orelse':
            code = ''
            trueLabel = frame.getNewLabel()
            endLabel = frame.getNewLabel()
            code += lhs
            # if lhs != 0 True
            code += self.emit.emitIFNE(trueLabel, frame)
            code += rhs
            # if rhs != 0 True
            code += self.emit.emitIFNE(trueLabel, frame)
            code += self.emit.emitPUSHICONST(0, frame)
            code += self.emit.emitGOTO(endLabel, frame)
            code += self.emit.emitLABEL(trueLabel, frame)
            code += self.emit.emitPUSHICONST(1, frame)
            code += self.emit.emitLABEL(endLabel, frame)
            rettype = BoolType()

        return code, rettype

    def visitUnaryOp(self, ast, param):
        frame = param.frame
        sym = param.sym

        bodycode, bodytype = self.visit(
            ast.body,
            Access(frame, sym)
        )

        code = ''
        code += bodycode
        if ast.op.lower() == 'not':
            code += self.emit.emitNOT(bodytype, frame)
        elif ast.op.lower() == '-':
            code += self.emit.emitNEGOP(bodytype, frame)

        return code, bodytype

    def visitCallExpr(self, ast, o):
        '''
        ast: CallExpr
        o: Access
        => (name, type) of function being called
        '''
        return self.callBody(ast, o)

    def visitId(self, ast, param):
        '''
        ast: Id
        param: Access
        '''
        res = self.lookup(
            ast.name,
            param.sym,
            lambda env: env.name
        )

        # not likely, checker catches
        if res is None:
            return None, None

        # function call
        if isinstance(res.mtype, MType):
            return res, res.mtype

        frame = param.frame
        # global variable
        # res: Symbol(,,CName)
        if isinstance(res.value, CName):
            varname = res.value.value + '/' + res.name
            if param.isLeft:
                code = self.emit.emitPUTSTATIC(
                    varname,
                    res.mtype,
                    frame
                )
            else:
                code = self.emit.emitGETSTATIC(
                    varname,
                    res.mtype,
                    frame
                )
            return code, res.mtype

        # Local variable
        if param.isLeft:
            code = self.emit.emitWRITEVAR(
                res.name,
                res.mtype,
                res.value.value,
                frame
            )
        else:
            code = self.emit.emitREADVAR(
                res.name,
                res.mtype,
                res.value.value,
                frame
            )
        return code, res.mtype

    def visitArrayCell(self, ast, param):
        '''
        ast: ArrayCell,
        param: Access
        '''
        frame = param.frame
        sym = param.sym
        arrcode, arrtype = self.visit(
            ast.arr,
            Access(frame, sym)
        )
        idxcode, idxtype = self.visit(
            ast.idx,
            Access(frame, sym)
        )
        return None

    def visitAssign(self, ast, param):
        '''
        ast: Assign
        param: SubBody
        '''
        frame = param.frame
        sym = param.sym
        expcode, exptype = self.visit(
            ast.exp,
            Access(frame, sym)
        )
        lhscode, lhstype = self.visit(
            ast.lhs,
            Access(frame, sym, isLeft=True)
        )

        if isinstance(exptype, Symbol):
            exptype = exptype.mtype.rettype

        if not isinstance(exptype, type(lhstype)):
            # float = int
            # others => checker catches
            expcode += self.emit.emitI2F(param.frame)

        code = ''
        code += expcode + lhscode
        self.emit.printout(code)

    def visitWith(self, ast, param):
        '''
        ast: With
        param: SubBody
        '''
        frame = param.frame
        sym = param.sym

        frame.enterScope(False)
        startLabel = self.emit.emitLABEL(frame.getStartLabel(), frame)
        endLabel = self.emit.emitLABEL(frame.getEndLabel(), frame)

        local = sym[:]
        for var in ast.decl:
            local = [self.visit(var, SubBody(frame, local))] + local

        self.emit.printout(startLabel)
        for stmt in ast.stmt:
            self.visit(stmt, SubBody(frame, local))
        self.emit.printout(endLabel)
        frame.exitScope()

    def visitIf(self, ast, param):
        '''
        ast: If
        param: SubBody
        '''
        frame = param.frame
        sym = param.sym
        haveElse = True if len(ast.elseStmt) > 0 \
            else False

        code = ''
        expcode, exptype = self.visit(
            ast.expr, Access(frame, sym)
        )
        code += expcode

        elseLabel = frame.getNewLabel()

        if haveElse:
            endLabel = frame.getNewLabel()

        code += self.emit.emitIFEQ(elseLabel, frame)

        self.emit.printout(code)
        code = ''

        # printout then code
        for stmt in ast.thenStmt:
            self.visit(stmt, param)

        if haveElse:
            code += self.emit.emitGOTO(endLabel, frame)
        code += self.emit.emitLABEL(elseLabel, frame)
        self.emit.printout(code)
        code = ''

        if not haveElse:
            return

        # printout else code
        for stmt in ast.elseStmt:
            self.visit(stmt, param)

        code += self.emit.emitLABEL(endLabel, frame)
        self.emit.printout(code)

    def visitFor(self, ast, param):
        conditionOp = '<=' if ast.up else '>='
        continueOp = '+' if ast.up else '-'

        loopCondition = BinaryOp(conditionOp, ast.id, ast.expr2)
        continueInstruction = Assign(
            ast.id, BinaryOp(
                continueOp, ast.id, IntLiteral(1)))
        loop = ast.loop[:] + [continueInstruction]

        param.isFor = True
        self.visit(Assign(ast.id, ast.expr1), param)
        self.visit(While(loopCondition, loop), param)

    def visitContinue(self, ast, param):
        frame = param.frame
        continueLabel = frame.getContinueLabel()
        code = self.emit.emitGOTO(continueLabel, frame)
        self.emit.printout(code)

    def visitBreak(self, ast, param):
        frame = param.frame
        breakLabel = frame.getBreakLabel()
        code = self.emit.emitGOTO(breakLabel, frame)
        self.emit.printout("\t; Break\n")
        self.emit.printout(code)

    def visitReturn(self, ast, param):
        frame = param.frame
        sym = param.sym
        rettype = frame.returnType

        if ast.expr:
            expcode, exptype = self.visit(
                ast.expr,
                Access(frame, sym)
            )
        else:
            expcode, exptype = '', VoidType()

        code = ''
        code += expcode
        if not isinstance(exptype, type(rettype)):
            # return int in float function
            # others -> Checker catches
            code += self.emit.emitI2F(frame)
        code += self.emit.emitRETURN(rettype, frame)
        self.emit.printout(code)

    def visitWhile(self, ast, param):
        '''
        ast: While
        param: SubBody
        '''
        frame = param.frame
        sym = param.sym
        isFor = param.isFor

        param.isFor = False
        code = ''

        frame.enterLoop()
        breakLabel = frame.getBreakLabel()
        continueLabel = frame.getContinueLabel()

        expcode, exptype = self.visit(
            ast.exp,
            Access(frame, sym)
        )
        if isFor:
            continueInstruction = ast.sl[-1]
            ast.sl = ast.sl[:-1]

        code += expcode
        code += self.emit.emitIFEQ(breakLabel, frame)

        bodyLabel = frame.getNewLabel()
        code += '; body\n'
        code += self.emit.emitLABEL(bodyLabel, frame)

        self.emit.printout(code)
        code = ''

        for stmt in ast.sl:
            self.visit(stmt, param)

        code += '; continue\n'
        code += self.emit.emitLABEL(continueLabel, frame)
        if isFor:
            self.emit.printout(code)
            code = ''
            self.visit(continueInstruction, param)
            code += expcode
            code += self.emit.emitIFNE(bodyLabel, frame)
        else:
            code += expcode
            code += self.emit.emitIFNE(bodyLabel, frame)

        code += '; break\n'
        code += self.emit.emitLABEL(breakLabel, frame)
        self.emit.printout(code)
        frame.exitLoop()

    def visitCallStmt(self, ast, o):
        '''
        ast: CallStmt
        o: SubBody
        '''
        code, symbol = self.callBody(ast, o)
        self.emit.printout(code)

    def visitIntLiteral(self, ast, param):
        '''
        ast: IntLiteral
        param: Access
        => code, type
        '''
        frame = param.frame
        return self.emit.emitPUSHICONST(
            ast.value,
            frame
        ), IntType()

    def visitFloatLiteral(self, ast, param):
        '''
        ast: FloatLiteral
        param: Access
        => code, type
        '''
        frame = param.frame
        return self.emit.emitPUSHFCONST(
            str(ast.value),
            frame
        ), FloatType()

    def visitBooleanLiteral(self, ast, param):
        frame = param.frame
        return self.emit.emitPUSHICONST(
            str(ast.value).lower(),
            frame
        ), BoolType()

    def visitStringLiteral(self, ast, param):
        frame = param.frame
        return self.emit.emitPUSHCONST(
            # emitLDC doesn't add "
            '"{}"'.format(ast.value),
            StringType(),
            frame
        ), StringType()
