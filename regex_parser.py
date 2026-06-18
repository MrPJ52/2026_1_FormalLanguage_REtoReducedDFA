"""Parser utilities for converting regex strings into AST nodes."""

from __future__ import annotations

import json
import webbrowser
from pathlib import Path
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


def _ast_to_d3_tree(node: Node) -> dict[str, object]:
        """Convert AST node into a D3-hierarchy compatible dict."""
        if node.kind == "literal":
                return {"name": f"literal: {node.value}", "children": []}

        if node.kind == "star":
                if node.left is None:
                        raise ValueError("Star node must have a left child.")
                return {
                        "name": "star (*)",
                        "children": [_ast_to_d3_tree(node.left)],
                }

        if node.left is None or node.right is None:
                raise ValueError(f"{node.kind} node must have two children.")

        if node.kind == "concat":
                label = "concat (·)"
        elif node.kind == "union":
                label = "union (+)"
        else:
                raise ValueError(f"Unsupported node kind for visualization: {node.kind}")

        return {
                "name": label,
                "children": [_ast_to_d3_tree(node.left), _ast_to_d3_tree(node.right)],
        }


def generate_d3_ast_html(ast: Node, output_path: Path) -> Path:
        """Generate a standalone HTML file with a D3 tree visualization for the AST."""
        tree_data = _ast_to_d3_tree(ast)
        payload = json.dumps(tree_data, ensure_ascii=False)

        html = f"""<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Regex AST D3 Tree</title>
    <style>
        :root {{
            --bg-1: #f4f9ff;
            --bg-2: #fdf7f2;
            --ink: #1f2a37;
            --accent: #0d9488;
            --node: #2563eb;
            --leaf: #16a34a;
            --edge: #64748b;
        }}
        body {{
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--ink);
            background: radial-gradient(circle at 20% 20%, var(--bg-1) 0%, var(--bg-2) 100%);
        }}
        header {{
            padding: 16px 20px;
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(6px);
            border-bottom: 1px solid rgba(100, 116, 139, 0.25);
        }}
        h1 {{ margin: 0; font-size: 1.1rem; }}
        p {{ margin: 6px 0 0; color: #475569; }}
        #tree {{ width: 100%; height: calc(100vh - 78px); }}
        .link {{ fill: none; stroke: var(--edge); stroke-width: 1.8px; }}
        .node circle {{ fill: var(--node); }}
        .node.leaf circle {{ fill: var(--leaf); }}
        .node text {{ font-size: 13px; fill: var(--ink); }}
    </style>
</head>
<body>
    <header>
        <h1>Regex AST Visualization (D3 Tree)</h1>
        <p>Generated from regex_parser.py</p>
    </header>
    <svg id=\"tree\"></svg>

    <script src=\"https://d3js.org/d3.v7.min.js\"></script>
    <script>
        const data = {payload};

        const svg = d3.select('#tree');
        const width = window.innerWidth;
        const height = window.innerHeight - 78;

        svg.attr('viewBox', [0, 0, width, height]);

        const root = d3.hierarchy(data);
        const treeLayout = d3.tree().size([width - 80, height - 80]);
        treeLayout(root);

        const g = svg.append('g').attr('transform', 'translate(40, 40)');

        g.selectAll('.link')
            .data(root.links())
            .enter()
            .append('path')
            .attr('class', 'link')
            .attr('d', d3.linkVertical()
                .x(d => d.x)
                .y(d => d.y)
            );

        const node = g.selectAll('.node')
            .data(root.descendants())
            .enter()
            .append('g')
            .attr('class', d => 'node' + ((d.children && d.children.length) ? '' : ' leaf'))
            .attr('transform', d => `translate(${{d.x}},${{d.y}})`);

        node.append('circle').attr('r', 8);

        node.append('text')
            .attr('dy', -12)
            .attr('text-anchor', 'middle')
            .text(d => d.data.name);
    </script>
</body>
</html>
"""

        output_path.write_text(html, encoding="utf-8")
        return output_path


def main() -> None:
    """Run parser-only CLI for quick AST inspection."""
    print("Regex Parser (AST) demo")
    regex = input("Enter regular expression: ").strip()

    try:
        ast = parse_regex(regex)
    except ValueError as exc:
        print(f"Parse error: {exc}")
        return

    print("AST (nested list):")
    print(ast.to_nested_list())

    ast_size = ast.size()
    arc_bound, arc_exact = ast.count_arcs()

    print(f"AST size: {ast_size}")
    print(f"Arc upper bound: {arc_bound}")
    print(f"Exact arc count: {arc_exact}")

    output_path = Path(__file__).with_name("ast_tree.html")
    generated = generate_d3_ast_html(ast, output_path)
    print(f"D3 AST HTML generated: {generated}")

    opened = webbrowser.open(generated.resolve().as_uri())
    if opened:
        print("Opened visualization in your default browser.")
    else:
        print("Could not auto-open browser. Open ast_tree.html manually.")


if __name__ == "__main__":
    main()
