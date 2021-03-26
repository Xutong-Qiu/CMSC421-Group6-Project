import numpy as np

#Constant variable
CONST = 0
VAR = 1
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

    def __eq__(self, predicate):#incomplete
        if self.name==predicate.name:
            if self.data1type == CONST and self.data2type == CONST:
                return self.data1 == predicate.data1 and self.data2 == predicate.data2
            elif self.data1type == CONST and self.data2type == VAR:
                return self.data1 == predicate.data1
        else: return False

    def negate(self):
        self.negation = not self.negation
    

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
 
                


class Clause:
    def __init__(self, predicates):
        self.predicates=predicates
    
    def add_predicate(self, predicate):
        np.append(self.predicates, predicate)

    def __str__(self):
        s=""
        for i in self.predicates:
            s += i.__str__()+' '
        return s


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
c.negate()#~food(b)
clause1=Clause(np.array([a,c]))#likes(X)V~food(b)
clause2=Clause(np.array([b,d]))#likes(a)Vfood(b)
#print(a.negation)
print(clause1.resolution(clause2))
#s=Solver()
test3=Clause(np.array([a]))
test4=Clause(np.array([b]))
#print(len(test3.resolution(test4).predicates))
'''sub=a.unifiable(b)
d.substitution(sub)
print(d)
print(a.unifiable(b))'''


