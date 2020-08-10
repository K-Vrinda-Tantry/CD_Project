import re
import prettytable as tb
import texttable as tt

list1 = []
keyword = ['else', 'if', 'int', 'while', 'return', 'void', 'float', 'begin', 'end', 'main', 'do']
oper = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
delim = ['\t', '\n', ',', ';', '(', ')', '{', '}', '[', ']', ' ']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

p = re.compile(r'(\d+(\.\d+)?([E][+|-]?\d+)?)')
file = open("input", "r")
comment_count = 0
line_comment = 0
is_comment = False
i = 0
iden = ""  # null string for identifiers to be built up
print_list = []
end_comment = False  # This is a bool value for a block comment
float_str = ""


def is_keyword(kw):
    if kw in keyword:
        return True
    return False


def is_delim(char):
    if char in delim:
        return True
    return False


def which_delim(char):
    if char in delim:
        if char != '\t' and char != '\n' and char != ' ':
            print("DELIMTER: %s " % char)
            list1.append(char)


def is_digit(char):
    if char in num:
        return True
    return False


def is_char(char):
    c = 0
    c = ord(char)
    if 97 <= c <= 122:
        return True
    return False


def is_oper(char):
    if char in oper:
        return True
    return False


def is_num(str):
    try:
        int(str)
        return True
    except:
        return False


def is_float(str):
    m = p.match(str)
    length = len(str)
    if m and length == len(m.group(0)):
        print("NUM: %s" % m.group(0))
        list1.append("num")
        return True
    else:
        return False


for line in file:
    if line != '\n':
        print("Input: %s" % (line))
        while line[i] != '\n':  # i and enumerate allows to iterate through line
            if line[i] is '/':
                if line[i + 1] is '/' and comment_count is 0:  # it's a line comment print it out
                    line_comment += 1
                elif line[i + 1] is '*':
                    i += 1
                    comment_count += 1
            elif (line[i] is '*') and (line[i + 1] is '/') and comment_count > 0:
                comment_count -= 1
                i += 1
                if comment_count == 0:
                    end_comment = True

            if comment_count is 0 and line_comment is 0 and end_comment == False:
                if is_digit(line[i]):  # check for float
                    j = i
                    while not is_delim(line[j]):
                        float_str += line[j]
                        j += 1
                    if is_float(float_str):
                        if (j < len(line)):
                            i = j
                        iden = ''
                    float_str = ''  # reset string at end use
                if is_char(line[i]) or is_digit(line[i]) and not is_oper(line[i]):
                    iden += line[i]
                if is_delim(line[i]) and iden == '':  # for delims w/ blank space
                    which_delim(line[i])
                if is_oper(line[i]) and iden is '':
                    temp = line[i] + line[i + 1]
                    if (is_oper(temp)):
                        print("OPERATOR: %s " % temp)
                        list1.append("op")
                        i += 1
                    else:
                        print("OPERATOR %s" %(line[i]))
                        list1.append(line[i])
                if not is_char(line[i]) and not is_digit(line[i]) and not is_oper(
                        line[i]) and iden is not '' and not is_delim(line[i]):
                    if is_keyword(iden):
                        print("KEYWORD: %s" % iden)
                        list1.append(iden)
                        print("ERROR: %s" % line[i])
                    elif is_oper(iden):
                        print("OPERATOR: %s " %(iden))
                        list1.append("op")
                        print("Error: %s" % line[i])
                    elif is_num(iden):
                        print("NUM: %s" % iden)
                        list1.append("number")
                        print("Error: %s" % line[i])
                    else:
                        print("ID: %s" % iden)
                        list1.append("id")
                        print("Error: %s" % line[i])
                    iden = ''
                elif not is_char(line[i]) and not is_digit(line[i]) and not is_oper(line[i]) and not is_delim(line[i]):
                    print("Error: %s" % line[i])
                if (is_delim(line[i]) or is_oper(line[i])) and iden != '':
                    if is_keyword(iden):
                        print("KEYWORD: %s" % iden)
                        list1.append(iden)
                    elif is_oper(line[i]):
                        temp = line[i] + line[i + 1]
                        if is_oper(temp):
                            if is_keyword(iden):
                                print("KEYWORD: %s" % iden)
                                list1.append(iden)
                            print("OPERATOR: %s" %(temp))
                            list1.append("op")
                            i += 1
                        else:
                            print("ID: %s" % iden)
                            list1.append("id")
                            print("OPERATOR:  %s " %(line[i]))
                            list1.append(line[i])
                    elif is_num(iden):
                        print("NUM: %s" % iden)
                        list1.append("num")
                    elif is_oper(iden):
                        temp = iden + line[i + 1]
                        if is_oper(temp):
                            print("OPERATOR: %s" %(temp))
                            list1.append("op")
                            i += 1
                        else:
                            print(iden)
                            list1.append(iden)
                    else:
                        print("ID: %s" % iden)
                        list1.append("id")
                    which_delim(line[i])
                    iden = ''
            i += 1  # increment i
            end_comment = False
        if line[i] == '\n' and iden != '':
            if is_keyword(iden):
                print("KEYWORD: %s" % iden)
                list1.append(iden)
            elif is_oper(iden):
                print("OPERATOR: %s" % iden)
                list1.append("op")
            else:
                print("ID: %s" % iden)
                list1.append("id")
            iden = ''
        if line[i] == '\n':
            print("NEW LINE: nl")
            list1.append("nl")
        print('\n')
        line_comment = 0  # reset line commment number
        i = 0  # reset i
