#!/usr/bin/env python3

# returns the current character while skipping over comments
import sys


def Look():
    # comments are entered by # and exited by \n or \0
    global pc
    if source[pc] == '#':
        while source[pc] != '\n' and source[pc] != '\0':
            # scan over comments here
            pc += 1
    return source[pc]


# takes away and returns the current character
def Take():
    global pc
    c = Look()
    pc += 1
    return c


# returns whether a certain string could be taken starting at pc
def TakeString(word):
    global pc
    copypc = pc
    for c in word:
        if Take() != c:
            pc = copypc
            return False
    return True


# returns the next non-whitespace character
def Next():
    while Look() == ' ' or Look() == '\t' or Look() == '\n' or Look() == '\r':
        Take()
    return Look()


# eats white-spaces, returns whether a certain character could be eaten
def TakeNext(c):
    if Next() == c:
        Take()
        return True
    else:
        return False


def IsDigit(c): return (c >= '0' and c <= '9')									# recognizers
def IsAlpha(c): return ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'))
def IsAlNum(c): return (IsDigit(c) or IsAlpha(c))
def IsAddOp(c): return (c == '+' or c == '-')
def IsMulOp(c): return (c == '*' or c == '/')


def TakeNextAlNum():
    alnum = ""
    if IsAlpha(Next()):
        while IsAlNum(Look()):
            alnum += Take()
    return alnum

# --------------------------------------------------------------------------------------------------


def BooleanFactor(act):
    inv = TakeNext('!')
    e = Expression(act)
    b = e[1]
    Next()
    if (e[0] == 'i'): 																			# a single mathexpression may also serve as a boolean factor
        if TakeString("=="):
            b = (b == MathExpression(act))
        elif TakeString("!="):
            b = (b != MathExpression(act))
        elif TakeString("<="):
            b = (b <= MathExpression(act))
        elif TakeString("<"):
            b = (b < MathExpression(act))
        elif TakeString(">="):
            b = (b >= MathExpression(act))
        elif TakeString(">"):
            b = (b > MathExpression(act))
    else:
        if TakeString("=="):
            b = (b == StringExpression(act))
        elif TakeString("!="):
            b = (b != StringExpression(act))
        else:
            b = (b != "")
    return act[0] and (b != inv)											# always returns False if inactive


def BooleanTerm(act):
    b = BooleanFactor(act)
    while TakeNext('&'):
        b = b & BooleanFactor(act)		# logical and corresponds to multiplication
    return b


def BooleanExpression(act):
    b = BooleanTerm(act)
    while TakeNext('|'):
        b = b | BooleanTerm(act)			# logical or corresponds to addition
    return b


def MathFactor(act):
    m = 0
    if TakeNext('('):
        m = MathExpression(act)
        if not TakeNext(')'):
            Error("missing ')'")
    elif IsDigit(Next()):
        while IsDigit(Look()):
            m = 10 * m + ord(Take()) - ord('0')
    elif TakeString("val("):
        s = String(act)
        if act[0] and s.isdigit():
            m = int(s)
        if not TakeNext(')'):
            Error("missing ')'")
    else:
        ident = TakeNextAlNum()
        if ident not in variable or variable[ident][0] != 'i':
            Error("unknown variable")
        elif act[0]:
            m = variable[ident][1]
    return m


def MathTerm(act):
    m = MathFactor(act)
    while IsMulOp(Next()):
        c = Take()
        m2 = MathFactor(act)
        if c == '*':
            m = m * m2													# multiplication
        else:
            m = m / m2																# division
    return m


def MathExpression(act):
    c = Next()																				# check for an optional leading sign
    if IsAddOp(c):
        c = Take()
    m = MathTerm(act)
    if c == '-':
        m = -m
    while IsAddOp(Next()):
        c = Take()
        m2 = MathTerm(act)
        if c == '+':
            m = m + m2													# addition
        else:
            m = m - m2																# subtraction
    return m


def String(act):
    s = ""
    if TakeNext('\"'):																# is it a literal string?
        while not TakeString("\""):
            if Look() == '\0':
                Error("unexpected EOF")
            if TakeString("\\n"):
                s += '\n'
            else:
                s += Take()
    elif TakeString("str("):													# str(...)
        s = str(MathExpression(act))
        if not TakeNext(')'):
            Error("missing ')'")
    elif TakeString("input()"):
        if act[0]:
            s = input()
    else:
        ident = TakeNextAlNum()
        if ident in variable and variable[ident][0] == 's':
            s = variable[ident][1]
        else:
            Error("not a string")
    return s


