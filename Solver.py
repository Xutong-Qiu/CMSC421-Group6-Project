
from coreClasses import *
import numpy as np

class Solver:
    #clauses: an array of clauses
    def __init__(self):
        self.kb = np.array([]) #knowledge base
        self.uniPre = np.array([])
        
    def add_knowledge(self, new_k):
        if not self.contain_knowledge(new_k):
            self.kb = np.append(self.kb,new_k)
        for predicate in new_k.predicates:
            if not predicate in self.uniPre:
                self.uniPre = np.append(self.uniPre, predicate)

    def contain_knowledge(self, k):
        for i in self.kb:
            if k == i:
                return True
        return False

    def solvable(self, conjecture):
        for predicate in conjecture.predicates:
            if not predicate in self.uniPre:
                return False
        return True


    def res(self):
        kbcopy = np.array(self.kb)
        for i in range(0, len(kbcopy)):
            for j in range(i+1, len(kbcopy)):
                if i == j:
                    continue
                result = kbcopy[i].resolution(kbcopy[j])
                print('result: {} |{} -> {}'.format(kbcopy[i],kbcopy[j],result))
                if  result != None:
                    if result.is_empty():
                       return True
                    else:
                        kbcopy = np.append(kbcopy, result)
        return False
                
    




