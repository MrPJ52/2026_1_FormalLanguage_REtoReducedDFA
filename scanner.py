"""Skeleton scanner based on the final Reduced DFA."""

from __future__ import annotations

from dfa import DFA


def scan(dfa: DFA, input_string: str) -> bool:
    """Return whether the DFA accepts the given input string.

    TODO:
    - Consume input one symbol at a time using DFA transitions.
    - Decide how to report dead transitions in a scanner-style workflow.
    """
    raise NotImplementedError("scan() is not implemented yet.")


def trace_scan(dfa: DFA, input_string: str) -> bool:
    """Trace a scan step-by-step and print accept/reject status.

    TODO:
    - Print current state, input symbol, next state, and final verdict.
    - Print accepted input as TOKEN(REGEX_TOKEN, "value") on success.
    """
    raise NotImplementedError("trace_scan() is not implemented yet.")
