
from SyntaxNode import *
from transpile import *

with open('test.txt', 'r') as readFile:
    l = readFile.readlines()
    lines = [c.strip() for c in l]

root = SyntaxNode(value='code_root', transform='')

expect_list = ['any']

for x, l in enumerate(lines):
    root = add_to_tree(
        rootNode=root, 
        string=l,
        line_number=x+1, expected=expect_list
        )

# go back to parent if not there:

print(root)