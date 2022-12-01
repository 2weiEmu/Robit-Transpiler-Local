from re import match

from SyntaxNode import *


def is_valid_var_or_arr_index(string: str) -> bool:
    return match("[a-zA-Z0-9\[\]]", string)

def is_all_caps(string: str):
    return string == string.upper()

"""
TODO: more strict syntax checking rules -> e.g. nothing else should be on the same line as 'ELSE'
TODO: have to make sure that when there is an if-statement it is also closed, i.e. that there is an ENDIF, and that tabs also matter.
But you can check on that later ->
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

# TODO: tab checking implementation
# TODO: endif / endcase / endwhile checking implementation
# I Think the EXPECTED() thing will just need more logic for that

# should this have an 'expected' token -> for better error checking?
def add_to_tree(rootNode: SyntaxNode, string: str, line_number: int, expected: Expected) -> SyntaxNode:
    

    # filtering out comments
    string = string.split("//")[0]

    t = string.split()
    if t==[]:
        return rootNode
    # * OUTPUT
    # is output statement?
    if t[0].lower() == "output":

        check_standard_keyword_syntax(t[0], expected, line_number)
 
        rootNode.add_child(SyntaxNode(
                'output',
                parent=rootNode
            ))

        string = " ".join(t[1:])
        string = string.split(",")

        for s in string:
            s = s.strip()
            add_to_tree(
                rootNode.children[-1], # adding to the last child of the rootnode (the one we just created)
                s, line_number, 
                expected=Expected(['expression', 'string', 'var', 'condition'])
                )

        return rootNode

    # * INPUT
    # case if is input statement
    elif t[0].lower() == "input":
        
        check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(SyntaxNode(
                'input',
                rootNode
            ))

        string = string.split()
        add_to_tree(rootNode.children[-1], # adding to the newest child of the rootnode -> the one we just added
            string[1], line_number, expected=Expected(['var']))
        return rootNode

    # * ENDWHILE
    elif t[0].lower() == "endwhile":

        if is_all_caps(t[0]):
            pass

        else:
            print(f"Syntax Error on Line {line_number}: 'ENDWHILE' not in all capitals.")
            exit()

    # * IF-STATEMENT
    elif t[0].lower() == "if":
        
        check_standard_keyword_syntax(t[0], expected, line_number)

        # add 'if' node to root
        rootNode.add_child(SyntaxNode(
            'if', 
            parent=rootNode
            )
        )

        # rootNode = if node
        rootNode = rootNode.children[-1] # changing rootnode to the latest added node, new rootnode

        # add condition to if node

        temp = t[1:]
        if temp[-1].lower() == 'then':
            temp = temp[:-1]
        condition_string = " ".join(temp)

        rootNode = add_to_tree(rootNode, condition_string, line_number, Expected(['condition']))

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
        check_standard_keyword_syntax(t[0], expected, line_number)
        
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

        check_standard_keyword_syntax(t[0], expected, line_number)
        
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
        
        check_standard_keyword_syntax(t[0], expected, line_number)
        
        expected.update_expected(['any'])
        
        # skip back to IF statement node (from else-body or if-body), then to the place we were before
        return rootNode.parent.parent
    
    # * FOR-LOOP
    elif t[0].lower() == 'for':

        check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(
            SyntaxNode(
                'for-loop',
                parent=rootNode
            )
        )

        # for-loop node
        rootNode = rootNode.children[-1]

        # FOR {VARIABLE/ARRAY_INDEX} <- {EXP} TO {EXP} [STEP {EXP}]
        # t = [FOR, VAR/ARRAY_INDEX | <- | EXP, TO, EXP, STEP, EXP]
        # we know for a fact that VAR/ARRAY_INDEX does not have any spaces inside

        # t = [VAR/ARR<- EXP, TO, EXP -> can be any size, STEP, EXP -> can be any size, right]
        # rest_string = VAR/ARR[]<-[]EXP TO EXP STEP EXP
        rest_string = " ".join(t[1:])
        # halves = [VAR/ARR<-EXP, EXP STEP EXP]
        halves = rest_string.split(" TO ") # using ' TO ' as string, because it makes sure there are spaces on either side
        first_half = halves[0].split("<-")
        var = first_half[0].strip()
        var_exp = first_half[1].strip()

        # adding the variable node
        rootNode = add_to_tree(rootNode, var, line_number, Expected(['var']))

        # adding the expression, for the starting points (starting range)
        rootNode = add_to_tree(rootNode, var_exp, line_number, Expected(['expression']))

        expressions = halves[1].split(" STEP ")

        # adding where to STOP. -> don't forget that in Pseudocode both sides are inclusive, yea mate?
        rootNode = add_to_tree(rootNode, expressions[0], line_number, Expected(['expression']))

        # adding the body as a new child
        rootNode.add_child(
            SyntaxNode(
                'for-body',
                parent=rootNode
            )
        )

        if len(expressions) > 1:
            rootNode = add_to_tree(rootNode, expressions[1], line_number, Expected(['expression']))

        if rootNode.children[-1].value != 'for-body':
            return rootNode.children[-2] # return the for-body if there was a STEP added
        else:
            return rootNode.children[-1] # otherwise return the for-body as it was the last one (if no step was added)

    # * NEXT
    elif t[0].lower() == 'next':

        check_standard_keyword_syntax(t[0], expected, line_number)

        # at this point the person should be in the for-body, let's see if they actually are
        if rootNode.value != 'for-body':
            print(f"NEXT was not inside body of FOR Statement on line {line_number}")
            exit()
        
        if rootNode.parent.value != 'for-loop':
            print(f"NEXT was not inside FOR statement on line {line_number}")
            exit()

        # go back from the for-body, to the for-loop, and then back the parent of that.
        return rootNode.parent.parent

    # * CASE
    if expected.expected[0] == 'case':
        
        rootNode.add_child(
            SyntaxNode(
                'cond-body',
                parent=rootNode
            )
        )

        # the newest conditional body added
        rootNode = rootNode.children[-1]
        
        # don't forget that string is the line ->
        t = string.split(":")

        # checking if this is the last statement
        if (k:=t[0].strip()).lower() == 'otherwise':
            
            if not(is_all_caps(k)):
                print(f"Syntax Error on line {line_number}, OTHERWISE is not written in all capitals")
                exit()
            
            # rootNode = newest cond-body
            rootNode.add_child(
                SyntaxNode(
                    'otherwise',
                    parent=rootNode
                )
            )
            
            rootNode.add_child(
                SyntaxNode(
                    'cond-sub-body',
                    parent=rootNode
                )
            )
            # ! This technically means that you cannot actually declare arrays in CASE statements (sorry, but I don't expect anyone to do that)
            rootNode = add_to_tree(rootNode, t[1], line_number, expected)

            expected.update_expected(['endcase'])

            # return the cond-sub-body
            return rootNode.children[1]

        else:
            
            rootNode = add_to_tree(rootNode, t[0].split()[1], line_number, Expected(['var', 'expression']))

            rootNode.add_child(
                SyntaxNode(
                    'cond-sub-body',
                    parent=rootNode
                )
            )
            # rootnode = conditional_sub_body
            rootNode = rootNode.children[-1]
            rootNode = add_to_tree(rootNode, t[1].strip(), line_number, expected)

            # cond-sub-body -> cond-body -> case, which is where the next statement has to be added again
            return rootNode.parent.parent


    # * CASEOF
    elif t[0].lower() == 'case':

        check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(
            SyntaxNode(
                'case',
                parent=rootNode
            )
        )

        # rootnode = CASE
        rootNode = rootNode.children[-1]
        # before: t = CASE OF {VAR}, now t = VAR (could also just do -1, but I have feeling like that could go wrong, a bit at least, even though technically VAR / ARR are not supposed to have spaces inside)
        t = t[2:]

        rootNode = add_to_tree(rootNode, t[0].strip(), line_number, Expected(['var']))

        expected.update_expected(['case'])

        # returning the CASE node
        return rootNode

    # in this case we have to check for the expected, because the line does not really have a strong identifier, for that

    # * ENDCASE
    elif t[0].lower() == 'endcase':

        check_standard_keyword_syntax(t[0], expected, line_number)
        
        expected.update_expected(['any'])

        if rootNode.value != 'cond-sub-body':
            print(f"ENDCASE not while inside a condition case statement on line: {line_number}")
            exit()

        if rootNode.parent.value != 'cond-body':
            print(f"ENDCASE not inside a CASE statement on line: {line_number}")
            exit()

        # from cond-sub-body -> cond-body -> case -> root before that.
        return rootNode.parent.parent.parent

    # * REPEAT
    elif t[0].lower() == 'repeat':

        check_standard_keyword_syntax(t[0], expected, line_number)

        # create a new repeat child for the main branch thing
        rootNode.add_child(
            SyntaxNode(
                value='repeat',
                parent=rootNode
            )
        )

        # move rootnode to that repeat branch
        rootNode = rootNode.children[-1]

        # create new body for that repeat branch
        rootNode.add_child(
            SyntaxNode(
                'repeat-body',
                parent=rootNode
            )
        )

        # return the repeat-body as part of the branch
        return rootNode.children[-1]

    # * UNTIL
    elif t[0].lower() == 'until':

        check_standard_keyword_syntax(t[0], expected, line_number)

        # rootnode should in this case be a repeat-body, and the parent of that a repeat node (though they technically come in pairs, but still better to make sure)
        
        if rootNode.value != 'repeat-body':
            print(f"UNTIL statement not in the body of a REPEAT statement on line: {line_number}")
            exit()

        if rootNode.parent.value != 'repeat':
            print(f"UNTIL not in a REPEAT statement on line: {line_number}")
            exit()

        # back to the repeat node
        rootNode = rootNode.parent

        rest_of_statement = "".join(t[1:])

        rootNode = add_to_tree(rootNode, rest_of_statement, line_number, Expected(['condition']))

        # return the parent of the repeat statemnt, i.e the one that came before the repeat statement
        return rootNode.parent

    # * WHILE
    # case if is while statement
    elif t[0].lower() == "while":

        check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(
            SyntaxNode(
                'while',
                parent=rootNode
            )
        )

        check_standard_keyword_syntax(t[-1], Expected(['do']), line_number)
        
        rest_string = " ".join(t[1:-1])

        # rootnode = WHILE node
        rootNode = rootNode.children[-1]

        # adding condition as new node to WHILE node
        rootNode = add_to_tree(rootNode, rest_string, line_number, Expected(['condition']))

        # adding the while-body as a new node to WHILE node
        rootNode.add_child(
            SyntaxNode(
                'while-body',
                parent=rootNode
            )   
        )

        return rootNode.children[-1] # returning the while-body

    # * ENDWHILE
    elif t[0].lower() == "endwhile":

        check_standard_keyword_syntax(t[0], expected, line_number)

        if rootNode.value != 'while-body':
            print(f"ENDWHILE on line {line_number} is not in a WHILE statement body.")
            exit()

        if rootNode.parent.value != 'while':
            print(f"ENDWHILE on line {line_number} is not in WHILE statement.")
        
        # going back to parent of the while statement (current rootNode = while-body)
        return rootNode.parent.parent

    # * DECLARE
    elif t[0].lower() == "declare":

        check_standard_keyword_syntax(t[0], expected, line_number)
        
        rest_declare = " ".join(t[1:])
        # {VARIABLE}: ARRAY[EXP:EXP] OF {TYPE}

        rootNode.add_child(
            SyntaxNode(
                'array',
                parent=rootNode
            )
        )
        # rootnode = array node
        rootNode = rootNode.children[-1]
                                #012345
        # rest_declare = [{VAR}, ARRAY[EXP, EXP] OF {TYPE}]
        rest_declare = rest_declare.split(":")

        rest_declare[0] = rest_declare[0].strip() # making sure the variable has no trailing or leading useless stuff
        rootNode = add_to_tree(rootNode, rest_declare[0], line_number, Expected(['var']))

        rest_declare[1] = (rest_declare[1].strip())[6:] # stripping and cutting off 'ARRAY[' part
        rootNode = add_to_tree(rootNode, rest_declare[1], line_number, Expected(['expression']))

        # temporary = [EXP, OF {TYPE}]
        temporary = (rest_declare[2].strip()).split(']')
        rootNode = add_to_tree(rootNode, temporary[0], line_number, Expected(['expression']))

        rootNode = add_to_tree(rootNode, (temporary[1].strip())[3:], line_number, Expected(['type']))

        rootNode = rootNode.parent
        return rootNode
    
    # * ASSIGNMENT
    elif "<-" in string:

        if not(in_expected(expected, 'assignment')):
            print(f"Unexpected Assignment on line {line_number}, instead expected: {expected.expected}")
            exit()

        rootNode.add_child(
            SyntaxNode(
                'assignment',
                parent=rootNode
            )
        )

        # making assignment node the new root
        rootNode = rootNode.children[-1]

        values = string.split("<-")

        if not(is_valid_var_or_arr_index(values[0])):
            print(f"Variable to be assigned to, on line {line_number} does not have a valid format.")
            exit()

        print(values[0].strip())
        print(values[1].strip())
        rootNode = add_to_tree(rootNode, values[0].strip(), line_number, Expected(['var']))

        rootNode = add_to_tree(rootNode, values[1].strip(), line_number, Expected(['expression', 'string', 'var']))

        return rootNode.parent # Return the parent of the assignment node

    # * TYPES
    elif string.lower() in ['integer', 'char', 'real', 'string', 'boolean']:


        if not(is_all_caps(string)):
            print(f"The type given on {line_number} was not in all capitals.")
            exit()
        
        if not(in_expected(expected, 'type')):
            print(f"Unexpected type on line {line_number}")
            exit()
        
        rootNode.add_child(
            SyntaxNode(
                f'type-{string.lower}',
                parent=rootNode
            )
        )

        return rootNode

    # * STRINGS
    # ! The guide says nothing about string concanetation using +, so I will not implement this.
    elif "'" in string or '"' in string:

        if not(in_expected(expected, 'string')):
            print(f"Unexpected STRING on line: {line_number}, instead expected: {expected.expected}")
            exit()

        string = string.strip()
        if "'" in string:
            if string[0] != string[-1] or string[0] != "'":
                print(f"String not of valid format, it does not both begin and end with ' or \" on line {line_number}")
                exit()
            
        if '"' in string:
            if string[0] != string[-1] or string[0] != '"':
                print(f"String not of valid format, it does not both begin and end with ' or \" on line {line_number}")
                exit()


        if string[0] in string[1:-1]:
            print(f"You used too many ' or \" symbols in the body of your string.")
            exit()
        
        rootNode.add_child(
            SyntaxNode(
                f'string-{string[1:-1]}',
                parent=rootNode
            )
        )
        return rootNode

    # ! GOOD that we check for conditions first, then expressions, which means that the two following statements will evaluate to the same thing (and that the second one won't break):
    # 5 + 5 = 1
    # 1 = 5 + 5
    # * CONDITION
    # ok wait, seeing as we use '=' to check for equality here, we can actually check for that, and the other symbols as they are also unique to this, and other places where it could have come up were already checked
    # ! don't forget that in booleans here != actually is written as <>
    elif contains_bool_op(string):
        
        if not(in_expected(expected, 'condition')):
            print(f"Unexpected CONDITION on line {line_number}, instead expected one of: {expected.expected}")
            exit()

        # ! time to care about brackets.
        # ! there may also be issues that occur when putting lone values directly inside brackets i.e. like 5 <> (CAR), don't do that
        # ! may contain numbers as immediate values -> but not strings

        # making sure that the given string has the right amount of brackets
        if string.count("(") != string.count(")"):
            print(f"You have unmatched brackets in your condition on line: {line_number}")
            exit()

        t_string = string

        while (t_string[0] == "(" and t_string[-1] == ")"):
            t_string = t_string[1:-1]
        
        key_values = split_first_bool_op(t_string)
        
        rootNode.add_child(
            SyntaxNode(
                f'condition-{key_values[0]}',
                parent=rootNode
            )
        )

        rootNode = rootNode.children[-1]

        rootNode = add_to_tree(rootNode, key_values[1].strip(), line_number, Expected(['condition', 'expression', 'var']))
        rootNode = add_to_tree(rootNode, key_values[2].strip(), line_number, Expected(['condition', 'expression', 'var']))

        return rootNode.parent

    # * EXPRESSIONS
    elif contains_exp_op(string):
        
        if not(in_expected(expected, 'expression')):
            print(f"Unexpected EXPRESSION on line {line_number}, instead expected one of: {expected.expected}")
            exit()
        
        if string.count("(") != string.count(")"):
            print(f"You have unmatched brackets in your expression on line: {line_number}")
            exit()
        
        t_string = string

        while (t_string[0] == "(" and t_string[-1] == ")"):
            t_string = t_string[1:-1]
        
        # this one should actually kinda follow the rules of BEDMAS, like such: Division, DIV, Multiply, Add, Sub, MOD (this means reverse order for the split function array)
        key_values = split_first_exp_op(t_string) # TODO: combine both instances of these into 1 method, with  the bool op and exp op, because like, yes, they just kinda use diff arrays.

        rootNode.add_child(
            SyntaxNode(
                f'exp-{key_values[0]}',
                parent=rootNode
            )
        )

        rootNode = rootNode.children[-1]

        rootNode = add_to_tree(rootNode, key_values[1].strip(), line_number, Expected(['var', 'expression']))
        rootNode = add_to_tree(rootNode, key_values[2].strip(), line_number, Expected(['var', 'expression']))

        return rootNode.parent
    
    # * NUMERIC VALUE
    elif match("^[0-9]+$", string):
        
        if not(in_expected(expected, 'expression')):
            print(f"Unexpected CONSTANT on line {line_number}, instead expected one of: {expected.expected}")
            exit()

        rootNode.add_child(
            SyntaxNode(
                f"constant-{string}",
                parent=rootNode
            )
        )

    # * VARIABLE
    elif is_valid_var_or_arr_index(string):

        if not(in_expected(expected, 'var')):
            print(f"Unexpected VARIABLE ({string}) on line {line_number}, instead expected one of: {expected.expected}")
            exit()
        
        rootNode.add_child(
            SyntaxNode(
                f'var-{string.strip()}',
                parent=rootNode
            )
        )
        
        return rootNode
    # Now the missing statements:
    # variables -> we already have a variable check thing

    # * if its nothing valid, we just kinda skip... I guess...
    return rootNode

def split_first_exp_op(source: str) -> list:
    valid_exps = ["MOD", "-", "+", "*", "DIV", "/"]
    
    for operator in valid_exps:
        nesting = 0
        for x in range(len(source) - (len(operator) - 1)):
            
            if (source[x] == ")"):
                nesting -= 1
            if (source[x] == "("):
                nesting += 1

            if (source[x:x+len(operator)] == operator and nesting == 0):

                return [operator, source[:x], source[x+len(operator):]]

def contains_exp_op(string: str) -> bool:
    valid_exp_ops = ["*", "-", "+", "/", "MOD", "DIV"]

    for op in valid_exp_ops:
        if op in string:
            return True

    return False


#  list as: [OP, first_half, second_half]
def split_first_bool_op(source: str) -> list:
    # ! <> has to have higher precedence or it selects < first, or > same goes for <= and >=
    # TODO: come up with a better algorithm for splitting this string, because right now, this has some very specific criteria under which it works, which it should really not have
    valid_booleans = ['OR', 'NOT', '<>', '<=', '>=', '=', '>', '<', 'AND']
    # ! have to make sure its not in a bracket

    # ? The way I do it here means that boolean operators have a certain precedence
    # ? the precedence is as in the array, with = having the highest one
    # ? this is because it would first match the latest and, before matching a AND for example.
    # TODO: Make sure to note this / make it clear to people!

    # TODO: Add error checking, in case the statement brakes somehow, technically entering (( CAR AND FISH) )
    # TODO: could break this mechanism (which probably means im not doing it right, let's be real)
    # TODO: and even if I added .strip() this would still break it: ((car AND) fish)
    # TODO: now we can fight over if that would be a valid statement.

    # basically make sure that it does not take into account things inside a bracket (i.e. nested)
    for operator in valid_booleans:
        nesting = 0
        for x in range(len(source) - (len(operator) - 1)):
            
            if (source[x] == ")"):
                nesting -= 1
            if (source[x] == "("):
                nesting += 1

            if (source[x:x+len(operator)] == operator and nesting == 0):

                return [operator, source[:x], source[x+len(operator):]]
                
    


def find_close_index(start: int, string: str) -> int:

    give: int = 0

    for x, c in enumerate(string[start:]):
        if c == "(":
            give += 1
        if c == ")":
            give -= 1
        
        if give == 0:
            return start + x
    return -1


def contains_bool_op(string: str) -> bool:

    # all the valid boolean operators (<> = !=)
    valid_booleans = ['AND', 'OR', 'NOT', '>', '<', '<=', '>=', '=', '<>', 'TRUE', 'FALSE']

    for v in valid_booleans:
        if v in string:
            return True

    return False

def in_expected(expected: Expected, keyword):

    return (keyword.lower() in expected.expected or expected.expected[0] == 'any')

def check_standard_keyword_syntax(keyword: str, expected: Expected, line_number: int) -> bool: 
    
    if not(is_all_caps(keyword)):
        print(f"Syntax Error on Line {line_number}: '{keyword.upper()}' not in all capitals.")
        exit()
    
    if not(in_expected(expected, keyword)):
        print(f"Unexpected Keyword: {keyword.upper()} on line {line_number}, instead expected one of the following: {expected}")
        exit()
    
    return True