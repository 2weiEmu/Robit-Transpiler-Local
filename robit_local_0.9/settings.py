compile_to_file : str = "storage.py" # Standard file that should be compiled to


# Dictionary of Error Types and their Descriptions
error_types : dict = {
    'name_error' : 
    'You defined a variable in a way that started with a number. You are not allowed to do that.',

    'invalid_statement' : 
    '''I dont know how you got here. 
    Maybe you misspelt something, maybe you tried using something not in 
    the documentation. Maybe you left a space somewhere you should not have''',

    'syntax' : 
    'You used the wrong syntax. Perhaps you forgot brackets? Quotation Marks?',

    'then_error' : 
    'You forgot / misspelled the THEN at the end of your IF Statement.',

    'end_error' : 
    'You placed an END to either end a loop or if, but you did not clearly state "loop" or "if".',

    'assignment_error' : 
    'You did not use "<-" to make an assignment',

    'immediate wait error':
    'You had incomplete syntax over multiple lines. You most likely forgot the THEN on the next line after an if statement.'
    }

def insertIntoFile(fileName : str, in_str : str): # Inserting things into a file
    j = open(fileName, "a")
    j.write(in_str + '\n')
    j.close()
