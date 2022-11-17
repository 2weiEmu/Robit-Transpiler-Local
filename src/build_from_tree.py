from SyntaxNode import SyntaxNode

def build_line_from_node(root: SyntaxNode) -> str:
    line = ""

    # * OUTPUT
    if root.value == 'output':
        
        outVals = [build_line_from_node(c) for c in root.children]

        return f"print({','.join(outVals)})\n"
    
    if root.value == 'if':
        pass

    if root.value.startswith("var"):
        return root.value[3:]

    return ""

def build_lines_from_tree(root: SyntaxNode) -> list:
    lines = []
    # Moving through LRP navigation
    for c in root.children:

        if c.value == 'output':
            
            lines.append(build_line_from_node(c))
    
    return lines