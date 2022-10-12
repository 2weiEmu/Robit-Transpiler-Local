from dataclasses import dataclass

statement_relations: dict = {
    # TYPE: [format, py_form, wait_create, wait_intermediate, wait_resolve, tab_count]
    "assignment": ["a", "x = y", [], [], [], 0],
    "input": ["INPUT x", "x = input()", [], [], [], 0],
    "output": ["OUTPUT x", "print(x)", [], [], [], 0],
    "if": ["IF b THEN", "if b:", ["endif", "then"], ["then"], [], 1],
    "else": ["ELSE", "else:", [], [], []],
    "case_of": ["CASE OF x", "match x:", ["case"], ["case"], []],
    "case": ["CASE x:", "case x:", [], ["case"], []],
    "then": ["THEN", "", [], [], ["then"], 0],
    "endif": ["ENDIF", "", [], [], ["then"], -1],
    "endcase": ["ENDCASE", "", [], [], ["endcase"], -1],
    "while": ["WHILE b DO", "while (b):", ["endwhile"], [], [], 1],
    "next": ["NEXT", "", [], [], ["next"], -1],
    "endwhile": ["ENDWHILE", "", [], [], ["endwhile"], -1],
    "for": ["FOR a TO n {STEP n}", "for a in range(x,y{,z})", ["next"], [], [], 1],
    "declare": ["DECLARE x: ARRAY[1:n] OF t", "x = [None for c in range(n)]", [], [], [], 0],
    "repeat": ["REPEAT", "while (True):", ["until"], [], [], 1],
    "until": ["UNTIL b", "if b: break", [], [], ["until"], -1]
}

@dataclass
class Statement:
    type: str
    py_form: list
    format: list
    vars: list
    wait_create: list
    wait_intermediate: list
    wait_resolve: list