"""NFA test skeletons for Thompson construction."""

from __future__ import annotations

import sys
from pathlib import Path

import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from ast_node import Node
from nfa import EPSILON, build_nfa_from_ast


class ThompsonSkeletonTests(unittest.TestCase):
    """Skeleton tests for Thompson-construction cases."""

    def test_literal_fragment(self) -> None:
        """Verify literal Thompson fragment shape and transitions."""
        ast = Node(kind="literal", value="a")
        nfa = build_nfa_from_ast(ast)

        self.assertEqual(len(nfa.states), 2)
        self.assertIn("a", nfa.alphabet)
        self.assertIsNotNone(nfa.start_state)
        self.assertEqual(len(nfa.final_states), 1)
        
        final_state = list(nfa.final_states)[0]
        self.assertIn(nfa.start_state, nfa.transitions)
        self.assertIn("a", nfa.transitions[nfa.start_state])
        self.assertIn(final_state, nfa.transitions[nfa.start_state]["a"])

    def test_union_fragment(self) -> None:
        """Verify union Thompson fragment with epsilon branches."""
        left_ast = Node(kind="literal", value="a")
        right_ast = Node(kind="literal", value="b")
        ast = Node(kind="union", value="+", left=left_ast, right=right_ast)
        nfa = build_nfa_from_ast(ast)

        self.assertIsNotNone(nfa.start_state)
        self.assertEqual(len(nfa.final_states), 1)
        
        self.assertIn(nfa.start_state, nfa.transitions)
        self.assertIn(EPSILON, nfa.transitions[nfa.start_state])
        self.assertEqual(len(nfa.transitions[nfa.start_state][EPSILON]), 2)
        
        self.assertIn("a", nfa.alphabet)
        self.assertIn("b", nfa.alphabet)

    def test_concat_fragment(self) -> None:
        """Verify concat Thompson fragment linking two sub-fragments."""
        left_ast = Node(kind="literal", value="a")
        right_ast = Node(kind="literal", value="b")
        ast = Node(kind="concat", value="·", left=left_ast, right=right_ast)
        nfa = build_nfa_from_ast(ast)

        self.assertIsNotNone(nfa.start_state)
        self.assertEqual(len(nfa.final_states), 1)
        self.assertIn("a", nfa.alphabet)
        self.assertIn("b", nfa.alphabet)

    def test_star_fragment(self) -> None:
        """Verify star Thompson fragment loop and bypass transitions."""
        child_ast = Node(kind="literal", value="a")
        ast = Node(kind="star", value="*", left=child_ast)
        nfa = build_nfa_from_ast(ast)

        self.assertIsNotNone(nfa.start_state)
        self.assertEqual(len(nfa.final_states), 1)
        
        self.assertIn(nfa.start_state, nfa.transitions)
        self.assertIn(EPSILON, nfa.transitions[nfa.start_state])
        self.assertEqual(len(nfa.transitions[nfa.start_state][EPSILON]), 2)


if __name__ == "__main__":
    unittest.main()
