# Lexer
import regex 
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        token = self.code[self.position]
        return token
# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.programLength = 0
        self.current_token = None
        self.operators = ['*', '/', '+', '-']
        self.brackets = ['(', ')']

    # function to parse the entire program
    def parse(self):
        result = ''
        self.lexer.code = self.lexer.code.split(' ')
        self.lexer.code = [token for token in self.lexer.code if token != '' and token != '\n']
        self.programLength = len(self.lexer.code)
        
        formatedList = []
        for i in range(self.programLength): #getting rid of the '\n'
            token = self.lexer.code[i]
            openParans = []
            closedParans = []
            for letter in token:
                if letter == '(':
                    openParans.append(letter)
                elif letter == ')':
                    closedParans.append(letter)
            formatedList += openParans + [token.strip('()\n')] + closedParans     
        self.lexer.code = formatedList
        self.programLength = len(self.lexer.code) #updating the length after finding paranthesis
        self.current_token = self.lexer.get_token()
        while self.lexer.position != self.programLength - 1:
            result += self.statement()
        print(result)
        return result
    # move to the next token.
    def advance(self):
        self.lexer.position += 1 
        self.current_token = self.lexer.get_token()

    # parse if, while, assignment sstatement.
    def statement(self):
        statement = ''
        if self.current_token == 'while':
            statement += self.while_loop()
        elif self.current_token == 'if':
            statement += self.if_statement()
        elif self.checkVariable(self.current_token): #check to make sure its a valid variable
            statement += self.assignment()  
        else:
            raise('Invalid synax in the example')
        return statement

    # parse assignment statements
    def assignment(self):
        # variable, equalSign, arthmeticExpr =  
        assignmentString = "('=', '" + self.current_token + "', "
        
        self.advance()
        #checking to make sure assignment is there
        if self.current_token != '=':
            raise('Invalid assignment')
        self.advance()
        #create stack, just defining the entire assignment
        assignmentTokens = []
        end = False
        while self.lexer.position+1<self.programLength and not end:
            assignmentTokens.append(self.current_token)
            self.advance()
            if self.lexer.position + 1 < self.programLength:
                nextToken = self.lexer.code[self.lexer.position + 1]
                if (self.current_token != '(' and self.current_token not in self.operators) and (nextToken not in self.brackets and nextToken not in self.operators):
                    end = True
            else:
                end = True
        if self.lexer.position == self.programLength - 1:
            assignmentTokens.append(self.current_token)
        assignmentString += self.arithmetic_expression(assignmentTokens) + ")"
        return assignmentString

    # parse arithmetic experssions
    def arithmetic_expression(self, assignmentTokens):
        stack = []
        currentTerm = []
        i = 0
        while i < len(assignmentTokens):
            term = assignmentTokens[i]
            if term == '+' or term == '-':
                stack.append(currentTerm) #appending last terms 
                stack.append(term)
                currentTerm = []
            elif term == '(':
                paranthesisStack = ['(']
                paranthesisTerm = ['(']
                while i+1< len(assignmentTokens) and len(paranthesisStack) != 0:
                    i += 1
                    paranthesisTerm.append(assignmentTokens[i])
                    if assignmentTokens[i] == '(':
                        paranthesisStack.append('(')
                    elif assignmentTokens[i] == ')':
                        paranthesisStack.pop()
                if len(paranthesisStack) != 0: #check for bad paranthesis 
                    raise('Invalid Paranthesis')
                currentTerm.append(paranthesisTerm)
            else:
                currentTerm.append(term)
            i += 1

        stack.append(currentTerm)   
        #reverse stack
        stack = stack[::-1]
        #parse stack and create prefix

        for i in range(len(stack)):
            if stack[i] != '+' and stack[i] != '-':
                stack[i] = self.term(stack[i])

        if len(stack) == 1:
            return stack[0]
        
        while len(stack) != 1:
            term1 = stack.pop()
            operator = stack.pop()
            term2 = stack.pop()
            stringified = "('" + operator + "', " + term1 + ", " + term2 + ")"
            stack.append(stringified) 

        return stack[0]
   
    def term(self, term):
        for i in range(len(term)):
            if term[i] != '*' and term[i] != '/':
                term[i] = self.factor(term[i])
        
        stack = term[::-1]
        while len(stack) != 1:
            factor1 = stack.pop()
            operator = stack.pop()
            factor2 = stack.pop()
            stringified = "('" + operator + "', " + factor1 + ", " + factor2 + ")"
            stack.append(stringified)
        
        return stack[0]

    def factor(self, factor):
        if factor[0] == '(':
            return self.arithmetic_expression(factor[1:len(factor) - 1])
        else:
            if factor.isnumeric():
                return factor
            else:
                return "'" + factor + "'"


    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        pass
    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        pass

    def condition(self):
        pass

    def checkVariable(self, token):
        if not token[0].isalpha():
                return False
        for letter in token:
            if not (letter.isnumeric() or letter.isalpha()):
                return False
        return True
            
# code_1 = '''
#     x = 5 + 3
#     y = 0
#     if x > y then
#         y = x
#     '''

test = '''
    x = 1
    y = 2
    z = 3
    a = x + y + z
'''

lexer = Lexer(test)
parser = Parser(lexer)
parser.parse()