import sys 
from enum import Enum


class TokenType(str,Enum):
    FUNCTION_NAME = "function_name"
    FUNCTION_START = "function_start"
    FUNCTION_END = "function_end"
    INSTRUCTION = "instruction"
    NUMBER = "number"
    FUNCTION_CALL = "function_call"

class Token:
    def __init__(self, value, type, position):
        self.value = value 
        self.type = type
        self.pos = position
    def __repr__(self):
        return f"[{self.type}:{self.value}:{self.pos}]"

class Tokenizer:
    def __init__(self):
        self.position = 0
        self.tokens = []
        self.source = ""
        self.curr_char = ''

    def get_source(self, source_path:str):
        with open(source_path, "r") as f:
            content = f.read() + "\0"
            self.curr_char = content[0]
            return content
    
    def get_function_start_or_end(self):
        value = ""
        starting_pos = self.position
        while self.curr_char != " ":
            value+=self.curr_char
            self.advance()
        token_type = TokenType.FUNCTION_START if value == "_begin" else TokenType.FUNCTION_END
        self.advance()
        return Token(value, token_type, starting_pos)

    def get_word(self):
        word = ""
        while self.curr_char.isalpha():
            word+=self.curr_char
            self.advance()
        return word

    def advance(self):
        self.position += 1
        self.curr_char = self.source[self.position]

    def tokenize(self, source_path: str):
        self.source = self.get_source(source_path)
        #breakpoint()
        while self.curr_char != "\0":
            if self.curr_char == "_":
                token = self.get_function_start_or_end()
                self.tokens.append(token)
                function_name_pos = self.position
                function_name = self.get_word()
                token = Token(function_name, TokenType.FUNCTION_NAME, function_name_pos)
                self.tokens.append(token)
            else:
                self.advance()
        print(self.tokens)



if __name__ == "__main__":
    t = Tokenizer()
    tokens = t.tokenize(sys.argv[1])
