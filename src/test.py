
from SyntaxNode import *
from transpile import *
from build_from_tree import build_lines_from_tree

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

print(root)
l = []
for c in root.children:
    lines = build_lines_from_tree(c)
    print("Lines", lines)
    l.append(lines)

print(l)

with open("temp.js", "w") as javascript:
    javascript.writelines(l)