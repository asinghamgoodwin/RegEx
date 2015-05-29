######createStatesMASTER makes a list of states (with their transitions) from  an expression######
######Things left to do: add a language class, add a penny/transitioning system, deal with |########

from regexParens import parens, parensPLUS, findBuddy


#I decided to make Language a class so that if you had a bunch of strings to check in the same language
#We only have to make the NFA once, and then you can call checkString as many times as you want.

class Language():
    def __init__(self, alphabet, expression):
        self.alphabet = alphabet #a list with each character in the alphabet
        self.expression = parensPLUS(alphabet, expression) #parens adds in the appropriate parenthesis for the NFA maker
                                                        #should only include letters in self.alphabet and (,),|,*,.
        self.states = createStatesMASTER(self.alphabet, self.expression) #list with all of the states in the machine


    def checkString(self, string):
        
        currentStates = set([s for s in self.states if s.startState]) #just the start state so far
        for character in string:
            nextStates = set()
            for state in currentStates: #transition on that character
                nextStates.add(state.outDict[character])

            currentStates = nextStates #now these are are current states...
            #nextStates = set()


            def freeTransitions(state):
                possibleNewStates = set()
                y = state #y will get updated at each state we step through on a free transition to ensure that we get as far as possible
                while 'free' in y.outDict.keys():
                    if type(y.outDict['free']) == list: #if you could transition freely to multiple states
                        for newState in y.outDict['free']:
                            possibleNewStates.add(newState) #put each of them into the nextStates set
                        branch0 = y.outDict['free'][0]
                        branch1 = y.outDict['free'][1]
                        y = branch0 #keep the first one and keep going through this process of checking for free transitions
                        z = branch1
                        possibleNewStates.union(freeTransitions(z))
                    else:
                        y = y.outDict['free']
                    possibleNewStates.add(y)
                return possibleNewStates



            for state in currentStates: #...but we also have to deal with free transitions.
                                        #Keep every state in the set, but add every state we /could/ get to through a free transition
                currentStates = currentStates.union(freeTransitions(state))


##
##                y = state #y will get updated at each state we step through on a free transition to ensure that we get as far as possible
##                while 'free' in y.outDict.keys():
##                    if type(y.outDict['free']) == list: #if you could transition freely to multiple states
##                        for newState in y.outDict['free']:
##                            nextStates.append(newState) #put each of them into the nextStates set
##                        y = y.outDict['free'][0] #keep the first one and keep going through this process of checking for free transitions
##                        z = y.outDict['free'][1]
##                        #########how to I deal with adding in more states through free transitions for the other branch???########
##                    else:
##                        y = y.outDict['free']
##                    nextStates.add(y)
##            currentStates = currentStates.union(nextStates) #now add the states we got to freely to the states we got from the character transition
## 
        for state in currentStates:
            if state.acceptState:
                return True
        return False


                                       
class State():
    def __init__(self, name, alphabet, trap, waitForDict=None):
        self.alphabet = alphabet
        self.name = name #take this out in the final version
        self.acceptState = False #these both get updated after the state is created
        self.startState = False
        
        #if the trap state doesn't exist yet, we need to just make an empty transition dict
        #but if it has already been defined elsewhere, we can pass it in and make a dict
        #that sends everything to the trap for now, until later when we might change
        #some of the destinations to new states or add 'free' transitions
        if waitForDict == None: 
            self.outDict = {'0': trap, '1': trap}
        else:
            self.outDict = {}

    #this is just for printing out while debugging so you can see a text representation of the state machine
    def prettyDict(self):
        prettyDict = {}
        for key in self.outDict.keys():
            if type(self.outDict[key]) == list:
                prettyDict[key] = [self.outDict[key][0].name, self.outDict[key][1].name]
            else:
                prettyDict[key] = self.outDict[key].name
        return prettyDict


names = ['r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j',
     'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'] #this is nice for debugging/visualizing, but I'll get rid of it later on


