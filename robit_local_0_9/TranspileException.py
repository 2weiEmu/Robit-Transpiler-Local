

class TranspileException(Exception):

    def __int__(self, message, line_number):
        super().__init__(message)
        self.message = message
        self.line_number = line_number

    def __str__(self):
        return f"{self.message} -> An Exception Occurred on line {self.line_number}."


class TranspileSyntaxException(TranspileException):

    def __init__(self, message, line_number):
        super().__init__(message, line_number)

    def __str__(self):
        return f"{self.message} -> You had a syntax error on line {self.line_number}"


class TranspileWaitException(TranspileException):

    def __init__(self, message, line_number):
        super().__init__(message, line_number)

    def __str__(self):
        return f"{self.message} -> You forgot some statement such as ENDCASE, or THEN, on line {self.line_number}"
