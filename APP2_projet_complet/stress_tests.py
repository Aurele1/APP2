"""Generation de scenarios et comparaison des tris."""

import random
from typing import Any

from policies import get_policy
from tris import insertion_sort, selection_sort

Aircraft = dict[str, Any]


def generate_traffic(size: int, scenario: str = "normal", seed: int = 42) -> list[Aircraft]:
    """Genere un trafic synthetique pour les stress tests."""
    rng = random.Random(seed)
    fleet: list[Aircraft] = []

    for i in range(size):
        aircraft = {
            "id": f"GEN{i:03}",
            "fuel": rng.randint(8, 50),
            "medical": rng.random() < 0.10,
            "technical_issue": rng.random() < 0.08,
            "diplomatic_level": rng.randint(1, 5),
            "arrival_time": 19.40 + i * 0.01,
        }

        if scenario == "fuel_crisis":
            aircraft["fuel"] = rng.randint(2, 20)
        elif scenario == "medical_crisis":
            aircraft["medical"] = rng.random() < 0.45
        elif scenario == "diplomatic_summit":
            aircraft["diplomatic_level"] = rng.choice([4, 5])
        elif scenario != "normal":
            raise ValueError(f"scenario inconnu: {scenario}")

        fleet.append(aircraft)

    return fleet


def benchmark_sorts(fleet: list[Aircraft], policy_name: str) -> list[dict[str, Any]]:
    """Mesure insertion vs selection sur une meme flotte."""
    policy = get_policy(policy_name)

    _, ins = insertion_sort(fleet, policy)
    _, sel = selection_sort(fleet, policy)

    return [
        {
            "algorithm": ins.algorithm,
            "comparisons": ins.comparisons,
            "writes": ins.writes,
            "elapsed_seconds": ins.elapsed_seconds,
        },
        {
            "algorithm": sel.algorithm,
            "comparisons": sel.comparisons,
            "writes": sel.writes,
            "elapsed_seconds": sel.elapsed_seconds,
        },
    ]


def run_stress_campaign(
    volumes: list[int],
    scenarios: list[str],
    policy_name: str,
    seed: int = 42,
) -> list[dict[str, Any]]:
    """Lance une campagne complete de benchmarks."""
    rows: list[dict[str, Any]] = []

    for scenario in scenarios:
        for n in volumes:
            fleet = generate_traffic(n, scenario=scenario, seed=seed + n)
            metrics = benchmark_sorts(fleet, policy_name)
            for metric in metrics:
                rows.append(
                    {
                        "scenario": scenario,
                        "volume": n,
                        **metric,
                    }
                )

    return rows
