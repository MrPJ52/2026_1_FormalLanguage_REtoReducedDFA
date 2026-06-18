"""CLI entry point for the regex-to-Reduced-DFA project."""

from __future__ import annotations

from ast_node import Node
from dfa import minimize_dfa, nfa_to_dfa, remove_unreachable_states, rename_dfa_states
from nfa import build_nfa_from_ast
from printer import print_ast, print_dfa, print_nfa
from regex_parser import parse_regex
from scanner import trace_scan


def _run_stage(stage_name: str, action):
	"""Run one pipeline stage and print a clear placeholder on missing parts."""
	print(f"\n=== {stage_name} ===")
	try:
		return action()
	except NotImplementedError as exc:
		print(f"[PENDING] {exc}")
		return None


def _print_ast_metrics(ast: Node) -> None:
	"""Print basic AST-derived metrics used later by Thompson construction."""
	print(f"AST size: {ast.size()}")
	states, arcs = ast.count_thompson_states_arcs()
	print(f"Estimated Thompson states: {states}")
	print(f"Estimated Thompson arcs: {arcs}")


def main() -> None:
	"""Run the staged CLI workflow for the assignment project."""
	print("Regex -> Reduced DFA project skeleton")
	regex = input("Enter regular expression: ").strip()

	ast = _run_stage("1-3. Parse regex into AST", lambda: parse_regex(regex))
	if ast is None:
		print("Stopping after parser stage. Implement parser stages next.")
		return

	print_ast(ast)
	_print_ast_metrics(ast)

	nfa = _run_stage("4-5. Build epsilon-NFA", lambda: build_nfa_from_ast(ast))
	if nfa is None:
		print("Stopping after NFA stage. Implement Thompson construction next.")
		return

	print_nfa(nfa)

	dfa = _run_stage("6. Subset construction", lambda: nfa_to_dfa(nfa))
	if dfa is None:
		print("Stopping after DFA stage. Implement subset construction next.")
		return

	print_dfa(dfa, title="DFA")

	reachable_dfa = _run_stage("7. Remove unreachable states", lambda: remove_unreachable_states(dfa))
	if reachable_dfa is None:
		print("Stopping after reachability stage. Implement unreachable-state removal next.")
		return

	reduced_dfa = _run_stage("8. Minimize DFA", lambda: minimize_dfa(reachable_dfa))
	if reduced_dfa is None:
		print("Stopping after minimization stage. Implement DFA minimization next.")
		return

	renamed_dfa = _run_stage("9. Rename Reduced DFA states", lambda: rename_dfa_states(reduced_dfa))
	if renamed_dfa is None:
		print("Stopping after state-renaming stage. Implement state renaming next.")
		return

	print_dfa(renamed_dfa, title="Reduced DFA")

	print("\n=== 10. Scanner ===")
	test_input = input("Enter input string to scan (or empty to skip): ").strip()
	if test_input:
		result = trace_scan(renamed_dfa, test_input)
		if result:
			print(f"Overall result: ACCEPT")
		else:
			print(f"Overall result: REJECT")
	else:
		print("No input provided, skipping scanner.")



if __name__ == "__main__":
	main()
