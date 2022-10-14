from dataclasses import dataclass

statement_relations: dict = {
    # TYPE: [format, py_form, wait_create, wait_intermediate, wait_resolve, tab_count]
    "assignment": ["a_", "_v", [], [], [], 0],
    "input": ["INPUT x_", "_v = input()", [], [], [], 0],
    "output": ["OUTPUT x_", "print(_v)", [], [], [], 0],
    "if": ["IF b THEN_", "if _v:", ["endif", "then"], ["then"], [], 1],
    "else": ["ELSE_", "else:", [], [], []],
    "case_of": ["CASE OF x_", "match _v:", ["case"], ["case"], []],
    "case": ["CASE x:_", "case _v:", [], ["case"], []],
    "then": ["THEN", "", [], [], ["then"], 0],
    "endif": ["ENDIF", "", [], [], ["then"], -1],
    "endcase": ["ENDCASE", "", [], [], ["endcase"], -1],
    "while": ["WHILE b DO", "while (_v):", ["endwhile"], [], [], 1],
    "next": ["NEXT", "", [], [], ["next"], -1],
    "endwhile": ["ENDWHILE", "", [], [], ["endwhile"], -1],
    "for": ["FOR a TO n {STEP n}_", "for _v in range(_v,_v{,_v})", ["next"], [], [], 1],
    "declare": ["DECLARE x: ARRAY[1:n] OF t_", "_v = [None for _ in range(_v)]", [], [], [], 0],
    "repeat": ["REPEAT", "while (True):", ["until"], [], [], 1],
    "until": ["UNTIL b_", "if b: break", [], [], ["until"], -1]
}

@dataclass
class Statement:
    type: str
    vars: list
    py_form: list
    tab_count: int


def build_statement_to_python(token: Statement) -> str:
    py_statement = ""
    formats = statement_relations[token.type]
    vars = iter(token.vars)
    if token.type != "for":
        for c in token.py_form.split(" "):
            if "_v" in c:
                py_statement += " " + c.replace("_v", next(vars))
    else:
        t = next(vars)
        py_statement = f"for {t.split('=')[0]} in range({t.split('=')[0]},{next(vars)})"


    return py_statement

def separate_out_vars(format_line, line):
    format_line = format_line.split(" ")
    line = line.split(" ")
    out_vars = []

    for x, c in enumerate(format_line):

        if c[-1] in ":_":
            c = c[:-1]

        if c in "axbnt":
            if c == "a":
                out_vars.append(line[x].split("<-")[0] + "=" + line[x].split("<-")[1])
            else:
                out_vars.append(line[x])

    return out_vars
