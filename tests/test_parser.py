"""Parser test skeletons for the regex assignment."""

from __future__ import annotations

import unittest


class ParserSkeletonTests(unittest.TestCase):
    """Skeleton tests for nested-list AST expectations."""

    def test_literal_a(self) -> None:
        """TODO: Assert that `a` parses to the literal AST `a`."""
        self.skipTest("TODO: compare nested list for literal parsing")

    def test_union_a_plus_b(self) -> None:
        """TODO: Assert that `a+b` parses to a union AST."""
        self.skipTest("TODO: compare nested list for union parsing")

    def test_concat_ab(self) -> None:
        """TODO: Assert that `ab` gets explicit concatenation in the AST."""
        self.skipTest("TODO: compare nested list for concatenation parsing")

    def test_star_a(self) -> None:
        """TODO: Assert that `a*` parses to a star AST."""
        self.skipTest("TODO: compare nested list for Kleene star parsing")

    def test_grouped_a_b_plus_c_star(self) -> None:
        """TODO: Assert that `a(b+c)*` respects parentheses and precedence."""
        self.skipTest("TODO: compare nested list for grouped expression parsing")

    def test_assignment_example(self) -> None:
        """TODO: Assert that `aA+b+0c*` matches the assignment's example AST."""
        self.skipTest("TODO: compare nested list for assignment sample input")


if __name__ == "__main__":
    unittest.main()
