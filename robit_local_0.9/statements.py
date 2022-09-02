# IMPORTS
from settings import insertIntoFile, error_types
from re import match
from validations import Validations as vals
# from robit_transpiler import RobitTranspiler as Transpiler


# CLASS DEFINITIONS
class trnp_err:
    
    def __init__(self, err_type : str, line_number : int):
        self.err_type : str = err_type
        self.line : int = line_number

    def throw_error(self):
        return self.err_type + " Line: " + str(self.line + 1) + "\nDescription: " + error_types[self.err_type]

# Generic Class
class BaseStatement:
    
    def __new__(cls, line_values : list, line_num : int):
        return object.__new__(cls)

    def __init__(self, line_values : list, line_num : int):
        self.type : str = '' # Type of the statement (e.g. out, case, whatever I assume?)
        self.value : list = [] # Value of the statement
        self.tab_change : int = 0 # By how much this thing changes the indent

    def resolve_wait(self, latest_token):
        return ''

    def create_wait(self, latest_token):
        return ''

    def build_to_python(self, file_name : str, tabs : int):
        insert_string : str = ''
        insertIntoFile(file_name, insert_string)

# OUTPUT STATEMENTS TRANSPILING
class out_st(BaseStatement): 
    
    def __init__(self, line_values : list, line_num : int):
        super().__init__(line_values, line_num)
        self.value : list = line_values[1:]
        self.type = "output"


    def build_to_python(self, file_name : str, tabs : int):
        tab_indent = tabs * '\t'
        total_value = " ".join(self.value)
        insert_string = f"{tab_indent}print({total_value})"

        insertIntoFile(file_name, insert_string)

# IF STATEMENT TRANSPILING
class if_st(BaseStatement):

    def __new__(cls, line_values : list, line_num : int):
        l_prompt = line_values[0].lower()
        print(f"prompt:{l_prompt}, line_values: {line_values}")
        if l_prompt == 'case' and line_values[1].lower() == 'of':
            return object.__new__(cls)
        elif l_prompt == 'case' and line_values[1].lower()[-1] == ":":
            pass
        elif l_prompt in ["then", "endif", "endcase", "if"]:
            return object.__new__(cls)
        else: 
            return trnp_err('invalid_statement', line_num) # TODO CHECK FOR VALID IDENTIFIERS (ESPECIALLY IN THE CASE, BUT THAT DOES NOT HAVE TO HAPPEN BECAUSE THEY HAVE TO DECLARE IT AT SOME POINT AND IF THE THING THEY DECLARED IS NOT VALID< WHICH IS ALREADY CHECKED THEN THINGS SHUOLD BE FINE)

    def __init__(self, line_values : list, line_num : int):
        super().__init__(line_values, line_num)
        self.type : str = line_values[0].lower()
        if self.type == 'if':
            self.tab_change = 1
            self.condition : str = line_values[1 :]
        elif self.type == 'case':
            # FIRST VALUE IN THE LIST FOR IDENTIFIER - NEXT FOR ALL CASES
            self.condition : list = [[line_values[2].lower(), "IDEN"]]
    
    def resolve_wait(self, latest_token):
        if self.type in ["then", "endif", "endcase"]:
            return self.type


    def create_wait(self, latest_token):
        t = self.type
        if t == "if":
            return ("immediate", "then")
        elif t == "case":
            print(latest_token)
            # equal_value = 0
            # temp = Transpiler()
            # token_to_execute = temp.find_line_token(line, line_num)
            # self.condition.append(equal_value, token_to_execute)
            # APPEND TO THE LIST: [line.split()[0].lower(), trp.find_line_token(" ".join(line.split()[2:]), line_count)]

            return ("normal", "endcase")


    def build_to_python(self, file_name : str, tabs : int):
        tab_indent = tabs * '\t'
        if self.type == "if":
            total_condition = "".join(self.condition)
            insert_string = f"{tab_indent}if {total_condition}:"
            insertIntoFile(file_name, insert_string) 

        elif self.type == "case":
            
            insert_con = f"{tab_indent}if {self.condition[0][0]} == {self.condition[1][0]}:"

            insertIntoFile(file_name, insert_con)
            self.condition[1][1].build_to_python(file_name, tabs + 1)


            for x in range(2, len(self.condition)):

                if self.condition[x][0] == 'otherwise':
                    insert_con = f"{tab_indent}else:"
                else:
                    insert_con = f"{tab_indent}elif {self.condition[0][0]} == {self.condition[x][0]}:"

                insertIntoFile(file_name, insert_con) 
                
                self.condition[x][1].build_to_python(file_name, tabs + 1)

