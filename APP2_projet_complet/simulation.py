"""Simulation dynamique des atterrissages."""

from dataclasses import dataclass
from typing import Any, Callable

from tris import SortStats, get_sort_algorithm

Aircraft = dict[str, Any]
Policy = Callable[[Aircraft, Aircraft], bool]
EventHook = Callable[[int, list[Aircraft]], None]


@dataclass
class SimulationResult:
    """Bilan d'une simulation complete."""

    saved: list[Aircraft]
    crashed: list[Aircraft]
    timeline: list[dict[str, Any]]
    total_turns: int
    total_comparisons: int


def simulate(
    fleet: list[Aircraft],
    policy: Policy,
    *,
    sort_name: str = "insertion",
    fuel_burn_per_turn: int = 1,
    event_hook: EventHook | None = None,
) -> SimulationResult:
    """Simule les atterrissages jusqu'a epuisement de la file.

    A chaque tour:
    - on trie les avions restants selon la policy
    - le premier atterrit (sauve)
    - le carburant des autres diminue
    - tout avion avec fuel <= 0 est crashe
    """
    waiting = [a.copy() for a in fleet]
    saved: list[Aircraft] = []
    crashed: list[Aircraft] = []
    timeline: list[dict[str, Any]] = []
    total_comparisons = 0
    turn = 0

    sort_algorithm = get_sort_algorithm(sort_name)

    while waiting:
        turn += 1

        if event_hook is not None:
            event_hook(turn, waiting)

        ordered, stats = sort_algorithm(waiting, policy)
        total_comparisons += stats.comparisons

        landing = ordered[0]
        saved.append(landing)

        survivors: list[Aircraft] = []
        crashed_this_turn: list[str] = []
        for aircraft in ordered[1:]:
            aircraft["fuel"] -= fuel_burn_per_turn
            if aircraft["fuel"] <= 0:
                crashed.append(aircraft)
                crashed_this_turn.append(aircraft["id"])
            else:
                survivors.append(aircraft)

        waiting = survivors
        timeline.append(
            {
                "turn": turn,
                "landed": landing["id"],
                "remaining": len(waiting),
                "crashed_this_turn": crashed_this_turn,
                "sort_stats": stats,
            }
        )

    return SimulationResult(
        saved=saved,
        crashed=crashed,
        timeline=timeline,
        total_turns=turn,
        total_comparisons=total_comparisons,
    )


def build_must_land_event(target_turn: int, target_id: str) -> EventHook:
    """Cree un evenement improvise: un avion devient must_land a un tour donne."""

    def _event(turn: int, waiting: list[Aircraft]) -> None:
        if turn != target_turn:
            return
        for aircraft in waiting:
            aircraft.setdefault("must_land", False)
            if aircraft["id"] == target_id:
                aircraft["must_land"] = True

    return _event
