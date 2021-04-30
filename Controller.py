from coreClasses import *
from Solver import Solver
import Converter
import Parser


print('Command: ak(add knowledge), solve, quit')
s=Solver()
'''
strings=[]
strings.append(Parser.parser('Every skier likes snow.'))
strings.append(Parser.parser('No climber likes rain.'))
strings.append(Parser.parser('Tony likes rain and snow.'))
strings.append(Parser.parser('Bill does not like whatever Tony likes.'))
strings.append(Parser.parser('Bill likes whatever Tony does not like.'))
strings.append(Parser.parser('All Alpine members are skiers or climbers.'))
strings.append(Parser.parser('Tony and Bill and John are members of Alpine.'))
for i in strings:
    fopl=Converter.string2fopl(i)
    clauses=Converter.fopl2clause(fopl)
    for j in clauses:
        s.add_knowledge(j)
        '''
while True:
    command = input("Enter command:")
    if command == 'ak':
        knowledge = input("Enter the knowledge:")
        while knowledge != 'done':
            foplstring=Parser.parser(knowledge)
            if foplstring == 'undefined':
                print('The sentence pattern is not defined.')
            else:
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
        while conjecture != 'done':               
                foplstring=Parser.parser(conjecture)
                if foplstring == 'undefined':
                    print('The sentence pattern is not defined.')
                else:
                    print('The FOPL string is {}.'.format(foplstring))
                    fopl=Converter.string2fopl(foplstring)
                    fopl.negate()
                    clauses=Converter.fopl2clause(fopl)
                    print(s.solve(clauses))
                conjecture = input("Enter the conjecture:")
    elif command == 'quit':
        print('Byebye')
        break
    else:
        print('No such commend. Please try again.')