import numpy as np

#Constant variable
CONST = 0
VAR = 1
#This is the predicate class. It supports one or two variable predicates.
class Predicate:
    def __init__(self, name, data1, data1type, data2=None, data2type = None): 
        self.name=name
        self.data1=data1
        self.data1type=data1type
        self.data2=data2
        self.data2type=data2type
        self.negation=False

    def __str__(self):
        if self.negation==False:
            return '{}({})'.format(self.name,self.data1,self.data2)
        else:
            return '~{}({})'.format(self.name,self.data1,self.data2)

    def __eq__(self, predicate):
        if predicate == None:
            return False
        elif self.name==predicate.name:
            if self.data1type == CONST and self.data2type == CONST and predicate.data1type == CONST and predicate.data2type == CONST:
                return self.data1 == predicate.data1 and self.data2 == predicate.data2
            elif self.data1type == CONST and self.data2type == VAR and predicate.data1type == CONST and predicate.data2type == VAR:
                return self.data1 == predicate.data1
            elif self.data1type == VAR and self.data2type == CONST and predicate.data1type == VAR and predicate.data2type == CONST:
                return self.data2 == predicate.data2
            elif self.data1type == VAR and self.data2type == VAR and predicate.data1type == VAR and predicate.data2type == VAR:
                return True
            else: return False
        else: return False

    def negate(self):
        self.negation = not self.negation
    
    #Tell whether two predicates are unifiable. If so, return the unifier as a list.
    #Example:
    #[True]: the two predicates are unifiable and no substitution is needed to unify.
    #[True X Y CONST]: the two predicates are unifiable and X needs to be substituted by Y, where Y is a CONST
    #[False]: the two predicates are not unifiable
    def unifiable(self, other):
        if self.name == other.name:
            if self.data2type != None:
                if self.data1type == CONST and (self.data1 == other.data1) and (self.data2type == CONST) and (self.data2 == other.data2):
                    return [True]
                elif self.data1type == VAR and (self.data2type == CONST) and (self.data2 == other.data2):
                    if other.data1type==CONST:
                        return [True, self.data1, other.data1,CONST]
                    else: 
                        return [True]
                elif self.data2type == VAR and (self.data1type == CONST) and (self.data1 == other.data1):
                    if other.data2type==CONST:
                        return [True, self.data2, other.data2, CONST]
                    else: 
                        return [False]
                elif self.data1type == VAR and (self.data2type == VAR):
                    if other.data1type==CONST and other.data2type==CONST:
                        return [True, self.data1, other.data1, CONST, self.data2, other.data2, CONST]
                    elif other.data1type==CONST and other.data2type==VAR:
                        return [True, self.data1, other.data1, CONST, self.data2, other.data2, VAR]
                    elif other.data1type==VAR and other.data2type==VAR:
                        return [True, self.data1, other.data1, VAR, self.data2, other.data2, VAR]
                    else:
                        return [True, self.data1, other.data1, VAR, self.data2, other.data2, CONST]
                else: return [False]
            else:
                if self.data1type == CONST and self.data1 == other.data1:
                    return [True]
                elif self.data1type == VAR:
                    if other.data1type==CONST:
                        return [True, self.data1, other.data1, CONST]
                    else: 
                        return [True]
                else:  
                    return [False]
        else: return [False]

    #The function takes in a sublist and do the substitution.
    #The sublist is returned by "unifiable"
    def substitution(self, sublist):
        if not sublist[0]: raise ValueError('invalid sublist')
        if len(sublist) >= 4:
            if self.data1== sublist[1]:
                if self.data1type==CONST: raise ValueError('error replacing constant') 
                self.data1=sublist[2]
                self.data1type = sublist[3]
            if self.data2== sublist[1]:
                if self.data2type==CONST: raise ValueError('error replacing constant') 
                self.data2=sublist[2]
                self.data2type = sublist[3]
        if len(sublist) > 4:
            if self.data1== sublist[4]:
                if self.data1type==CONST: raise ValueError('error replacing constant') 
                self.data1=sublist[5]
                self.data1type = sublist[6]
            if self.data2== sublist[4]:
                if self.data2type==CONST: raise ValueError('error replacing constant') 
                self.data2=sublist[5]
                self.data2type = sublist[6]            
 
                

#This is the clause class
class Clause:
    def __init__(self, predicates):
        self.predicates=predicates
    
    def add_predicate(self, predicate):
        for i in self.predicates:
            if i == predicate:
                return
        np.append(self.predicates, predicate)

    def __str__(self):
        s=self.predicates[0].__str__()
        for i in range(1, len(self.predicates)):
            s += ' V ' + self.predicates[i].__str__()
        return s
        
    #This function carries out the resolution process. 
    def resolution(self, clause):
        for i in range(0,len(self.predicates)):
            for j in range(0,len(clause.predicates)):
                if self.predicates[i].name==clause.predicates[j].name and self.predicates[i].negation != clause.predicates[j].negation:
                    #print(i,j)
                    sub=self.predicates[i].unifiable(clause.predicates[j])
                    result = np.append(self.predicates,clause.predicates)
                    result= np.delete(result,i)
                    result= np.delete(result,len(self.predicates)+j-1)
                    for n in result:
                        n.substitution(sub)
                    return Clause(result)
        return None

#This is the first order predicate logic class which will be used by parser and intepreter.
#The class is implemented in binary tree
AND=1
OR=2
EXIST=3
ALL=4
NEG=5
class FOPL:
    def __init__(self, op, p1, p2):
        self.op=op
        if isinstance(op,Predicate):
            self.p1=None
            self.p2=None
        else:
            self.p1=p1
            self.p2=p2
    
    def __str__(self):
        if isinstance(self.op, Predicate):
            return '{}'.format(self.op)
        elif self.op==AND:
            return 'AND({},{})'.format(self.p1,self.p2)
        elif self.op==OR:
            return 'OR({},{})'.format(self.p1,self.p2)
        elif self.op==ALL:
            return 'ALL[{}]({})'.format(self.p2,self.p1)
        elif self.op==EXIST:
            return 'EXIST[{}]({})'.format(self.p2,self.p1)
        elif self.op==NEG:
            return 'NEG({},{})'.format(self.p1,self.p2)


    def negate(self):
        if isinstance(self.op,Predicate):
            self.op.negate()
        elif self.op == AND:
            self.op = OR
            self.p1.negate()
            self.p2.negate()
        elif self.op == OR:
            self.op = AND
            self.p1.negate()
            self.p2.negate()
        elif self.op == NEG:
            self.p1
        elif self.op == EXIST:
            self.op = ALL
            self.p1.negate()
        elif self.op == ALL:
            self.op = EXIST
            self.p1.negate()
    

   
class Solver:
    #clauses: an array of clauses
    def __init__(self, clauses=np.array([])):
        self.kb = clauses #knowledge base

    def add_knowledge(self, new_k):
        #incomplete: check duplication
        self.kb = np.append(self.kb,new_k)

    def res(self):
       0
    




#debug code
a = Predicate("likes", 'X', VAR)#likes(X)
#a.negate()#~likes(X)
b = Predicate("likes", 'a', CONST)#likes(a)
c = Predicate("food", 'b', CONST)#food(b)
d=Predicate("food", 'b', CONST)#food(b)
#c.negate()#~food(b)
clause1=Clause(np.array([a,c]))#likes(X)V~food(b)
clause2=Clause(np.array([b,d]))#likes(a)Vfood(b)
print(clause1)
'''#print(a.negation)
print(clause1.resolution(clause2))
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
y.negate()
print(y)

