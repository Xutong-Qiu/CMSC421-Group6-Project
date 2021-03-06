
from coreClasses import *
import numpy as np

class Solver:
    #clauses: an array of clauses
    def __init__(self):
        self.kb = np.array([]) #knowledge base
        self.uniPreName = np.array([])
        
    def add_knowledge(self, new_k):
        if not self.contain_knowledge(new_k):
            self.kb = np.append(self.kb,new_k)
        for predicate in new_k.predicates:
            if not self.contain_predicate(predicate):
                self.uniPreName = np.append(self.uniPreName, predicate.name)

    def contain_knowledge(self, k):
        for i in self.kb:
            if k == i:
                return True
        return False

    def contain_predicate(self, predicate):
        for i in self.uniPreName:
                if i == predicate.name:
                    return True
        return False
    
    def solvable(self, conjecture):
        #print(self.uniPreName)
        for clause in conjecture:
            for predicate in clause.predicates:
                if not self.contain_predicate(predicate):
                    print(predicate)
                    return False
        return True

    def copykb(self):
        a = np.array([])
        for i in self.kb:
            #print(i,i.copy())
            a = np.append(a,i.copy())
        return a

    def solve(self, conjectures):
        if not self.solvable(conjectures):
            return 'not enough info'
        else:
            support = conjectures
            kbcopy = self.copykb()
            answer = None
            lengthsupport=len(support)-1
            lengthkbcopy = len(kbcopy)-1
            while lengthsupport != len(support):
                #print(len(support),lengthsupport)
                lengthsupport=len(support)
                lengthkbcopy = len(kbcopy)
                #resolving with the set of support
                for i in range(0, len(support)):
                    for j in range(i+1, len(support)):
                        if i == j:
                            continue
                        result = support[i].resolution(support[j])
                        #print('not here')
                        print('Step: {} + {} -> {}'.format(support[i],support[j],result))
                        if  result != None:
                            if result.is_empty():
                                return 'True'
                            else:#check if knowledge exists, if not, add
                                exist = False
                                for k in support:
                                    if result == k:
                                        exist = True
                                if not exist:
                                    support = np.append(support, result)
                #resolving with premises
                for i in range(0, len(support)):
                    for j in range(0, len(kbcopy)):
                        #print('here12313131312',support[i],kbcopy[j])
                        result = support[i].resolution(kbcopy[j])
                        print('Step: {} + {} -> {}'.format(support[i],kbcopy[j],result))
                        if  result != None:
                            if result.is_empty():
                                return 'True'
                            else:#check if knowledge exists, if not, add
                                exist = False
                                for k in support:
                                    if result == k:
                                        exist = True
                                if not exist:
                                    support = np.append(support, result)
            return 'False'

'''
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
                
    '''




