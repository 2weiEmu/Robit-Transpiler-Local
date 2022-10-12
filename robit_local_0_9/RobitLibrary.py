from TranspilerStatements import *
from TranspileException import *
from LineFormat import *


class RobitLibrary:

    @staticmethod
    def transpile_exec_text(text):
        # Splitting the text into lines
        lines: list = text.split('\n')

        # Creating some important vars to keep track
        wait_stack: list = []
        allow_list: list = []
        intermediate_save: list = []
        tab_count: int = 0

        for line_number, line in enumerate(lines):

            # Splitting into their individual values and getting rid of comments
            line_vals = line.partition("//")[0].split(" ")

            # setting a default value, otherwise PyCharm is upset
            statement_type = "skip"

            # Checking what the statement is, with some special cases
            if wait_stack[-1] == "case":
                if line_vals[0] == "case":
                    statement_type = "case"
            elif line_vals[0] == "case":
                statement_type = "case_of"
            elif line_vals[0].islower():
                statement_type = "assignment"
            elif not line_vals:
                continue
            else:
                statement_type = line_vals[0].lower()

            # Getting the relevant format information based on the statement
            formats: list = statement_relations[statement_type]

            # doing format matching
            matching_format = match_format(formats[0], line)

            # raising error if it failed
            if not(matching_format[0]):
                raise TranspileSyntaxException("Mismatch with Expected Line", line_number)
            else:
                # checking if the statement is allowed to happen right now
                allowed = False
                if allow_list:
                    for c in allow_list:
                        if c == statement_type:
                            allowed = True
                else:
                    allowed = True
                # If statement is not allowed to happen, raise Exception
                if not allowed:
                    raise TranspileException("Un-allowed statement at this point.", line_number)

                # Checking if the statement resolves any waits

                # Changing tab count according to statement

                # Checking if the statement creates any waits
                if formats[2]:
                    for w in formats[2]:
                        wait_stack.append(w)
