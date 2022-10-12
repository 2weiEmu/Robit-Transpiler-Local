# IMPORTS - EXTERNAL then INTERNAL
from re import match

from validations import Validations as val
from statements import *


# Transpiler Class
class RobitTranspiler:

    # Initialisation of Transpiler
    def __init__(self, in_args : list[str]): # Creating Transpiler with file validations and settings
        self.token_list : list = []
        self.tab_count : int = 1
        self.wait : list = []
        self.immediate_wait : list = []
        if in_args[0] == 'text':
            
            # Inserting Code read as Text into Default Compilation File
            write_file = open('test.txt', 'w')
            out = in_args[1].split('\n')
            write_file.writelines("\n".join(out))
            write_file.close()

            self.compile_file = 'test.txt'
            self.storage_file : str ='storage.py'
        else:
            self.compile_file : str = ""
            try:
                self.compile_file : str = val.check_compile_file(in_args[1])
            except IndexError:
                print("No compile file entered.")
                exit
            if not(self.compile_file): quit()
            self.storage_file : str = val.check_storage_file(in_args)

    def check_wait_resolutions(self, latest_token, line_count):

        # Immediate Wait Resolutions
        if self.immediate_wait:

            im_wait = self.immediate_wait[0]

            if latest_token.resolve_wait(latest_token) == im_wait:
                self.immediate_wait = []
            else:
                return(trnp_err("immediate wait error", line_count).throw_error())
                exit(-1)

        # Normal Wait Resolutions        
        if self.wait:

            latest_wait = self.wait[-1]

            if not(isinstance(latest_wait, str)) and latest_wait == latest_token.resolve_wait(latest_token):
                self.wait.pop()

        return "success"

    def check_wait_creations(self, latest_token, line_count):

        if isinstance(latest_token, str): return "success"

        wait_creation = latest_token.create_wait(latest_token)
        if not(wait_creation): return "success"
        if wait_creation[0] == "immediate":
            self.immediate_wait.append(wait_creation[1])
        else:
            self.wait.append(wait_creation[1])
        return "success"

    # Cleaning Up Storage File
    def setup_storage_file(self):
        storage_open = open(self.storage_file, 'w')
        storage_open.writelines('def user_func(in_bool):\n')
        storage_open.close()

    # Getting Lines from Compile File
    def get_lines(self):
        read_file = open(self.compile_file, 'r')
        read_lines : list = read_file.readlines()
        read_file.close()
        return read_lines

    # Identifying Token of Line
    def find_line_token(self, line : str, line_num : int): # Extracting tokens from a line
        
        # LINE SETUP
        if "//" in line: line = line[:line.index("//")]

        if line == '\n' or line == '': return # if the line is empty just ignore it
        line = line.strip() # Removing the tabs from the front of a statement
        #print("LINE ===", line)

        #line_values = str(line).split(" ")
        line_values = line.split(" ")
        l_prompt : str = line_values[0].lower()

        if len(line_values) > 1: 
            if line_values[1] == ":": 
                self.token_list.append("case")
                return
        
        # RETURN TYPE CHECKS
        for check in prompt_calls:
            if l_prompt == check:
                if type(k:=prompt_calls[check]) == str:
                    self.token_list.append(k)
                    return
                else:
                    debug = prompt_calls[check](line_values, line_num)
                    self.token_list.append(debug)
                    return

        if match('[a-zA-Z0-9_"]',l_prompt): # If no other checks are confirmed then a variable must be checked for
            self.token_list.append(asgn_st(line_values, line_num))
            return 
        else:
            self.token_list.append(trnp_err('invalid_statement', line_num))
            return # Consider returning an error here, and if an error is returned to the variable at any point, just throwing an error instead of making it handle weirldly afterward. I.e. this function either returns nothing or an error