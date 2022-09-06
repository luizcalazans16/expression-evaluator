import re


LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

class Lexer:
    """Implements the expression lexer."""

    OPEN_PAR = 1
    CLOSE_PAR = 2
    NUMBER = 3
    PLUS      = 4
    MINUS     = 5
    MULTIPLY  = 6
    DIVIDE    = 7
    POWER = 8
    IDENTIFIER = 9

    def __init__(self, data):
        """Initialize object."""
        self.data = data
        self.current = 0
        self.previous = -1
        self.num_re = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")
        self.identifier = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")


    def __iter__(self):
        """Start the lexer iterator."""
        self.current = 0
        return self

    def error(self, msg=None):
        err = (
            f"Error at {self.current}: "
            f"{self.data[self.current - 1:self.current + 10]}"
        )
        if msg is not None:
            err = f"{msg}\n{err}"
        raise Exception(err)

    def put_back(self):
        self.current = self.previous

    def __next__(self):
        """Retrieve the next token."""
        if self.current < len(self.data):
            while self.data[self.current] in " \t\n\r":
                self.current += 1
            self.previous = self.current
            char = self.data[self.current]
            self.current += 1
            if char == "(":
                return (Lexer.OPEN_PAR, char)
            if char == ")":
                return (Lexer.CLOSE_PAR, char)
            if char == "+":
                return (Lexer.PLUS, char)
            if char == "-":
                return (Lexer.MINUS, char)
            if char == "*":
                return (Lexer.MULTIPLY, char)
            if char == "/":
                return (Lexer.DIVIDE, char)
            if char in "^":
                return (Lexer.POWER, char)
            # user defined identifier
            if char in LETTERS:
                self.current -= 1
                identifier = self.identifier.match(self.data, self.current)
                if identifier is None:
                    self.error("Invalid identifier")
                self.current = identifier.end()
                return (Lexer.IDENTIFIER, identifier.group())
            match = self.num_re.match(self.data[self.current - 1 :])
            if match is None:
                # If we get here, there is an error an unexpected char.
                raise Exception(
                    f"Error at {self.current}: "
                    f"{self.data[self.current - 1:self.current + 10]}"
                )
            self.current += match.end() - 1
            return (Lexer.NUMBER, match.group().replace(" ", ""))
        raise StopIteration()


def parse_E(data):
    """Parse an expression E."""
    T = parse_T(data)
    E_prime = parse_E_prime(data)
    return T if E_prime is None else T + E_prime


def parse_E_prime(data):
    """Parse an expression E'."""
    try:
        token, operator = next(data)
    except StopIteration:
        return None
    if token != Lexer.OPEN_PAR and token != Lexer.CLOSE_PAR:
        if token != Lexer.PLUS and token != Lexer.MINUS:
            data.error(f"Unexpected token: '{operator}'.")
        T = parse_T(data)
        # We don't need the result of the recursion,
        # only the recuscion itself
        _E_prime = parse_E_prime(data)  # noqa
        return T if operator == "+" else -1 * T
    data.put_back()
    return None


def parse_T(data):
    """Parse an expression T."""
    F = parse_F(data)
    T_prime = parse_T_prime(data)
    F_prime = parse_F_prime(data)

    if F_prime is not None:
        return F ** F_prime
    print('parse_T',F, T_prime)
    return F if T_prime is None else F * T_prime

def parse_F_prime(data):
    try:
        token, operator = next(data)
    except StopIteration:
        return None
    if token == Lexer.POWER:
        F = parse_F(data)
        _F_prime = parse_F_prime(data)
        return F if operator == "^" else None
    data.put_back()
    return None

def parse_T_prime(data):
    """Parse an expression T'."""
    try:
        token, operator = next(data)
    except StopIteration:
        return None
    if token == Lexer.MULTIPLY or token == Lexer.DIVIDE:
        # else:
        F = parse_F(data)
        _T_prime = parse_T_prime(data)  # noqa
        if _T_prime is not None:
            return F * _T_prime
        # We don't need the result of the recursion,
        # only the recuscion itself
        return F if operator == "*" else 1 / F
    data.put_back()
    return None

def parse_F(data):
    """Parse an expression F."""
    try:
        token, value = next(data)
    except StopIteration:
        raise Exception("Unexpected end of source.") from None
    if token == Lexer.OPEN_PAR:
        E = parse_E(data)
        if next(data) != (Lexer.CLOSE_PAR, ")"):
            data.error("Unbalanced parenthesis.")
        return E
    if token == Lexer.NUMBER:
        return float(value)
    raise data.error(f"Unexpected token: {value}.")


def parse(source_code):
    """Parse the source code."""
    lexer = Lexer(source_code)
    return parse_E(lexer)


if __name__ == "__main__":
    expressions = [
        "4 ^ 3",
        "4 * 4 * 5",
        "4 ^ 2 + (2 + 3)",
        "4 * 4 * 4",
        "105 / 9"
    ]
    for expression in expressions:
        print(f"Expression: {expression}\t Result: {parse(expression)}")