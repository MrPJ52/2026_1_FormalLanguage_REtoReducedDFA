"""Manual test for DFA construction."""

from regex_parser import parse_regex
from nfa import build_nfa_from_ast
from dfa import nfa_to_dfa
from printer import print_ast, print_nfa, print_dfa

regex = "a(b+c)*"
print(f"Input regex: {regex}\n")

ast = parse_regex(regex)
print("=== AST ===")
print_ast(ast)

nfa = build_nfa_from_ast(ast)
print("\n=== NFA ===")
print_nfa(nfa)

dfa = nfa_to_dfa(nfa)
print("\n=== DFA ===")
print_dfa(dfa)
