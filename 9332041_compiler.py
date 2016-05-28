
stack = []
math = ['+', '-', '*', '/', '<', '>', '>=', '<=', '==', '!=', '%']
inloop = False

class Math_op:
    def __init__(self, stack):
        if isinstance(stack[-1],str) or isinstance(stack[-2],str):self.canDO = False
        else :
            self.canDO = True
            self.a1 = stack.pop()
            self.a2 = stack.pop()
    def choose(self, op):
        if   op== '+':return self.a2 + self.a1
        elif op== '-':return self.a2 - self.a1
        elif op== '*':return self.a2 * self.a1
        elif op== '/':return self.a2 / self.a1
        elif op== '%':return self.a2 % self.a1
        elif op== '<':return int(self.a2 <  self.a1)
        elif op== '>':return int(self.a2 >  self.a1)
        elif op=='==':return int(self.a2 == self.a1)
        elif op=='<=':return int(self.a2 <= self.a1)
        elif op=='>=':return int(self.a2 >= self.a1)
        elif op=='!=':return int(self.a2 != self.a1)
    
def dup():stack.append(stack[-1])
def depth():stack.append(len(stack))
def drop():stack.pop()
def printIt():print stack.pop(),
def endl():print
def key():
    if isinstance(stack[-1], str):
        stack.append(ord(stack.pop()))
    else :
        print 'KEY arg not in range(256)'
def emit():
    if stack[-1] in range(256):
        stack.append(chr(int(stack.pop())))
    else :
        print 'EMIT expected character'
def pick():
    a1 = stack.pop()
    try:
        a2 = stack.pop(int(-a1))
        stack.append(a2)
    except:print 'stack index out of range' 
def roll():
    a1 = stack.pop()
    try:
        a2 = stack[int(-a1)]
        stack.append(a2)
    except:print 'stack index out of range'
def swap():
    a1 = stack.pop()
    a2 = stack.pop()
    stack.append(a1)
    stack.append(a2)

def find_end(lst, starter, finisher):
    end = 1
    for i in range(len(lst)):
        if lst[i] == starter:
            end += 1
        elif lst[i] == finisher:
            end -= 1
        if end == 0:
            return i

def CreatFuntion(fun):
    try :
        end = find_end(fun, ':', ';')
        if fun[0] in CreatFuntion_duc.keys():
            print "There is a Funtion named :",lst[0]," Try a diffrent name"
        else:
            CreatFuntion_duc.update({fun[0]:fun[1:end]})
        compileIt(fun[(end+1):])
    except :
        print "EROR! Invalid syntax (creatFuntion)"

def if_else_then(iet):
    a1 = stack.pop()
    if_end = find_end(iet, 'IF', 'THEN')
    i=0
    while i<len(iet):
        if iet[i] == 'IF':
            i += find_end(iet[i+1:], 'IF', 'THEN')
        elif iet[i] == 'ELSE':
            break
        i += 1
    else_start = i
    if i == len(iet):else_start = if_end
    if   a1 != 0: compileIt(iet[:else_start])
    elif a1 == 0: compileIt(iet[(else_start+1):if_end])
    compileIt(iet[(if_end+1):])

def loop(lst):
    a1 = stack.pop()
    a2 = stack.pop()
    loop_end = find_end(lst, 'DO', 'LOOP')
    in_loop = True
    for i in range(int(a1),int(a2)):
        compileIt(lst[:loop_end])
    in_loop = False
    compileIt(lst[(loop_end+1):])

def b_u(lst):
    loop_end = find_end(lst, 'BEGIN', 'UNTIL')
    inloop = True
    while stack[-1] != 0:
        compileIt(lst[:loop_end])
    inloop = False
    compileIt(lst[(loop_end)+1:])
    
def show():
    print 'STACK :', stack

def openfile():
    inFile_name = raw_input('Enter file name : ')
    try :
        File = open(inFile_name, 'r')
        for EachLine in File:
            listedLine = EachLine.split()
            compileIt(listedLine)
        File.close()
    except :
        print "EROR! No such file or directory :",inFile_name

CreatFuntion_duc = {}

fun_duc = {'IF':if_else_then, ':':CreatFuntion, 'DO':loop, 'BEGIN':b_u}

duc = {'DUP':dup, 'DROP':drop, 'SWAP':swap, '.':printIt, 'PICK':pick, 'ROLL':roll, 'EMIT':emit, 'KEY':key, 'OPEN_FILE':openfile,
       'CR':endl, 'SHOW':show, 'DEPTH':depth}

argument = {'DUP':1, 'DROP':1, 'SWAP':2, '.':1,'PICK':1, 'ROLL':1, 'EMIT':1, 'KEY':1, 'OPEN_FILE':0,
       'CR':0, 'SHOW':0, 'DEPTH':0}

def compileIt(lst):
    if lst == []:
        return 
    elif lst[0] in duc.keys():
        if len(stack) < argument[lst[0]]:
            print "EROR! ",lst[0],"need exactly",argument[lst[0]],"stack home (there is only",len(stack),"home)"
        else:
            duc[lst[0]]()
            compileIt(lst[1:])
    elif lst[0] in math:
        if len(stack) < 2:
            print "EROR! math operation need exactly 2 stack home (there is only",len(stack),"home)"
        else:
            op = Math_op(stack)
            if op.canDO:stack.append(op.choose(lst[0]))
            else : print 'Math operation expect int or float , got string'
            compileIt(lst[1:])
    elif lst[0] in fun_duc.keys():
        fun_duc[lst[0]](lst[1:])
    elif lst[0] in CreatFuntion_duc.keys():
        compileIt(CreatFuntion_duc[lst[0]])
        compileIt(lst[1:])
    elif lst[0][0]=='(':
        compileIt(lst[1:])
    elif inloop and lst[0]=='LEAVE':
        compileIt(lst[(loop_end)+1:])
    elif lst[0][0] in '-0123456789':
            stack.append(float(lst[0]))
            compileIt(lst[1:])
    else :
            print "EROR! No such funtion or valid input :", lst[0]
            return

def openshell():
    while True:
        iN = raw_input("\n>>> ")
        if iN == '':
            break
        compileIt(iN.split())
        
def main():
    ask = raw_input('Enter File ? (y/n) ')
    if ask == 'y':openfile()
    openshell()
    
main()
