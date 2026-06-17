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


def build_nfa_from_ast(ast: Node) -> NFA:
    """Build an epsilon-NFA from an AST using Thompson construction.

    TODO:
    - Implement recursive fragment construction for literal, union, concat, star.
    - Wire fragment entry/exit states with epsilon transitions.
    - Finalize `start_state`, `final_states`, and transition table.
    """
    raise NotImplementedError(
        "Thompson construction skeleton is in place, but build_nfa_from_ast() is not implemented yet."
    )
