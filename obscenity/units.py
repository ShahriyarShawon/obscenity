from enum import Enum
from itertools import chain

from obscenity.dicts import *


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
