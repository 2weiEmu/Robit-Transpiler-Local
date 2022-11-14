
from SyntaxNode import *
from transpile import *

root = SyntaxNode(value='code_root', transform='')


add_to_tree(rootNode=root, string="OUTPUT fire, house", line_number=1)
print(root)