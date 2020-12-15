import re
if __name__ is not None and "." in __name__:
    from .SkylineParser import SkylineParser
    from .SkylineVisitor import SkylineVisitor
    from .Skyline import *
else:
    from SkylineParser import SkylineParser
    from SkylineVisitor import SkylineVisitor
    from Skyline import *


class EvalVisitor(SkylineVisitor):
    symbolTable = {}

    def visitRoot(self, ctx: SkylineParser.RootContext):
        n = next(ctx.getChildren())
        res = self.visit(n)
        return res

    def visitExpr(self, ctx: SkylineParser.ExprContext):
        l = [n for n in ctx.getChildren()]
        if len(l) == 1:
            var = l[0].getText()
            if isinstance(l[0], SkylineParser.EdificiosContext):
                return self.visit(ctx.edificios())
            else:
                s = Skyline()
                if var in self.symbolTable:
                    s = self.symbolTable[var]
                else:
                    print(var + " is not defined")
                return s
        elif len(l) > 1:
            mid = l[1].getText()
            left = l[0].getText()
            if mid == '+':
                return self.visit(l[0]) + self.visit(l[2])
            elif mid == '-':
                return self.visit(l[0]) - self.visit(l[2])
            elif mid == '*':
                return self.visit(l[0]) * self.visit(l[2])
            elif left == '-':
                return -(self.visit(l[1]))
            elif left == '(':
                return self.visit(l[1])
            else:
                # case: ID ':=' expr
                # print(self.symbolTable)
                cleanID = left
                result = self.visit(l[2])
                if isinstance(result, Skyline):
                    self.symbolTable[cleanID] = result
                    # print("Success")
                    # print(self.symbolTable)
                    return result
                else:
                    # print("WEIRD assignment")
                    return Skyline()

    def visitNum(self, ctx: SkylineParser.NumContext):
        l = [n for n in ctx.getChildren()]
        return int(l[0].getText())

    def visitEdificio(self, ctx: SkylineParser.EdificioContext):
        start, height, end = [self.visit(ctx.num(i)) for i in range(3)]
        return Building(start, height, end)

    def visitEdif(self, ctx):
        return Skyline([self.visit(ctx.edificio())])

    def visitList(self, ctx):
        return Skyline(self.visit(ctx.args()))

    def visitArgs(self, ctx):
        l = [n for n in ctx.getChildren()]
        return [self.visit(ctx.edificio(i/2)) for i in range(0, len(l), 2)]

    def visitRandom(self, ctx):
        s = Skyline()
        n, h, w, xmin, xmax = [self.visit(ctx.num(i)) for i in range(5)]
        s.generate(n, h, w, xmin, xmax)
        return s
