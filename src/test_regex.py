
from SyntaxNode import *
from transpile_regex import *
from Expected import Expected
from build_from_tree import build_lines_from_tree
from varkeeper import VarKeeper

import os

with open('test.txt', 'r') as readFile:
    l = readFile.readlines()
    lines = [c.strip() for c in l]

root = SyntaxNode(value='code_root')

expected = Expected()

os.system('clear')

for x, l in enumerate(lines):
    root = add_to_tree(
        rootNode=root, 
        string=l,
        line_number=x+1, expected=expected
        )
    # print("Root after:", root)

# go back to parent if not there:

varkeeper = VarKeeper()

print(root)
l = ["let btn = document.getElementById('run');\nbtn.addEventListener('click', event=> { code(); });\nfunction code() {\n"]
l.append("\ndocument.getElementById('output').innerHTML=\"\";\n")
for c in root.children:
    lines = build_lines_from_tree(c, varkeeper)
    print("Lines", lines)
    l.append(lines)

print(l)
l.append("\n}")
with open("temp.js", "w") as javascript:
    javascript.writelines(l)

