import sly
import math

# read about sly
# here https://github.com/dabeaz/sly
# and here https://sly.readthedocs.io/en/latest/


class ExampleLexer(sly.Lexer):
    # a set of tokes we spit out
    tokens = { NUMBER, E, PI, SIN, COS, TG, TAN, CTG, CTAN, COT,
               ARCSIN, ASIN, ARCCOS, ACOS, ARCTG, ARCTAN, ATG, ATAN, ARCCTG, ACTG, ACTAN, ARCCOT, ARCCOTAN,
               LOG, LG, LN, SH, CH, SQRT}

    # these are also tokens, but they don't have state and take up exactly one
    # symbol, so it's more convinient this way. Otherwise this is completely
    # equivalent to defining PLUS, LPAREN, RPAREN.
    literals = { '+', '-', '*', '/', '^', '(', ')', '{', '}', '[', ']', ','}

    # ignore any of these symbols
    ignore = ' \r\t\n'

    # we can also ignore any regular expression (start the name with `ignore_`)
    #
    # read about the r'' strings here https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
    # basically, it's so don't have to type '\\' each time.
    #
    # read about regular expressions
    # here https://docs.python.org/3/howto/regex.html#regex-howto
    # and here https://docs.python.org/3/library/re.html
    ignore_comment = r'\#.*'

    E = r'\\?e'
    PI = r'\\?pi'
    SIN = 'sin'
    COS = 'cos'
    TG = 'tg'
    TAN = 'tan'
    CTG = 'ctg'
    CTAN = 'ctan'
    COT = 'cot'
    ARCSIN = 'arcsin'
    ASIN = 'asin'
    ARCCOS = 'arccos'
    ACOS = 'acos'
    ARCTG = 'arctg'
    ARCTAN = 'arctan'
    ATG = 'atg'
    ATAN = 'atan'
    ARCCTG = 'arcctg'
    ACTG = 'actg'
    ACTAN = 'actan'
    ARCCOT = 'arccot'
    ARCCOTAN = 'arccotan'
    SH = 'sh'
    CH = 'ch'
    LOG = 'log'
    LG = 'lg'
    LN = 'ln'
    SQRT = 'sqrt'

    # this is a definition of a token, also a regex, we must provide one for every token in `tokens` set.
    #
    # this one reads "one or more digits, then a stop ('.'), then one or more digits.
    # not the best one, but good enough as an example
    @_(r'[0-9]+\.[0-9]+', r'\d+')
    def NUMBER(self, t):
        # the token is a string by default.
        # we can define a function that does some "preprocessing".
        # here we convert it to a float.
        # if we didn't want to convert anything, we could just write
        # NUMBER = r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        return t

    @_(r'[a-df-z_]')
    def NAME(self, t):
        t.value = 0 #(int)(t.value)
        return t


# base class for our tree
# AST stands for Abstract Syntax Tree
# read about it here https://en.wikipedia.org/wiki/Abstract_syntax_tree
class ASTNode(object):
    # AST nodes should be computable, i.e. return a number
    def compute(self):
        raise NotImplementedError

    # AST nodes should have a text representation
    def __str__(self):
        raise NotImplementedError

class VarNode(ASTNode):
    def __init__(self, n):
        self.n = n

    def compute(self):
        return 0

    def __str__(self):
        return str(self.n)


        
# this one represents a number
class NumNode(ASTNode):
    # we just store a number in this type of AST node
    def __init__(self, n):
        self.n = n

    # we alredy know this node's numeric value
    def compute(self):
        return self.n

    # to convert it to text, we just return the number as text
    def __str__(self):
        return str(self.n)

class MinusNode(ASTNode):
    def __init__(self, n):
        self.n = n

    def compute(self):
        return (-1) * self.n.compute()

    def __str__(self):
        return "-" + str(self.n)

class ENode(ASTNode):
    def __init__(self):
        self.n = math.e

    def compute(self):
        return math.e

    def __str__(self):
        return "e"

class PiNode(ASTNode):
    def __init__(self):
        self.n = math.pi

    # we alredy know this node's numeric value
    def compute(self):
        return math.pi

    # to convert it to text, we just return the number as text
    def __str__(self):
        return "pi"

# this one represents a sum of two expressions
class AddNode(ASTNode):
    # we store references to another two AST nodes, the left operand of the
    # plus, and the right
    def __init__(self, l, r):
        self.l = l
        self.r = r

    # to compute this node's numeric value, we must compute values of our left
    # and right children and add them
    def compute(self):
        return self.l.compute() + self.r.compute()

    # the textual representation is '(left)+(right)'
    def __str__(self):
        return f'({self.l})+({self.r})'


class SubNode(ASTNode):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def compute(self):
        return self.l.compute() - self.r.compute()

    def __str__(self):
        return f'({self.l})-({self.r})'


class MultNode(ASTNode):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def compute(self):
        return self.l.compute() * self.r.compute()

    def __str__(self):
        return f'({self.l})*({self.r})'


class DivNode(ASTNode):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def compute(self):
        return self.l.compute() / self.r.compute()

    def __str__(self):
        return f'({self.l})/({self.r})'


class PowNode(ASTNode):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def compute(self):
        return math.pow(self.l.compute(), self.r.compute())

    def __str__(self):
        return f'({self.l})^({self.r})'


class SqrtNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.sqrt(self.l.compute())

    def __str__(self):
        return f'sqrt({self.l})'


class SinNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.sin(self.l.compute())

    def __str__(self):
        return f'sin({self.l})'


class CosNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.cos(self.l.compute())

    def __str__(self):
        return f'cos({self.l})'


class TgNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.tan(self.l.compute())

    def __str__(self):
        return f'tg({self.l})'


class CtgNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.tan(math.pi / 2 - self.l.compute())

    def __str__(self):
        return f'ctg({self.l})'


class ArcsinNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.asin(self.l.compute())

    def __str__(self):
        return f'arcsin({self.l})'


class ArccosNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.acos(self.l.compute())

    def __str__(self):
        return f'arccos({self.l})'


class ArctgNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.atan(self.l.compute())

    def __str__(self):
        return f'arctg({self.l})'


class ArcctgNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.pi / 2 - math.atan(self.l.compute())

    def __str__(self):
        return f'arcctg({self.l})'


class ShNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.sinh(self.l.compute())

    def __str__(self):
        return f'sh({self.l})'


class ChNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.cosh(self.l.compute())

    def __str__(self):
        return f'ch({self.l})'


class LogNode(ASTNode):
    def __init__(self, l):
        self.l = l

    def compute(self):
        return math.log(self.l.compute())

    def __str__(self):
        return f'log({self.l})'
    
class Log2Node(ASTNode):
    def __init__(self, l, r):
            self.l = l
            self.r = r

    def compute(self):
        return math.log(self.l.compute(), self.r.compute())

    def __str__(self):
        return f'(log({self.l}, {self.r}))'


class ExampleParser(sly.Parser):
    # this means that
    # a + b + c
    # is parsed as
    # (a + b) + c
    # rather than
    # a + (b + c)
    # read about precedence here https://en.wikipedia.org/wiki/Order_of_operations
    # and here https://en.wikipedia.org/wiki/Operator_associativity
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        ('right', 'SIN', 'COS', 'TG', 'TAN', 'CTG', 'CTAN', 'COT',
               'ARCSIN', 'ASIN', 'ARCCOS', 'ACOS', 'ARCTG', 'ARCTAN', 'ATG', 'ATAN', 'ARCCTG', 'ACTG', 'ACTAN',
               'ARCCOT', 'ARCCOTAN', 'LOG', 'LG', 'LN', 'SH', 'CH', 'SQRT'),
        ('left', '^'),
    )
    # declare that we use tokens from the ExampleLexer
    tokens = ExampleLexer.tokens

    # number is an expression
    @_('NUMBER')
    def expr(self, p):
        return NumNode(p.NUMBER)

    @_('NAME')
    def expr(self, n):
        return VarNode(n.NAME);

    @_('E')
    def expr(self, n):
        return ENode()

    @_('PI')
    def expr(self, n):
        return PiNode()

    # expression in parentheses in an expression
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"{" expr "}"')
    def expr(self, p):
        return p.expr

    @_('"[" expr "]"')
    def expr(self, p):
        return p.expr

    # expression, then plus, then expression is an expression
    @_('expr "+" expr')
    def expr(self, p):
        return AddNode(p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return SubNode(p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return MinusNode(p.expr)

    @_('expr "*" expr')
    def expr(self, p):
        return MultNode(p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return DivNode(p.expr0, p.expr1)

    @_('expr "^" expr')
    def expr(self, p):
        return PowNode(p.expr0, p.expr1)

    @_('SQRT expr')
    def expr(self, p):
        return SqrtNode(p.expr)

    @_('SIN expr')
    def expr(self, p):
        return SinNode(p.expr)

    @_('COS expr')
    def expr(self, p):
        return CosNode(p.expr)

    @_('TG expr', 'TAN expr')
    def expr(self, p):
        return TgNode(p.expr)

    @_('CTG expr', 'CTAN expr', 'COT expr')
    def expr(self, p):
        return CtgNode(p.expr)

    @_('ARCSIN expr', 'ASIN expr')
    def expr(self, p):
        return ArcsinNode(p.expr)

    @_('ARCCOS expr', 'ACOS expr')
    def expr(self, p):
        return ArccosNode(p.expr)

    @_('ARCTG expr', 'ARCTAN expr', 'ATG expr', 'ATAN expr')
    def expr(self, p):
        return ArctgNode(p.expr)
   
    @_('ARCCTG expr', 'ACTG expr', 'ACTAN expr', 'ARCCOT expr', 'ARCCOTAN expr')
    def expr(self, p):
        return ArcctgNode(p.expr)

    @_('SH expr')
    def expr(self, p):
        return ShNode(p.expr)

    @_('CH expr')
    def expr(self, p):
        return ChNode(p.expr)

    @_('LOG expr', 'LN expr')
    def expr(self, p):
        return LogNode(p.expr)
    
    @_('LG expr')
    def expr(self, p):
        return Log2Node(p.expr, 10)
    
    @_('LOG "(" expr "," expr ")" ')
    def expr(self, p):
        return Log2Node(p.expr0, p.expr1)



# this is a kind of function that you need to write, but for the full grammar
def parse(s):
    lexer = ExampleLexer()
    parser = ExampleParser()
    return parser.parse(lexer.tokenize(s))

def answer(s):
    result = parse(s)
    return ("$" + str(result) + "$", result.compute())

if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        try:
            res = parse(s)
            print('tree representation:', res)
            print('tree value:', res.compute())
        except Exception as e:
            print(e)
    print()
