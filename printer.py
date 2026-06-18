"""Console-oriented pretty printers for ASTs and automata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ast_node import Node
from dfa import DFA
from nfa import NFA


def print_ast(ast: Node) -> None:
    """Print a readable summary of an AST."""
    print("AST nested list:")
    print(ast.to_nested_list())


def print_nfa(nfa: NFA) -> None:
    """Print a readable summary of an NFA."""
    print("NFA states:", sorted(nfa.states))
    print("NFA alphabet:", sorted(nfa.alphabet))
    print("NFA start state:", nfa.start_state)
    print("NFA final states:", sorted(nfa.final_states))
    nfa.print_transition_table()


def print_dfa(dfa: DFA, title: str = "DFA") -> None:
    """Print a readable summary of a DFA-like automaton."""
    print(f"{title} states:", sorted(dfa.states, key=str))
    print(f"{title} alphabet:", sorted(dfa.alphabet))
    print(f"{title} start state:", dfa.start_state)
    print(f"{title} final states:", sorted(dfa.final_states, key=str))
    print_transition_table(dfa)


def print_transition_table(automaton: Any) -> None:
    """Print transition data in a simple tabular text format."""
    print("Transitions:")
    transitions = getattr(automaton, "transitions", {})
    if not transitions:
        print("  (no transitions)")
        return
    for src in sorted(transitions, key=str):
        for symbol, destinations in sorted(transitions[src].items(), key=lambda item: item[0]):
            print(f"  {src} --{symbol}--> {destinations}")


def export_ast_to_json(ast: Node, path: str | Path) -> None:
    """Export AST data to JSON for future visualization tooling.

    TODO:
    - Replace the nested-list export with a richer node/edge JSON shape for D3.js.
    """
    Path(path).write_text(json.dumps(ast.to_nested_list(), ensure_ascii=False, indent=2), encoding="utf-8")


def export_automaton_to_json(automaton: Any, path: str | Path) -> None:
    """Export automaton data to JSON for future visualization tooling.

    TODO:
    - Define a stable JSON schema for automaton states, edges, and metadata.
    """
    payload = {
        "states": sorted(getattr(automaton, "states", []), key=str),
        "alphabet": sorted(getattr(automaton, "alphabet", [])),
        "start_state": getattr(automaton, "start_state", None),
        "final_states": sorted(getattr(automaton, "final_states", []), key=str),
        "transitions": getattr(automaton, "transitions", {}),
    }
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
