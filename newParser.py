###  a more legit parser for regular expression patterns  ##

#   regex             <-  expression+ %make_regex
#
#   expression        <-  matcher modifier? %make_expression
#
#   matcher           <-  capture_group / any_char / plaintext
#
#   capture_group     <-  "(" regex ("|" regex)* ")" %make_capture_group
#
#   any_char          <-  "."
#
#   plaintext         <-  ("0" %make_plaintext / "1" %make_plaintext)
#
#   modifier          <-  star
#
#   star              <-  "*" %make_star


class Regex():
    def __init__(self, expressionList):
        self.expressionList = expressionList

    def __repr__(self):
        return "".join(map(lambda x: x.__repr__(), self.expressionList))


class Expression():
    def __init__(self, matcher, modifier=None):
        self.matcher = matcher
        self.modifier = modifier

    def __repr__(self):
        if self.modifier != None:
            return self.matcher.__repr__()+self.modifier.__repr__()
        return self.matcher.__repr__()


##### MATCHERS #####
class Matcher():
    pass #not really sure what to do here

class CaptureGroup(Matcher):
    def __init__(self, regex):
        self.regex = regex

    def __repr__(self):
        return "<"+self.regex.__repr__()+">"

class Pipe(CaptureGroup):
    def __init__(self, regex1, regex2):
        self.regex1 = regex1
        self.regex2 = regex2

    def __repr__(self):
        return "<("+self.regex1.__repr__()+")|("+self.regex2.__repr__()+")>"


class AnyChar(Matcher):
    def __init__(self):
        pass

    def __repr__(self):
        return "."


class Character(Matcher):
    def __init__(self, character):
        self.character = character

    def __repr__(self):
        return self.character

# add in a class for escaped characters? probably not...


##### MODIFIERS #####
class Modifier():
    pass

class Star(Modifier):
    def __init__(self):
        pass

    def __repr__(self):
        return "*"

# later on add in +, ?, anchors (^, $), and more?

##### READING EXPRESSIONS ####

ALPHABET = ["0", "1"]

MODIFIERS = ["*"]

def findBuddy(expression, location): 
    """ helper function to find the matching paren
    takes a string or a list, knows whether you're matching ( or )
    outputs the index of the match
    """

    # if we're trying to match a closed one
    if expression[location] == ")":
        # start on that close paren and go backwards through the string to the beginning
        indexList = range(location, -1, -1)

    # if we're trying to match an open paren 
    else:
        # start on that open paren and go forwards through the string
        indexList = range(location, len(expression))

    counter = 0
    # the counter will immediately be either +1 or -1 since our indexList includes initial paren
    for i in indexList: 
        if expression[i] == "(":
            counter -= 1
        elif expression[i] == ")":
            counter += 1
        if counter == 0:
            return i

def parenthesizePipeIfNeeded(regex):
    """ add parens around the whole regex if there's a | that is not properly contained """
    counter = 0
    for char in regex:
        if char == "(":
            counter -= 1
        elif char == ")":
            counter += 1
        elif char == "|":
            if counter == 0:
                return "("+regex+")"
    return regex


def parse(regex):
    regex = parenthesizePipeIfNeeded(regex)
    expressionList = []

    # looking for expressions to put into the list
    # EXPRESSION  <-- MATCHER MODIFIER?
    i = 0
    while i < len(regex):
        if regex[i] == ".":
            matcher = AnyChar()
            i += 1

        elif regex[i] in ALPHABET:
            matcher = Character(regex[i])
            i += 1

        elif regex[i] == "\\": # an escaped character (checking if it is \)
            matcher = Character(regex[i+1])
            i += 2

        elif regex[i] == "(":
            closeParen = findBuddy(regex, i)
            expressionInParens = regex[i+1:closeParen]

            if "|" in expressionInParens:
                pipeLocation = expressionInParens.find("|") # this will just find the first instance
                matcher = Pipe(parse(expressionInParens[:pipeLocation]), parse(expressionInParens[pipeLocation+1:]))

            else:
                matcher = CaptureGroup(parse(expressionInParens))

            i = closeParen+1

        # if we aren't seeing any matcher (ex. a close paren or a * out of context)
        else:
            return "FAILURE - "+regex[i]+" doesn't make sense at spot "+str(i+1)


        modifier = None
        # Reminder: i has been augmented to now point to the next spot (potential modifier or matcher)
        # if the next thing is a modifier, it must get lumped with this matcher
        if i < len(regex) and regex[i] in MODIFIERS:
            if regex[i] == "*":
                modifier = Star()
                i += 1
            else:
                return "FAILURE - not dealing with "+regex[i]+" modifier yet"

        expressionList.append(Expression(matcher, modifier))

    return Regex(expressionList)


##### TESTS #####
testList = ["10*",
            "(10)*",
            "111(010)*111",
            "(00|11)",
            "(00|11|01)"
            ]

for test in testList:
    print test
    regex = parse(test)
    print map(lambda x: x.__repr__(), regex.expressionList)
    print ""









