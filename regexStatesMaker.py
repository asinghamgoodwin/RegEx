######createStatesMASTER makes a list of states (with their transitions) from  an expression######
######Things left to do: add a language class, add a penny/transitioning system, deal with |########

from regexParens import parens, findBuddy


class Language():
    def __init__(self, alphabet, expression):
        self.alphabet = alphabet #a list with each character in the alphabet
        self.expression = parens(alphabet, expression) #a string to be parsed
        #should only include letters in self.alphabet and (,),|,*,.
        self.states = createStatesMASTER(self.alphabet, self.expression) #list with all of the states in the machine


    def checkString(self, string):
        
        currentStates = set([self.states[1]]) #just the start state so far
        for character in string:

            #print character

            nextStates = set()
            for state in currentStates:
                nextStates.add(state.outDict[character])

            currentStates = nextStates
            nextStates = set()

            for state in currentStates:
                y = state
                while 'free' in y.outDict.keys():
                    y = y.outDict['free']
                    nextStates.add(y)
            currentStates = currentStates.union(nextStates)
            nextStates = set()

            #print "currentStates"
            #for state in currentStates:
            #    print state.name

            #print ''

        for state in currentStates:
            if state.acceptState:
                return True
        return False
                                       

class State():
    def __init__(self, name, alphabet, trap, waitForDict=None):
        self.alphabet = alphabet
        self.name = name
        self.acceptState = False
        self.startState = False
        if waitForDict == None:
            self.outDict = {'0': trap, '1': trap}
        else:
            self.outDict = {}

    def prettyDict(self):
        prettyDict = {}
        for key in self.outDict.keys():
            prettyDict[key] = self.outDict[key].name
        return prettyDict


names = ['r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j',
     'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'] #this is nice for debugging/visualizing, but I can probably get rid of it later on


def createStates(alphabet, expression, holding, trap, statesList, holdingSTAR=None):
    holding = holding
    holdingSTAR = holdingSTAR

    if expression[0] == "(" and findBuddy(expression, 0) == len(expression)-1:
        expression = expression[1:-1]

    
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

            if expression[close-1] == "*":
                star = State(names.pop(), alphabet, trap)
                statesList.append(star)

                output = createStates(alphabet, expression[i+1:close-1], holding, trap, statesList, star)
                output.outDict['free'] = holding
                holding.outDict['free'] = star

                holding = star
                
            else:     
                output = createStates(alphabet, expression[i+1:close], holding, trap, statesList)
                holding = output
            
            i = close+1

##        elif x == "|":
##            pass
          
    
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
        

def check(alphabet, expression, string):
    language = Language(alphabet, expression)
    return language.checkString(string)



#print "Tests!"

binary = ['0', '1']

B = "1(1(00)*1)*"
C = ".(11(0*))*(1*)" #didn't work with an extra * at the end.....why??
E = "1(011*)*."


##bLang = Language(binary, parens(binary, B))
##bCheck1 = '1100001' #true
bCheck2 = '110000111' #true
##bCheck3 = '11000011' #false
##bCheck4 = '11000010' #false
##bCheck5 = '110001' #false
##bCheck6 = '1' #true
##
##bCheckList = [bCheck1, bCheck2, bCheck3, bCheck4, bCheck5, bCheck6]
##for s in bCheckList:
##    print bLang.checkString(s)


print check(binary, B, bCheck2)

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


##for state in bList:
##    print state.name
##    if state.acceptState == True:
##            print "acceptState"
##    print state.prettyDict()
##    print ''

#yay! substituting bList or cList in for eList will print out a description of the correct NFA for each.
