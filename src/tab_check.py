# the goal of this function is simply to check that everything has the right amount of spaces before (we start parsing)\

# this is basically just taking care of syntax loving bs

def check_tabs(code: str) -> None:
    tab_count = 0
    