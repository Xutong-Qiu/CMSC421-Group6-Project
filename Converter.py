import re
import numpy as np
from coreClasses import *

def string2fopl(str):
    tokens=re.split('\s',str)
    print(tokens)
    return matchF(tokens)


def  matchQ(tokens):
    ele=tokens.pop(0)
    a=re.match('^All\(([A-Z][a-z]*)\)$',ele)
    b=re.match('^Ex\(([A-Z][a-z]*)\)$',ele)
    if a:
        fopl = FOPL(ALL,a.group(1), None)
    elif b:
        fopl = FOPL(EXIST,a.group(1), None)
    else:
        fopl = None
    return fopl

#def  matchI(tokens):

def  matchF(tokens):
    ele=tokens.pop(0)
    q = matchQ([ele])
    if q:
        if len(tokens)==0:
            return q
        q.p2 = matchF(tokens)
        return q
    #check ~
    neg=re.match('^~',ele)
    if neg:
        return matchF(tokens).negate()
    #check p|F, p->F, p&F, p
    p = matchP([ele])
    #print(p)
    if p !=None:
        if len(tokens)==0:
            return p
        a = re.match('^&',tokens[0])
        o = re.match('^\|',tokens[0])
        imp = re.match('^->',tokens[0])
        if a:
            tokens.pop(0)
            return FOPL(AND, p, matchF(tokens))
        elif o:
            tokens.pop(0)
            return FOPL(OR, p, matchF(tokens))
        elif imp:
            tokens.pop(0)
            return FOPL(IMP, p, matchF(tokens))
        else:
            #print(p)
            return p
    #check (F), (F)&F, (F)->F, (F)|F
    parenthesis = re.match('^\(',ele)
    if parenthesis:
        f = matchF(tokens)
        if len(tokens)==0 or not re.match('^\)',tokens[0]): ValueError('missing right parenthesis')
        tokens.pop(0)
        if len(tokens)==0:
            return f
        a = re.match('^&',tokens[0])
        o = re.match('^\|',tokens[0])
        imp = re.match('^->',tokens[0])
        if a:
            tokens.pop(0)
            return FOPL(AND, f, matchF(tokens))
        elif o:
            tokens.pop(0)
            return FOPL(OR, f, matchF(tokens))
        elif imp:
            tokens.pop(0)
            return FOPL(IMP, f, matchF(tokens))
    ValueError('conversion failed: unsupported pattern')


def  matchP(tokens):
    ele=tokens.pop(0)
    neg=re.match('^~',ele)
    #two var
    two_var=re.match('^~?(\w+)\(([A-Z]\w*),([A-Z]\w*)\)$',ele)
    #one var front
    one_varf=re.match('^~?(\w+)\(([a-z]\w*),([A-Z]\w*)\)$',ele)
    #one var back
    one_varb=re.match('^~?(\w+)\(([A-Z]\w*),([a-z]\w*)\)$',ele)
    #two cons
    two_const=re.match('^~?(\w+)\(([a-z]\w*),([a-z]\w*)\)$',ele)

    single_var = re.match('^~?(\w+)\(([A-Z]\w*)\)$',ele)
    single_const = re.match('^~?(\w+)\(([a-z]\w*)\)$',ele)
    if two_var:
        p = Predicate(two_var.group(1), two_var.group(2), VAR, two_var.group(3), VAR)
    elif one_varf:
        p = Predicate(one_varf.group(1), one_varf.group(2), VAR, one_varf.group(3), CONST)
    elif one_varb:
        p = Predicate(one_varb.group(1), one_varb.group(2), CONST, one_varb.group(3), VAR)
    elif two_const:
        p = Predicate(two_const.group(1), two_const.group(2), CONST, two_const.group(3), CONST)
    elif single_var:
        p = Predicate(single_var.group(1), single_var.group(2), VAR)
    elif single_const:
        p = Predicate(single_const.group(1), single_const.group(2), CONST)
    else:
        return None
    if neg:
        p.negate()
    return FOPL(p, None, None)

#string2fopl('All(X) ( person(X) & buy(X,computer) -> play(X,game) )')
#tokens = ['~likes(asfd)']
#string2fopl('( person(X) )')
print(string2fopl('All(X) ( person(X) & buy(X,computer) -> play(X,game) )'))