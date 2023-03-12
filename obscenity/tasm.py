import sys

from obscenity.compiler import Parser, Tokenizer


def main():
    t = Tokenizer()
    tokens = t.tokenize(sys.argv[1])
    # for token in tokens:
    #    print(token)
    p = Parser()
    nodes = p.parse(tokens)
    for node in nodes:
        print(node.get_asm())


if __name__ == "__main__":
    main()
