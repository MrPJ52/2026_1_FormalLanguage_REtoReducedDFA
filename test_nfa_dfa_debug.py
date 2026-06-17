"""Debug NFA-to-DFA conversion step by step."""

from regex_parser import parse_regex
from nfa import build_nfa_from_ast, EPSILON
from dfa import epsilon_closure, move, nfa_to_dfa

regex = "a(b+c)*"
print(f"Input regex: {regex}\n")

ast = parse_regex(regex)
nfa = build_nfa_from_ast(ast)

print("--- Step 1: Start closure ---")
start_closure = epsilon_closure(nfa, {nfa.start_state})
print(f"epsilon_closure({{ {nfa.start_state} }}) = {start_closure}")

print("\n--- Step 2: From start, follow 'a' ---")
after_a = move(nfa, start_closure, 'a')
print(f"move({start_closure}, 'a') = {after_a}")
closure_after_a = epsilon_closure(nfa, after_a)
print(f"epsilon_closure({after_a}) = {closure_after_a}")

print("\n--- Step 3: From closure_after_a, follow 'b' ---")
after_b = move(nfa, closure_after_a, 'b')
print(f"move({closure_after_a}, 'b') = {after_b}")
if after_b:
    closure_after_b = epsilon_closure(nfa, after_b)
    print(f"epsilon_closure({after_b}) = {closure_after_b}")

print("\n--- Step 4: From closure_after_a, follow 'c' ---")
after_c = move(nfa, closure_after_a, 'c')
print(f"move({closure_after_a}, 'c') = {after_c}")
if after_c:
    closure_after_c = epsilon_closure(nfa, after_c)
    print(f"epsilon_closure({after_c}) = {closure_after_c}")

print("\n--- Calling nfa_to_dfa ---")
dfa = nfa_to_dfa(nfa)
print(f"DFA created with {len(dfa.states)} states")
print(f"DFA states: {dfa.states}")
