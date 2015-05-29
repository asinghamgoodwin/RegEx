def findBuddy(expression, location): #can take in a string or a list, knows whether you're trying to match ( or )
    counter = 0

    if expression[location] == ")": #if we're trying to match a closed one
        indexList = range(location, -1, -1) #start on that close paren (it'll +1) and go backwards through the string to the beginning
    else: #if we're trying to match an open paren 
        indexList = range(location, len(expression)) #start on that open paren (it'll -1) and go forwards through the string

    for i in indexList: 
        if expression[i] == "(":
            counter -= 1
        elif expression[i] == ")":
            counter += 1
        if counter == 0:
            return i



def parens(alphabet, stringExpression):
    expression = list(stringExpression)

    #first find all the stars and deal with them
    starList = []
    for i in range(len(expression)):
        if expression[i] == "*":
            starList.append(i)

    #this for loop takes care of all of the stars that directly follow a character
    starList.reverse() #largest to smallest
    for star in starList:
        if expression[star-1] in alphabet+["."]: #if it is immediately after a character or .
            starList.remove(star) #take it out of the list, because it has been dealt with
            if not (expression[star-2] == "(" and expression[star+1] == ")"): #and our a* isn't surrounded by parens
                expression.insert(star-1,"(") #put a ( before the character
                expression.insert(star+2,")") #put a ) before what comes after the star (which has no moved over one)
                for i in range(len(starList)): #look through the rest of the star positions...
                    if starList[i] > star: #...for any stars appearing later in the expression
                        starList[i] += 2 #and add two to their position, because the expression has grown by 
    
    #the only stars left in the list are ones right after a ), and this while loop takes care of them
    starList.reverse()
    while len(starList) > 0:
        star = starList[0]
        if expression[star-1] == ")": #double check just to be sure
            starList.remove(star)
            closeP = star-1
            openP = findBuddy(expression, closeP) #to find the open paren that goes with this close paren, everything inside is getting *'d
            if expression[openP-1] != "(" or expression[star+1] != ")": #if our (abc)* isn't surrounded by parens
                expression.insert(openP,"(")
                expression.insert(star+2,")")
                for i in range(len(starList)):
                    if starList[i] > openP:
                        starList[i] += 1
                    if starList[i] > star:
                        starList[i] += 1


    #the rest of this is to take care of the |'s
    barList = []
    for i in range(len(expression)):
        if expression[i] == "|":
            barList.append(i)

    while len(barList) > 0:
        bar = barList[0]
        barList.remove(bar)
        #finding the start and end of the or
        counter = 0
        for j in range(bar,len(expression)):
            if expression[j] == "(":
                counter += 1
            elif expression[j] == ")":
                counter -= 1
            if counter == -1:
                endOr = j #this must be the end of the or, since its the first unmatched close paren after the |
                break
        startOr = findBuddy(expression, endOr) #and its buddy is the start of the or

        #checking to see if both halves are enclosed within parenthesis and adding them in if not
        if expression[bar+1] != "(" or expression[endOr-1] != ")": #if the second half isn't inside parens
            expression.insert(endOr, ")") #put a close paren right before the end
            expression.insert(bar+1, "(") #put an open paren right before the character after the |
            for i in range(len(barList)):
                if barList[i] > bar:
                    barList[i] += 1
                if barList[i] > endOr:
                    barList[i] += 1
            
        if expression[startOr+1] != "(" or expression[bar-1] != ")": #if the first half isn't inside parens
            expression.insert(bar, ")") #put a close paren right before the |
            expression.insert(startOr+1, "(") #pyt an open paren right before the character after the start
            for i in range(len(barList)):
                if barList[i] > bar:
                    barList[i] += 1
                if barList[i] > startOr:
                    barList[i] += 1


    #making the list back into a string
    new = ""
    for char in expression:
        new += char
   
    return new


