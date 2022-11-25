from SyntaxNode import SyntaxNode

def build_lines_from_tree(c: SyntaxNode) -> str:
    
    # * OUTPUT
    if c.value == "output":

        build_string = "document.getElementById(\"output\").innerHTML +="
        for k in c.children:
            build_string += build_lines_from_tree(k)
        build_string += ";\n"


        return build_string

    # 0123456
    # string-
    # * STRING
    elif c.value[:7] == 'string-':

        build_string = "\""

        build_string += c.value[7:]

        build_string += "<br\\>\""

        return build_string

    # * INPUT
    elif c.value == "input":

        pass