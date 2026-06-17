"""Parser utilities for converting regex strings into AST nodes."""

from __future__ import annotations

from typing import Final

from ast_node import Node

CONCAT_OPERATOR: Final[str] = "·"
UNION_OPERATOR: Final[str] = "+"
STAR_OPERATOR: Final[str] = "*"
LEFT_PAREN: Final[str] = "("
RIGHT_PAREN: Final[str] = ")"
OPERATORS: Final[set[str]] = {CONCAT_OPERATOR, UNION_OPERATOR, STAR_OPERATOR}
PRECEDENCE: Final[dict[str, int]] = {
    UNION_OPERATOR: 1,
    CONCAT_OPERATOR: 2,
    STAR_OPERATOR: 3,
}


def is_literal(ch: str) -> bool:
    """Return whether a token is an allowed literal symbol."""
    return len(ch) == 1 and ch.isalnum()


def tokenize(regex: str) -> list[str]:
    """Split the input regex into one-character tokens.

    TODO:
    - Add richer validation and clearer error messages.
    - Consider supporting escaped characters if the assignment later expands.
    """
    tokens: list[str] = []
    for ch in regex.replace(" ", ""):
        if is_literal(ch) or ch in OPERATORS or ch in {LEFT_PAREN, RIGHT_PAREN}:
            tokens.append(ch)
            continue
        raise ValueError(f"Unsupported regex character: {ch!r}")
    return tokens


def insert_concat(tokens: list[str]) -> list[str]:
    """Insert explicit concatenation operators between adjacent concat terms."""
    result: list[str] = []
    for index, token in enumerate(tokens):
        result.append(token)
        if index == len(tokens) - 1:
            continue

        current_is_concat_term = is_literal(token) or token in {RIGHT_PAREN, STAR_OPERATOR}
        next_token = tokens[index + 1]
        next_starts_concat_term = is_literal(next_token) or next_token == LEFT_PAREN

        if current_is_concat_term and next_starts_concat_term:
            result.append(CONCAT_OPERATOR)
    return result


def to_postfix(tokens: list[str]) -> list[str]:
    """Convert infix regex tokens to postfix using shunting-yard.

    TODO:
    - Re-check associativity handling against the assignment examples.
    - Add stronger malformed-expression detection.
    """
    output: list[str] = []
    operators: list[str] = []

    for token in tokens:
        if is_literal(token):
            output.append(token)
            continue

        if token == LEFT_PAREN:
            operators.append(token)
            continue

        if token == RIGHT_PAREN:
            while operators and operators[-1] != LEFT_PAREN:
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses in regex.")
            operators.pop()
            continue

        if token == STAR_OPERATOR:
            output.append(token)
            continue

        while operators and operators[-1] != LEFT_PAREN and PRECEDENCE[operators[-1]] >= PRECEDENCE[token]:
            output.append(operators.pop())
        operators.append(token)

    while operators:
        operator = operators.pop()
        if operator in {LEFT_PAREN, RIGHT_PAREN}:
            raise ValueError("Mismatched parentheses in regex.")
        output.append(operator)

    return output


def postfix_to_ast(postfix_tokens: list[str]) -> Node:
    """Build an AST from postfix regex tokens."""
    stack: list[Node] = []

    for token in postfix_tokens:
        if is_literal(token):
            stack.append(Node(kind="literal", value=token))
            continue

        if token == STAR_OPERATOR:
            if not stack:
                raise ValueError("Malformed postfix regex: missing operand for star.")
            operand = stack.pop()
            stack.append(Node(kind="star", value=STAR_OPERATOR, left=operand))
            continue

        if len(stack) < 2:
            raise ValueError("Malformed postfix regex: missing binary operands.")
        right = stack.pop()
        left = stack.pop()
        if token == CONCAT_OPERATOR:
            stack.append(Node(kind="concat", value=CONCAT_OPERATOR, left=left, right=right))
        elif token == UNION_OPERATOR:
            stack.append(Node(kind="union", value=UNION_OPERATOR, left=left, right=right))
        else:
            raise ValueError(f"Unknown postfix token: {token}")

    if len(stack) != 1:
        raise ValueError("Malformed postfix regex: AST stack did not collapse to one node.")
    return stack[0]


def parse_regex(regex: str) -> Node:
    """Parse a regex string into an AST.

    This stage is partially implemented because it is a stable foundation for the
    later NFA and DFA phases.
    """
    if not regex:
        raise ValueError("Regex input must not be empty.")
    tokens = tokenize(regex)
    explicit_tokens = insert_concat(tokens)
    postfix_tokens = to_postfix(explicit_tokens)
    return postfix_to_ast(postfix_tokens)
