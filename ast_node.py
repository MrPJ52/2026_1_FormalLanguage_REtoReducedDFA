"""AST node definitions for regular expressions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

NodeKind = Literal["literal", "union", "concat", "star"]


@dataclass(slots=True)
class Node:
    """Node in the regular-expression abstract syntax tree."""

    kind: NodeKind
    value: str
    left: Node | None = None
    right: Node | None = None

    def size(self) -> int:
        """Return the number of AST nodes in this subtree."""
        left_size = self.left.size() if self.left is not None else 0
        right_size = self.right.size() if self.right is not None else 0
        return 1 + left_size + right_size

    def to_nested_list(self) -> Any:
        """Return the AST as a nested-list structure for debugging and tests."""
        if self.kind == "literal":
            return self.value
        if self.kind == "star":
            if self.left is None:
                raise ValueError("Star node must have a left child.")
            return [self.value, self.left.to_nested_list()]
        if self.left is None or self.right is None:
            raise ValueError(f"{self.kind} node must have two children.")
        return [self.value, self.left.to_nested_list(), self.right.to_nested_list()]

    def count_arcs(self) -> tuple[int, int]:
        """Return (arc_upper_bound, arc_exact_count) for Thompson construction.

        Arc upper bound is calculated as states² (theoretical maximum).
        Arc exact count is the actual number of arcs in Thompson NFA.
        """
        states, arcs = self._count_thompson_states_arcs()
        arc_upper_bound = states * states
        arc_exact_count = arcs
        return arc_upper_bound, arc_exact_count

    def _count_thompson_states_arcs(self) -> tuple[int, int]:
        """Internal: count Thompson-construction state and arc counts from the AST."""
        if self.kind == "literal":
            return 2, 1
        if self.kind == "union":
            if self.left is None or self.right is None:
                raise ValueError("Union node must have two children.")
            left_states, left_arcs = self.left._count_thompson_states_arcs()
            right_states, right_arcs = self.right._count_thompson_states_arcs()
            return left_states + right_states + 2, left_arcs + right_arcs + 4
        if self.kind == "concat":
            if self.left is None or self.right is None:
                raise ValueError("Concat node must have two children.")
            left_states, left_arcs = self.left._count_thompson_states_arcs()
            right_states, right_arcs = self.right._count_thompson_states_arcs()
            return left_states + right_states, left_arcs + right_arcs + 1
        if self.kind == "star":
            if self.left is None:
                raise ValueError("Star node must have a left child.")
            child_states, child_arcs = self.left._count_thompson_states_arcs()
            return child_states + 2, child_arcs + 4
        raise ValueError(f"Unsupported node kind: {self.kind}")