#this is exactly the same as the parens function, except that if there is a |
#it puts a special character (for now || but maybe that's confusing)
#at the beginning of the parenthesis so that you know that you're about to see
#something of the form (Machine1)|(Machine2), which helps out my Matching functions.
def parensPLUS(alphabet, stringExpression):
    expression = list(stringExpression)

    #first find all the stars and deal with them
    starList = []
    for i in range(len(expression)):
        if expression[i] == "*":
            starList.append(i)

    #this for loop takes care of all of the stars that directly follow a character
    starList.reverse() #largest to smallest
    for star in starList:
        if expression[star-1] in alphabet+["."]: #if it is immediately after a character or .
            starList.remove(star) #take it out of the list, because it has been dealt with
            if not (expression[star-2] == "(" and expression[star+1] == ")"): #and our a* isn't surrounded by parens
                expression.insert(star-1,"(") #put a ( before the character
                expression.insert(star+2,")") #put a ) before what comes after the star (which has no moved over one)
                for i in range(len(starList)): #look through the rest of the star positions...
                    if starList[i] > star: #...for any stars appearing later in the expression
                        starList[i] += 2 #and add two to their position, because the expression has grown by 
    
    #the only stars left in the list are ones right after a ), and this while loop takes care of them
    starList.reverse()
    while len(starList) > 0:
        star = starList[0]
        if expression[star-1] == ")": #double check just to be sure
            starList.remove(star)
            closeP = star-1
            openP = findBuddy(expression, closeP) #to find the open paren that goes with this close paren, everything inside is getting *'d
            if expression[openP-1] != "(" or expression[star+1] != ")": #if our (abc)* isn't surrounded by parens
                expression.insert(openP,"(")
                expression.insert(star+2,")")
                for i in range(len(starList)):
                    if starList[i] > openP:
                        starList[i] += 1
                    if starList[i] > star:
                        starList[i] += 1


    #the rest of this is to take care of the |'s
    barList = []
    for i in range(len(expression)):
        if expression[i] == "|":
            barList.append(i)

    while len(barList) > 0:
        bar = barList[0]
        barList.remove(bar)
        #finding the start and end of the or
        counter = 0
        for j in range(bar,len(expression)):
            if expression[j] == "(":
                counter += 1
            elif expression[j] == ")":
                counter -= 1
            if counter == -1:
                endOr = j #this must be the end of the or, since its the first unmatched close paren after the |
                break
        startOr = findBuddy(expression, endOr) #and its buddy is the start of the or

        #checking to see if both halves are enclosed within parenthesis and adding them in if not
        if expression[bar+1] != "(" or expression[endOr-1] != ")": #if the second half isn't inside parens
            expression.insert(endOr, ")") #put a close paren right before the end
            expression.insert(bar+1, "(") #put an open paren right before the character after the |
            for i in range(len(barList)):
                if barList[i] > bar:
                    barList[i] += 1
                if barList[i] > endOr:
                    barList[i] += 1
            
        if expression[startOr+1] != "(" or expression[bar-1] != ")": #if the first half isn't inside parens
            expression.insert(bar, ")") #put a close paren right before the |
            expression.insert(startOr+1, "(") #pyt an open paren right before the character after the start
            for i in range(len(barList)):
                if barList[i] > bar:
                    barList[i] += 1
                if barList[i] > startOr:
                    barList[i] += 1

        expression.insert(startOr+1, "|") #put a | right after the start of the whole thing
        expression.insert(startOr+1, "|") #and another one
        for i in range(len(barList)):
            if barList[i] > startOr:
                barList[i] += 2


    #making the list back into a string
    new = ""
    for char in expression:
        new += char
   
    return new





A = "1.*(01)*1(000|1*)"
newA = "1(.*)((01)*)1((000)|(1*))"
newerA = '1(.*)((01)*)1(||(000)|(1*))'
B = "1(1(11)*1)*"
newB = "1((1((11)*)1)*)"
C = "1(11(1*))*(1*)*"
newC = "1((11(1*))*)((1*)*)"
D = "((0((10)*)1)|(1((111)*)))"
newD = "((0((10)*)1)|(1((111)*)))"
newerD = '(||(0((10)*)1)|(1((111)*)))'
E = "1(011*)*1"
newE = "1((01(1*))*)1"

##print "Tests!"
##print parens(["1", "0"], A) == newA
##print parens(["1", "0"], B) == newB
##print parens(["1", "0"], C) == newC
##print parens(["1", "0"], D) == newD
##print parens(["1", "0"], E) == newE
##
##print parensPLUS(["1", "0"], A) == newerA
##print parensPLUS(["1", "0"], D) == newerD


