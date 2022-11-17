from re import match

from SyntaxNode import *


def is_valid_var_or_arr_index(string: str) -> bool:
    return match("[a-zA-Z0-9\[\]]", string)

def is_all_caps(string: str):
    return string == string.upper()

def in_expected(expected: list, keyword):

    return (keyword.lower() in expected or expected[0] == 'any')


"""
TODO: more strict syntax checking rules -> e.g. nothing else should be on the same line as 'ELSE'
"""

# should this have an 'expected' token -> for better error checking?
def add_to_tree(rootNode: SyntaxNode, string: str, line_number: int, expected: list) -> SyntaxNode:
    
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
                    expected=['expression', 'string', 'var']
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
            add_to_tree(rootNode.children[0], string[1], line_number, expected=['var'])
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

        if t[-1].lower() == "then":
            
            if not(is_all_caps(t[-1])):
                print(f"Syntax Error on Line {line_number}: 'THEN' not in all capitals.")
                exit()
            
            # add if-body to if node
            expected = ['any']
            rootNode.add_child(SyntaxNode(
                'if-body',
                parent=rootNode
            )
            )

            # return if-body as new root
            return rootNode.children[1]

        else:
            # set expected to then statement (as that was missing)
            expected = ['then']
            print("expecting a then next")
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
        expected = ['any']

        # add if-body as new child to if node
        rootNode.add_child(SyntaxNode(
            'if-body',
            parent=rootNode
        ))

        # Give back the if-body as where to append (condition is child[0])
        return rootNode.children[1]

    # * ELSE
    elif t[0].lower() == 'else':
        pass

    # * ENDIF
    elif t[0].lower() == 'endif':
        
        # I know this is getting dumb -> consider putting in all caps method
        if not(is_all_caps(t[0])):
            print(f"Syntax Error on Line {line_number}: 'ENDIF' not in all capitals.")
            exit()
        
        if not(in_expected(expected, t[0])):
            print(f"Unexpected Keyword: ENDIF, expected one of the following: {expected}")
            exit()
        
        expected = ['any']
        
        # skip back to IF statement node, then to the place we were before
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

    # TODO: expected never seems to go to a THEN statement?

    # if (expected == ['then']):
    #     print("HI, missing a THEN, are we?")
    #     exit()

    # if (expected != ['any']):
    #     print("SOMETHING WAS EXPECTED!", expected)
    #     exit()
    # else:
    return rootNode