# Loop Statement Transpiling Class
class lp_st(BaseStatement):

    # Validation checks for new object in __new__
    def __new__(cls, line_values : list, line_num : int):
        if (l_prompt := line_values[0].lower()) == "for":
            # Is correct syntax used? (FOR _var_ <- _start_ TO _end_)
            if line_values[4].lower() != "to" or line_values[2] != '<-':
                return trnp_err('invalid_statement', line_num) # Incorrect Syntax -> Error
            elif not(vals.valid_identifier(line_values[1])):
                return trnp_err('name_error', line_num) # Invalid Name -> Error
            else: # New Object Creation if Valid
                return object.__new__(cls)
        elif l_prompt == "while":
            if line_values[-1].lower() != 'do': # Checks correct Syntax ()
                return trnp_err('invalid_statement', line_num)
            else:
                return object.__new__(cls)
        elif l_prompt in ["next", "endwhile"]:
            return object.__new__(cls)

        else: return trnp_err('invalid_statement', line_num)
    # INIT
    def __init__(self, line_values : list, line_num : int):
        super().__init__(line_values, line_num)
        self.tab_change = 1
        self.type = line_values[0].lower()
        
        if (self.type == 'for'):
            # CONDITION AS = [IDENTIFIER, START, STOP, (STEP)]
            self.condition = [line_values[1], line_values[3], line_values[5]]
            if line_values[-2].lower() == 'step':
                self.condition.append(line_values[-1])
        elif (self.type == 'while'):
            self.condition = line_values[1:-1]

    def resolve_wait(self, latest_token):
        if self.type in ["next", "endwhile"]:
            return self.type

    def create_wait(self, latest_token):
        if self.type == "while":
            return ("normal", "endwhile")


    def build_to_python(self, file_name : str, tabs : int):
        
        tab_indent = tabs * '\t'

        if self.type == 'for':
            if len(self.condition) == 4:

                if int(self.condition[3]) < 0:
                    self.condition[2] = str(int(self.condition[2]) - 1)
                else:
                    self.condition[2] = str(int(self.condition[2]) + 1)
            else:
                self.condition[2] = str(int(self.condition[2]) + 1)
            insert_string = f"{tab_indent}for {self.condition[0]} in range({self.condition[1]},{self.condition[2]}"
            if len(self.condition) == 4:
                insert_string = f"{insert_string},{self.condition[3]}):"
            else:
                insert_string = f"{insert_string}):"

            insertIntoFile(file_name, insert_string)
        elif self.type == 'while':
            total_condition = "".join(self.condition)
            insert_string = f"{tab_indent}while {total_condition}:"
            insertIntoFile(file_name, insert_string)

        else:
            pass


 # DOESNT YET WORK WHEN TEXT IN FRONT OF INPUT, BUT JUST USE AN OUTPUT STATEMENT FOR THAT FOR NOW