#print(list1)

datatype1 = ['int', 'float', 'char', 'double']
operator = ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=']

list2 = []

for token in list1:
    if token in datatype1:
        list2.append("datatype")
    elif token in operator:
        list2.append("op")
    elif token == ";":
        list2.append("sc")
    elif token == ",":
        list2.append("comma")
    elif token == '=':
        list2.append("equalsto")
    else:
        list2.append(token)
#print("\n")
#print(list2)
#print("\n")

list4 = []
for j in list2:
    if j == "datatype":
        list4.append("a")
    elif j == "nl":
        list4.append("b")
    elif j == "begin":
        list4.append("c")
    elif j == "main":
        list4.append("d")
    elif j == "(":
        list4.append("e")
    elif j == ")":
        list4.append("f")
    elif j == "sc":
        list4.append("g")
    elif j == "do":
        list4.append("h")
    elif j == "end":
        list4.append("i")
    elif j == "comma":
        list4.append("j")
    elif j == "id":
        list4.append("k")
    elif j == "equalsto":
        list4.append("l")
    elif j == "num":
        list4.append("m")
    elif j == "while":
        list4.append("n")
    else:
        list4.append("p")

print("\n")
#print(list4)
############################PARSER#############################################

list3 = "".join(list4)
#print(list3)

index = 0
inpIndex = 0  # input pointer

flage = 1
input = []
stack = []
action1 = []
Ps = []
Is = []


# Is.append(list4)
class Stack:
    def __init__(self):
        self.s = []

    def pop(self):
        return self.s.pop()

    def push(self, item):
        self.s.append(item)

    def sizeOfStack(self):
        return len(self.s)

    def peak(self):
        return self.s[len(self.s) - 1]

    def printStack(self):
        sl = []
        for i in range(len(self.s)):
            sl.append(str(self.s[i]))
        Ps.append(sl)


def foo(string):
    global index, inpIndex, inp, s, flage


    action1.append(string)

    if string[0] == 'r':  # do reducing
        temp = RulesTable[int(string[1:])]

        temp = temp.split("->")
        g = temp[1].split(" ")
        for i in range(len(g) * 2):
            label = s.pop()
        num = s.peak()

        s.push(temp[0])



        s.push(int(LR1Table[num][goto[temp[0]]]))
        index = (int(LR1Table[num][goto[temp[0]]]))
        k = []
        for i in range(inpIndex, len(inp)):
            k.append(inp[i])
        Is.append(k)
        s.printStack()





    else:  # do shifting
        s.push(inp[inpIndex])
        k = []
        for i in range(inpIndex, len(inp)):
            k.append(inp[i])
        Is.append(k)

        s.push(int(string[1:]))
        inpIndex += 1
        index = s.peak()
        s.printStack()


s = Stack()

list3 += "$"
inp = list3

#print(inp)

terminals = ['a', 'c', 'b', 'i', 'd', 'e', 'f', 'g', 'j', 'k', 'l', 'm', 'p', 'n']
nonterminals = ['S\'', 'S', 'A', 'B', 'C', 'D', 'E', 'I', 'J', 'F', 'K', 'G', 'L']

action = {'a': 0, 'c': 1, 'b': 2, 'i': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'j': 8, 'k': 9, 'l': 10, 'm': 11, 'p': 12,
          'n': 13, '$': 14}
goto = {'S\'': 15, 'S': 16, 'A': 17, 'B': 18, 'C': 19, 'D': 20, 'E': 21, 'I': 22, 'J': 23, 'F': 24, 'K': 25, 'G': 26,
        'L': 27}

# rl(1) table
LR1Table = []
f = open("C:/Users/lishe/Desktop/input2.csv")

state = []
i = 0
for line in f:

    state = line.split(',')
    l5 = []

    for i in state:
        if i != '\n':
            l5.append(i)

    LR1Table.append(l5)


