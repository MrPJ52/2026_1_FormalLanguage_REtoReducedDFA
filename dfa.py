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

    Uses partition refinement to merge equivalent states while preserving the
    recognized language.
    """
    if dfa.start_state is None:
        raise ValueError("DFA must have a start state")

    working = remove_unreachable_states(dfa)
    if not working.states:
        return working

    final_group = set(working.final_states)
    non_final_group = set(working.states - working.final_states)

    partitions: list[set[object]] = []
    if final_group:
        partitions.append(final_group)
    if non_final_group:
        partitions.append(non_final_group)

    changed = True
    while changed:
        changed = False
        new_partitions: list[set[object]] = []

        state_to_partition: dict[object, int] = {}
        for part_index, part in enumerate(partitions):
            for state in part:
                state_to_partition[state] = part_index

        for part in partitions:
            buckets: dict[tuple[object, ...], set[object]] = {}

            for state in part:
                signature: list[object] = []
                for symbol in sorted(working.alphabet):
                    next_state = working.transitions.get(state, {}).get(symbol)
                    if next_state is None:
                        signature.append(None)
                    else:
                        signature.append(state_to_partition[next_state])

                bucket_key = tuple(signature)
                buckets.setdefault(bucket_key, set()).add(state)

            new_partitions.extend(buckets.values())
            if len(buckets) > 1:
                changed = True

        partitions = new_partitions

    minimized = DFA()
    minimized.alphabet = working.alphabet.copy()

    part_to_state: dict[int, frozenset[object]] = {}
    state_to_min_state: dict[object, frozenset[object]] = {}

    for part_index, part in enumerate(partitions):
        min_state = frozenset(part)
        part_to_state[part_index] = min_state
        minimized.states.add(min_state)
        for state in part:
            state_to_min_state[state] = min_state

    minimized.start_state = state_to_min_state[working.start_state]

    for part in partitions:
        representative = next(iter(part))
        min_src_state = state_to_min_state[representative]

        if any(state in working.final_states for state in part):
            minimized.final_states.add(min_src_state)

        for symbol, next_state in working.transitions.get(representative, {}).items():
            min_dst_state = state_to_min_state[next_state]
            minimized.transitions.setdefault(min_src_state, {})[symbol] = min_dst_state

    return minimized


def rename_dfa_states(dfa: DFA) -> DFA:
    """Rename DFA states to user-friendly labels such as D0, D1, D2.

    Assigns D0 to the start state and explores remaining states via BFS,
    assigning D1, D2, ... sequentially for deterministic, stable naming.
    """
    if dfa.start_state is None:
        raise ValueError("DFA must have a start state")

    renamed = DFA()
    renamed.alphabet = dfa.alphabet.copy()

    state_to_new_name: dict[object, str] = {}
    new_name_counter = 0
    queue: list[object] = [dfa.start_state]
    visited: set[object] = {dfa.start_state}

    state_to_new_name[dfa.start_state] = f"D{new_name_counter}"
    new_name_counter += 1

    while queue:
        current_state = queue.pop(0)
        for symbol in sorted(dfa.alphabet):
            next_state = dfa.transitions.get(current_state, {}).get(symbol)
            if next_state is None or next_state in visited:
                continue
            visited.add(next_state)
            state_to_new_name[next_state] = f"D{new_name_counter}"
            new_name_counter += 1
            queue.append(next_state)

    renamed.start_state = state_to_new_name[dfa.start_state]
    renamed.states = {state_to_new_name[state] for state in dfa.states}
    renamed.final_states = {state_to_new_name[state] for state in dfa.final_states}

    for old_src, transitions_from_src in dfa.transitions.items():
        new_src = state_to_new_name[old_src]
        for symbol, old_dst in transitions_from_src.items():
            new_dst = state_to_new_name[old_dst]
            renamed.transitions.setdefault(new_src, {})[symbol] = new_dst

    return renamed
