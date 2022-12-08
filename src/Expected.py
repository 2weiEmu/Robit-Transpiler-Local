class Expected:

    def __init__(self, expected_list = ['any']):
        self.expected = expected_list

    def update_expected(self, new_expected):
        self.expected = new_expected
    
    def __str__(self):
        return str(self.expected)
