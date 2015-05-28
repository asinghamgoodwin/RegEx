######createStatesMASTER makes a list of states (with their transitions) from  an expression######
######Things left to do: add a language class, add a penny/transitioning system, deal with |########

from regexParens import parens, findBuddy

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
        


##print "Tests!"

binary = ['0', '1']

B = "1(1(00)*1)*"
C = ".(11(1*))*(1*)"
E = "1(011*)*."

##bList = createStatesMASTER(binary, parens(binary, B))
##cList = createStatesMASTER(binary, parens(binary, C))
##eList = createStatesMASTER(binary, parens(binary, E))
##
##
##for state in eList:
##    print state.name
##    if state.acceptState == True:
##            print "acceptState"
##    print state.prettyDict()
##    print ''

#yay! substituting bList or cList in for eList will print out a description of the correct NFA for each.

