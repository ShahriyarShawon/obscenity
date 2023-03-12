from obscenity.units import FunctionNode, InstructionNode, Token, TokenType


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
