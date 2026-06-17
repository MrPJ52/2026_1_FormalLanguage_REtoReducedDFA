"""Parser test skeletons for the regex assignment."""

from __future__ import annotations

import sys
from pathlib import Path

import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from regex_parser import parse_regex


class ParserSkeletonTests(unittest.TestCase):
    """Skeleton tests for nested-list AST expectations."""

    def test_literal_a(self) -> None:
        """Assert that `a` parses to the literal AST `a`."""
        ast = parse_regex("a")
        self.assertEqual(ast.to_nested_list(), "a")

    def test_union_a_plus_b(self) -> None:
        """Assert that `a+b` parses to a union AST."""
        ast = parse_regex("a+b")
        self.assertEqual(ast.to_nested_list(), ["+", "a", "b"])

    def test_concat_ab(self) -> None:
        """Assert that `ab` gets explicit concatenation in the AST."""
        ast = parse_regex("ab")
        self.assertEqual(ast.to_nested_list(), ["·", "a", "b"])

    def test_star_a(self) -> None:
        """Assert that `a*` parses to a star AST."""
        ast = parse_regex("a*")
        self.assertEqual(ast.to_nested_list(), ["*", "a"])

    def test_grouped_a_b_plus_c_star(self) -> None:
        """Assert that `a(b+c)*` respects parentheses and precedence."""
        ast = parse_regex("a(b+c)*")
        self.assertEqual(ast.to_nested_list(), ["·", "a", ["*", ["+", "b", "c"]]])

    def test_assignment_example(self) -> None:
        """Assert that `aA+b+0c*` matches the assignment's example AST."""
        ast = parse_regex("aA+b+0c*")
        self.assertEqual(
            ast.to_nested_list(),
            ["+", ["+", ["·", "a", "A"], "b"], ["·", "0", ["*", "c"]]]
        )


if __name__ == "__main__":
    unittest.main()
