# External Imports
import unittest

# Internal Imports
from robit_local_0_9.LineFormat import match_format
# Unit Testing
"""
All line formats:
x<-n
INPUT x
OUTPUT x
IF x THEN
ELSE
CASE OF x
CASE x:
THEN
ENDIF
ENDCASE
WHILE x DO
NEXT
ENDWHILE
FOR x<-u TO z {STEP k}
DECLARE x: ARRAY[1:n] OF t
REPEAT
UNTIL x
"""
class SimpleTest(unittest.TestCase):


    def testAssignTrue(self):
        test = match_format("a_", "a<-5")
        self.assertTrue(test[0])

    def testInputTrue(self):
        test = match_format("INPUT x_", "INPUT fish")
        self.assertTrue(test[0])

    def testOutputTrue(self):
        test = match_format("OUTPUT x_", "OUTPUT a")
        self.assertTrue(test[0])

    def testIfTrue(self):
        test = match_format("IF b THEN_", "IF x/2==0 THEN")
        self.assertTrue(test[0])

    def testElseTrue(self):
        test = match_format("ELSE_", "ELSE")
        self.assertTrue(test[0])

    def testCaseOfTrue(self):
        test = match_format("CASE OF x_", "CASE OF tent")
        self.assertTrue(test[0])

    def testCaseTrue(self):
        test = match_format("CASE x:_", "CASE 10:")
        self.assertTrue(test[0])

    def testThenTrue(self):
        test = match_format("THEN_", "THEN")
        self.assertTrue(test[0])

    def testEndIfTrue(self):
        test = match_format("ENDIF_", "ENDIF")
        self.assertTrue(test[0])

    def testEndCaseTrue(self):
        test = match_format("ENDCASE_", "ENDCASE")
        self.assertTrue(test[0])

    def testWhileTrue(self):
        test = match_format("WHILE b DO_", "WHILE k>0 DO")
        self.assertTrue(test[0])

    def testNextTrue(self):
        test = match_format("NEXT_", "NEXT")
        self.assertTrue(test[0])

    def testEndWhileTrue(self):
        test = match_format("ENDWHILE_", "ENDWHILE")
        self.assertTrue(test[0])

    def forNoStepTrue(self):
        test = match_format("FOR a TO n {STEP n}_", "FOR x<-0 TO fish")
        self.assertTrue(test[0])

    def forStepTrue(self):
        test = match_format("FOR a TO n {STEP n}_", "FOR x<-0 TO fish STEP 3")
        self.assertTrue(test[0])

    def declareArrayTrue(self):
        test = match_format("DECLARE x: ARRAY[1:n] OF t_", "DECLARE cars: ARRAY[1:10] of string")
        self.assertTrue(test[0])

    def repeatTrue(self):
        test = match_format("REPEAT_", "REPEAT")
        self.assertTrue(test[0])

    def untilTrue(self):
        test = match_format("UNTIL b_", "UNTIL house = 0")
        self.assertTrue(test[0])

    # False Tests
    def testAssignFalse(self):
        test = match_format("a", "house=fish")
        self.assertFalse(test[0])

    def testInputFalse(self):
        test = match_format("INPUT x", "INPUT ")
        self.assertFalse(test[0])

    def testOutputFalse(self):
        test = match_format("OUTPUT x", "OUTPUT ")
        self.assertFalse(test[0])

    def testIfFalse(self):
        test = match_format("IF b THEN", "IF _ THEN")
        self.assertFalse(test[0])

    def testElseFalse(self):
        test = match_format("ELSE", "else")
        self.assertFalse(test[0])

    def testCaseOfFalse(self):
        test = match_format("CASE OF x", "CASE of number")
        self.assertFalse(test[0])

    def testCaseFalse(self):
        test = match_format("CASE x:", "CASE 10")
        self.assertFalse(test[0])

    def testThenFalse(self):
        test = match_format("THEN", "DEN")
        self.assertFalse(test[0])

    def testEndIfFalse(self):
        test = match_format("ENDIF", "end if")
        self.assertFalse(test[0])

    def testEndCaseFalse(self):
        test = match_format("ENDCASE", "end-case")
        self.assertFalse(test[0])

    def testWhileFalse(self):
        test = match_format("WHILE b DO", "WHILE there is something DO")
        self.assertFalse(test[0])

    def testNextFalse(self):
        test = match_format("NEXT", "Nxt")
        self.assertFalse(test[0])

    def testEndWhileFalse(self):
        test = match_format("ENDWHILE", "end-while")
        self.assertFalse(test[0])

    def forNoStepFalse(self):
        test = match_format("FOR a TO n {STEP n}", "FOR x0 to fish")
        self.assertFalse(test[0])

    def forStepFalse(self):
        test = match_format("FOR a TO n {STEP n}", "FOR x<-0 TO fish s 3")
        self.assertFalse(test[0])

    def declareArrayFalse(self):
        test = match_format("DECLARE x: ARRAY[1:n] OF t", "DECLARE cars: ARRAY[1:10] of string")
        self.assertFalse(test[0])

    def repeatFalse(self):
        test = match_format("REPEAT", "rpt")
        self.assertTrue(test[0])

    def untilFalse(self):
        test = match_format("UNTIL b", "UNTIL house 0")
        self.assertTrue(test[0])


if __name__ == '__main__':
    unittest.main()
