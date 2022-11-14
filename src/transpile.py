from SyntaxNode import *
from re import match

def is_valid_var_or_arr_index(string: str) -> bool:
    return match("[a-zA-Z0-9\[\]]", string)

def is_all_caps(string: str):
    return string == string.upper()

# should this have an 'expected' token -> for better error checking?
def add_to_tree(rootNode: SyntaxNode, string: str, line_number: int) -> None:
    
    t = string.split()
    
    # is output statement?
    if t[0].lower() == "output":
        
        # output written in all capitals?
        if t[0] == "OUTPUT":
            # yes

            rootNode.add_child(SyntaxNode(
                'output',
                "print(__allchildren)"
            ))

            string = " ".join(t[1:])
            string = string.split(",")

            for s in string:
                s = s.strip()
                add_to_tree(rootNode.children[0], s, line_number)

        else:
            print(f"Syntax Error on Line {line_number}: 'OUTPUT' not in all capitals.")

    # case if is input statement
    elif t[0].lower() == "input":
        
        # input written in all caps?
        if t[0] == "INPUT":
            # yes
            
            rootNode.add_child(SyntaxNode(
                'input'
                "__child1 = input()"
            ))

            string = string.split()
            add_to_tree(rootNode.children[0], string[1], line_number)

        # not writtein all caps
        else:
            print(f"Syntax Error on Line {line_number}: 'INPUT' not in all capitals.")


    elif t[0].lower() == "endwhile":

        if is_all_caps(t[0]):
            

        else:
            print(f"Syntax Error on Line {line_number}: 'ENDWHILE' not in all capitals.")

    # case if is while statement
    elif t[0].lower() == "while":

        # WHILE writtein in all caps?
        if t[0] == "WHILE":
            # yes
            pass

        else:
            print(f"Syntax Error on Line {line_number}: 'WHILE' not in all capitals.")


