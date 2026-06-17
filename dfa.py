"""Skeleton for subset construction and DFA minimization."""

from __future__ import annotations

from dataclasses import dataclass, field

from nfa import NFA


@dataclass(slots=True)
class DFA:
    """Deterministic finite automaton representation."""

    states: set[object] = field(default_factory=set)
    alphabet: set[str] = field(default_factory=set)
    start_state: object | None = None
    final_states: set[object] = field(default_factory=set)
    transitions: dict[object, dict[str, object]] = field(default_factory=dict)


def epsilon_closure(nfa: NFA, states: set[int] | frozenset[int]) -> frozenset[int]:
    """Return the epsilon-closure of a set of NFA states.

    TODO:
    - Implement DFS/BFS over epsilon transitions.
    - Reuse this in subset construction without duplicating traversal logic.
    """
    raise NotImplementedError("epsilon_closure() is not implemented yet.")


def move(nfa: NFA, states: set[int] | frozenset[int], symbol: str) -> frozenset[int]:
    """Return all NFA states reachable by one symbol transition.

    TODO:
    - Collect transitions from each source state for the given symbol.
    - Keep output compatible with `epsilon_closure()` and subset construction.
    """
    raise NotImplementedError("move() is not implemented yet.")


def nfa_to_dfa(nfa: NFA) -> DFA:
    """Convert an epsilon-NFA to a DFA using subset construction.

    TODO:
    - Use frozenset-based DFA states.
    - Track discovered subsets with a work queue.
    - Mark final states when a subset contains an NFA final state.
    """
    raise NotImplementedError("nfa_to_dfa() is not implemented yet.")


def remove_unreachable_states(dfa: DFA) -> DFA:
    """Return an equivalent DFA with unreachable states removed.

    TODO:
    - Traverse from the start state.
    - Rebuild a filtered DFA preserving alphabet and transitions.
    """
    raise NotImplementedError("remove_unreachable_states() is not implemented yet.")


def minimize_dfa(dfa: DFA) -> DFA:
    """Minimize a DFA to produce the Reduced DFA.

    TODO:
    - Choose a minimization algorithm, such as partition refinement.
    - Preserve acceptance semantics while collapsing equivalent states.
    """
    raise NotImplementedError("minimize_dfa() is not implemented yet.")


def rename_dfa_states(dfa: DFA) -> DFA:
    """Rename DFA states to user-friendly labels such as D0, D1, D2.

    TODO:
    - Order states deterministically.
    - Rebuild the transition table with renamed states.
    """
    raise NotImplementedError("rename_dfa_states() is not implemented yet.")
