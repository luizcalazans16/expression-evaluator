import re


class Lexer:
    """Implements the expression lexer."""

    OPEN_PAR = 1
    CLOSE_PAR = 2
    NUMBER = 3
    OPERATOR = 4
    IDENTIFIER = 5

    def __init__(self, data):
        """Initialize object."""
        self.data = data
        self.current = 0
        self.previous = -1
        self.num_re = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(e\d+)?")
        self.identifier = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
        self.symbol_table = {}

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

    def next_operator(self):
        char = self.data[self.current + 1]
        if char in "+/*^=":
            return (Lexer.OPERATOR, char)
        return None

    def add_to_symbol_table(self, value, key):
        self.symbol_table[key] = value
        return value

    def get_from_symbol_table(self, value):
        return self.symbol_table.get(value)

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
            if char in "+/*^=":
                return (Lexer.OPERATOR, char)

            match_variable = self.identifier.match(
                self.data[self.current - 1:])
            match = self.num_re.match(self.data[self.current - 1:])

            if match_variable is not None:
                self.current += match_variable.end() - 1
                return (Lexer.IDENTIFIER,
                        match_variable.group().replace(" ", ""))

            if match is None and match_variable is None:
                if char == "-":
                    return (Lexer.OPERATOR, char)
                raise Exception(
                    f"Error at {self.current}: "
                    f"{self.data[self.current - 1:self.current + 10]}"
                )
            else:
                self.current += match.end() - 1
                return (Lexer.NUMBER, match.group().replace(" ", ""))
        raise StopIteration()


def parse_E(data):
    """Parse an expression E."""
    T = parse_T(data)
    E_prime = parse_E_prime(data)
    return T if E_prime is None else T + E_prime


def parse_P(data):
    return parse_S(data)
    if P_prime is not None:
        return parse_P(data=data)
    else:
        return P_prime


def parse_S(data):
    ID = parse_Id(data)
    equals = parse_equals(data)
    data.add_to_symbol_table(equals, ID)
    if equals is None:
        return parse_E(data=data)
    return parse_S(data=data)


def parse_equals(data):
    try:
        token, operator = next(data)
    except StopIteration:
        return None
    if token == Lexer.OPERATOR and operator == "=":
        return parse_E(data=data)
    data.put_back()
    return None


def parse_Id(data):
    try:
        token, value = next(data)
    except StopIteration:
        return None

    if token == Lexer.IDENTIFIER:
        if data.next_operator() == (Lexer.OPERATOR, "="):
            return value
    data.put_back()
    return None


def parse_E_prime(data):
    """Parse an expression E'."""
    try:
        token, operator = next(data)
    except StopIteration:
        return None

    if token == Lexer.OPERATOR:
        if operator not in "+-":
            data.error(f"Unexpected token: '{operator}'.")
        T = parse_T(data)
        _E_prime = parse_E_prime(data)
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
    return F if T_prime is None else F * T_prime


def parse_F_prime(data):
    """Parse an expression T'."""
    try:
        token, operator = next(data)
    except StopIteration:
        return None
    if token == Lexer.OPERATOR and operator in "^":
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
    if token == Lexer.OPERATOR and operator in "*/":
        # else:
        F = parse_F(data)
        _T_prime = parse_T_prime(data)  # noqa
        if _T_prime is not None:
            return F * _T_prime
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
    if token == Lexer.IDENTIFIER:
        return data.get_from_symbol_table(value)
    raise data.error(f"Unexpected token: {value}.")


def parse(source_code):
    """Parse the source code."""
    lexer = Lexer(source_code)
    return parse_P(lexer)


if __name__ == "__main__":
    expressions = [
        "x = 2 ^ 2 y = 4 (x + y) / 2",
        "4 ^ 3",
        "4 * 4 * 5",
        "4 ^ 2 + (2 + 3)",
        "4 * 4 * 4",
        "105 / 9"
    ]
    for expression in expressions:
        print(f"Expression: {expression}\t Result: {parse(expression)}")
