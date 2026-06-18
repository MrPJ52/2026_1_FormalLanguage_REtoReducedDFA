"""Simple test for scanner."""

from regex_parser import parse_regex
from nfa import build_nfa_from_ast
from dfa import nfa_to_dfa, minimize_dfa, rename_dfa_states
from scanner import scan, trace_scan

regex = "a"
ast = parse_regex(regex)
nfa = build_nfa_from_ast(ast)
dfa = nfa_to_dfa(nfa)
minimized = minimize_dfa(dfa)
renamed = rename_dfa_states(minimized)

print(f"Regex: {regex}")
print(f"scan('a'): {scan(renamed, 'a')}")
print(f"scan('b'): {scan(renamed, 'b')}")
print()
trace_scan(renamed, "a")