#this is sort of the inside of recusive part of createStatesMASTER.
#it creates a bunch of states that together make some NFA.
#it takes in a state called "holding" which is whatever state comes before this machine
#and a second state to hold on to, holdingSTAR, in case the whole machine is getting *'d
def createStates(alphabet, expression, holding, trap, statesList, holdingSTAR=None):
    holding = holding
    holdingSTAR = holdingSTAR

    if expression[0] == "(" and findBuddy(expression, 0) == len(expression)-1 and expression[-2] != "*":
        expression = expression[1:-1] #we can take out parenthases if they enclose the whole machine
    
    i = 0
    while i < len(expression):
        x = expression[i]
        if x in alphabet+["."]: #if its just a regular character
            newState = State(names.pop(), alphabet, trap) #make the new state
            if x == ".":
                for char in alphabet: #if anything leads into it
                    holding.outDict[char] = newState #make a dict that always points there
            else: #otherwise, all can stay a trap except for this one character
                holding.outDict[x] = newState
                
            statesList.append(newState)

            holding = newState
            
            i += 1
            
        elif x == "(":
            close = findBuddy(expression, i)

            if expression[close-1] == "*": #if the whole machine inside of these parens gets *'d, we need to do some set-up:
                star = State(names.pop(), alphabet, trap) #make the state that allows us to circumvent the machine all together (0 iterations of the *)
                statesList.append(star)

                #set off to make the machine inside the parens. whatever comes out of that should lead into the next state, after the machine
                output = createStates(alphabet, expression[i+1:close-1], holding, trap, statesList, star)
                output.outDict['free'] = holding
                holding.outDict['free'] = star

                holding = star

            elif expression[i+1] == "|" and expression[i+2] == "|": #if this set of parens encases an OR
                #the expression has to be in the following format, starting at i:  (||(m1)|(m2))

                m1close = findBuddy(expression, i+3)
                separator = m1close+1
                    
                m1expression = expression[i+3:m1close+1]
                
                m1helper = State(names.pop(), alphabet, trap)
                statesList.append(m1helper)
                m1output = createStates(alphabet, m1expression, m1helper, trap, statesList)


                m2expression = expression[separator+1:close]
                
                m2helper = State(names.pop(), alphabet, trap)
                statesList.append(m2helper)
                m2output = createStates(alphabet, m2expression, m2helper, trap, statesList)

                holding.outDict['free'] = [m1helper, m2helper]

                endHelper = State(names.pop(), alphabet, trap)
                statesList.append(endHelper)
                
                m1output.outDict['free'] = endHelper
                m2output.outDict['free'] = endHelper

                holding = endHelper                

            
            else:     
                output = createStates(alphabet, expression[i+1:close], holding, trap, statesList)
                holding = output
            
            i = close+1


    return holding



def createStatesMASTER(alphabet, expression):
    statesList = []
    
    trap = State('trap', alphabet, 'place holder for trap state', True)
    for char in alphabet:
        trap.outDict[char] = trap
        
    start = State('start', alphabet, trap)
    start.startState = True

    statesList.append(trap)
    statesList.append(start)

    accept = createStates(alphabet, expression, start, trap, statesList)
    accept.acceptState = True

    return statesList
        

def match(alphabet, expression, string):
    language = Language(alphabet, expression)
    return language.checkString(string)



#print "Tests!"

binary = ['0', '1']

A = "1.*(01)*1(000|1*)"
B = "1(1(00)*1)*"
C = ".(11(0*))*(1*)" #didn't work with an extra * at the end.....why??
E = "1(011*)*."
F = "1(00|101)"

##aCheck1 = '111111000'
##aCheck2 = '1111110000'
##aCheck3 = '1001111'

##print match(binary, A, aCheck1) == True
##print match(binary, A, aCheck2) == False
##print match(binary, A, aCheck3) == True

##aLang = Language(binary, A)


##fCheck1 = "1101" #true
##fCheck2 = "100101" #false
##fCheck3 = "110" #false

##fLang = Language(binary, F)

##print match(binary, F, fCheck1) == True
##print match(binary, F, fCheck2) == False
##print match(binary, F, fCheck3) == False


##bLang = Language(binary, parens(binary, B))
##bCheck1 = '1100001' #true
##bCheck2 = '110000111' #true
##bCheck3 = '11000011' #false
##bCheck4 = '11000010' #false
##bCheck5 = '110001' #false
##bCheck6 = '1' #true
##
##bCheckList = [bCheck1, bCheck2, bCheck3, bCheck4, bCheck5, bCheck6]
##for s in bCheckList:
##    print bLang.checkString(s)


##print match(binary, B, bCheck2)

##cLang = Language(binary, parens(binary, C))
##cCheck1 = '0110001' #true
##cCheck2 = '01100010' #false
##cCheck3 = '01111' #true
##cCheck4 = '1111111' #true
##cCheck5 = '01110001' #false
##cCheck6 = '101' #false
##
##cCheckList = [cCheck1, cCheck2, cCheck3,cCheck4, cCheck5, cCheck6]
##for s in cCheckList:
##    print cLang.checkString(s)
##


#bList = createStatesMASTER(binary, parens(binary, B))
#cList = createStatesMASTER(binary, parens(binary, C))
#eList = createStatesMASTER(binary, parens(binary, E))

##
##for state in aLang.states:
##    print state.name
##    if state.acceptState == True:
##            print "acceptState"
##    print state.prettyDict()
##    print ''

#yay! substituting bList or cList in for eList will print out a description of the correct NFA for each.
