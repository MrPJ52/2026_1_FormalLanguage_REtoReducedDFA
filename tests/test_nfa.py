"""NFA test skeletons for Thompson construction."""

from __future__ import annotations

import unittest


class ThompsonSkeletonTests(unittest.TestCase):
    """Skeleton tests for Thompson-construction cases."""

    def test_literal_fragment(self) -> None:
        """TODO: Verify literal Thompson fragment shape and transitions."""
        self.skipTest("TODO: implement literal Thompson construction test")

    def test_union_fragment(self) -> None:
        """TODO: Verify union Thompson fragment with epsilon branches."""
        self.skipTest("TODO: implement union Thompson construction test")

    def test_concat_fragment(self) -> None:
        """TODO: Verify concat Thompson fragment linking two sub-fragments."""
        self.skipTest("TODO: implement concat Thompson construction test")

    def test_star_fragment(self) -> None:
        """TODO: Verify star Thompson fragment loop and bypass transitions."""
        self.skipTest("TODO: implement star Thompson construction test")


if __name__ == "__main__":
    unittest.main()
