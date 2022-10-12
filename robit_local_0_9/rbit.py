import sys

from settings import insertIntoFile, error_types
from robit_transpiler import RobitTranspiler
from statements import trnp_err


def main(text : str):

    # Text is written into a file
    trp : RobitTranspiler = RobitTranspiler(['text', text])

    # Lines are taken out of the file
    Lines : list = trp.get_lines()

    for line_count, line in enumerate(Lines):
        # Should always return latest token
        latest_token = trp.find_line_token(line, line_count)

        # ! REMEMBER THAT .THROW_ERROR does not PRINT IT, just gives a string
        # If there is an error, throw the error, call it a day.
        # Should speed up program if it has an error
        if isinstance(latest_token, trnp_err):
            latest_token.throw_error()
            exit(-1)
        else:
            latest_token = trp.token_list[-1]

        # ! I'm doing this test twice because of bad returning,
        # in the find_line_token function, fix some other time, now we just test things work
        # ! Make sure to fix that mess
        if isinstance(latest_token, trnp_err):
            print(latest_token.throw_error())
            exit()

        # Check Wait Resolution
        check = trp.check_wait_resolutions(latest_token, line_count)
        if isinstance(check, trnp_err):
            check.throw_error()

        # Check Wait Creation
        check = trp.check_wait_creations(latest_token, line_count)
        if isinstance(check, trnp_err):
            check.throw_error()
    
    if trp.wait or trp.immediate_wait:
        if trp.wait: failure = trp.wait[-1]
        if trp.immediate_wait: failure = trp.immediate_wait[0]
        return(f"You failed to complete a statement with: {failure}")
    
    trp.setup_storage_file()
    
    for line_num, token in enumerate(trp.token_list):

        if not(token): insertIntoFile(trp.storage_file, '')

        else:
            token.build_to_python(trp.storage_file, trp.tab_count)
            trp.tab_count += token.tab_change

    insertIntoFile(trp.storage_file, "\tprint('//END//' * in_bool)")

    from storage import user_func  
    # True for Web running, False otherwise
    user_func(False)
    return "transpiler success"