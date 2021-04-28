from coreClasses import *
from Solver import Solver
import Converter
import Parser


print('Command: add knowledge, solve, quit')
s=Solver()
while True:
    command = input("Enter command:")
    if command == 'add knowledge':
        knowledge = input("Enter the knowledge:")
        while knowledge != 'done':
            foplstring=Parser.parser(knowledge)
            print('The FOPL string is {}.'.format(foplstring))
            fopl=Converter.string2fopl(foplstring)
            print('The FOPL is {}.'.format(fopl))
            clauses=Converter.fopl2clause(fopl)
            print('The clauses are')
            for i in clauses:
                print(i)
                s.add_knowledge(i)
            knowledge = input("Enter the knowledge:")
    elif command == 'solve':
            conjecture = input("Enter the conjecture:")
            foplstring=Parser.parser(conjecture)
            print('The FOPL string is {}.'.format(foplstring))
            fopl=Converter.string2fopl(foplstring)
            fopl.negate()
            clauses=Converter.fopl2clause(fopl)
            print(s.solve(clauses))
    elif command == 'quit':
        print('Byebye')
        break