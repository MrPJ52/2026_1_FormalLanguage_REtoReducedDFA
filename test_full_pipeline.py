"""Test full pipeline: regex -> AST -> NFA -> DFA -> minimize -> rename -> scan."""

from ast_node import Node
from dfa import minimize_dfa, nfa_to_dfa, remove_unreachable_states, rename_dfa_states
from nfa import build_nfa_from_ast
from printer import print_ast, print_dfa
from regex_parser import parse_regex
from scanner import trace_scan

regex = "a"
ast = parse_regex(regex)

print(f"Input regex: {regex}\n")
print("=== AST ===")
print_ast(ast)

nfa = build_nfa_from_ast(ast)
print("\n=== NFA -> DFA ===")

dfa = nfa_to_dfa(nfa)
print(f"DFA states before cleanup: {len(dfa.states)}")

reachable_dfa = remove_unreachable_states(dfa)
print(f"After unreachable removal: {len(reachable_dfa.states)}")

minimized = minimize_dfa(dfa)
print(f"After minimization: {len(minimized.states)}")

renamed = rename_dfa_states(minimized)
print_dfa(renamed, title="Final Reduced DFA")

print("\n=== Scanner ===")
trace_scan(renamed, "a")
