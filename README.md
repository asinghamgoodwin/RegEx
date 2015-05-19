I’ve made a program that allows me to check whether a string belongs to a specified regular language.

First, I convert the given regular expression into a nondeterministic finite automaton (NFA, a state machine that allows “free” transitions) to represent that language. Imagining a state machine drawn on paper, I check the string by putting a penny on the start state and then moving it through the state machine with each character in the string, duplicating the pennies on those “free” transitions and moving them all through the NFA until the end of the string, checking if any ended up in an “accept” state.

So far, I’ve written this according what I learned about regular expressions in my theoretical computer science class, but I know that regular expressions are used a lot in real world programming and are slightly different, so I’m hoping to add on to this project including:

-the rest of the operators: ^, $, ?, +, {m,n}

-options to make it greedy or not

-finding a match anywhere in the string instead of just matching the whole string exactly
