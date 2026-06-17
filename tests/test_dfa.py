"""DFA test skeletons for subset construction and scanning."""

from __future__ import annotations

import sys
from pathlib import Path

import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from dfa import nfa_to_dfa
from nfa import build_nfa_from_ast
from regex_parser import parse_regex


class DFASkeletonTests(unittest.TestCase):
    """Skeleton tests for DFA acceptance behavior."""

    def _dfa_accepts(self, dfa, input_string: str) -> bool:
        """Check if a DFA accepts the given input string.

        Simple deterministic simulation.
        """
        current_state = dfa.start_state
        for char in input_string:
            if current_state not in dfa.transitions:
                return False
            if char not in dfa.transitions[current_state]:
                return False
            current_state = dfa.transitions[current_state][char]
        return current_state in dfa.final_states

    def test_acceptance_for_a_b_plus_c_star(self) -> None:
        """Build DFA for `a(b+c)*` and verify accepted/rejected strings.

        Accept cases:
        - a
        - ab
        - ac
        - acb
        - abcb
        - abc...

        Reject cases:
        - b
        - ba
        - aa
        - ab (wait, this should be accepted!)
        """
        regex = "a(b+c)*"
        ast = parse_regex(regex)
        nfa = build_nfa_from_ast(ast)
        dfa = nfa_to_dfa(nfa)

        accept_cases = ["a", "ab", "ac", "abc", "acb", "abcb", "acbcb"]
        for test_input in accept_cases:
            with self.subTest(input=test_input):
                self.assertTrue(
                    self._dfa_accepts(dfa, test_input),
                    f"DFA should accept '{test_input}'"
                )

        reject_cases = ["", "b", "ba", "aa", "cab", "ca"]
        for test_input in reject_cases:
            with self.subTest(input=test_input):
                self.assertFalse(
                    self._dfa_accepts(dfa, test_input),
                    f"DFA should reject '{test_input}'"
                )


if __name__ == "__main__":
    unittest.main()