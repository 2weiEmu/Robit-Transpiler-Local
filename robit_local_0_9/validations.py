# IMPORTS
from re import match

# MAIN
class Validations:

    # RETURNS COMPILED FILE IF SPECIFICED, FALSE OTHERWISE
    @staticmethod
    def check_compile_file(file_name : str):
        try:
            # ! CHECK IF THE FILE EXISTS
            return file_name
        except IndexError:
            Exception("No file to be compiled was specified")
            return(False)
    
    # STATIC METHOD TO CHECK STORAGE FILE - STORAGE FILE IF PRESENT, DEFAULT OTHERWISE
    @staticmethod
    def check_storage_file(sys_arr : list, default : str = "storage.py"):
        try:
            storageFile : str = sys_arr[2]
            return storageFile
        except IndexError:
            return default

    # DEPENDING ON HOW THINGS WILL WORK I MAY HAVE TO USE THIS IN THE CODE
    @staticmethod
    def valid_int_string(instr : str):
        try: return int(instr)
        except Exception:
            return str

    # EASY CHECKING FOR A VALID IDENTIFIER
    @staticmethod
    def valid_identifier(in_str : str):
        in_str = in_str.lower()
        if match('[a-zA-Z0-9_"]', in_str) and not(in_str[0] in '1234567890'):
            # Should there be quotations in the regular expression match?
            return True
        return False

    # CHECKING SYS ARGUMENTS FOR LOCAL COMPILER (MOVE THIS LATER TO JUST THE LOCAL TRANSPILER)
    @staticmethod
    def check_system_arguments(system_arguments : list): 
        for argument in system_arguments:

            compile_file, storage_file, output_file = "standard.txt", "storage.py", "out.txt"

            larg = argument.lower() 
            if larg == "python" or larg == "python3" or larg == "main.py": continue

            argument = argument.split("=")

            # TODO: Make standard sys arg checking, by just making the entering of the sys arg thing standard in the settings, and this will automatically check through it or something

    # CALCULATING DIFFERENCE BETWEEN TWO STRINGS TO MAKE SUGGESTIONS WHEN ERRORS ARE THROWN
    @staticmethod
    def compare_strings(str1: str, str2: str):
        
        diff_num : int = abs(len(str1) - len(str2))

        small_len = min( len(str1), len(str2) )
        for x in range(small_len):
            if str1[x] != str2[x]: diff_num += 1

        return diff_num