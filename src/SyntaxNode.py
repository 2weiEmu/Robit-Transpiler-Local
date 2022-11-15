"""
Types of Nodes:

rootnode
OUTPUT
INPUT

ASSIGNMENT
ARRAY ASSIGNMENT
BODY / BRANCH
IF-CONDITION
ELSE-BODY
CONDITION
VARIABLE
OPERATOR
CASE-CONDITION
WHILE
REPEAT
(For loop can be just simply transformed into a while loop)

VARIABLE
CONSTANTS
EXPRESSIONS

Example of a Syntax Tree for the following program:

x <- (2 * 3) + 5

CASE OF x * 2

    3 : OUTPUT "three", x
    5 : OUTPUT "five", x
    10 : OUTPUT "ten", x
    OTHERWISE : OUTPUT "None"

ENDCASE

                SYNTAX_TREE
                /          \
            ASSIGNMENT      \
            /       \        \
        ADD OP    VAR : x     \
        /   \                CASE
    MUL OP C : 5             /   \
    /   \                MUL OP  CONDITION_BODY   
  C : 2, C : 3          /   \       /       \
                   VAR : x, C : 2  condition \
                                            BODY

Also considering switching around the values for ASSIGNMENT

Nodes Evaluated from left-to-right.
Post-Order (Right?)
LRP, Left, Right, Parent


Array Declaration Syntax:
(type checking is going to have to wait a bit)
DECLARE house : ARRAY[1:10] OF INT

    CREATE_ARRAY
    /   |   |   \
VAR:x, EXP, EXP, TYPE


consider reducing things such as addition and multiplication
etc. down to one operation thing - where the symbol is just
an extra child in the middle

The pseudocode of how the system works

-> user enters Pseudocode (as by the specifications, also in the README.)

Split into lines

Construct new Syntax Node attached to Root Node

    If OUTPUT statement:

        Check Syntax:
            is OUTPUT first word, all capital?

        deconstruct line into:
            OUTPUT node
                remove OUTPUT from line
                take rest of the statements -> should be comma seperated
                (seperate line by commas)
                    apply deconstruction on the rest of the all the nodes,
                    and add to this node as if it were the root (i.e. pass the root)
                

    IF ASSIGNMENT statement:
        Check a '<-' is present
        Create new Assignment Node

        split by '<-'
            Create new nodes appended to assignment
            ndoe -> first the variable node
            second the expression node
    
    IF DECLARE statement:
        
        remove keywords from String
        Create syntax node and append
        
        
Create python code from syntax tree

    Syntax Node

"""


class SyntaxNode:

    def __init__(self, value, transform, parent = None):
        self.value = value
        self.transform = transform
        self.parent = parent
        self.children = []

    def add_child(self, new_child) -> None:
        self.children.append(new_child)

    def __str__(self):
        return f"val={self.value}, transform={self.transform}\nChildren=[{f'{chr(10)}'.join([str(c) for c in self.children])}]"
    