import nltk

#run the following once
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

verbose = True
new = True     # set to true when analyzing new syntax

def parser(sentence):
    
    tokens = nltk.word_tokenize(sentence)   
    standardTags = nltk.tag.pos_tag(tokens)               # the standard tag set has a zillion tags   
    tags = nltk.tag.pos_tag(tokens, tagset='universal')   # 'universal' is a simplified tag set
    syntax = [item[1] for item in tags]

    if(syntax == ['NOUN', 'VERB', 'ADJ', '.']):
        modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
        noun = [item[0] for item in tags if item[1] == 'NOUN'][0]
        fopl = modifier +'(' + noun + ')'   
    elif(syntax == ['NOUN', 'VERB', 'ADJ', 'CONJ', 'ADJ', '.']):  # 'CONJ' can be 'and', 'or'
        modifiers = [item for item in tags if item[1] == 'ADJ']
        noun = [item[0] for item in tags if item[1] == 'NOUN'][0]
        conj = [item[0] for item in tags if item[1] == 'CONJ'][0]
        if(conj == 'or'):
            symbol = ' | '
        elif(conj == 'and'):
            symbol = ' & '
        else:
            return('invalid symbol')
        fopl = modifiers[0][0] +'(' + noun + ')' + symbol + modifiers[1][0] +'(' + noun + ')' 
    elif(syntax == ['NOUN', 'VERB', 'DET', 'NOUN', '.']):           # 'VERB' is 'is' 
         nouns = [item for item in tags if item[1] == 'NOUN']
        # noun = [item[0] for item in tags if item[1] == 'NOUN'][0]
         verb = [item[0] for item in tags if item[1] == 'VERB'][0]
         if(verb == 'is'):
             fopl = nouns[1][0] + '(' + nouns[0][0] + ')'
         else:
             fopl = verb + '(' + nouns[0][0] + ', ' + nouns[1][0] + ')'
    elif(syntax == ['DET', 'NOUN', 'VERB', 'DET', 'NOUN', '.']):    # VERB is not 'is' (to be or not to be) 
         verb = [item[0] for item in tags if item[1] == 'VERB'][0]
         nouns = [item for item in tags if item[1] == 'NOUN']
         fopl = verb + '(' + nouns[0][0] + ', ' + nouns[1][0] + ')'
    #elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens == ['All', '', 'are', '']):
    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens[0] == 'All' and tokens[2] == 'are'):
        fopl = 'All(x) ' + tokens[3] + '(' + tokens[1] + ')' 
    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens[0] == 'Some' and tokens[2] == 'are'):
        fopl = 'Ex(x) ' + tokens[3] + '(' + tokens[1] + ')' 
    elif(syntax == ['NOUN', 'VERB', 'DET', 'ADJ', 'NOUN', '.']):    # 'VERB' is 'is'  -- need to distinguish not 'is'
         modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
         nouns = [item for item in tags if item[1] == 'NOUN']
         fopl = modifier + '(' + nouns[0][0] + ') & ' + nouns[1][0] + '(' + nouns[0][0] + ')'
    elif(new):  
        fopl = 'undefined'    
    else:
        return ('Syntax not recognized: ', syntax)
        
    if(verbose):
        print('sentence: ', sentence)
        print('tokens: ', tokens)
        print('standard tags: ', standardTags)
        print('simple tags:  ', tags)
        print('syntax: ', syntax)
        print('fopl: ', fopl)
        print()
        
    return fopl

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
parser('All people are mortal.')
parser('Some cats are nice.')
    
# syllogism
#text = 'All people are mortal. Socrates is a person. Therefore, Socrates is mortal.'
#sentences = nltk.sent_tokenize(text)
#for sentence in sentences:
#   parser(sentence)