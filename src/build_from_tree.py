from SyntaxNode import SyntaxNode
from varkeeper import VarKeeper

def build_lines_from_tree(c: SyntaxNode, exist_vars: VarKeeper) -> str:
    
    # * OUTPUT 
    if c.value == "output":
        build_string = "document.getElementById(\"output\").innerHTML +="
        build_string += "".join([build_lines_from_tree(k, exist_vars) for k in c.children])
        build_string += "+\"<br>\";\n"
        return build_string

    # * STRING
    elif c.value[:7] == 'string-':
        return f"\"{c.value[7:]}\""

    # * INPUT
    elif c.value == "input":

        var_to_build = build_lines_from_tree(c.children[0], exist_vars)
        if exist_vars.existed_before(var_to_build):
            return f"{var_to_build} = prompt('Input', 'Your input...');\n"
        else:
            exist_vars.add_var(var_to_build)
            return f"var {var_to_build} = prompt('Input', 'Your input...');\n"

    # * VARIABLE
    elif c.value[:4] == "var-":
        return f"{c.value[4:]}"
    
    # * IF-STATEMENT
    elif c.value == 'if':

        build_string = f"if ({build_lines_from_tree(c.children[0], exist_vars)}"+") {\n"
        # building the sub-body.
        build_string += "\n".join([build_lines_from_tree(s, exist_vars) for s in c.children[1].children])
        
        build_string += "}\n"

        if len(c.children) == 3:
            build_string += "else {\n" + "\n".join([build_lines_from_tree(s, exist_vars) for s in c.children[2].children]) + "\n}\n"

        return build_string
    
    # * ASSIGNMENT
    elif c.value == 'assignment':
        
        build_string = ""
        var_to_build = build_lines_from_tree(c.children[0], exist_vars)
        if not exist_vars.existed_before(var_to_build):
            build_string += "var "
            exist_vars.add_var(var_to_build)
        # the cutting off should only be applied, when the thing is a string, so we check for that here

        if c.children[1].value[:7] == "string-":
            return build_string + f"{var_to_build} = \"{build_lines_from_tree(c.children[1], exist_vars)[4:-5]}\";\n" # the 4:-5 at the end is to remove the "<p> and </p>"
        else:
            return build_string + f"{var_to_build} = {build_lines_from_tree(c.children[1], exist_vars)};\n"

    # * NUMERIC VALUES
    elif c.value[:9] == 'constant-':
        return f"{c.value[9:]}"

    # * EXPRESSIONS
    elif c.value[:4] == 'exp-':
        print("EXPRESSION:", c)
        operator = c.value[4:]
        if operator == "MOD":
            return f"(parseInt({build_lines_from_tree(c.children[0], exist_vars)}) % parseInt({build_lines_from_tree(c.children[1], exist_vars)}))"
        elif operator == "DIV":
            return f"(parseInt(({build_lines_from_tree(c.children[0], exist_vars)}) / parseInt({build_lines_from_tree(c.children[1], exist_vars)})>>0))"
        else:
            return f"(parseInt({build_lines_from_tree(c.children[0], exist_vars)}) {operator} parseInt({build_lines_from_tree(c.children[1], exist_vars)}))"

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
            return f"(!({build_lines_from_tree(c.children[0], exist_vars)}))"
        else:
            return f"({build_lines_from_tree(c.children[0], exist_vars)} {translate[c.value[10:]]} {build_lines_from_tree(c.children[1], exist_vars)})"

    # don't really need TYPE translation
    # or any of the end-statements as those are more for building the tree anyways

    # * DECLARE (ARRAYS)
    elif c.value == 'array':   
        return f"var {build_lines_from_tree(c.children[0], exist_vars)} = new Array({build_lines_from_tree(c.children[2], exist_vars)} - {build_lines_from_tree(c.children[1], exist_vars)} + 1);"

    # * WHILE
    elif c.value == 'while':
        build_string = "while (" +  build_lines_from_tree(c.children[0], exist_vars) + ") {\n"
        
        build_string += "\n".join([build_lines_from_tree(s, exist_vars) for s in c.children[1].children])
        build_string += "\n}\n"
        return build_string

    # * REPEAT-UNTIL
    elif c.value == "repeat":

        build_string = "{" + "\n".join([build_lines_from_tree(s, exist_vars) for s in c.children[0].children]) + "}\n"
        build_string += "while (!(" + build_lines_from_tree(c.children[1], exist_vars) + ")) {\n"
        build_string += "\n".join([build_lines_from_tree(s, exist_vars) for s in c.children[0].children])
        build_string += "}\n"
        return build_string
    
    # * CASE OF
    elif c.value == "case":
        build_string = "switch (" + build_lines_from_tree(c.children[0], exist_vars)+ ") {\n"

        for child in c.children[1:]:
            
            if child.children[0].value == 'otherwise':
                build_string += "\ndefault:\n{\n"
                print("Otherwise Sibling:", child.children[1])
            else:
                build_string += "\ncase (" + build_lines_from_tree(child.children[0], exist_vars)  + "):\n{\n"

            build_string += "\n".join([build_lines_from_tree(s, exist_vars) for s in child.children[1].children])

            build_string += "\n}\nbreak;"

        build_string += "\n}\n"
        return build_string

    # * FOR-LOOP
    elif c.value == "for-loop":
        var_to_build = build_lines_from_tree(c.children[0], exist_vars)
        start_pos = build_lines_from_tree(c.children[1], exist_vars)
        end_pos = build_lines_from_tree(c.children[2], exist_vars)
        body = "\n".join([build_lines_from_tree(s, exist_vars) for s in c.children[3].children])  
        if len(c.children) == 5:
            step = build_lines_from_tree(c.children[4], exist_vars)
        else: step = 1

        before = exist_vars.existed_before(var_to_build)

        build_string = f"for ({'var' * (not(before))} {var_to_build} = parseInt({start_pos}); {var_to_build} < parseInt({end_pos}) + 1;"
        build_string += f"{var_to_build} += {step})"
        build_string += "{\n"
        build_string += body + "}\n"

        return build_string
