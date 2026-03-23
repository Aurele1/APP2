"""Point d'entree du projet APP2.

Lance:
1) Validation du dataset initial
2) Demonstration de tri selon une policy
3) Campagne de stress tests (10, 30, 50, 100)
4) Simulation dynamique avec et sans evenement improvise
"""

from data import load_initial_traffic
from policies import get_policy, list_policies
from simulation import build_must_land_event, simulate
from stress_tests import run_stress_campaign
from tris import insertion_sort, selection_sort
from utils import find_min_by_key, print_fleet, validate_fleet


def print_stress_table(rows: list[dict]) -> None:
    """Affiche une table compacte de resultats de benchmarks."""
    header = (
        f"{'scenario':<18} | {'n':>4} | {'algo':<10} | "
        f"{'comparisons':>12} | {'writes':>8} | {'time_ms':>10}"
    )
    print("\n" + header)
    print("-" * len(header))

    for row in rows:
        print(
            f"{row['scenario']:<18} | {row['volume']:>4} | {row['algorithm']:<10} | "
            f"{row['comparisons']:>12} | {row['writes']:>8} | {row['elapsed_seconds'] * 1000:>10.3f}"
        )


def demo_sort_on_initial(policy_name: str) -> None:
    """Montre l'impact d'une policy sur le jeu initial."""
    fleet = load_initial_traffic()
    policy = get_policy(policy_name)

    ordered_ins, stats_ins = insertion_sort(fleet, policy)
    ordered_sel, stats_sel = selection_sort(fleet, policy)

    print_fleet(ordered_ins[:8], title=f"Top 8 insertion / policy={policy_name}")
    print_fleet(ordered_sel[:8], title=f"Top 8 selection / policy={policy_name}")

    print("\nComparaison rapide sur le dataset initial")
    print(
        f"Insertion: comparisons={stats_ins.comparisons}, "
        f"writes={stats_ins.writes}, time_ms={stats_ins.elapsed_seconds * 1000:.3f}"
    )
    print(
        f"Selection: comparisons={stats_sel.comparisons}, "
        f"writes={stats_sel.writes}, time_ms={stats_sel.elapsed_seconds * 1000:.3f}"
    )


def demo_simulation(policy_name: str) -> None:
    """Lance deux simulations: standard puis evenement improvise."""
    fleet_a = load_initial_traffic()
    fleet_b = load_initial_traffic()
    policy = get_policy(policy_name)

    result_normal = simulate(fleet_a, policy, sort_name="insertion")

    event = build_must_land_event(target_turn=3, target_id="QR555")
    result_event = simulate(fleet_b, policy, sort_name="insertion", event_hook=event)

    print("\nSimulation standard")
    print(
        f"Tours={result_normal.total_turns}, "
        f"sauves={len(result_normal.saved)}, crashes={len(result_normal.crashed)}, "
        f"comparisons_total={result_normal.total_comparisons}"
    )

    print("\nSimulation avec evenement improvise (must_land au tour 3)")
    print(
        f"Tours={result_event.total_turns}, "
        f"sauves={len(result_event.saved)}, crashes={len(result_event.crashed)}, "
        f"comparisons_total={result_event.total_comparisons}"
    )


def main() -> None:
    """Execute une demonstration complete conforme aux exigences APP2."""
    fleet = load_initial_traffic()

    ok, errors = validate_fleet(fleet)
    if not ok:
        print("Donnees invalides:")
        for err in errors:
            print(f"- {err}")
        return

    min_fuel = find_min_by_key(fleet, "fuel")
    print("Policies disponibles:", ", ".join(list_policies()))
    print(f"Avion avec fuel minimum: {min_fuel['id']} (fuel={min_fuel['fuel']})")

    chosen_policy = "balanced"
    demo_sort_on_initial(chosen_policy)

    volumes = [10, 30, 50, 100]
    scenarios = ["normal", "fuel_crisis", "medical_crisis", "diplomatic_summit"]
    rows = run_stress_campaign(volumes, scenarios, policy_name=chosen_policy)
    print_stress_table(rows)

    demo_simulation(chosen_policy)


if __name__ == "__main__":
    main()
