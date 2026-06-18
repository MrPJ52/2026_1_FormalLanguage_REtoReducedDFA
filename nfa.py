"""Skeleton for Thompson-construction epsilon-NFA building."""

from __future__ import annotations

from dataclasses import dataclass, field

from ast_node import Node

EPSILON = "ε"


@dataclass(slots=True)
class NFAFragment:
    """Temporary fragment used while assembling a Thompson NFA."""

    start_state: int
    final_state: int


@dataclass(slots=True)
class NFA:
    """Epsilon-NFA representation."""

    states: set[int] = field(default_factory=set)
    alphabet: set[str] = field(default_factory=set)
    start_state: int | None = None
    final_states: set[int] = field(default_factory=set)
    transitions: dict[int, dict[str, set[int]]] = field(default_factory=dict)
    _next_state_id: int = 0

    def new_state(self) -> int:
        """Allocate and register a new state identifier."""
        state = self._next_state_id
        self._next_state_id += 1
        self.states.add(state)
        return state

    def add_transition(self, src: int, symbol: str, dst: int) -> None:
        """Add one transition to the NFA transition graph."""
        if symbol != EPSILON:
            self.alphabet.add(symbol)
        self.transitions.setdefault(src, {}).setdefault(symbol, set()).add(dst)

    def _format_transition_rows(self) -> list[tuple[str, str, str]]:
        """Return sorted transition rows as string tuples for table rendering."""
        rows: list[tuple[str, str, str]] = []
        for src in sorted(self.transitions):
            for symbol in sorted(self.transitions[src], key=lambda item: (item != EPSILON, item)):
                dst_states = sorted(self.transitions[src][symbol])
                dst_text = "{" + ", ".join(str(state) for state in dst_states) + "}"
                rows.append((str(src), symbol, dst_text))
        return rows

    def print_transition_table(self) -> None:
        """Print NFA transitions as a plain text table."""
        rows = self._format_transition_rows()
        if not rows:
            print("(no transitions)")
            return

        header = ("SRC", "SYMBOL", "DST")
        src_width = max(len(header[0]), *(len(row[0]) for row in rows))
        symbol_width = max(len(header[1]), *(len(row[1]) for row in rows))
        dst_width = max(len(header[2]), *(len(row[2]) for row in rows))

        border = f"+-{'-' * src_width}-+-{'-' * symbol_width}-+-{'-' * dst_width}-+"
        header_line = (
            f"| {header[0].ljust(src_width)} | "
            f"{header[1].ljust(symbol_width)} | "
            f"{header[2].ljust(dst_width)} |"
        )

        print(border)
        print(header_line)
        print(border)
        for src, symbol, dst in rows:
            print(f"| {src.ljust(src_width)} | {symbol.ljust(symbol_width)} | {dst.ljust(dst_width)} |")
        print(border)


def _build_fragment(nfa: NFA, ast: Node) -> NFAFragment:
    """Recursively build a Thompson fragment for an AST subtree.

    For each AST node kind, returns a fragment with entry and exit states.
    Fragments are combined using epsilon transitions where needed.
    """
    if ast.kind == "literal":
        start = nfa.new_state()
        final = nfa.new_state()
        nfa.add_transition(start, ast.value, final)
        return NFAFragment(start, final)

    if ast.kind == "union":
        if ast.left is None or ast.right is None:
            raise ValueError("Union node must have two children.")

        left_frag = _build_fragment(nfa, ast.left)
        right_frag = _build_fragment(nfa, ast.right)

        start = nfa.new_state()
        final = nfa.new_state()

        nfa.add_transition(start, EPSILON, left_frag.start_state)
        nfa.add_transition(start, EPSILON, right_frag.start_state)
        nfa.add_transition(left_frag.final_state, EPSILON, final)
        nfa.add_transition(right_frag.final_state, EPSILON, final)

        return NFAFragment(start, final)

    if ast.kind == "concat":
        if ast.left is None or ast.right is None:
            raise ValueError("Concat node must have two children.")

        left_frag = _build_fragment(nfa, ast.left)
        right_frag = _build_fragment(nfa, ast.right)

        nfa.add_transition(left_frag.final_state, EPSILON, right_frag.start_state)
        return NFAFragment(left_frag.start_state, right_frag.final_state)

    if ast.kind == "star":
        if ast.left is None:
            raise ValueError("Star node must have a left child.")

        child_frag = _build_fragment(nfa, ast.left)

        start = nfa.new_state()
        final = nfa.new_state()

        nfa.add_transition(start, EPSILON, child_frag.start_state)
        nfa.add_transition(start, EPSILON, final)
        nfa.add_transition(child_frag.final_state, EPSILON, child_frag.start_state)
        nfa.add_transition(child_frag.final_state, EPSILON, final)

        return NFAFragment(start, final)

    raise ValueError(f"Unsupported AST node kind: {ast.kind}")


def build_nfa_from_ast(ast: Node) -> NFA:
    """Build an epsilon-NFA from an AST using Thompson construction.

    Steps:
    1. Create a new NFA object
    2. Recursively build fragments for the entire AST
    3. Set the start state and final states
    4. Return the complete NFA
    """
    nfa = NFA()
    root_fragment = _build_fragment(nfa, ast)
    nfa.start_state = root_fragment.start_state
    nfa.final_states.add(root_fragment.final_state)
    return nfa


def main() -> None:
    """Run NFA demo: regex input -> AST build -> NFA build -> print components."""
    from regex_parser import parse_regex

    print("Thompson NFA demo")
    regex = input("Enter regular expression: ").strip()

    try:
        ast = parse_regex(regex)
        nfa = build_nfa_from_ast(ast)
    except ValueError as exc:
        print(f"Build error: {exc}")
        return

    print("\n=== AST (nested list) ===")
    print(ast.to_nested_list())

    print("\n=== NFA Components ===")
    print(f"States: {sorted(nfa.states)}")
    print(f"Alphabet: {sorted(nfa.alphabet)}")
    print(f"Start state: {nfa.start_state}")
    print(f"Final states: {sorted(nfa.final_states)}")

    print("\n=== NFA Transition Table ===")
    nfa.print_transition_table()


if __name__ == "__main__":
    main()
