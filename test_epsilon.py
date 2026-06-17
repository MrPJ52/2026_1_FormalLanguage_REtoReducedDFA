"""Debug epsilon_closure and move."""

from regex_parser import parse_regex
from nfa import build_nfa_from_ast, EPSILON
from dfa import epsilon_closure, move

regex = "a(b+c)*"
print(f"Input regex: {regex}\n")

ast = parse_regex(regex)
nfa = build_nfa_from_ast(ast)

print(f"NFA states: {sorted(nfa.states)}")
print(f"NFA start: {nfa.start_state}")
print(f"NFA final: {nfa.final_states}")
print(f"NFA alphabet: {nfa.alphabet}")
print(f"\nNFA transitions:")
for src in sorted(nfa.transitions.keys()):
    for symbol in sorted(nfa.transitions[src].keys()):
        dests = nfa.transitions[src][symbol]
        print(f"  {src} --{symbol}--> {dests}")

print(f"\n--- Testing epsilon_closure ---")
start_closure = epsilon_closure(nfa, {nfa.start_state})
print(f"epsilon_closure({{ {nfa.start_state} }}) = {start_closure}")
