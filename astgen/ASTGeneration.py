from parser.MPVisitor import MPVisitor
from parser.MPParser import MPParser
from functools import reduce

# * is not a good use case
from utils.AST import (
    IntType,
    FloatType,
    BoolType,
    StringType,
    ArrayType,
    # VoidType,
    Program,
    # Decl,
    VarDecl,
    FuncDecl,
    # Stmt,
    Assign,
    If,
    While,
    For,
    Break,
    Continue,
    Return,
    With,
    CallStmt,
    # Expr,
    BinaryOp,
    UnaryOp,
    CallExpr,
    # LHS,
    Id,
    ArrayCell,
    # Literal,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    BooleanLiteral
)


def flatten(listOflist):
    return reduce(lambda x, item: x + item, listOflist, [])


class ASTGeneration(MPVisitor):
    def visitProgram(self, ctx: MPParser.ProgramContext):
        """
        return Program(list of Decl)
        where Decl:
            + VarDecl  ==> var_decl
            + FuncDecl ==> func_decl
            + ProcDecl ==> proc_decl
        """
        return Program(self.visit(ctx.manydecl()))

    def visitManydecl(self, ctx: MPParser.ManydeclContext):
        """
        return list of decl expanded
        """
        decl = self.visit(ctx.decl())
        if ctx.manydecl():
            return decl + self.visit(ctx.manydecl())
        else:
            return decl

    def visitDecl(self, ctx: MPParser.DeclContext):
        """
        return either
            + var_decl
            + func_decl
            + proc_decl
        """
        decl = self.visit(ctx.getChild(0))
        if ctx.var_decl():
            return decl
        return [decl]

    def visitVar_decl(self, ctx: MPParser.Var_declContext):
        """
        return varlist
        """
        return self.visit(ctx.varlist())

    def visitVarlist(self, ctx: MPParser.VarlistContext):
        """
        return list of VarDecl(iden, mptype)
        """
        var = self.visit(ctx.var())
        if ctx.varlist():
            return var + self.visit(ctx.varlist())
        else:
            return var

    def visitVar(self, ctx: MPParser.VarContext):
        """
        return list of VarDecl(iden, mptype)
        """
        mptype = self.visit(ctx.mptype())
        idenlist = self.visit(ctx.idenlist())

        # apply VarDecl(x, mptype) to idenlist where x is item in idenlist
        def compose(f, arg):
            def h(x):
                return f(x, arg)
            return h
        hoo = compose(lambda x, y: VarDecl(x, y), mptype)
        return list(map(hoo, idenlist))

    def visitIdenlist(self, ctx: MPParser.IdenlistContext):
        """
        return list of iden
        """
        ident = Id(ctx.IDENT().getText())
        if ctx.idenlist():
            return [ident] + self.visit(ctx.idenlist())
        else:
            return [ident]

    def visitMptype(self, ctx: MPParser.MptypeContext):
        return self.visit(ctx.getChild(0))

    def visitPrimitive_type(self, ctx: MPParser.Primitive_typeContext):
        if ctx.INTEGER():
            return IntType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.REAL():
            return FloatType()
        elif ctx.STRING():
            return StringType()

    def visitCompound_type(self, ctx: MPParser.Compound_typeContext):
        """
        return ArrayType(low, high, type)
        """
        low, high = self.visit(ctx.array_value())
        pri_type = self.visit(ctx.primitive_type())
        return ArrayType(low, high, pri_type)

    def visitArray_value(self, ctx: MPParser.Array_valueContext):
        """
        return low, high
        """
        low = int(ctx.NUM_INT(0).getText())
        high = int(ctx.NUM_INT(1).getText())
        sub = len(ctx.MINUS())
        if sub == 0:
            pass
        elif sub == 2:
            low = -low
            high = -high
        elif ctx.getChild(1).getText() == '-':
            low = -low
        else:
            high = -high
        return low, high

    def visitFunc_decl(self, ctx: MPParser.Func_declContext):
        ident = Id(ctx.IDENT().getText())
        param_list = self.visit(ctx.param_list()) if ctx.param_list() else []
        mptype = self.visit(ctx.mptype())
        var_decl = flatten(list(map(self.visit, ctx.var_decl())))
        compound_statement = self.visit(ctx.compound_statement())
        return FuncDecl(
            ident,
            param_list,
            var_decl,
            compound_statement,
            mptype
        )

    def visitParam_list(self, ctx: MPParser.Param_listContext):
        """
        return list of VarDecl(iden, mptype)
        """
        var = self.visit(ctx.var())
        # var is a list of VarDecl
        if ctx.param_list():
            # concat
            return var + self.visit(ctx.param_list())
        else:
            # plain list return
            return var
        return

    def visitProc_decl(self, ctx: MPParser.Proc_declContext):
        ident = Id(ctx.IDENT().getText())
        param_list = self.visit(ctx.param_list()) if ctx.param_list() else []
        var_decl = flatten(list(map(self.visit, ctx.var_decl())))
        compound_statement = self.visit(ctx.compound_statement())
        return FuncDecl(
            ident,
            param_list,
            var_decl,
            compound_statement
        )

    def visitExpression(self, ctx: MPParser.ExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv1())
        if ctx.AND():
            op = "andthen"
        else:
            op = "orelse"
        return BinaryOp(
            op,
            self.visit(ctx.expression()),
            self.visit(ctx.expression_lv1())
        )

    def visitExpression_lv1(self, ctx: MPParser.Expression_lv1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv2(0))
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.expression_lv2(0)),
            self.visit(ctx.expression_lv2(1))
        )

    def visitExpression_lv2(self, ctx: MPParser.Expression_lv2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv3())
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.expression_lv2()),
            self.visit(ctx.expression_lv3())
        )

    def visitExpression_lv3(self, ctx: MPParser.Expression_lv3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expression_lv4())
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.expression_lv3()),
            self.visit(ctx.expression_lv4())
        )

    def visitExpression_lv4(self, ctx: MPParser.Expression_lv4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.index_expression())
        return UnaryOp(
            ctx.getChild(0).getText(),
            self.visit(ctx.expression_lv4())
        )

    def visitIndex_expression(self, ctx: MPParser.Index_expressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.factor())
        return ArrayCell(
            self.visit(ctx.index_expression()),
            self.visit(ctx.expression())
        )

    def visitInvocation_expression(
            self, ctx: MPParser.Invocation_expressionContext):
        if ctx.call_param():
            return self.visit(ctx.call_param())
        return []

    def visitFactor(self, ctx: MPParser.FactorContext):
        if ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.invocation_expression():
            return CallExpr(Id(ctx.IDENT().getText()),
                            self.visit(ctx.invocation_expression()))
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.IDENT():
            return Id(ctx.IDENT().getText())
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        return

    def visitStatement(self, ctx: MPParser.StatementContext):
        return self.visit(ctx.getChild(0))

    def visitStructured_statement(
            self, ctx: MPParser.Structured_statementContext):
        if ctx.compound_statement():
            return self.visit(ctx.getChild(0))
        else:
            return [self.visit(ctx.getChild(0))]

    def visitNormal_statement(self, ctx: MPParser.Normal_statementContext):
        if ctx.assignment_statement():
            return self.visit(ctx.getChild(0))
        else:
            return [self.visit(ctx.getChild(0))]

    def visitAssignment_statement(
            self, ctx: MPParser.Assignment_statementContext):
        """
        return list of Assign(lhs, exp)
        """
        expression = self.visit(ctx.expression())
        assignment_lhs_list = self.visit(ctx.assignment_lhs_list())

        rhs_list = assignment_lhs_list[1:] + [expression]

        # def compose(arg):
        #     def h(x):
        #         return Assign(x, arg)
        #     return h
        # hoo = list(map(lambda x: compose(x), rhs_list))
        return [Assign(lhs, rhs)
                for lhs, rhs in zip(assignment_lhs_list, rhs_list)][::-1]

    def visitAssignment_lhs_list(
            self, ctx: MPParser.Assignment_lhs_listContext):
        """
        return list of lhs
        """
        lhs = self.visit(ctx.lhs())
        if ctx.assignment_lhs_list():
            return [lhs] + self.visit(ctx.assignment_lhs_list())
        else:
            return [lhs]

    def visitLhs(self, ctx: MPParser.LhsContext):
        """
        return IDENT or index_pression
        """
        if ctx.IDENT():
            return Id(ctx.IDENT().getText())
        else:
            return self.visit(ctx.index_expression())

    def visitIf_statement(self, ctx: MPParser.If_statementContext):
        expression = self.visit(ctx.expression())
        if ctx.ELSE():
            then_statement = self.visit(ctx.statement(0))
            else_statement = self.visit(ctx.statement(1))
            return If(expression, then_statement, else_statement)
        else:
            then_statement = self.visit(ctx.statement(0))
            return If(expression, then_statement)

    def visitWhile_statement(self, ctx: MPParser.While_statementContext):
        return While(self.visit(ctx.expression()), self.visit(ctx.statement()))

    def visitFor_statement(self, ctx: MPParser.For_statementContext):
        up = True if ctx.TO() else False
        return For(
            Id(ctx.IDENT().getText()),
            self.visit(ctx.expression(0)),
            self.visit(ctx.expression(1)),
            up,
            self.visit(ctx.statement()))

    def visitBreak_statement(self, ctx: MPParser.Break_statementContext):
        return Break()

    def visitContinue_statement(self, ctx: MPParser.Continue_statementContext):
        return Continue()

    def visitReturn_statement(self, ctx: MPParser.Return_statementContext):
        if ctx.expression():
            return Return(self.visit(ctx.expression()))
        else:
            return Return()

    def visitCompound_statement(self, ctx: MPParser.Compound_statementContext):
        if ctx.statement():
            return flatten(list(map(self.visit, ctx.statement())))
        else:
            return []

    def visitWith_statement(self, ctx: MPParser.With_statementContext):
        return With(self.visit(ctx.varlist()), self.visit(ctx.statement()))

    def visitCall_statement(self, ctx: MPParser.Call_statementContext):
        param = self.visit(ctx.call_param()) if ctx.call_param() else []
        return CallStmt(Id(ctx.IDENT().getText()), param)

    def visitCall_param(self, ctx: MPParser.Call_paramContext):
        expression = self.visit(ctx.expression())
        if ctx.call_param():
            return [expression] + self.visit(ctx.call_param())
        else:
            return [expression]

    def visitEmpty(self, ctx: MPParser.EmptyContext):
        return

    def visitLiteral(self, ctx: MPParser.LiteralContext):
        if ctx.number():
            return self.visit(ctx.number())
        elif ctx.BOOL_LIT():
            if ctx.BOOL_LIT().getText().lower() == 'true':
                return BooleanLiteral(True)
            else:
                return BooleanLiteral(False)
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        return

    def visitNumber(self, ctx: MPParser.NumberContext):
        if ctx.NUM_INT():
            return IntLiteral(int(ctx.NUM_INT().getText()))
        elif ctx.NUM_REAL():
            return FloatLiteral(float(ctx.NUM_REAL().getText()))
