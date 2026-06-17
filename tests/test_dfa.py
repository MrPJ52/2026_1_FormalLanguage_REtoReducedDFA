"""DFA test skeletons for subset construction and scanning."""

from __future__ import annotations

import unittest


class DFASkeletonTests(unittest.TestCase):
    """Skeleton tests for DFA acceptance behavior."""

    def test_acceptance_for_a_b_plus_c_star(self) -> None:
        """TODO: Build DFA for `a(b+c)*` and verify accepted strings.

        Accept cases to check later:
        - a
        - ab
        - acb
        - abcb

        Reject cases to check later:
        - b
        - ba
        - aa
        """
        self.skipTest("TODO: implement DFA acceptance test for assignment sample")


if __name__ == "__main__":
    unittest.main()