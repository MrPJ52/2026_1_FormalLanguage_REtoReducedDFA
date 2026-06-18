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

    Uses BFS to traverse all epsilon transitions from the given states.
    """
    from nfa import EPSILON
    
    closure: set[int] = set(states)
    queue: list[int] = list(states)
    
    while queue:
        state = queue.pop(0)
        if state not in nfa.transitions:
            continue
        if EPSILON not in nfa.transitions[state]:
            continue
        
        for next_state in nfa.transitions[state][EPSILON]:
            if next_state not in closure:
                closure.add(next_state)
                queue.append(next_state)
    
    return frozenset(closure)


def move(nfa: NFA, states: set[int] | frozenset[int], symbol: str) -> frozenset[int]:
    """Return all NFA states reachable by one symbol transition.

    Collects transitions from each source state for the given symbol.
    """
    result: set[int] = set()
    for state in states:
        if state not in nfa.transitions:
            continue
        if symbol not in nfa.transitions[state]:
            continue
        result.update(nfa.transitions[state][symbol])
    
    return frozenset(result)


def nfa_to_dfa(nfa: NFA) -> DFA:
    """Convert an epsilon-NFA to a DFA using subset construction.

    Algorithm:
    1. Start with the epsilon-closure of the NFA start state
    2. Maintain a worklist of DFA states to process
    3. For each DFA state and each symbol, compute the next DFA state
    4. Mark DFA states as final if they contain any NFA final state
    """
    if nfa.start_state is None:
        raise ValueError("NFA must have a start state")
    
    dfa = DFA()
    dfa.alphabet = nfa.alphabet.copy()
    
    start_closure = epsilon_closure(nfa, {nfa.start_state})
    dfa.start_state = start_closure
    
    worklist: list[frozenset[int]] = [start_closure]
    processed: set[frozenset[int]] = set()
    
    while worklist:
        current_nfa_states = worklist.pop(0)
        if current_nfa_states in processed:
            continue
        processed.add(current_nfa_states)
        
        dfa.states.add(current_nfa_states)
        
        if any(nfa_state in nfa.final_states for nfa_state in current_nfa_states):
            dfa.final_states.add(current_nfa_states)
        
        for symbol in sorted(dfa.alphabet):
            next_nfa_states = move(nfa, current_nfa_states, symbol)
            if not next_nfa_states:
                continue
            next_closure = epsilon_closure(nfa, next_nfa_states)
            
            dfa.transitions.setdefault(current_nfa_states, {})[symbol] = next_closure
            
            if next_closure not in processed:
                worklist.append(next_closure)
    
    return dfa


def remove_unreachable_states(dfa: DFA) -> DFA:
    """Return an equivalent DFA with unreachable states removed.

    Traverse from the start state, keep only reachable states, and rebuild a
    filtered DFA that preserves the original language.
    """
    if dfa.start_state is None:
        raise ValueError("DFA must have a start state")

    reachable: set[object] = set()
    queue: list[object] = [dfa.start_state]

    while queue:
        state = queue.pop(0)
        if state in reachable:
            continue
        reachable.add(state)

        for symbol, next_state in dfa.transitions.get(state, {}).items():
            if next_state not in reachable:
                queue.append(next_state)

    filtered = DFA()
    filtered.alphabet = dfa.alphabet.copy()
    filtered.start_state = dfa.start_state
    filtered.states = reachable.copy()
    filtered.final_states = {state for state in dfa.final_states if state in reachable}

    for state in reachable:
        state_transitions = dfa.transitions.get(state, {})
        for symbol, next_state in state_transitions.items():
            if next_state in reachable:
                filtered.transitions.setdefault(state, {})[symbol] = next_state

    return filtered


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
