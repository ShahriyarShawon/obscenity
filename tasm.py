import sys
from enum import Enum
from itertools import chain

function_name_to_opcode = {
    "push": 1,
    "fetch": 2,
    "store": 3,
    "if": 4,
    "loop": 5,
    "break": 6,
    "return": 7,
    "call": 8,
    "fpplus": 9,
    "add": 10,
    "sub": 11,
    "mul": 12,
    "div": 13,
    "mod": 14,
    "not": 15,
    "and": 16,
    "or": 17,
    "xor": 18,
    "eq": 19,
    "neq": 20,
    "lt": 21,
    "leq": 22,
    "gt": 23,
    "geq": 24,
    "pop": 25,
    "lshift": 26,
    "rshift": 27,
}

built_in_function_to_opcode = {
    "iprint": -101,
    "sprint": -102,
    "iread": -103,
    "sread": -104,
    "nl": -105,
    "random": -106,
    "timer": -107,
    "stoptimer": -108,
    "makeimg": -201,
    "setimg": -202,
    "button": -203,
    "html": -204,
    "makelabel": -205,
    "setlabel": -206,
    "alloc": -109,
    "free": -110,
    "i2s": -111,
    "maketable": -207,
    "setcell": -208,
    "setcellcolor": -209,
    "buttonlabel": -210,
}


class TokenType(str, Enum):
    FUNCTION_NAME = "function_name"
    FUNCTION_START = "function_start"
    FUNCTION_END = "function_end"
    INSTRUCTION = "instruction"
    NUMBER = "number"
    FUNCTION_CALL = "function_call"
    NULL = "null"
    SEMICOLON = "semicolon"


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
        self.curr_char = ""

    def get_source(self, source_path: str):
        with open(source_path, "r") as f:
            content = f.read() + "\0"
            self.curr_char = content[0]
            return content

    def get_function_start_or_end(self):
        value = ""
        starting_pos = self.position
        while self.curr_char != " ":
            value += self.curr_char
            self.advance()
        token_type = (
            TokenType.FUNCTION_START if value == "_begin" else TokenType.FUNCTION_END
        )
        self.advance()
        return Token(value, token_type, starting_pos)

    def get_number(self):
        num_str = ""
        while self.curr_char.isnumeric():
            num_str += self.curr_char
            self.advance()
        return num_str

    def get_word(self):
        word = ""
        while self.curr_char.isalpha():
            word += self.curr_char
            self.advance()
        return word

    def advance(self):
        self.position += 1
        self.curr_char = self.source[self.position]

    def tokenize(self, source_path: str):
        self.source = self.get_source(source_path)
        # breakpoint()
        while self.curr_char != "\0":
            if self.curr_char == "_":
                token = self.get_function_start_or_end()
                self.tokens.append(token)
                function_name_pos = self.position
                function_name = self.get_word()
                token = Token(function_name, TokenType.FUNCTION_NAME, function_name_pos)
                self.tokens.append(token)
            elif self.curr_char.isalpha():
                instruction_name = self.get_word()
                instruction_pos = self.position
                token = Token(instruction_name, TokenType.INSTRUCTION, instruction_pos)
                self.tokens.append(token)
            elif self.curr_char == "#":
                function_name = "$"
                self.advance()
                function_name += self.get_word()
                pos = self.position
                token = Token(function_name, TokenType.FUNCTION_NAME, pos)
                self.tokens.append(token)
            elif self.curr_char.isnumeric():
                number = self.get_number()
                token = Token(number, TokenType.NUMBER, 0)
                self.tokens.append(token)
            elif self.curr_char == ";":
                token = Token("", TokenType.SEMICOLON, 0)
                self.tokens.append(token)
                self.advance()
            else:
                self.advance()
        return self.tokens


class InstructionNode:
    def __init__(self):
        self.instruction: Token = None
        self.args: list[Token] = []

    def get_asm(self):
        values = [function_name_to_opcode[self.instruction.value]]
        values.extend(
            [
                int(v.value)
                if v.value.isnumeric()
                else built_in_function_to_opcode[v.value.replace("$", "").lower()]
                for v in self.args
            ]
        )
        return values

    def __repr__(self):
        return f"INS: {self.instruction.value} ARGS: {','.join([v.value for v in self.args])}"


class FunctionNode:
    def __init__(self):
        self.function_name: Token = None
        self.instructions = []

    def get_asm(self):
        return list(chain(*[ins.get_asm() for ins in self.instructions]))

    def __repr__(self) -> str:
        return f"Function: {self.function_name}\n{[ins for ins in self.instructions]}"


class Parser:
    def __init__(self):
        self.position = 0
        self.curr_token: Token = None
        self.tokens = []
        self.nodes = []

    def advance(self):
        self.position += 1
        self.curr_token = self.tokens[self.position]

    def get_instruction_node(self):
        ins_node = InstructionNode()
        ins_node.instruction = self.curr_token
        self.advance()
        while self.curr_token.type != TokenType.SEMICOLON:
            ins_node.args.append(self.curr_token)
            self.advance()
        self.advance()

        return ins_node

    def get_function_node(self):
        self.advance()
        function_name = self.curr_token
        self.advance()
        instructions = []
        while self.curr_token.type != TokenType.FUNCTION_END:
            instructions.append(self.get_instruction_node())
        f = FunctionNode()
        f.function_name = function_name
        f.instructions = instructions
        return f

    def parse(self, tokens: list[Token]) -> list[FunctionNode]:
        self.tokens = tokens
        self.tokens.append(Token("", TokenType.NULL, 0))
        self.curr_token = self.tokens[0]
        nodes = []
        while self.curr_token.type != TokenType.NULL:
            if self.curr_token.type == TokenType.FUNCTION_START:
                fn = self.get_function_node()
                nodes.append(fn)
            self.advance()
        return nodes


if __name__ == "__main__":
    t = Tokenizer()
    tokens = t.tokenize(sys.argv[1])
    # for token in tokens:
    #    print(token)
    p = Parser()
    nodes = p.parse(tokens)
    for node in nodes:
        print(node.get_asm())
