from fastapi import FastAPI as FP
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from SyntaxNode import *
from transpile import *
from Expected import Expected
from build_from_tree import build_lines_from_tree
from varkeeper import VarKeeper

app = FP()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    # allow_headers=["*"]
)

def transpile(transmitted: str) -> str:
    # Transpiler Setup

    # Line formatting into list
    t = transmitted.split("\n")
    lines = [l.strip() for l in t]

    print(lines)
    
    # setting up base specs for transpiler
    root = SyntaxNode(value='code_root')
    expected = Expected()

    for x, l in enumerate(lines):
        print(l)
        root = add_to_tree(
            rootNode=root, 
            string=l,
            line_number=x+1, expected=expected
        )

    # Setting up for building of code
    varkeeper = VarKeeper()
    l = []

    for c in root.children:
        lines = build_lines_from_tree(c, varkeeper)
        l.append(lines)
    
    return l

@app.post("/entered_code")
async def eval_entered_code(request: Request):

    data = str(await request.body())[2:-1]

    data = data.split("\\n")
    data = "\n".join(data)
    # print(data)
    # with open("temp.txt", "w") as write_file:
    #     write_file.writelines(data)
    
    try:
        returnCode = transpile(data)
    except:
        pass

    return returnCode