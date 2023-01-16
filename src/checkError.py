from Expected import Expected

class checkError:

    @staticmethod
    def check_is_all_caps(keyword: str, line_number: int) -> bool:
        if (keyword != keyword.upper()):
            raise Exception(f"Syntax Error on line: {line_number} => Cause: '{keyword}' ({keyword.upper()}) not in all capitals.")
            # print(f"Syntax Error on line: {line_number}\nCause: {keyword} ({keyword.upper()}) not in all capitals.")
            # exit(-1)

    @staticmethod
    def check_in_expected(keyword: str, expected: Expected, line_number: int) -> bool:
        if not(keyword.lower() in expected.expected or expected.expected[0] == 'any'):
            raise Exception(f"Syntax Error on line: {line_number} => Cause: Unexpected keyword '{keyword.upper()}' => Instead Expected one of the following: {'/'.join(expected.expected)}")
            # print(f"Syntax Error on line: {line_number}\nCause: Unexpected keyword {keyword.upper()}\nInstead Expected one of the following: {'/'.join(expected.expected)}")
            # exit(-1)

    @staticmethod
    def check_standard_keyword_syntax(keyword: str, expected: Expected, line_number: int) -> bool:

        checkError.check_is_all_caps(keyword, line_number)
        checkError.check_in_expected(keyword, expected, line_number)

        return True