"""Tris quadratiques pour classer les avions selon une policy."""

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable

Aircraft = dict[str, Any]
Policy = Callable[[Aircraft, Aircraft], bool]


@dataclass
class SortStats:
    """Metriques de tri pour comparaison empirique."""

    algorithm: str
    comparisons: int
    writes: int
    elapsed_seconds: float


def selection_sort(fleet: list[Aircraft], policy: Policy) -> tuple[list[Aircraft], SortStats]:
    """Tri par selection (O(n^2), non stable en general)."""
    arr = [a.copy() for a in fleet]
    n = len(arr)
    comparisons = 0
    writes = 0

    start = perf_counter()
    for i in range(n):
        best = i
        for j in range(i + 1, n):
            comparisons += 1
            if policy(arr[j], arr[best]):
                best = j

        if best != i:
            arr[i], arr[best] = arr[best], arr[i]
            writes += 2
    elapsed = perf_counter() - start

    return arr, SortStats("selection", comparisons, writes, elapsed)


def insertion_sort(fleet: list[Aircraft], policy: Policy) -> tuple[list[Aircraft], SortStats]:
    """Tri par insertion (O(n^2), stable si le comparateur est strict)."""
    arr = [a.copy() for a in fleet]
    comparisons = 0
    writes = 0

    start = perf_counter()
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if policy(key_item, arr[j]):
                arr[j + 1] = arr[j]
                writes += 1
                j -= 1
            else:
                break

        arr[j + 1] = key_item
        writes += 1
    elapsed = perf_counter() - start

    return arr, SortStats("insertion", comparisons, writes, elapsed)


def get_sort_algorithm(name: str):
    """Renvoie la fonction de tri choisie par son nom."""
    mapping = {
        "selection": selection_sort,
        "insertion": insertion_sort,
    }
    try:
        return mapping[name]
    except KeyError as exc:
        accepted = ", ".join(mapping.keys())
        raise ValueError(f"tri inconnu: {name}. Choix: {accepted}") from exc
