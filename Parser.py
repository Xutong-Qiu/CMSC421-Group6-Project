import nltk
from pattern.en import pluralize, singularize
from nltk.stem import WordNetLemmatizer

#using the following import command if not work
#from pattern.text.en import pluralize, singularize

#### run the following once to install or download necessary libraries###
# pip install pattern
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

verbose = True
new = True     # set to true when analyzing new syntax
lemmatizer = WordNetLemmatizer()

def parser(sentence):
    
    tokens = nltk.word_tokenize(sentence)   
    standardTags = nltk.tag.pos_tag(tokens)               # the standard tag set has a zillion tags   
    tags = nltk.tag.pos_tag(tokens, tagset='universal')   # 'universal' is a simplified tag set
    syntax = [item[1] for item in tags]

    if(syntax == ['NOUN', 'VERB', 'ADJ', '.']):  # Jack is smart.
        modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN'][0]
        fopl = modifier +'(' + noun + ')'

    elif(syntax == ['NOUN', 'VERB', 'ADJ', 'CONJ', 'ADJ', '.']): # Jack is smart and/or kind.
        # 'CONJ' can be 'and', 'or'
        modifiers = [item for item in tags if item[1] == 'ADJ']
        noun = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN'][0]
        conj = [item[0] for item in tags if item[1] == 'CONJ'][0]
        if(conj == 'or'):
            symbol = ' | '
        elif(conj == 'and'):
            symbol = ' & '
        else:
            return('invalid symbol')
        fopl = modifiers[0][0] +'(' + noun + ')' + symbol + modifiers[1][0] +'(' + noun + ')'

    elif(syntax == ['NOUN', 'VERB', 'DET', 'NOUN', '.']): # Jack is a student. 
        # 'VERB' is 'is' 
         nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        # noun = [item[0] for item in tags if item[1] == 'NOUN'][0]
         verb = [item[0] for item in tags if item[1] == 'VERB'][0]
         det = [item[0] for item in tags if item[1] == 'DET'][0]
         if verb == 'is' or verb == 'are':
            fopl = nouns[1] + '(' + nouns[0] + ')'
         else:
            if det == 'all' or det == 'every':
                fopl = 'All(X) ((' + nouns[1] + '(X) & ' + '(' + nouns[0] + '(X)))'
            elif det == 'some':
                fopl = 'Ex(X) ((' + nouns[1] + '(X) | ' + '(' + nouns[0] + '(X)))'
            else:
                verb = lemmatizer.lemmatize(verb, 'v')
                fopl = verb + '(' + nouns[0] + ', ' + nouns[1] + ')'

    elif(syntax == ['DET', 'NOUN', 'VERB', 'DET', 'NOUN', '.']): # A dog chases a car.
        # VERB is not 'is' (to be or not to be)
         verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
         nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
         fopl = verb + '(' + nouns[0] + ', ' + nouns[1] + ')'

    #elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens == ['All', '', 'are', '']):
    
    

    
    elif(syntax == ['DET', 'NOUN', 'VERB', 'NOUN', '.']): 
        # All men are mortals. ∀(x) ((man(x)) → (mortal(x)))
        # No cat loves fish. ¬∃(X) ((cat(X) → (love(X, dog)))
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        (det, _) = tags[0]
        if(det == 'All') or (det == 'Every'):
            if(verb == 'is') or (verb == 'are'):
                fopl = 'All(X) ((' + nouns[0] + '(X) ->' + '(' + nouns[1] + '(X)))'
            else:
                fopl = 'All(X) ((' + nouns[0] + '(X) -> (' + verb + '(X, ' + nouns[1]+ ')))'
        elif det == 'Some':
            if(verb == 'is') or (verb == 'are'):
                fopl = 'Ex(X) ((' + nouns[0] + '(X) -> ' + '(' + nouns[1] + '(X)))'
            else:
                fopl = 'Ex(X) ((' + nouns[0] + '(X) -> (' + verb + '(X, ' + nouns[1]+ ')))'
        elif det == 'No':
            if(verb == 'is') or (verb == 'are'):
                fopl = '~Ex(X) ((' + nouns[0] + '(X) -> ' + '(' + nouns[1] + '(X)))'
            else:
                fopl = '~Ex(X) ((' + nouns[0] + '(X) -> (' + verb + '(X, ' + nouns[1]+ ')))'

    elif((syntax == ['ADV', 'DET', 'NOUN', 'VERB', 'NOUN', '.'] or 
    syntax == ['ADV', 'DET', 'NOUN', 'ADP', 'NOUN', '.']) and
    ((tokens[0] == 'Not' and tokens[1] == 'all') or ((tokens[0] == 'Not' and tokens[1] == 'every')))):
    # 'Not every cat likes dogs.'
    # 'Not all cats like dogs.'
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB' or item[1] == 'ADP'][0]
        if(verb == 'is') or (verb == 'are'):
                fopl = '~All(X) ((' + nouns[0] + '(X) -> ' + '(' + nouns[1] + '(X)))'
        else:
            fopl = '~All(X) ((' + nouns[0] + '(X) -> (' + verb + '(X, ' + nouns[1]+ ')))'

    # elif(syntax == ['DET', 'NOUN', 'VERB', 'ADV', 'ADJ', '.']):
        # All flowers are not fragrant.


    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens[0] == 'All' and 
    (tokens[2] == 'are' or tokens[2] == 'is')):
        # All water is precious.        All dogs are nice.
        # fopl = 'All(x) ' + tokens[3] + '(' + tokens[1] + ')' 
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        fopl = 'All(X) ((' + nouns[0] + '(X) -> ' + tokens[3] + '(X' + '))' 

    elif(syntax == ['DET', 'NOUN', 'VERB', 'ADJ', '.'] and tokens[0] == 'Some' and 
    (tokens[2] == 'are' or tokens[2] == 'is')):
        # Some water is expensive.      Some cats are nice.
        # fopl = '∃(x) ' + tokens[3] + '(' + tokens[1] + ')' 
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        fopl = 'Ex(X) ((' + nouns[0] + '(X) -> ' + tokens[3] + '(X' + '))' 

    elif(syntax == ['NOUN', 'VERB', 'DET', 'ADJ', 'NOUN', '.']): # Jack is a smart student.
        # 'VERB' is 'is' -- need to distinguish not 'is'
         modifier = [item[0] for item in tags if item[1] == 'ADJ'][0]
         nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
         fopl = modifier + '(' + nouns[0] + ') & ' + nouns[1] + '(' + nouns[0] + ')'

    # New edit
    elif(syntax == ['NOUN', 'VERB', 'NOUN', 'CONJ', 'NOUN', '.'] or
        syntax == ['NOUN', 'VERB', 'DET', 'NOUN', 'CONJ', 'DET', 'NOUN', '.']): 
        # Bill loves cheese and bacon.
        # Tom buys a notebook and a pencil.
        # 'CONJ' can be 'and', 'or'
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        conj = [item[0] for item in tags if item[1] == 'CONJ'][0]
        if(conj == 'or'):
            symbol = ' ∨ '
        elif(conj == 'and'):
            symbol = ' ∧ '
        else:
            return('invalid symbol')
        fopl = verb +'(' + nouns[0] + ', ' + nouns[1] + ')' + symbol + ' ' + verb +'(' + nouns[0] + ', ' + nouns[2] + ')'

    elif(syntax == ['DET', 'NOUN', 'DET', 'VERB', 'DET', 'NOUN', 'VERB', 'ADJ', '.'] or
        syntax == ['DET', 'NOUN', 'DET', 'VERB', 'NOUN', 'VERB', 'ADJ', '.']):
        # All student that finishes the homework is excellent.
        # Some student that take mathematics is smart.
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verb = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB'][0]
        modifier = [item for item in tags if item[1] == 'ADJ'][0][0]
        if (tokens[0] == 'All' or tokens[0] == 'Every'):
            fopl = 'All(X) (' + nouns[0] + '(X) ' + '∧  ' + verb + '(X, ' + nouns[1] + ') -> ' + modifier + '(X))'
        else:
            fopl = 'Ex(X) (' + nouns[0] + '(X) ' + '∧  ' + verb + '(X, ' + nouns[1] + ') -> ' + modifier + '(X))'
    
    elif(syntax == ['DET', 'NOUN', 'DET', 'VERB', 'DET', 'NOUN', 'VERB', 'NOUN', '.'] or
        syntax == ['DET', 'NOUN', 'DET', 'VERB', 'NOUN', 'VERB', 'NOUN', '.']):
        # Every person that buys a computer plays games.
        # Some student that take mathematics passes mathematics.
        nouns = [lemmatizer.lemmatize(item[0].lower(), 'n') for item in tags if item[1] == 'NOUN']
        verbs = [lemmatizer.lemmatize(item[0], 'v') for item in tags if item[1] == 'VERB']
        if (tokens[0] == 'All' or tokens[0] == 'Every'):
            fopl = 'All(X) (' + nouns[0] + '(X) ' + '∧  ' + verbs[0] + '(X, ' + nouns[1] + ') -> ' + verbs[1] + '(X, ' + nouns[2] + '))'
        else:
            fopl = 'Ex(X) (' + nouns[0] + '(X) ' + '∧  ' + verbs[0] + '(X, ' + nouns[1] + ') -> ' + verbs[1] + '(X, ' + nouns[2] + '))'

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

parser('Cats are lazy.')
parser('Socrates is mortal.')
parser('Jack is a student.')
parser('Cats love some fish.')

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
parser('All dogs are nice.')
parser('All water is precious.')
parser('Some water is expensive.')
parser('All men are mortals.')
parser('No cats loves dog.')
parser('Some cats catch mice.')
parser('Every dog loves humans.')
parser('Not all cats like dogs.')
parser('Not every cat likes dogs.')


parser('All men are mortals.')
parser('No cats loves dog.')
# parser('A cat loves fish.') # ['DET', 'NOUN', 'VERB', 'ADJ', '.'], nlkt library error.
parser('Some cats catch mice.')

# syllogism
#text = 'All people are mortal. Socrates is a person. Therefore, Socrates is mortal.'
#sentences = nltk.sent_tokenize(text)
#for sentence in sentences:
#   parser(sentence)

parser('Bill loves coffee and bacon.')
parser('Bill loves coffee or bacon.')
parser('Tom buys the a notebook and a pencil.')
parser('All student that finishes the homework is excellent.')
parser('Some student that take mathematics is smart.')
parser('All person that buys a computer plays games.')
parser('Some student that takes mathematics loves mathematics.')
