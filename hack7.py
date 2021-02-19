from helpers import *

registers = [0] * 8

def addr(a, b, c):
    global registers
    registers[c] = registers[a] + registers[b]

def addi(a, b, c):
    global registers
    registers[c] = registers[a] + b

def mulr(a, b, c):
    global registers
    registers[c] = registers[a] * registers[b]

def muli(a, b, c):
    global registers
    registers[c] = registers[a] * b

def banr(a, b, c):
    global registers
    registers[c] = registers[a] & registers[b]

def bani(a, b, c):
    global registers
    registers[c] = registers[a] & b

def borr(a, b, c):
    global registers
    registers[c] = registers[a] | registers[b]

def bori(a, b, c):
    global registers
    registers[c] = registers[a] | b

def setr(a, b, c):
    global registers
    registers[c] = registers[a]

def seti(a, b, c):
    global registers
    registers[c] = a

def gtir(a, b, c):
    global registers
    registers[c] = 1 if a > registers[b] else 0

def gtri(a, b, c):
    global registers
    registers[c] = 1 if registers[a] > b else 0

def gtrr(a, b, c):
    global registers
    registers[c] = 1 if registers[a] > registers[b] else 0

def eqir(a, b, c):
    global registers
    registers[c] = 1 if a == registers[b] else 0

def eqri(a, b, c):
    global registers
    registers[c] = 1 if registers[a] == b else 0

def eqrr(a, b, c):
    global registers
    registers[c] = 1 if registers[a] == registers[b] else 0


opcodes = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]

def attempt_parser(lines):
    lines = lines.strip()
    if not lines:
        return None
    before, ops, after = lines.split('\n')
    before = eval(before.split(':')[1])
    ops = list(map(int, ops.split()))
    after = eval(after.split(':')[1])
    return (before, ops, after)

attempts = list(filter(None, parse_items(read_paragraphs('hack7.txt'), attempt_parser)))

#print(attempts[0])

avails = list(opcodes)
founds = {}

def func_could_be_opcode(op, func):
    global registers
    for att in attempts:
        if att[1][0] != op:
            continue
        registers = list(att[0])
        func(att[1][1], att[1][2], att[1][3])
        for i, j in zip(registers, att[2]):
            if i != j:
                return False
    return True

def could_be_opcode(op):
    possibles = []
    for f in avails:
        if func_could_be_opcode(op, f):
            possibles.append(f)
    return possibles

def find_opcodes():
    while len(founds) < 16:
        possible_mappings = {}
        for op in range(16):
            if op in founds:
                continue
            possible_mappings[op] = could_be_opcode(op)
        for op, fs in possible_mappings.items():
            if len(fs) == 1:
                founds[op] = fs[0]
                avails.remove(fs[0])
                #print(founds)

find_opcodes()
correct_ops = founds

prog = read_lines('hack7_2.txt')

def parse_op(text):
    return list(map(int, text.split()))

prog = map(parse_op, prog)

registers = [0] * 8

for op, a,b,c in prog:
    correct_ops[op](a, b, c)

print(registers[0])
