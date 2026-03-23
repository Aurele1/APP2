"""Fonctions utilitaires: validation, affichage, extraction."""

from copy import deepcopy
from typing import Any, Iterable

REQUIRED_FIELDS: dict[str, type] = {
    "id": str,
    "fuel": (int, float),
    "medical": bool,
    "technical_issue": bool,
    "diplomatic_level": int,
    "arrival_time": (int, float),
}


def clone_fleet(fleet: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Retourne une copie profonde de la flotte."""
    return deepcopy(list(fleet))


def validate_aircraft(aircraft: dict[str, Any]) -> list[str]:
    """Verifie un avion et renvoie une liste d'erreurs (vide si OK)."""
    errors: list[str] = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in aircraft:
            errors.append(f"champ manquant: {field}")
            continue
        if not isinstance(aircraft[field], expected_type):
            errors.append(f"type invalide pour {field}: {type(aircraft[field]).__name__}")

    if "fuel" in aircraft and isinstance(aircraft["fuel"], (int, float)) and aircraft["fuel"] < 0:
        errors.append("fuel doit etre >= 0")
    if "diplomatic_level" in aircraft and isinstance(aircraft["diplomatic_level"], int):
        if not (1 <= aircraft["diplomatic_level"] <= 5):
            errors.append("diplomatic_level doit etre entre 1 et 5")

    return errors


def validate_fleet(fleet: Iterable[dict[str, Any]]) -> tuple[bool, list[str]]:
    """Verifie une flotte complete et renvoie (ok, liste_erreurs)."""
    all_errors: list[str] = []
    ids_seen: set[str] = set()

    for index, aircraft in enumerate(fleet):
        aircraft_errors = validate_aircraft(aircraft)
        for err in aircraft_errors:
            all_errors.append(f"avion #{index}: {err}")

        aircraft_id = aircraft.get("id")
        if isinstance(aircraft_id, str):
            if aircraft_id in ids_seen:
                all_errors.append(f"avion #{index}: id duplique ({aircraft_id})")
            ids_seen.add(aircraft_id)

    return (len(all_errors) == 0, all_errors)


def find_min_by_key(fleet: Iterable[dict[str, Any]], key: str) -> dict[str, Any] | None:
    """Renvoie l'avion avec la plus petite valeur pour la cle donnee."""
    minimum: dict[str, Any] | None = None
    for aircraft in fleet:
        if minimum is None or aircraft[key] < minimum[key]:
            minimum = aircraft
    return minimum


def extract_subset(
    fleet: Iterable[dict[str, Any]],
    *,
    medical: bool | None = None,
    technical_issue: bool | None = None,
    max_fuel: int | float | None = None,
) -> list[dict[str, Any]]:
    """Extrait un sous-ensemble d'avions selon des filtres simples."""
    subset: list[dict[str, Any]] = []
    for aircraft in fleet:
        if medical is not None and aircraft["medical"] != medical:
            continue
        if technical_issue is not None and aircraft["technical_issue"] != technical_issue:
            continue
        if max_fuel is not None and aircraft["fuel"] > max_fuel:
            continue
        subset.append(aircraft)
    return subset


def format_aircraft_line(aircraft: dict[str, Any]) -> str:
    """Formate un avion sur une ligne lisible en console."""
    return (
        f"{aircraft['id']:>6} | fuel={aircraft['fuel']:>4} | "
        f"med={str(aircraft['medical']):<5} | tech={str(aircraft['technical_issue']):<5} | "
        f"diplo={aircraft['diplomatic_level']} | eta={aircraft['arrival_time']:.2f}"
    )


def print_fleet(fleet: Iterable[dict[str, Any]], title: str = "Flotte") -> None:
    """Affiche une flotte complete avec un titre."""
    fleet_list = list(fleet)
    print(f"\n=== {title} ({len(fleet_list)} avions) ===")
    for aircraft in fleet_list:
        print(format_aircraft_line(aircraft))
