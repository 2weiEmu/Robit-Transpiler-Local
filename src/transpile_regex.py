from re import match

from checkError import checkError
from Expected import Expected
from SyntaxNode import *

def is_valid_var_or_arr_index(string: str) -> bool:
    return match("[a-zA-Z0-9\[\]]", string)


"""
The plan for this add_to_tree function.
There are a couple RegEx patterns against which it will match.
If none of the patterns matches, it will go through preset patterns, and a slower
algorithm in order to find which pattern it matches most closely (some manually defined)
rules, in order to throw a more informative error for the user. This should not compromise on performance
for actually working code, because if your code does not transpile, then like... yes.
"""

def add_to_tree(rootNode: SyntaxNode, string: str, line_number: int, expected: Expected) -> SyntaxNode:
    
    # filtering out comments, tabs and spaces (at either end)
    string = string.split("//")[0]
    string = string.strip("\\t")
    string = string.strip(" ")

    print(f"add_to_tree Pass on: {string}\nExpected: {expected.expected}")

    # Skip if the line is empty
    t = string.split()
    if t==[]:
        return rootNode

    statement_regexs = [
        r"^OUTPUT\s+[a-zA-Z0-9\"\"\[\]\s,]+$":,
        r"^INPUT\s+[a-zA-Z0-9\[\]]+$":,
        r"^ENDWHILE$":,
        r"^IF\s+.+$|^IF\s+.+\s+THEN$":,
        r"^THEN$":,
        r"^ELSE$":,
        r"^ENDIF$":,
        r"^FOR\s+.+<-.+\s+TO\s+[a-zA-Z0-9\+\*\-/\[\]\"\"]+(\s+STEP\s+.+)?$":,
        r"^NEXT$":,
        r"^CASE OF\s+.+$":,
        r"^ENDCASE$":,
        r"^REPEAT$":,
        r"^UNTIL\s+.+$":,
        r"^WHILE\s+.+\s+DO$":,
        r"^DECLARE\s+.+\s*:\s*ARRAY\s+\[.+:.+\]\s+OF\s+.+$":,
        r"^.+<-.+$":,
        r"^INTEGER$|^CHAR$|^REAL$|^STRING$|^BOOLEAN$":,
        r"^\"[^\"]*\"$":,
        r"^.+((\s+OR\s+)|(\s+AND\s+)|(<>)|(<=)|(>=)|(\<[^-])|[\>\=]){1}.+$|^TRUE$|^FALSE$|^NOT\s+.+$":,
        r"":,
        r"^[0-9]+$":,
        r"^[a-zA-Z]{1}[a-zA-Z0-9\[\]]*$":,
    ]

    # * OUTPUT
    # is output statement?
    # Regex for OUTPUT: ^OUTPUT\s+[a-zA-Z0-9\"\"\[\]\s,]+$
    if match(r"^OUTPUT\s+[a-zA-Z0-9\"\"\[\]\s,]+$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(SyntaxNode(
                'output',
                parent=rootNode
            ))

        string = " ".join(t[1:]) # Joing everything except the OUTPUT statement
        string = string.split(",") # Split at the commas

        for s in string:
            s = s.strip()
            add_to_tree( # Add a new node to the tree for every argument that the OUTPUT call receives
                rootNode.children[-1], # adding to the last child of the rootnode (the one we just created)
                s, line_number, 
                expected=Expected(['expression', 'string', 'var', 'condition'])
                )

        return rootNode

    # * INPUT
    # case if is input statement
    # Regex for INPUT: ^INPUT\s+[a-zA-Z0-9\[\]]+$
    elif match(r"^INPUT\s+[a-zA-Z0-9\[\]]+$", string):
        
        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(SyntaxNode(
                'input',
                rootNode
            ))

        string = string.split()
        add_to_tree(rootNode.children[-1], # adding to the newest child of the rootnode -> the one we just added
            string[1], line_number, expected=Expected(['var']))
        return rootNode

    # * ENDWHILE
    # Regex for ENDWHILE: ^ENDWHILE$
    elif match(r"^ENDWHILE$", string):
        checkError.check_is_all_caps(t[0], line_number)

    # * IF-STATEMENT
    # Regex for IF: ^IF\s+.+$|^IF\s+.+\s+THEN$
    elif match(r"^IF\s+.+$|^IF\s+.+\s+THEN$", string):
        
        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

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
            
            if not(checkError.check_is_all_caps(t[-1], line_number)):
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
    # Regex for then: ^THEN$
    elif match(r"^THEN$", string):
        checkError.check_standard_keyword_syntax(t[0], expected, line_number)
        
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
    # RegEx for else: ^ELSE$
    elif match(r"^ELSE$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)
        
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
    # RegEx for ENDIF: ^ENDIF$
    elif match(r"^ENDIF$", string):
        
        checkError.check_standard_keyword_syntax(t[0], expected, line_number)
        
        expected.update_expected(['any'])
        
        # skip back to IF statement node (from else-body or if-body), then to the place we were before
        return rootNode.parent.parent
    
    # * FOR-LOOP
    # RegEx for for loop: ^FOR\s+.+<-.+\s+TO\s+[a-zA-Z0-9\+\*\-/\[\]\"\"]+(\s+STEP\s+.+)?$
    elif match(r"^FOR\s+.+<-.+\s+TO\s+[a-zA-Z0-9\+\*\-/\[\]\"\"]+(\s+STEP\s+.+)?$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

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
        rootNode = add_to_tree(rootNode, var_exp, line_number, Expected(['var', 'expression']))

        expressions = halves[1].split(" STEP ")

        # adding where to STOP. -> don't forget that in Pseudocode both sides are inclusive, yea mate?
        rootNode = add_to_tree(rootNode, expressions[0], line_number, Expected(['var','expression']))

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
    # RegEx for next: ^NEXT$
    elif match(r"^NEXT$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

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
    # RegEX for CASE: 
    elif expected.expected[0] == 'case':
        
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
            
            checkError.check_is_all_caps(k, line_number)
            
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
            rootNode = rootNode.children[-1]
            # ! This technically means that you cannot actually declare arrays in CASE statements (sorry, but I don't expect anyone to do that)
            rootNode = add_to_tree(rootNode, t[1], line_number, Expected(['any']))

            expected.update_expected(['endcase'])

            # return the cond-sub-body
            return rootNode

        else:
            print(f"t -> {t}")
            rootNode = add_to_tree(rootNode, t[0], line_number, Expected(['var', 'expression']))

            rootNode.add_child(
                SyntaxNode(
                    'cond-sub-body',
                    parent=rootNode
                )
            )
            # rootnode = conditional_sub_body
            rootNode = rootNode.children[-1]
            rootNode = add_to_tree(rootNode, t[1].strip(), line_number, Expected(['any']))

            # cond-sub-body -> cond-body -> case, which is where the next statement has to be added again
            return rootNode.parent.parent

    # * CASEOF
    # RegEx for CASEOF: ^CASE OF\s+.+$
    elif match(r"^CASE OF\s+.+$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

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

        rootNode = add_to_tree(rootNode, t[0].strip(), line_number, Expected(['var', 'expression']))

        expected.update_expected(['case'])

        # returning the CASE node
        return rootNode

    # in this case we have to check for the expected, because the line does not really have a strong identifier, for that
    # * ENDCASE
    # RegEx for endcase: ^ENDCASE$
    elif match(r"^ENDCASE$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)
        
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
    # RegEx for REPEAT: ^REPEAT$
    elif match(r"^REPEAT$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

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
    # RegEx for Until: ^UNTIL\s+.+$
    elif match(r"^UNTIL\s+.+$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

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
    # RegEx for While: ^WHILE\s+.+\s+DO$
    elif match(r"^WHILE\s+.+\s+DO$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)

        rootNode.add_child(
            SyntaxNode(
                'while',
                parent=rootNode
            )
        )

        checkError.check_standard_keyword_syntax(t[-1], Expected(['do']), line_number)
        
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

    # * DECLARE
    # RegEx for Declare (declaring an array): ^DECLARE\s+.+\s*:\s*ARRAY\s+\[.+:.+\]\s+OF\s+.+$
    elif match(r"^DECLARE\s+.+\s*:\s*ARRAY\s+\[.+:.+\]\s+OF\s+.+$", string):

        checkError.check_standard_keyword_syntax(t[0], expected, line_number)
        
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
    # RegEx for assignment: ^.+<-.+$ 
    elif match(r"^.+<-.+$", string):
        
        checkError.check_in_expected('assignment', expected, line_number)

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
    # RegEx for types: ^INTEGER$|^CHAR$|^REAL$|^STRING$|^BOOLEAN$
    elif match(r"^INTEGER$|^CHAR$|^REAL$|^STRING$|^BOOLEAN$", string):

        checkError.check_in_expected('type', expected, line_number)
        checkError.check_is_all_caps(string, line_number)
        
        rootNode.add_child(
            SyntaxNode(
                f'type-{string.lower}',
                parent=rootNode
            )
        )

        return rootNode

    # * STRINGS
    # RegEx for Strings: ^\"[^\"]*\"$
    elif match(r"^\"[^\"]*\"$", string):

        checkError.check_in_expected('string', expected, line_number)

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
    # RegEx for CONDITION: ^.+((\s+OR\s+)|(\s+AND\s+)|(<>)|(<=)|(>=)|[\>\<\=]){1}.+$|^TRUE$|^FALSE$|^NOT\s+.+$
    # this RegEx has been deemed good enough for now, obv there are improvements that can be made for more specific testing for all of them
    # so that I have to do even less checking for syntax mistakes
    # fuck this one has bad bracket matching. Or - to be more precise, it works, but like... yea it won't match the right one
    elif match(r"^.+((\s+OR\s+)|(\s+AND\s+)|(<>)|(<=)|(>=)|(\<[^-])|[\>\=]){1}.+$|^TRUE$|^FALSE$|^NOT\s+.+$", string):
        
        checkError.check_in_expected('condition', expected, line_number)

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
    # RegEx for Expressions: 
    elif contains_exp_op(string):
        checkError.check_in_expected('expression', expected, line_number)
        
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
    # Regex For Numberic Value: ^[0-9]+$
    elif match(r"^[0-9]+$", string):
        
        checkError.check_in_expected('expression', expected, line_number)

        rootNode.add_child(
            SyntaxNode(
                f"constant-{string}",
                parent=rootNode
            )
        )

        return rootNode

    # * VARIABLE
    # Regex for Variable: ^[a-zA-Z]{1}[a-zA-Z0-9\[\]]*$
    elif match(r"^[a-zA-Z]{1}[a-zA-Z0-9\[\]]*$", string):
    # elif is_valid_var_or_arr_index(string):

        checkError.check_in_expected('var', expected, line_number)
        
        rootNode.add_child(
            SyntaxNode(
                f'var-{string.strip()}',
                parent=rootNode
            )
        )
        
        return rootNode

    # TODO If nothing is valid we call the large compare function, and will end up throwing an informative error please
    identify_potential_error(string, line_number, expected)
    

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

    # TODO: make sure that it basically has an array of values sorted by the depth in the brackets (in valid bracket combinations)
    # TODO: meaning, also check that all brackets match, and then basically select the one with the lowest depth, as technically the one with depth 0
    # TODO: isn't guaranteed to exist (ok maybe it is, because I always remove all the brackets, but you catch my drift, it would make life easier)
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


def identify_potential_error(string: str, line_number: int, expected: Expected):
    
    # we don't have to really check expectation matching, because that is taken care of in each matching

    raise Exception(f"Could not identify potential Error, though there is a mistake on Line: {line_number}\n at \"{string}\"")