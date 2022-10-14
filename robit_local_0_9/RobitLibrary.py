from TranspilerStatements import *
from TranspileException import *
from LineFormat import *
from settings import *

class RobitLibrary:

    @staticmethod
    def transpile_exec_text(text):
        # Splitting the text into lines
        lines: list = text.split('\n')

        # Creating some important vars to keep track
        wait_stack: list = []
        allow_list: list = []
        tab_count: int = 0

        token_list: list = []

        for line_number, line in enumerate(lines):

            # Splitting into their individual values and getting rid of comments
            line_vals = line.partition("//")[0].split(" ")

            # setting a default value, otherwise PyCharm is upset
            statement_type = "skip"

            # Checking what the statement is, with some special cases
            if wait_stack:
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
                if not allow_list: allowed = True
                elif not(statement_type in allow_list): allowed = False
                else: allowed = False
                # If statement is not allowed to happen, raise Exception
                if not allowed:
                    raise TranspileException("Un-allowed statement at this point.", line_number)

                # Checking if the statement resolves any waits
                if wait_stack:
                    if wait_stack[-1] == formats[-2]:
                        wait_stack.pop()
                # Changing tab count according to statement
                tab_count += formats[-1]

                # Checking if the statement creates any waits
                if formats[2]:
                    for w in formats[2]:
                        wait_stack.append(w)

                allow_list = formats[-3]

                # parsing out the vars - this is somewhat dependant on matching_format
                # so for now I can simply separate by spaces, as matching format is
                # picky like that, but I also need to separate them out based on the
                # line format, so make a method for that, thanks
                vars_token = separate_out_vars(formats[0], line)
                token_list.append(Statement(statement_type, vars_token, formats[1], tab_count))



        for token in token_list:

            # CANNOT DO FOR LOOPS WITH STEPS YET - thanks please fix
            insertIntoFile("temp.txt", build_statement_to_python(token))


if __name__ == "__main__":
    RobitLibrary.transpile_exec_text("a<-5\nOUTPUT a")
