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
