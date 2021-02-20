from helpers import *

registers = [0] * 8
instruction = 0
streams =[
    None,
    '',
    '',
]

def text_to_int(text):
    i = 0
    data = []
    while i < len(text):
        if i+3 < len(text) and text[i] == '\\' and text[i+1] == 'x':
            data.append(int(text[i+2:i+4], 16))
            i += 4
        else:
            data.append(ord(text[i]))
            i += 1
    return data


streams[1] = text_to_int(open('hack8.encrypted.txt', 'r', encoding='utf8', errors='surrogatepass').read())
print(streams[1])
streams[2] = open('hack8.key.txt', 'rb').read()
print(streams[2])

streams_indexes = [
    0, 0, 0,
]

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

def jmpz(a, b, c):
    global instruction
    global registers
    if registers[a]:
        return
    instruction = b

def jmpnz(a, b, c):
    global instruction
    global registers
    if not registers[a]:
        return
    instruction = b

def rdr(a, b, c):
    global registers
    global streams
    global streams_indexes
    registers[c] = streams[a][streams_indexes[a]]
    streams_indexes[a] += 1

def wrr(a, b, c):
    global registers
    global streams
    print(chr(registers[a]), end='')

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

find_opcodes()
correct_ops = founds

prog = read_lines('hack8.prog.txt')

def parse_op(text):
    return list(map(int, text.split()))

prog = list(map(parse_op, prog))

#print(prog)

registers = [0] * 8

correct_ops[16] = jmpz
correct_ops[17] = jmpnz
correct_ops[18] = rdr
correct_ops[19] = wrr

while True:
    if instruction < 0 or instruction >= len(prog):
        break
    op, a, b, c = prog[instruction]
    correct_ops[op](a, b, c)
    instruction += 1

print('')
