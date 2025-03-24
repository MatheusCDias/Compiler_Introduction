import re

# Lexical Analyzer
def lexer(code):
    tokens = []
    token_specification = [
        ('NUMBER', r'\d+'),                 # Integer numbers
        ('OP', r'[+\-*/]'),                 # Operators (+, -, *, /)
        ('PAREN', r'[()]'),                 # Parentheses (both '(' and ')')
        ('ASSIGN', r'='),                   # Assignment '='
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers (variables)
        ('SKIP', r'[ \t]+'),                # Spaces and tabs (to skip)
        ('MISMATCH', r'.')                  # Any other character (error)
    ]
    token_re = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    for match in re.finditer(token_re, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        tokens.append((kind, value))
    return tokens

# Syntax Analyzer and Evaluation
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.env = {}  # Variable environment (dictionary)
    
    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return self.tokens[self.pos - 1][1]
        raise RuntimeError(f'Syntax error: expected {expected_type}, found {self.tokens[self.pos] if self.pos < len(self.tokens) else "EOF"}')
        
    def factor(self):
        """factor ::= NUMBER | ID | (expr)"""
        if self.tokens[self.pos][0] == 'NUMBER':
            return int(self.consume('NUMBER'))
        elif self.tokens[self.pos][0] == 'ID':
            var_name = self.consume('ID')
            if var_name in self.env:
                return self.env[var_name]  # Returns the value of the variable
            else:
                raise RuntimeError(f'Undefined variable: {var_name}')
        elif self.tokens[self.pos][0] == 'PAREN':  # Checks if it's a parenthesis
            self.consume('PAREN')  # Consumes '('
            result = self.expr()  # Evaluates the expression inside the parentheses
            self.consume('PAREN')  # Consumes ')'
            return result
        raise RuntimeError('Syntax error in factor')

    
    def term(self):
        """term ::= factor ((OP) factor)*"""
        result = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP' and self.tokens[self.pos][1] in ('*', '/'):
            op = self.consume('OP')  # Consumes multiplication or division operators
            if op == '*':
                result *= self.factor()
            elif op == '/':
                result /= self.factor()
        return result
    
    def expr(self):
        """expr ::= term ((OP) term)*"""
        result = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP' and self.tokens[self.pos][1] in ('+', '-'):
            op = self.consume('OP')  # Consumes addition or subtraction operators
            if op == '+':
                result += self.term()
            elif op == '-':
                result -= self.term()
        return result

    def statement(self):
        """statement ::= ID ASSIGN expr"""
        if self.tokens[self.pos][0] == 'ID':
            var_name = self.consume('ID')  # Consumes the identifier (variable)
            self.consume('ASSIGN')  # Consumes the assignment sign '='
            value = self.expr()  # Evaluates the expression on the right
            self.env[var_name] = value  # Assigns the value to the variable
            return value
        else:
            raise RuntimeError('Syntax error: expected a variable (ID) for assignment')
    
    def parse(self):
        result = None
        while self.pos < len(self.tokens):
            result = self.statement()  # For each line, we try to process an assignment
        return result

# Function to read the file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()  # Reads the content of the file
    except FileNotFoundError:
        raise RuntimeError(f'The file {file_path} was not found.')

# Main function of the compiler
def main():
    file_path = 'code.txt'
    
    try:
        code = read_file(file_path)  # Reads the code from the file
        tokens = lexer(code)  # Lexical analysis
        parser = Parser(tokens)  # Syntax analyzer
        result = parser.parse()  # Evaluation
        print("Result:", result)
    except RuntimeError as e:
        print("Syntax Error:", e)

if __name__ == "__main__":
    main()
