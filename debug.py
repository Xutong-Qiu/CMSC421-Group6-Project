from coreClasses import *
from Solver import Solver


#debug code
a = Predicate("likes", 'X', VAR)#likes(X)
#a.negate()#~likes(X)
b = Predicate("likes", 'a', CONST)#likes(a)
c = Predicate("food", 'b', CONST)#food(b)
d=Predicate("food", 'b', CONST)#food(b)
c.negate()#~food(b)
clause1=Clause(np.array([a,c]))#likes(X)V~food(b)
clause2=Clause(np.array([b,d]))#likes(a)Vfood(b)
#clause1=Clause(np.array([c]))#likes(X)V~food(b)
#clause2=Clause(np.array([d]))#likes(a)Vfood(b)
#print(clause1)
#print(clause2)
print(clause1.resolution(clause2))
s = Solver()
s.add_knowledge(clause1)
s.add_knowledge(clause2)
print(s.res())
'''#print(a.negation)

#s=Solver()
test3=Clause(np.array([a]))
test4=Clause(np.array([b]))
#print(len(test3.resolution(test4).predicates))
sub=a.unifiable(b)
d.substitution(sub)
print(d)
print(a.unifiable(b))
'''
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