# Assignment Statement Transpiling Class
class asgn_st(BaseStatement):


    # Validation Checking in __new__
    def __new__(cls, line_values : list, line_num : int):
        # Define Line Prompt (i.e. first value)
        prompt : str = line_values[0].lower()
        if "<-" in prompt:
            add_values = prompt.split("<-")
            add_values.append(None)
            temp_values = line_values
            line_values = [add_values[0], "<-", add_values[1] if add_values[1] else None]
            for v in temp_values[1:]:
                line_values.append(v)

        # Check for Valid Variable Name if Prompt is 'input'
        if prompt == 'input':

            # Regular Expression Matching to Determine if Valid Variable
            if not(vals.valid_identifier(line_values[1])):
                return trnp_err('name_error', line_num)

        # Check for Valid Variable Name and Assignment (using '<-')
        else:
            if not(vals.valid_identifier(prompt)): 
                return trnp_err('name_error', line_num)
            else:
                if line_values[1] != '<-': return trnp_err('assignment_error', line_num)

        # New Object of Class Returned if Valid
        return object.__new__(cls)


    # Object Intialisation in __init__
    def __init__(self, line_values : list, line_num : int):
        prompt : str = line_values[0].lower()
        if "<-" in prompt:
            add_values = prompt.split("<-")
            add_values.append(None)
            temp_values = line_values
            line_values = [add_values[0], "<-", add_values[1] if add_values[1] else None]
            for v in temp_values[1:]:
                line_values.append(v)
        super().__init__(line_values, line_num)
        if prompt == "input":

            self.value = ["|IN|"]
            self.var = line_values[1]
        else:
            self.var = line_values[0]
            self.value = line_values[2:]

    
    def build_to_python(self, file_name : str, tabs : int):
        tab_indent = tabs * '\t'
        if self.value[0] == "|IN|":
            self_str = str(self.var)
            insert_string = f"{tab_indent}print('//IN//' * in_bool)"
            insertIntoFile(file_name, insert_string)
            insert_string = f"{tab_indent}{self_str}=input()"
        else:
            total_value = " ".join(self.value)
            insert_string = f"{tab_indent}{self.var}={total_value}"

        insertIntoFile(file_name, insert_string)

# ARRAY STATEMENT TRANSPILING
class arr_st(BaseStatement):
    
    def __new__(cls, line_values : list, line_num : int):
        if line_values[2] == ":" and (line_values[3])[:5].lower() == "array":
            return object.__new__(cls)
        else:
            return trnp_err('syntax', line_num)

    def __init__(self, line_values : list, line_num : int):
        super().__init__(line_values, line_num)
        print(line_values)
        self.identifier : str = line_values[1]
        self.arr_length : int = int((line_values[3].split(":")[1])[:-1])
        self.arr : list = [None for x in range(self.arr_length)]

    def build_to_python(self, file_name : str, tabs : int):
        tab_indent = tabs * '\t'
        insert_string = f"{tab_indent}{self.identifier} : list = [None for x in range({str(self.arr_length + 1)})]"
        insertIntoFile(file_name, insert_string)

# REPEAT UNTIL STATEMENT TRANSPILING
class RptState(BaseStatement):
    
    def __init__(self, line_values : list, line_num : int):
        super().__init__(line_values, line_num)
        self.tab_change = 1
        self.type = line_values[0].lower()
        if self.type == 'until':
            self.tab_change = -1
            self.condition : list = line_values[1:]

    def build_to_python(self, file_name : str, tabs : int):
        tab_indent = tabs * '\t'
        if self.type == 'repeat':
            insert_string = f"{tab_indent}while True:"
            insertIntoFile(file_name, insert_string)
        
        elif self.type == 'until':
            total_condition = " ".join(self.condition) 
            insert_string = f"{tab_indent}if {total_condition}: break"
            insertIntoFile(file_name, insert_string)

# Dicitonary that Refers a Prompt to an Action
prompt_calls : dict = {
    'output' : out_st,
    'input' : asgn_st,
    'if' : if_st,
    'endif' : if_st,
    '//' : None,
    'for' : lp_st,
    'case' : if_st,
    'then' : if_st,
    'repeat' : RptState,
    'until' : RptState,
    'endcase' : if_st,
    'endwhile' : lp_st,
    'next' : lp_st,
    'while' : lp_st,
    'declare' : arr_st
}