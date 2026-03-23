"""Policies de priorisation des avions.

Une policy est une fonction policy(a1, a2) -> bool qui renvoie True
si a1 doit passer avant a2.
"""

from typing import Any, Callable

Aircraft = dict[str, Any]
Policy = Callable[[Aircraft, Aircraft], bool]


def _compare_keys(a1: Aircraft, a2: Aircraft, keys: list[tuple[str, bool]]) -> bool:
    """Compare deux avions par liste de cles ordonnees.

    keys: liste de tuples (nom_cle, ordre_croissant)
    - ordre_croissant=True: plus petit en premier
    - ordre_croissant=False: plus grand en premier
    """
    for key, ascending in keys:
        v1 = a1.get(key)
        v2 = a2.get(key)
        if v1 == v2:
            continue
        if ascending:
            return v1 < v2
        return v1 > v2

    # Tie-break final pour ordre total deterministe
    return a1["id"] < a2["id"]


def policy_fuel_first(a1: Aircraft, a2: Aircraft) -> bool:
    """Policy orientee carburant: moins de fuel passe d'abord.

    Hierarchie:
    1) must_land (si present)
    2) fuel croissant
    3) technical_issue True d'abord
    4) medical True d'abord
    5) diplomatic_level decroissant
    6) arrival_time croissant
    """
    return _compare_keys(
        a1,
        a2,
        [
            ("must_land", False),
            ("fuel", True),
            ("technical_issue", False),
            ("medical", False),
            ("diplomatic_level", False),
            ("arrival_time", True),
        ],
    )


def policy_incident_first(a1: Aircraft, a2: Aircraft) -> bool:
    """Policy orientee securite: incidents et urgences avant tout."""
    return _compare_keys(
        a1,
        a2,
        [
            ("must_land", False),
            ("technical_issue", False),
            ("medical", False),
            ("fuel", True),
            ("diplomatic_level", False),
            ("arrival_time", True),
        ],
    )


def policy_diplomatic_first(a1: Aircraft, a2: Aircraft) -> bool:
    """Policy orientee diplomatie: importance politique privilegiee."""
    return _compare_keys(
        a1,
        a2,
        [
            ("must_land", False),
            ("diplomatic_level", False),
            ("technical_issue", False),
            ("medical", False),
            ("fuel", True),
            ("arrival_time", True),
        ],
    )


def policy_balanced(a1: Aircraft, a2: Aircraft) -> bool:
    """Policy de crise equilibree proposee dans l'enonce."""
    return _compare_keys(
        a1,
        a2,
        [
            ("must_land", False),
            ("technical_issue", False),
            ("medical", False),
            ("fuel", True),
            ("diplomatic_level", False),
            ("arrival_time", True),
        ],
    )


def get_policy(policy_name: str) -> Policy:
    """Renvoie la policy correspondant au nom demande."""
    mapping: dict[str, Policy] = {
        "fuel": policy_fuel_first,
        "incident": policy_incident_first,
        "diplomatic": policy_diplomatic_first,
        "balanced": policy_balanced,
    }
    try:
        return mapping[policy_name]
    except KeyError as exc:
        accepted = ", ".join(mapping.keys())
        raise ValueError(f"policy inconnue: {policy_name}. Choix: {accepted}") from exc


def list_policies() -> list[str]:
    """Liste les policies disponibles."""
    return ["fuel", "incident", "diplomatic", "balanced"]
