import random

albatro_avvistato = 0
albatro_ucciso    = False


def uomoInMare(personaggi_selezionati: list) -> list:
    p = random.choice(personaggi_selezionati)
    personaggi_selezionati.remove(p)
    return personaggi_selezionati


def verduraInMare(verdura: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return verdura - (verdura * c)


def fruttaInMare(frutta: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return frutta - (frutta * c)


def carneInMare(carne: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return carne - (carne * c)


def acquaInMare(acqua: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return acqua - (acqua * c)


def pescaMiracolosa(carne: float) -> float:
    return carne + random.randint(11, 20)


def tempestaMiracolosa(acqua: float) -> float:
    return acqua + random.randint(11, 20)


def ventiFavorevoli(settimane_rimaste: int, morale_equipaggio: int) -> tuple:
    bonus_morale = random.randint(5, 15)
    settimane_rimaste = max(0, settimane_rimaste - 1)
    morale_equipaggio += bonus_morale
    return settimane_rimaste, morale_equipaggio


def cattivoTempo(medicinali: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return medicinali - (medicinali * c)


def ondata(armi: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return armi - (armi * c)


def infestazioneRatti(stoffe: float) -> float:
    c = random.choice([0.5, 0.33, 0.25, 0.20])
    return stoffe - (stoffe * c)

'''
def avvistamentoAlbatro(personaggi: list, armi: float, carne: float) -> tuple:
    global albatro_avvistato, albatro_ucciso

    if albatro_avvistato >= 3:
        return armi, carne

    albatro_avvistato += 1

    if armi <= 0:
        return armi, carne

    scelta = input("Vuoi tentare di abbattere l'albatro? (s/n): ").strip().lower()
    if scelta != "n":
        return armi, carne

    tentativi = int(min(armi, len(personaggi)))
    armi -= tentativi
    abbattuto = any(random.random() < 0.5 for _ in range(tentativi))

    if abbattuto:
        carne += random.randint(10, 15)
        albatro_ucciso = True

    return armi, carne
'''

def avvistamentoScialuppa(personaggi: list, armi: float, stoffe: float) -> tuple:
    RUOLI = ["cuoco", "navigatore", "medico", "meccanico", "marinaio"]

    scelta = input("Vuoi salvare i 4 naufraghi? (s/n): ").strip().lower()
    if scelta != "s":
        return personaggi, armi, stoffe

    for _ in range(4):
        nuovo_membro = {
            "ruolo": random.choice(RUOLI),
            "morale": random.randint(25, 75),
            "pagato": False
        }
        personaggi.append(nuovo_membro)

    guadagno = random.randint(10, 20)
    armi   += guadagno
    stoffe += guadagno

    return personaggi, armi, stoffe


def epidemia(personaggi: list, medicinali: float) -> tuple:
    medici = [p for p in personaggi if p.get("ruolo") == "medico"]
    non_medici = [p for p in personaggi if p.get("ruolo") != "medico"]

    malati = [p for p in non_medici if random.random() < 0.7]
    curati = []
    morti  = []

    for malato in malati:
        if medici and medicinali >= 1:
            medicinali -= 1
            curati.append(malato)
        else:
            morti.append(malato)
            personaggi.remove(malato)

    return personaggi, medicinali


def attaccoPirata(personaggi: list, armi: float) -> tuple:
    num_pirati   = random.randint(3, 10)
    num_difensori = int(min(armi, len(personaggi)))
    armi -= num_difensori

    uomini_persi = min(num_pirati - num_difensori, len(personaggi))

    if uomini_persi > 0:
        for _ in range(uomini_persi):
            if personaggi:
                personaggi.remove(random.choice(personaggi))

    return personaggi, armi


def danniAlTimone(settimane_rimaste: int, personaggi: list) -> int:
    ha_meccanico = any(p.get("ruolo") == "meccanico" for p in personaggi)
    ritardo = 1 if ha_meccanico else random.randint(2, 4)
    return settimane_rimaste + ritardo


def rafficheDiVento(settimane_rimaste: int, personaggi: list) -> int:
    ha_navigatore = any(p.get("ruolo") == "navigatore" for p in personaggi)
    ritardo = 1 if ha_navigatore else random.randint(2, 4)
    return settimane_rimaste + ritardo


def avvistamentoIsola(personaggi: list, armi: float, stoffe: float, settimane_rimaste: int) -> tuple:
    global albatro_avvistato, albatro_ucciso

    scelta = input("Vuoi approdare sull'isola? (s/n): ").strip().lower()
    if scelta != "s":
        return personaggi, armi, stoffe, settimane_rimaste

    settimane_rimaste += random.randint(1, 2)
    abitata = random.random() < 0.5

    if not abitata:
        return personaggi, armi, stoffe, settimane_rimaste

    ostili = random.random() < 0.5
    if ostili:
        return personaggi, armi, stoffe, settimane_rimaste

    if albatro_avvistato > 0 and not albatro_ucciso:
        guadagno = random.randint(20, 40)
    else:
        guadagno = random.randint(5, 20)

    armi   += guadagno
    stoffe += guadagno

    return personaggi, armi, stoffe, settimane_rimaste


def nessunoImprevisto():
    pass