from coreClasses import *
from Solver import Solver
import Converter
import Parser

s=Solver()
foplstring=Parser.parser('All humans are mortal.')
fopl=Converter.string2fopl(foplstring)
clauses1=Converter.fopl2clause(fopl)
for i in clauses1:
    #print('all humans are mortal')
    #print(i)
    s.add_knowledge(i)
foplstring=Parser.parser('Amy is human.')
fopl=Converter.string2fopl(foplstring)
clauses=Converter.fopl2clause(fopl)
for i in clauses:
    #print('amy is human')
    #print(i)
    s.add_knowledge(i)
foplstring=Parser.parser('Amy is mortal.')
fopl=Converter.string2fopl(foplstring)
fopl.negate()
clauses2=Converter.fopl2clause(fopl)
for i in clauses2:
    #print('amy is mortal')
    print('------')
#print('result')
#r1=clauses1[0].resolution(clauses2[0])
print(s.solve(clauses2))
#print(r1.resolution(clauses[0]))
'''
parser('Socrates is mortal.')
parser('Socrates is mortal and Greek.')
parser('Socrates is mortal or Greek.')
parser('Socrates is a philospher.')
parser('A dog chases a car.')
parser('Socrates is a mortal philospher.')
parser('Joe climbs a ladder.')
parser('Joe climbs a ladder.')

print('***Multiple sentences***\n')
text = 'A dog chases a car. Socrates is a mortal philospher. '
sentences = nltk.sent_tokenize(text)
for sentence in sentences:
    parser(sentence)
    
print("***Quantifiers***")
parser('Some cats are nice.')

parser('All men are mortals.')
parser('No cats loves dog.')
# parser('A cat loves fish.') # ['DET', 'NOUN', 'VERB', 'ADJ', '.'], nlkt library error.
parser('Some cats catch mice.')
'''
# syllogism
#text = 'All people are mortal. Socrates is a person. Therefore, Socrates is mortal.'
#sentences = nltk.sent_tokenize(text)
#for sentence in sentences:
#   parser(sentence)

'''
#debug code
a = Predicate("likes", 'X', VAR)#likes(X)
nota=Predicate("likes", 'X', VAR)
a.negate()
#a.negate()#~likes(X)
b = Predicate("likes", 'a', CONST)#likes(a)
c = Predicate("food", 'b', CONST)#food(b)
d=Predicate("food", 'b', CONST)#food(b)
c.negate()#~food(b)
clause1=Clause(np.array([a,c]))#likes(X)V~food(b)
clause2=Clause(np.array([b,d]))#likes(a)Vfood(b)
clause3=Clause(np.array([a]))
clause4=Clause(np.array([nota]))
#print(clause1)
#print(clause2)
print(clause3)
print(clause4)
s = Solver()
s.add_knowledge(clause3)
#print('is solvable? {}'.format(s.solvable([clause2])))
#print(clause1.resolution(clause2)==clause2.resolution(clause1))
print(s.solve([clause4]))
s.add_knowledge(clause2)
#print(s.res())
#print(a.negation)

#s=Solver()
test3=Clause(np.array([a]))
test4=Clause(np.array([b]))
#print(len(test3.resolution(test4).predicates))
sub=a.unifiable(b)
d.substitution(sub)
print(d)
print(a.unifiable(b))

#test FOPL
x = FOPL(a, None, None)
y=FOPL(ALL, x, 'X')
y.negate()
#y.negate()
#print(y)

ab3 = Clause([Predicate("ab", 'b', CONST, 'c', CONST)])#ab(b,c)
ab2 = Clause([Predicate("ab", 'a', CONST, 'b', CONST)])#ab(a,b)
in1=Clause([Predicate("in", 'e', CONST, 'f', CONST)])#in(e,f)
rt4 = Clause([Predicate("rt", 'd', CONST, 'c', CONST)])#rt
rt5 = Clause([Predicate("rt", 'b', CONST, 'f', CONST)])#rt
in6 = Predicate("in", 'X', VAR, 'Y', VAR)#in(X,Y)
in6.negate()#~in(X,Y)
rt6 = Predicate("rt", 'Z', VAR, 'Y', VAR)#rt(Z,Y)
rt6.negate()#~rt(Z,Y)
rt62 = Predicate("rt", 'Z', VAR, 'X', VAR)#rt(Z,X)
c6=Clause([in6,rt6,rt62])

rt7 = Predicate("rt", 'X1', VAR, 'Y1', VAR)#rt(X1,Y1)
rt7.negate()
for i in s.uniPre:
    print(i)

'''