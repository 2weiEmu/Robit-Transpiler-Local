from re import match

from SyntaxNode import *


def is_valid_var_or_arr_index(string: str) -> bool:
    return match("[a-zA-Z0-9\[\]]", string)

def is_all_caps(string: str):
    return string == string.upper()

"""
TODO: more strict syntax checking rules -> e.g. nothing else should be on the same line as 'ELSE'
"""

# I need to make sure that changing expected actually works.
# time to make an expected object

class Expected:

    def __init__(self, expected_list = ['any']):
        self.expected = expected_list

    def update_expected(self, new_expected):
        self.expected = new_expected
    
    def __str__(self):
        return str(self.expected)


# should this have an 'expected' token -> for better error checking?
def add_to_tree(rootNode: SyntaxNode, string: str, line_number: int, expected: Expected) -> SyntaxNode:
    
    t = string.split()
    if t==[]:
        return rootNode
    # * OUTPUT
    # is output statement?
    if t[0].lower() == "output":

        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: OUTPUT, expected one of the following: {expected}")
            exit()
        
        # output written in all capitals?
        if t[0] == "OUTPUT":
            # yes

            rootNode.add_child(SyntaxNode(
                'output',
                parent=rootNode
            ))

            string = " ".join(t[1:])
            string = string.split(",")

            for s in string:
                s = s.strip()
                add_to_tree(
                    rootNode.children[0], 
                    s, line_number, 
                    expected=Expected(['expression', 'string', 'var'])
                    )

            return rootNode

        else:
            print(f"Syntax Error on Line {line_number}: 'OUTPUT' not in all capitals.")
            exit()

    # * INPUT
    # case if is input statement
    elif t[0].lower() == "input":
        
        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: INPUT, expected one of the following: {expected}")
            exit()

        # input written in all caps?
        if t[0] == "INPUT":
            # yes
            
            rootNode.add_child(SyntaxNode(
                'input',
                rootNode
            ))

            string = string.split()
            add_to_tree(rootNode.children[0], string[1], line_number, expected=Expected(['var']))
            return rootNode

        # not writtein all caps
        else:
            print(f"Syntax Error on Line {line_number}: 'INPUT' not in all capitals.")
            exit()

    # * ENDWHILE
    elif t[0].lower() == "endwhile":

        if is_all_caps(t[0]):
            pass

        else:
            print(f"Syntax Error on Line {line_number}: 'ENDWHILE' not in all capitals.")
            exit()

    # * IF-STATEMENT
    elif t[0].lower() == "if":
        
        if not(is_all_caps(t[0])):
            print(f"Syntax Error on Line {line_number}: 'IF' not in all capitals.")
            exit()

        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: IF, expected one of the following: {expected}")
            exit()

        # add 'if' node to root
        rootNode.add_child(SyntaxNode(
            'if', 
            parent=rootNode
            )
        )

        # rootNode = if node
        rootNode = rootNode.children[0]

        # add condition to if node
        # TODO: (we actually have to add to the tree HERE)
        rootNode.add_child(SyntaxNode(
            'condition',
            parent=rootNode
        ))

        # is next node then node?
        if t[-1].lower() == "then":
            
            if not(is_all_caps(t[-1])):
                print(f"Syntax Error on Line {line_number}: 'THEN' not in all capitals.")
                exit()
            
            # add if-body to if node
            expected.update_expected(['any'])
            rootNode.add_child(SyntaxNode(
                'if-body',
                parent=rootNode
            )
            )

            # return if-body as new root
            return rootNode.children[1]

        else:
            # set expected to then statement (as that was missing)
            expected.update_expected(['then'])
            # return if node
            return rootNode
            
    # * THEN
    elif t[0].lower() == 'then':
        if not(is_all_caps(t[0])):
            print(f"Syntax Error on Line {line_number}: 'THEN' not in all capitals.")
            exit()

        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: IF, expected one of the following: {expected}")
            exit()
        
        # if found and not break -> expected back to any
        expected.update_expected(['any'])

        # add if-body as new child to if node
        rootNode.add_child(SyntaxNode(
            'if-body',
            parent=rootNode
        ))

        # Give back the if-body as where to append (condition is child[0])
        return rootNode.children[1]

    # * ELSE
    elif t[0].lower() == 'else':

        if not(is_all_caps(t[0])):
            print(f"Syntax Error on Line {line_number}: 'ELSE' not in all capitals.")
            exit()

        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: ELSE, expected one of the following: {expected}")
            exit()
        
        if rootNode.parent.value != 'if':
            print(f"Else statement not inside IF block, on line: {line_number}")
            exit()
        
        rootNode = rootNode.parent

        rootNode.add_child(
            SyntaxNode(
                'else-body',
                parent=rootNode
            )
        )
        rootNode = rootNode.children[2]

        # return else-body
        return rootNode

    # * ENDIF
    elif t[0].lower() == 'endif':
        
        # I know this is getting dumb -> consider putting in all caps method
        if not(is_all_caps(t[0])):
            print(f"Syntax Error on Line {line_number}: 'ENDIF' not in all capitals.")
            exit()
        
        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: ENDIF, expected one of the following: {expected}")
            exit()
        
        expected.update_expected(['any'])
        
        # skip back to IF statement node (from else-body or if-body), then to the place we were before
        return rootNode.parent.parent

    # * WHILE
    # case if is while statement
    elif t[0].lower() == "while":

        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: WHILE, expected one of the following: {expected}")
            exit()

        # WHILE writtein in all caps?
        if t[0] == "WHILE":
            # yes
            pass

        else:
            print(f"Syntax Error on Line {line_number}: 'WHILE' not in all capitals.")
            exit()

    elif t[0].lower() == "declare":

        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: DECLARE, expected one of the following: {expected}")
            exit()
        
        if not(is_all_caps(t[0])):
            print(f"Syntax Error on Line {line_number}: 'DECLARE' not in all capitals.")
            exit()
        
        rest_declare = " ".join(t[1:])
        # {VARIABLE}: ARRAY[EXP:EXP] OF {TYPE}

        rootNode.add_child(
            SyntaxNode(
                'array',
                parent=rootNode
            )
        )
        rootNode = rootNode.children[-1]

    # TODO: expected never seems to go to a THEN statement?

    # if (expected == ['then']):
    #     print("HI, missing a THEN, are we?")
    #     exit()

    # if (expected != ['any']):
    #     print("SOMETHING WAS EXPECTED!", expected)
    #     exit()
    # else:
    return rootNode

def in_expected(expected: Expected, keyword):

    return (keyword.lower() in expected.expected or expected.expected[0] == 'any')