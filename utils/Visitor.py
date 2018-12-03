from abc import ABC, abstractmethod  # , ABCMeta


class Visitor(ABC):

    def visit(self, ast, param):
        return ast.accept(self, param)

    @abstractmethod
    def visitProgram(self, asttree, param):
        pass

    @abstractmethod
    def visitVarDecl(self, asttree, param):
        pass

    @abstractmethod
    def visitFuncDecl(self, asttree, param):
        pass

    @abstractmethod
    def visitIntType(self, asttree, param):
        pass

    @abstractmethod
    def visitFloatType(self, asttree, param):
        pass

    @abstractmethod
    def visitBoolType(self, asttree, param):
        pass

    @abstractmethod
    def visitStringType(self, asttree, param):
        pass

    @abstractmethod
    def visitVoidType(self, asttree, param):
        pass

    @abstractmethod
    def visitArrayType(self, asttree, param):
        pass

    @abstractmethod
    def visitBinaryOp(self, asttree, param):
        pass

    @abstractmethod
    def visitUnaryOp(self, asttree, param):
        pass

    @abstractmethod
    def visitCallExpr(self, asttree, param):
        pass

    @abstractmethod
    def visitId(self, asttree, param):
        pass

    @abstractmethod
    def visitArrayCell(self, asttree, param):
        pass

    @abstractmethod
    def visitAssign(self, asttree, param):
        pass

    @abstractmethod
    def visitWith(self, asttree, param):
        pass

    @abstractmethod
    def visitIf(self, asttree, param):
        pass

    @abstractmethod
    def visitFor(self, asttree, param):
        pass

    @abstractmethod
    def visitContinue(self, asttree, param):
        pass

    @abstractmethod
    def visitBreak(self, asttree, param):
        pass

    @abstractmethod
    def visitReturn(self, asttree, param):
        pass

    @abstractmethod
    def visitWhile(self, asttree, param):
        pass

    @abstractmethod
    def visitCallStmt(self, asttree, param):
        pass

    @abstractmethod
    def visitIntLiteral(self, asttree, param):
        pass

    @abstractmethod
    def visitFloatLiteral(self, asttree, param):
        pass

    @abstractmethod
    def visitBooleanLiteral(self, asttree, param):
        pass

    @abstractmethod
    def visitStringLiteral(self, asttree, param):
        pass


class BaseVisitor(Visitor):

    def visitProgram(self, asttree, param):
        return None

    def visitVarDecl(self, asttree, param):
        return None

    def visitFuncDecl(self, asttree, param):
        return None

    def visitIntType(self, asttree, param):
        return None

    def visitFloatType(self, asttree, param):
        return None

    def visitBoolType(self, asttree, param):
        return None

    def visitStringType(self, asttree, param):
        return None

    def visitVoidType(self, asttree, param):
        return None

    def visitArrayType(self, asttree, param):
        return None

    def visitBinaryOp(self, asttree, param):
        return None

    def visitUnaryOp(self, asttree, param):
        return None

    def visitCallExpr(self, asttree, param):
        return None

    def visitId(self, asttree, param):
        return None

    def visitArrayCell(self, asttree, param):
        return None

    def visitAssign(self, asttree, param):
        return None

    def visitWith(self, asttree, param):
        return None

    def visitIf(self, asttree, param):
        return None

    def visitFor(self, asttree, param):
        return None

    def visitContinue(self, asttree, param):
        return None

    def visitBreak(self, asttree, param):
        return None

    def visitReturn(self, asttree, param):
        return None

    def visitWhile(self, asttree, param):
        return None

    def visitCallStmt(self, asttree, param):
        return None

    def visitIntLiteral(self, asttree, param):
        return None

    def visitFloatLiteral(self, asttree, param):
        return None

    def visitBooleanLiteral(self, asttree, param):
        return None

    def visitStringLiteral(self, asttree, param):
        return None
