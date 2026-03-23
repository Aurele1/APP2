APP2 - Projet complet (Algorithmique avancee 1)

Objectif
- Classer des avions en approche selon des policies de priorisation.
- Comparer deux tris quadratiques (insertion et selection).
- Simuler l'ecoulement du temps (atterrissage, baisse de carburant, crash).
- Realiser des stress tests sur plusieurs scenarios et tailles de trafic.

Structure
- data.py: dataset initial et chargement.
- utils.py: validation, affichage, recherche minimum, extraction sous-ensemble.
- policies.py: policies de priorisation (fuel, incident, diplomatic, balanced).
- tris.py: tri insertion + tri selection avec metriques.
- simulation.py: simulation dynamique et evenement improvise.
- stress_tests.py: generateur de trafic et campagne de benchmarks.
- main.py: script de demonstration complete.
- docs/: documents pedagogiques (fonctions et flux E/S).

Execution
1) Ouvrir un terminal dans ce dossier.
2) Executer:
   python main.py

Resultats attendus
- Validation du dataset.
- Demonstration des classements.
- Tableau de comparaison des tris sur 4 scenarios x 4 volumes.
- Bilan de simulation (avions sauves et crashes).
