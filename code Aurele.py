def score (copie):
    for "médical" in copie: 
        a=copie["medical"]
    for "technical_issue" in copie:
        b=copie["technical_issue"]
    for "diplomatic_level" in copie:
        c=copie["diplomatic_level"]
    for "fuel" in copie:
        d=copie["fuel"]
    for "scoring" in copie:
        "scoring" = a+b+c+d
    return "scoring"


    


def defragmentation_du_fuel(liste_avions, fuel_perdue):
    for avion in liste_avions:
        avion["fuel"] -= fuel_perdue

    return liste_avions


        

