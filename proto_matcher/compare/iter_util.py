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

    xs = sorted(xs, key=key, reverse=True)
    ys = sorted(ys, key=key, reverse=True)

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
