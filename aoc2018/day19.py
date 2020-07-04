from typing import List

from utils import read_input, test_case

Input = read_input(19)
InputTest = test_case('''
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
''')


def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    registers[c] = registers[a] | b


def setr(registers, a, _, c):
    registers[c] = registers[a]


def seti(registers, a, _, c):
    registers[c] = a


def gtir(registers, a, b, c):
    registers[c] = 1 if a > registers[b] else 0


def gtri(registers, a, b, c):
    registers[c] = 1 if registers[a] > b else 0


def gtrr(registers, a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0


def eqir(registers, a, b, c):
    registers[c] = 1 if a == registers[b] else 0


def eqri(registers, a, b, c):
    registers[c] = 1 if registers[a] == b else 0


def eqrr(registers, a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0


class Program:
    def __init__(self, input_: List[str], register_0=0):
        self.registers = [register_0, 0, 0, 0, 0, 0]
        self.ran = False
        self.input = input_

    def run(self):
        if self.ran:
            return
        else:
            self.ran = True

        registers = self.registers

        ip_register = int(self.input[0][-1])
        ip = 0

        code = [line.split() for line in self.input[1:]]
        while 0 <= ip < len(code):
            registers[ip_register] = ip
            op, a, b, c = code[ip]
            stmt = op + '(registers, ' + a + ', ' + b + ', ' + c + ')'
            print(f'{ip} : {stmt}\n{registers}\n')
            eval(stmt)
            ip = registers[ip_register]
            ip += 1


def part1(input_: List[str]):
    program = Program(input_)
    program.run()

    print(program.registers[0])


def part2(input_: List[str]):
    program = Program(input_, 1)
    program.run()

    print(program.registers[0])


part2(Input)
