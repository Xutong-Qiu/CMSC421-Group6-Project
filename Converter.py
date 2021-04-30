import re
import numpy as np
from coreClasses import *

def string2fopl(str):
    tokens=re.split('\s',str)
    #print(tokens)
    f, t = matchI(tokens)
    #print(f)
    return f


def  matchQ(tokens):
    ele=tokens.pop(0)
    a=re.match('^All\(([A-Z][a-z]*)\)$',ele)
    b=re.match('^Ex\(([A-Z][a-z]*)\)$',ele)
    #print(b.group(1))
    if a:
        fopl = FOPL(ALL,a.group(1), None)
    elif b:
        fopl = FOPL(EXIST,b.group(1), None)
    else:
        fopl = None
    return fopl

def  matchI(tokens):
    ele=tokens.pop(0)
    q = matchQ([ele])
    if q:
        if len(tokens)==0:
            return q, tokens
        f,t = matchI(tokens) 
        q.p2 = f
        return q, t
    #[ele]+tokens)
    f, t= matchF([ele]+tokens)  
    if len(t)==0:
        return f,t
    else:
        imp = re.match('^->',t[0])
        if not imp:
            ValueError('missing ->')
        else:
            t.pop(0)
            f1, t1 = matchF(t)
        return FOPL(IMP, f, f1), t1

def  matchF(tokens):
    ele=tokens.pop(0)
    '''q = matchQ([ele])
    if q:
        if len(tokens)==0:
            return q, tokens
        f,t=matchF(tokens)
        q.p2 = f
        return q, t'''
    #check ~
    neg=re.match('^~$',ele)
    if neg:
        f,t= matchF(tokens)
        f.negate()
        return f, t
    #check p|F, p->F, p&F, p
    p, t = matchP([ele])
    #print(p)
    if p !=None:
        if len(tokens)==0:
            #print(p,tokens)
            return p, tokens
        a = re.match('^&',tokens[0])
        o = re.match('^\|',tokens[0])
        imp = re.match('^->',tokens[0])
        if a:
            tokens.pop(0)
            f,t= matchF(tokens)
            return FOPL(AND, p, f), t
        elif o:
            tokens.pop(0)
            f,t= matchF(tokens)
            return FOPL(OR, p, f), t
        elif imp:
            tokens.pop(0)
            return FOPL(IMP, p, matchF(tokens)[0]), tokens
        else:
            #print(p)
            return p, t
    #check (F), (F)&F, (F)->F, (F)|F
    parenthesis = re.match('^\(',ele)
    if parenthesis:
        f,t = matchF(tokens)
        if len(tokens)==0 or not re.match('^\)',tokens[0]): ValueError('missing right parenthesis')
        tokens.pop(0)
        if len(tokens)==0:
            return f, tokens
        a = re.match('^&',tokens[0])
        o = re.match('^\|',tokens[0])
        imp = re.match('^->',tokens[0])
        if a:
            tokens.pop(0)
            f1,t1= matchF(tokens)
            return FOPL(AND, f, f1), t1
        elif o:
            tokens.pop(0)
            f1,t1= matchF(tokens)
            return FOPL(OR, f, f1), t1
        elif imp:
            tokens.pop(0)
            f1,t1= matchF(tokens)
            return FOPL(IMP, f, f1), t1

    ValueError('conversion failed: unsupported pattern')


def  matchP(tokens):
    ele=tokens.pop(0)
    neg=re.match('^~',ele)
    #two var
    two_var=re.match('^~?(\w+)\(([A-Z]\w*),([A-Z]\w*)\)$',ele)
    #one var back
    one_varb=re.match('^~?(\w+)\(([a-z]\w*),([A-Z]\w*)\)$',ele)
    #one var front
    one_varf=re.match('^~?(\w+)\(([A-Z]\w*),([a-z]\w*)\)$',ele)
    #two cons
    two_const=re.match('^~?(\w+)\(([a-z]\w*),([a-z]\w*)\)$',ele)

    single_var = re.match('^~?(\w+)\(([A-Z]\w*)\)$',ele)
    single_const = re.match('^~?(\w+)\(([a-z]\w*)\)$',ele)
    if two_var:
        p = Predicate(two_var.group(1), two_var.group(2), VAR, two_var.group(3), VAR)
    elif one_varb:
        p = Predicate(one_varb.group(1), one_varb.group(2), CONST, one_varb.group(3), VAR)
    elif one_varf:
        p = Predicate(one_varf.group(1), one_varf.group(2), VAR, one_varf.group(3), CONST)
    elif two_const:
        p = Predicate(two_const.group(1), two_const.group(2), CONST, two_const.group(3), CONST)
    elif single_var:
        p = Predicate(single_var.group(1), single_var.group(2), VAR)
    elif single_const:
        p = Predicate(single_const.group(1), single_const.group(2), CONST)
    else:
        return None, tokens
    if neg:
        p.negate()
    return FOPL(p, None, None), tokens



