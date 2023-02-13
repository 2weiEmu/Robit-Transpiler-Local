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

def get_request_body(body):

    data = str(body)[2:-1]

    data = data.split("\\n")
    data = "\n".join(data)

    return data

@app.post("/entered_code")
async def eval_entered_code(request: Request):

    data = get_request_body(await request.body())
    # print(data)
    # with open("temp.txt", "w") as write_file:
    #     write_file.writelines(data)
    
    try:
        returnCode = transpile(data)
    except Exception as e:
        returnCode = ['robit_trp_failure', str(e)]

    return returnCode

# TODO: Implement a feature so that you can print the syntax tree.
# @app.post("/syntax_tree")
# async def eval_entered_to_syntax_tree(request: Request):

#     data = get_request_body(await request.body())


