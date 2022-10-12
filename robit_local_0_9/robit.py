import sys
import validations as Vals
from rbit import main as transp

def main(system_arguments : list):

    # Checking for valid system argument. Only transpile .txt
    for arg in system_arguments: 
        if arg.endswith(".txt"): file_to_compile = arg

    # Reading Lines and removing newlines
    with open(file_to_compile, "r") as in_file: lines = in_file.readlines()

    # Transpilation
    transp("".join(lines))
    
if __name__ == "__main__":
    main(sys.argv)