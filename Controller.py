from coreClasses import *
from Solver import Solver
import Parser

print('Command: add knowledge, solve, quit')
s=Solver()
while True:
    command = input("Enter command:")
    if command == 'add knowledge':
        knowledge = input("Enter the knowledge:")
        while knowledge != 'done':
            foplstring=Parser.parser(knowledge)
            fopl=converter1(foplstring)
            clause=converter2(fopl)
            s.add_knowledge(clause)
            knowledge = input("Enter the knowledge:")
    elif command == 'solve':
            print(s.res())
    elif command == 'quit':
        print('Byebye')
        break
