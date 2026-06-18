"""Skeleton scanner based on the final Reduced DFA."""

from __future__ import annotations

from dfa import DFA


def scan(dfa: DFA, input_string: str) -> bool:
    """Return whether the DFA accepts the given input string.

    Consumes input one symbol at a time using DFA transitions.
    Returns False if any symbol has no defined transition.
    """
    current_state = dfa.start_state
    for char in input_string:
        if current_state not in dfa.transitions:
            return False
        if char not in dfa.transitions[current_state]:
            return False
        current_state = dfa.transitions[current_state][char]
    return current_state in dfa.final_states


def trace_scan(dfa: DFA, input_string: str) -> bool:
    """Trace a scan step-by-step and print accept/reject status.

    Prints each transition and final verdict.
    On acceptance, prints TOKEN(REGEX_TOKEN, "value") format.
    """
    current_state = dfa.start_state
    print(f"Scanning: {input_string!r}")
    print(f"Start state: {current_state}")

    for index, char in enumerate(input_string):
        if current_state not in dfa.transitions:
            print(f"Step {index + 1}: No transitions from state {current_state}")
            print("REJECT: Dead state reached.")
            return False

        if char not in dfa.transitions[current_state]:
            print(f"Step {index + 1}: No transition from {current_state} on {char!r}")
            print("REJECT: No transition for symbol.")
            return False

        next_state = dfa.transitions[current_state][char]
        is_final_marker = " (final)" if next_state in dfa.final_states else ""
        print(f"Step {index + 1}: {current_state} --{char}--> {next_state}{is_final_marker}")
        current_state = next_state

    if current_state in dfa.final_states:
        print(f"ACCEPT: Reached final state {current_state}")
        print(f"TOKEN(REGEX_TOKEN, {input_string!r})")
        return True
    else:
        print(f"REJECT: Ended at non-final state {current_state}")
        return False

