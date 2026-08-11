from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Callable, TypeVar

T = TypeVar("T")

KeyFn = Callable[[T], Any]


def zip_pairs(
    xs: Iterable[T], ys: Iterable[T], key: KeyFn | None = None
) -> Iterator[tuple[T | None, T | None]]:
    if not key:
        key = lambda x: 0

    # Reverse the *stable* sort (not sorted(reverse=True), which keeps ties in
    # input order): the default key ties every element and the loop below pops
    # from the tail, so ties must come out in input order to keep
    # repeated-field diffs index-aligned.
    xs = sorted(xs, key=key)[::-1]
    ys = sorted(ys, key=key)[::-1]

    while xs or ys:
        if not xs:
            yield None, ys.pop()
            continue
        if not ys:
            yield xs.pop(), None
            continue

        x_key = key(xs[-1])
        y_key = key(ys[-1])
        yield (
            xs.pop() if x_key <= y_key else None,
            ys.pop() if y_key <= x_key else None,
        )