####################################
#########fopl2clause################
####################################

def fopl2clause(fopl):
  fopls=[]
  clauses=[]
  counter=0
  eliIMP(fopl,counter)
  fopl.distribute_or()
  breakintoClause(fopl,fopls)

  for i in range(len(fopls)):
    predicates=[]
    convert(fopls[i],predicates)
    clauses.append(Clause(predicates))

  return clauses

def convert (fopl, predicates):
  if fopl.op == OR:
    convert(fopl.p1, predicates)
    convert(fopl.p2, predicates)
  elif isinstance(fopl.op,Predicate):
    predicates.append(fopl.op)
#eliminate IMPLY also handle negation
def eliIMP(fopl,counter):
  if isinstance(fopl,FOPL):
    if fopl.op==IMP:
      fopl.eliminateIMP()
      eliIMP(fopl.p1,counter)
      eliIMP(fopl.p2,counter)
      
    elif fopl.op==NEG:
      fopl.negate()
      eliIMP(fopl,counter)
    elif fopl.op==ALL:
      fopl.eliminateALL()
      eliIMP(fopl,counter)
    elif fopl.op==EXIST:
      fopl.substitution([True,fopl.p1,'a'+str(counter),CONST])
    elif fopl.op==OR:
      #standardize same quantifier
      if (fopl.p1.op== ALL) and (fopl.p2.op== ALL):
        if fopl.p1.p1 == fopl.p2.p1:
          counter+=1
          fopl.substitution([True,fopl.p2.p1,fopl.p2.p1+str(counter),VAR])
      if (fopl.p1.op== EXIST) and (fopl.p2.op== EXIST):
        eliIMP(fopl.p1,counter)
        counter+=1
        eliIMP(fopl.p2,counter)
      else:
        eliIMP(fopl.p1,counter)
        eliIMP(fopl.p2,counter)
    elif fopl.op==AND:
      #standardize same quantifier
      if (fopl.p1.op==(ALL)) and (fopl.p2.op==(ALL)):
        if fopl.p1.p1 == fopl.p2.p1:
          counter+=1
          fopl.op.substitution([True,fopl.p2.p1,fopl.p2.p1+str(counter),VAR])
      if (fopl.p1.op== EXIST) and (fopl.p2.op== EXIST):
        eliIMP(fopl.p1,counter)
        counter+=1
        eliIMP(fopl.p2,counter)
      else:
        eliIMP(fopl.p1,counter)
        eliIMP(fopl.p2,counter)

#break into clauses
def breakintoClause(fopl,clauses):
  if isinstance(fopl.op,Predicate):
    clauses.append(fopl)
  elif fopl.op==AND:
    breakintoClause(fopl.p1,clauses)
    breakintoClause(fopl.p2,clauses)
  elif fopl.op==OR:

    clauses.append(fopl)


#string2fopl('All(X) person(X) & buy(X,computer) -> play(X,game)')
#tokens = ['~likes(asfd)']  Ex(Y) animal(Y) & loves(X,Y)
#string2fopl('( person(X) )')
#print(matchQ(['Ex(Y)']))   All(X) human(X) -> mortal(X)
#f= string2fopl('All(X) ~ ( climber(X) -> like(X,rain) )')
#f= string2fopl('All(X) human(X) -> mortal(X)')
#f1= string2fopl('Ex(Y) likes(Y,X)')
#print(f)
#result=fopl2clause(f1)
#for index in range(len(result)):
#  print(result[index])
#f.eliminateIMP()
#f.negate()
#print(f)

