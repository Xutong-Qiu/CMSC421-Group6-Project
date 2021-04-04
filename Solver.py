
from coreClasses import *
import numpy as np

class Solver:
    #clauses: an array of clauses
    def __init__(self, clauses=np.array([])):
        self.kb = clauses #knowledge base

    def add_knowledge(self, new_k):
        if not self.contain_knowledge(new_k):
            self.kb = np.append(self.kb,new_k)

    def contain_knowledge(self, k):
        for i in self.kb:
            if k == i:
                return True
        return False

    def res(self):
        for i in range(0, len(self.kb)):
            for j in range(i+1, len(self.kb)):
                if i == j:
                    continue
                result = self.kb[i].resolution(self.kb[j])
                print('result: {} |{} -> {}'.format(self.kb[i],self.kb[j],result))
                if  result != None:
                    if result.is_empty():
                       return True
                    else:
                        self.add_knowledge(result)
        return False
                
    