# rules table
RulesTable = []
RulesTable.append("S->S")
RulesTable.append("S->a A")
RulesTable.append("A->B c b C i b")
RulesTable.append("B->d e f b")
RulesTable.append("C->D C")
RulesTable.append("C->D")
RulesTable.append("D->E g b")
RulesTable.append("D->F g b")
RulesTable.append("D->G")
RulesTable.append("E->a I")
RulesTable.append("I->J")
RulesTable.append("I->J j I")
RulesTable.append("J->k")
RulesTable.append("J->k l m")
RulesTable.append("F->k l K")
RulesTable.append("F->k l K p K")
RulesTable.append("F->K")
RulesTable.append("K->k")
RulesTable.append("K->m")
RulesTable.append("G->n e F f L")
RulesTable.append("L->b c b C i b")


s.push(0)
s.printStack()
temp = LR1Table[index][action[inp[inpIndex]]]

while (temp != "acc"):
    if temp == '':
        print("Error")
        break
    foo(temp)
    try:
        temp = LR1Table[index][action[inp[inpIndex]]]
    except:
        print("Error")

if temp == "acc":

    action1.append("acc")
    k2=[]
    k2.append("$")
    Is.append(k2)
# print the table
Printtable = LR1Table
j = 0
column = ['state','datatype', 'begin', 'nl', 'end', 'main', '(', ')', 'sc', 'comma', 'id', 'equalsto', 'num',
          'op', 'while',  '$', 'S\'', 'S', 'MAINFUNC', 'MAIN', 'STMTS', 'STMT',
          'DECLARE', 'DECVARS', 'DECVAR', 'EXP', 'VARNUM', 'WHILESTMT', 'WTSTMT']
for i in Printtable:
    i.insert(0, j)
    j = j + 1

x = tb.PrettyTable(column)
for i in Printtable:
    x.add_row(i)

print("LR(1) PARSING TABLE")
print(x)

#######
Is2 = []

for row1 in Is:
    k2 = []
    for row2 in row1:
        if row2 == 'a':
            k2.append('datatype')
        elif row2 == 'b':
            k2.append('nl')
        elif row2 == 'c':
            k2.append('begin')
        elif row2 == 'd':
            k2.append('main')
        elif row2 == 'e':
            k2.append('(')
        elif row2 == 'f':
            k2.append(')')
        elif row2 == 'g':
            k2.append('sc')

        elif row2 == 'i':
            k2.append('end')
        elif row2 == 'j':
            k2.append('comma')
        elif row2 == 'k':
            k2.append('id')
        elif row2 == 'l':
            k2.append('equalsto')
        elif row2 == 'm':
            k2.append('num')
        elif row2 == 'n':
            k2.append('while')

        elif row2 == 'p':
            k2.append('op')
        else:
            k2.append('$')
    k3 = " ".join(k2)
    Is2.append(k3)
Ps2=[]
for row1 in Ps:
    k2 = []
    for row2 in row1:
        if row2 == 'a':
            k2.append('datatype')
        elif row2 == 'b':
            k2.append('nl')
        elif row2 == 'c':
            k2.append('begin')
        elif row2 == 'd':
            k2.append('main')
        elif row2 == 'e':
            k2.append('(')
        elif row2 == 'f':
            k2.append(')')
        elif row2 == 'g':
            k2.append('sc')

        elif row2 == 'i':
            k2.append('end')
        elif row2 == 'j':
            k2.append('comma')
        elif row2 == 'k':
            k2.append('id')
        elif row2 == 'l':
            k2.append('equalsto')
        elif row2 == 'm':
            k2.append('num')
        elif row2 == 'n':
            k2.append('while')

        elif row2 == 'p':
            k2.append('op')
        elif row2 == 'A':
            k2.append('MAINFUNC')
        elif row2 == 'B':
            k2.append('MAIN')
        elif row2 == 'C':
            k2.append('STMTS')
        elif row2 == 'D':
            k2.append('STMT')
        elif row2 == 'F':
            k2.append('EXP')
        elif row2 == 'G':
            k2.append('WHILESTMT')
        elif row2 == 'H':
            k2.append('RETURNSTMT')
        elif row2 == 'I':
            k2.append('DECVARS')
        elif row2 == 'J':
            k2.append('DECVAR')
        elif row2 == 'K':
            k2.append('VARNUM')
        elif row2 == 'E':
            k2.append('DECLARE')
        elif row2 == 'L':
            k2.append('WTSTMT')


        else:
            k2.append(row2)
    k3 = " ".join(k2)
    Ps2.append(k3)


headings = ['STACK', 'INPUT', 'ACTION']
tab = tt.Texttable()
tab.header(headings)
for row4 in zip(Ps2,Is2,action1):
    tab.add_row(row4)
s=tab.draw()
print("\nPARSING STEPS")
print(s)



