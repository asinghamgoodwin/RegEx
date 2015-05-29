#How to use this code#

1) You'll need to supply an alphabet in the form of a list of strings, each one character.
2) Write your pattern string that defines the rules of your language. This should be a string containing only characters from your alphabet or ., (, ), |, * (note: I hope to add more capabilities soon!)
3) The string you want to check should be a string that only contains characters from the alphabet. My code will only make sure that the entire string matches your pattern exactly.
4) In the regexMatching.py file, you can either use the match() function (supplying an alphabet, pattern, and string to be checked), or you can define a Language and then check as many strings as you want for membership in that language using the checkString() method.

#Rough sketch of what it does#

I’ve made a program that allows me to check whether a string belongs to a specified regular language.

First, I convert the given regular expression into a nondeterministic finite automaton (NFA, a state machine that allows “free” transitions) to represent that language. Imagining a state machine drawn on paper, I check the string by putting a penny on the start state and then moving it through the state machine with each character in the string, duplicating the pennies on those “free” transitions and moving them all through the NFA until the end of the string, checking if any ended up in an “accept” state. (In reality, I don't keep track of two pennies if they ended up at the same state at the same time through different paths)

#Future Plans#

So far, I’ve written this according what I learned about regular expressions in my theoretical computer science class, but I know that regular expressions are used a lot in real world programming and are slightly different, so I’m hoping to add on to this project including:

-the rest of the operators: ^, $, ?, +, {m,n}

-options to make it greedy or not

-finding a match anywhere in the string instead of just matching the whole string exactly
