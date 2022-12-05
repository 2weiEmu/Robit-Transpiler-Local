class VarKeeper:

    def __init__(self):
        self.prevs = []

    def add_var(self, var: str) -> None:
        self.prevs.append(var)

    def existed_before(self, var: str) -> bool:
        return var in self.prevs