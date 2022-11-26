from SyntaxNode import SyntaxNode

# TODO: make this and transpile more efficient than just a row of IF statements

def build_lines_from_tree(c: SyntaxNode) -> str:
    
    # * OUTPUT
    if c.value == "output":
        build_string = "document.getElementById(\"output\").innerHTML +="
        for k in c.children:
            build_string += build_lines_from_tree(k)
        build_string += "+\"<br>\";\n"
        
        return build_string

    # 0123456
    # string-
    # * STRING
    elif c.value[:7] == 'string-':

        build_string = "\""

        build_string += c.value[7:]

        build_string += "\""

        return build_string

    # * INPUT
    elif c.value == "input":

        # TODO: make it so that the most recent line before is also displayed inside the prompt,
        # TODO: to make it easier for the person what the input is wanted for.
        # TODO: there are probably a couple ways this could be done -> but go ahead and figure it out, somehow
        # TODO: there is probably a clever way you can think of and be proud of by the end of the day
        build_string = f"var {build_lines_from_tree(c.children[0])} = prompt('Input', 'Your input...');\n"
        return build_string
    # 0123
    # var-
    # * VARIABLE
    elif c.value[:4] == "var-":
        return f"{c.value[4:]}"
    
    # TODO: * IF-STATEMENT
    elif c.value == 'if':

        build_string = "if ("

        build_string += ") {\n" 
        
        build_string += "}\n"
    
    # * ASSIGNMENT
    elif c.value == 'assignment':
        
        # the cutting off should only be applied, when the thing is a string, so we check for that here

        if c.children[1].value[:7] == "string-":
            return f"var {build_lines_from_tree(c.children[0])} = \"{build_lines_from_tree(c.children[1])[4:-5]}\";\n" # the 4:-5 at the end is to remove the "<p> and </p>"
        else:
            return f"var {build_lines_from_tree(c.children[0])} = {build_lines_from_tree(c.children[1])};\n"
    # 012345678
    # constant-
    # * NUMERIC VALUES
    elif c.value[:9] == 'constant-':
        return f"{c.value[9:]}"

    # 0123
    # exp-
    # * EXPRESSIONS
    elif c.value[:4] == 'exp-':
        print("EXPRESSION:", c)
        operator = c.value[4:]
        if operator == "MOD":
            return f"(parseInt({build_lines_from_tree(c.children[0])} % {build_lines_from_tree(c.children[1])}))"
        elif operator == "DIV":
            return f"(parseInt(({build_lines_from_tree(c.children[0])} / {build_lines_from_tree(c.children[1])})>>0))"
        else:
            return f"(parseInt({build_lines_from_tree(c.children[0])} {operator} {build_lines_from_tree(c.children[1])}))"

    # 0123456789
    # condition-
    # * CONDITION
    elif c.value[:10] == 'condition-':

        # ! NOT is not in here, it gets its own special case
        translate = {
            "=":"==",
            "OR": "||",
            ">" : ">",
            "<" : "<",
            "<=" : "<=",
            ">=" : ">=",
            "AND" : "&&",
            "<>" : "!="
        }

        if c.value[10:] == "NOT":
            return f"(!({build_lines_from_tree(c.children[0])}))"
        else:
            return f"({build_lines_from_tree(c.children[0])} {translate[c.value[10:]]} {build_lines_from_tree(c.children[1])})"

    # don't really need TYPE translation
    # or any of the end-statements as those are more for building the tree anyways

    # * DECLARE (ARRAYS)
    elif c.value == 'array':
        
        return f"var {build_lines_from_tree(c.children[0])} = new Array({build_lines_from_tree(c.children[2])} - {build_lines_from_tree(c.children[1])} + 1);"

    # * WHILE
    elif c.value == 'while':
        build_string = "while (" +  build_lines_from_tree(c.children[0]) + ") {\n"
        
        build_string += "\n".join([build_lines_from_tree(s) for s in c.children[1].children])
        build_string += "\n}\n"
        return build_string

    # * REPEAT-UNTIL