def StringExpression(act):
    s = String(act)
    while TakeNext('+'):
        # string addition = concatenation
        s += String(act)
    return s


def Expression(act):
    global pc
    copypc = pc
    ident = TakeNextAlNum()
    # scan for identifier or "str"
    pc = copypc
    if(Next() == '\"' or ident == "str"
            or ident == "input"
            or (ident in variable and variable[ident][0] == 's')):
        return ('s', StringExpression(act))
    else:
        return ('i', MathExpression(act))


def DoWhile(act):
    global pc
    local = [act[0]]
    # save PC of the while statement
    pc_while = pc
    while BooleanExpression(local):
        Block(local)
        pc = pc_while
    # scan over inactive block and leave while
    Block([False])


def DoIfElse(act):
    b = BooleanExpression(act)
    if act[0] and b:
        # process if block?
        Block(act)
    else:
        Block([False])
    Next()
    # process else block?
    if TakeString("else"):
        if act[0] and not b:
            Block(act)
        else:
            Block([False])


def DoGoSub(act):
    global pc
    ident = TakeNextAlNum()
    if ident not in variable or variable[ident][0] != 'p':
        Error("unknown subroutine")
    ret = pc
    pc = variable[ident][1]
    Block(act)
    # execute block as a subroutine
    pc = ret


def DoSubDef():
    global pc
    ident = TakeNextAlNum()
    if ident == "":
        Error("missing subroutine identifier")
    variable[ident] = ('p', pc)
    Block([False])


def DoAssign(act):
    ident = TakeNextAlNum()
    if not TakeNext('=') or ident == "":
        Error("unknown statement")
    e = Expression(act)
    if act[0] or ident not in variable:
        variable[ident] = e		# assert initialization even if block is inactive


def DoBreak(act):
    if act[0]:
        # switch off execution within enclosing loop (while, ...)
        act[0] = False


def DoPrint(act):
    while True:																								# process comma-separated arguments
        e = Expression(act)
        if act[0]:
            print(e[1], end="")
        if not TakeNext(','):
            return


def DoFormat(act):
    while True:																								# process comma-separated arguments
        e = Expression(act)
        if act[0]:
            print(e[1], end="\n")
        if not TakeNext(','):
            return


def DoExit(act):
    global pc
    ident = TakeNextAlNum()
    if ident == "1":
        raise Error("error code 1, quitting")
    elif ident == "-1":
        raise Error("error code -1, quitting")
    elif ident == "":
        exit()


def Statement(act):
    if TakeString("OUTPUT"):
        DoPrint(act)
    elif TakeString("FORMAT"):
        DoFormat(act)
    elif TakeString("EXIT"):
        DoExit(act)
    elif TakeString("IF"):
        DoIfElse(act)
    elif TakeString("WHILE"):
        DoWhile(act)
    elif TakeString("BREAK"):
        DoBreak(act)
    elif TakeString("RUN"):
        DoGoSub(act)
    elif TakeString("DEFINE"):
        DoSubDef()
    else:
        DoAssign(act)


def Block(act):
    if TakeNext("%"):
        while not TakeNext("%"):
            Block(act)
    else:
        Statement(act)


def Program():
    act = [True]
    while Next() != '\0':
        Block(act)


def Error(text):
    s = source[:pc].rfind("\n") + 1
    e = source.find("\n", pc)
    print("\nERROR " + text + " in line " +
          str(source[:pc].count("\n") + 1) + ": '" + source[s:pc] + "_" + source[pc:e] + "'\n")
    sys.exit(1)

# --------------------------------------------------------------------------------------------------


pc = 0
# program couter, identifier -> (type, value) lookup table
variable = {}

if len(sys.argv) < 2:
    print('USAGE: qs.py <sourcefile>')
    sys.exit(1)
try:
    f = open(sys.argv[1], 'r')																					# open source file
except:
    print("ERROR: Can't find source file \'" + sys.argv[1] + "\'.")
    sys.exit(1)
source = f.read() + '\0'
f.close()																			# append a null termination

Program()