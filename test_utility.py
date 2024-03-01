'''
  Please carefully read this script before starting the project, particularly pay attention to
  how output is constructed for a given piece of code. We understand that there are multiple ways
  to represent program in-memory, all forms evaluate to same result. Given that it is infeasible
  for us to grade your work if every one of you pick your favorite representation, then we(graders)
  have to spend lot of time to understand your work and possibly sync with you. It is time-consuming
  for you and us. So we have picked a caconical form as below, please emit your code representation
  according to it, we run automated scripts to grade your work. If you don't follow this form, then
  the script will fail to count your submission even if your code generation is logically consistent.

  PLEASE STICK TO THIS CACONICAL FORM.
  
  Note: Grading requests to submissions that don't follow the guidelines, will not be entertained.

  Caconical form to follow for submission:
  for a statement below:
    a = 10 + 20

    your parser must emit : ('=', 'a', ('+', 10, 20))

    ('+', 10, 20) - first the operator, then LHS and RHS.

    the same logic applies for a = 10 + 20 expression.
'''

import project1_parser

def test_parser(code, expected_ast_str):
    lexer = project1_parser.Lexer(code)
    parser = project1_parser.Parser(lexer)
    ast = parser.parse()
    ast_str = ''.join(map(str, ast))

    if ast_str == expected_ast_str:
         print(f"Test passed. AST: {ast}")
         return 0
    else:
        print(f"Test failed. Expected: {expected_ast_str}, Got: {ast_str}")
        return 1


def testSimpleStatements():
    passed = 0
    # Test Case 1
    code_1 = '''
    x = 5 + 3
    '''
    expected_ast_str_1 = "('=', 'x', ('+', 5, 3))"
    if test_parser(code_1, expected_ast_str_1) == 1:
        return passed
    passed+=1

    # Test Case 2
    code_2 = '''
    y = y + z
    '''
    expected_ast_str_2 = "('=', 'y', ('+', 'y', 'z'))"
    if test_parser(code_2, expected_ast_str_2) == 1:
        return passed

    passed+=1

    # Test Case 3
    code_4 = '''
    x = 1
    y = 2
    z = 3
    a = x + y + z
    '''

    expected_ast_str_4 = "('=', 'x', 1)('=', 'y', 2)('=', 'z', 3)('=', 'a', ('+', ('+', 'x', 'y'), 'z'))"
    if test_parser(code_4, expected_ast_str_4) == 1:
        return passed
    
    passed+=1

     # Test Case 4
    code_5 = '''
    x = 1  y = 2
    b = (x + 1) * y
    '''

    expected_ast_str_5 = "('=', 'x', 1)('=', 'y', 2)('=', 'b', ('*', ('+', 'x', 1), 'y'))"
    if test_parser(code_5, expected_ast_str_5) == 1:
        return passed
    
    passed += 1
    
    return passed

def testIfStatements():
    # Test Case 5
    code_1 = '''
    x = 5 + 3
    y = 0
    if x > y then
        y = x
    '''
    expected_ast_str_1 = "('=', 'x', ('+', 5, 3))('=', 'y', 0)('if', ('>', 'x', 'y'), ('=', 'y', 'x'))"
    if test_parser(code_1, expected_ast_str_1) == 1:
        return 0
    return 1


def testWhileStatements():
    passed = 0
    # Test Case 6
    code_1 = '''
    x = 1
    x99 = 1234
    c99 = (x99 * x)
    cnt = 0
    while c99 > x99 do
        cnt = cnt + 1
    '''
    expected_ast_str_1 = "('=', 'x', 1)('=', 'x99', 1234)('=', 'c99', ('*', 'x99', 'x'))('=', 'cnt', 0)('while', ('>', 'c99', 'x99'), [('=', 'cnt', ('+', 'cnt', 1))])"
    if test_parser(code_1, expected_ast_str_1) == 1:
        return passed
    
    passed += 1
    # Test Case 7
    code_2 = '''
    x = 5 + 3 + 10
    y = x + 3
    if y > 8 then z = y - x else z = y + x
    x = x / y
    x = y + x * x
    while x > 0 do
        while y > 0 do
            x = x - 1
    '''
    expected_ast_str_2 = "('=', 'x', ('+', ('+', 5, 3), 10))('=', 'y', ('+', 'x', 3))('if', ('>', 'y', 8), ('=', 'z', ('-', 'y', 'x')), ('=', 'z', ('+', 'y', 'x')))('=', 'x', ('/', 'x', 'y'))('=', 'x', ('+', 'y', ('*', 'x', 'x')))('while', ('>', 'x', 0), [('while', ('>', 'y', 0), [('=', 'x', ('-', 'x', 1))])])"
    if test_parser(code_2, expected_ast_str_2) == 1:
        return passed
    passed += 1
    return passed


def main():

    totalPassed = 0
    totalPassed += testSimpleStatements()

    totalPassed += testIfStatements()
    
    totalPassed += testWhileStatements()

    print("Test cases Passed : ", totalPassed)
    
if __name__ == "__main__":
    main()