import random

# Adatta gli eventi dal codice ricostruito "Nuovo Mondo" alla struttura dati del progetto

def conta_membri_vivi(personaggi):
    return sum(1 for p in personaggi if p.get("stats", {}).get("alive", True))

def presenza_ruolo(personaggi, ruolo):
    return any(p.get("info", {}).get("ruolo") == ruolo and p.get("stats", {}).get("alive", True) for p in personaggi)

def trova_cibo_per_nome(cibo_scelto, nome):
    for c in cibo_scelto:
        if c["info"]["name"] == nome:
            return c
    return None

def trova_equip_per_tipo(equip_scelto, tipo):
    for e in equip_scelto:
        if e["stats"].get("tipo") == tipo:
            return e
    return None

def evento_uomo_in_mare(personaggi_selezionati):
    vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
    if vivi:
        vittima = random.choice(vivi)
        vittima["stats"]["alive"] = False
    return personaggi_selezionati

def evento_scorte_in_mare(cibo_scelto, nome_cibo):
    cibo = trova_cibo_per_nome(cibo_scelto, nome_cibo)
    if cibo:
        c = random.choice([0.5, 0.33, 0.25, 0.20])
        cibo["stats"]["saturazione"] = max(0, cibo["stats"]["saturazione"] * (1 - c))
    return cibo_scelto

def evento_pesca_miracolosa(cibo_scelto):
    carne = trova_cibo_per_nome(cibo_scelto, "carne")
    if carne:
        carne["stats"]["saturazione"] += random.randint(11, 20)
    return cibo_scelto

def evento_tempesta_miracolosa(cibo_scelto):
    acqua = trova_cibo_per_nome(cibo_scelto, "acqua")
    if acqua:
        acqua["stats"]["saturazione"] += random.randint(11, 20)
    return cibo_scelto

def evento_venti_favorevoli(settimane_rimaste, personaggi_selezionati):
    bonus_morale = random.randint(5, 15)
    settimane_rimaste = max(0, settimane_rimaste - 1)
    for p in personaggi_selezionati:
        if p.get("stats", {}).get("alive", True):
            morale_attuale = p.get("morale", 100)
            p["morale"] = min(100, morale_attuale + bonus_morale)
    return settimane_rimaste, personaggi_selezionati

def evento_cattivo_tempo(equip_scelto):
    medicinale = trova_equip_per_tipo(equip_scelto, "medicinale")
    if medicinale:
        c = random.choice([0.5, 0.33, 0.25, 0.20])
        medicinale["stats"]["heal"] = max(0, medicinale["stats"]["heal"] * (1 - c))
    return equip_scelto

def evento_ondata(equip_scelto):
    cannone = trova_equip_per_tipo(equip_scelto, "arma")
    if cannone:
        c = random.choice([0.5, 0.33, 0.25, 0.20])
        cannone["stats"]["danno_nave"] = max(0, cannone["stats"]["danno_nave"] * (1 - c))
    return equip_scelto

def evento_avvistamento_albatro(personaggi_selezionati, equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso):
    if albatro_avvistato >= 3:
        return equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso
    
    albatro_avvistato += 1
    cannone = trova_equip_per_tipo(equip_scelto, "arma")
    if not cannone or cannone["stats"]["danno_nave"] <= 0:
        return equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso
    
    # Logica adattata dalla ricostruzione
    numero_armi = cannone["stats"]["danno_nave"]
    numero_uomini = conta_membri_vivi(personaggi_selezionati)
    tentativi = min(numero_armi, numero_uomini)
    
    # 15% di successo per colpo (dalla ricostruzione)
    albatro_abbattuto = random.random() < (tentativi * 0.15)
    
    if albatro_abbattuto:
        carne = trova_cibo_per_nome(cibo_scelto, "carne")
        if carne:
            carne["stats"]["saturazione"] += random.randint(3, 8)
        albatro_ucciso = True
        # Rimuovi armi usate
        cannone["stats"]["danno_nave"] = max(0, numero_armi - tentativi)
    else:
        albatro_ucciso = False
    
    return equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso

def evento_scialuppa(personaggi_selezionati, equip_scelto, cibo_scelto):
    RUOLI = ["capitano", "cuoco", "navigatore", "medico", "marinaio", "meccanico", "bardo", "tesoriere"]
    
    for _ in range(4):
        nuovo_membro = {
            "stats": {"cost": 20, "hp": 3, "alive": True},
            "pos": {"main": {"x_attuale": random.randint(400, 800), "y_attuale": random.randint(430, 470)}},
            "info": {"name": "Naufrago", "ruolo": random.choice(RUOLI)},
            "morale": random.randint(25, 75)
        }
        personaggi_selezionati.append(nuovo_membro)
    
    # Aggiungi risorse
    guadagno = random.randint(10, 20)
    
    for nome in ["verdura", "frutta", "carne", "acqua"]:
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if cibo:
            cibo["stats"]["saturazione"] += guadagno
    
    return personaggi_selezionati, equip_scelto, cibo_scelto

def evento_epidemia(personaggi_selezionati, equip_scelto):
    medici = [p for p in personaggi_selezionati if p.get("info", {}).get("ruolo") == "medico" and p.get("stats", {}).get("alive", True)]
    non_medici = [p for p in personaggi_selezionati if p.get("info", {}).get("ruolo") != "medico" and p.get("stats", {}).get("alive", True)]
    
    membri_malati = random.randint(1, max(1, len(non_medici) // 2))
    membri_curati = 0
    membri_morti = 0
    
    medicinale = trova_equip_per_tipo(equip_scelto, "medicinale")
    bottiglie_disponibili = medicinale["stats"]["heal"] if medicinale else 0
    
    if medici and bottiglie_disponibili >= membri_malati:
        membri_curati = membri_malati
        if medicinale:
            medicinale["stats"]["heal"] -= membri_malati
    else:
        membri_morti = random.randint(1, membri_malati)
        vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True) and p.get("info", {}).get("ruolo") != "medico"]
        random.shuffle(vivi)
        for i in range(min(membri_morti, len(vivi))):
            vivi[i]["stats"]["alive"] = False
    
    return personaggi_selezionati, equip_scelto

def evento_attacco_pirata(personaggi_selezionati, equip_scelto):
    numero_pirati = random.randint(5, 15)
    cannone = trova_equip_per_tipo(equip_scelto, "arma")
    numero_armi = cannone["stats"]["danno_nave"] if cannone else 0
    numero_membri = conta_membri_vivi(personaggi_selezionati)
    
    numero_difensori = min(numero_armi + numero_membri, numero_membri)
    
    if numero_difensori > numero_pirati:
        # Vittoria senza perdite
        pass
    else:
        perdite = random.randint(1, max(1, numero_membri // 3))
        vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
        random.shuffle(vivi)
        for i in range(min(perdite, len(vivi))):
            vivi[i]["stats"]["alive"] = False
    
    # Rimuovi armi usate
    if cannone and numero_armi > 0:
        cannone["stats"]["danno_nave"] = max(0, numero_armi - min(numero_armi, numero_membri))
    
    return personaggi_selezionati, equip_scelto

def evento_danni_timone(settimane_rimaste, personaggi_selezionati):
    ha_meccanico = presenza_ruolo(personaggi_selezionati, "meccanico")
    if ha_meccanico:
        ritardo = 1
    else:
        ritardo = random.randint(2, 4)
    return settimane_rimaste + ritardo

def evento_raffiche_vento(settimane_rimaste, personaggi_selezionati):
    ha_navigatore = presenza_ruolo(personaggi_selezionati, "navigatore")
    if ha_navigatore:
        ritardo = 1
    else:
        ritardo = random.randint(2, 3)
    return settimane_rimaste + ritardo

def evento_avvistamento_isola(personaggi_selezionati, equip_scelto, cibo_scelto, settimane_rimaste, albatro_avvistato, albatro_ucciso):
    settimane_rimaste += random.randint(1, 2)
    
    isola_abitata = random.random() < 0.6
    if not isola_abitata:
        return personaggi_selezionati, equip_scelto, cibo_scelto, settimane_rimaste
    
    isolani_ostili = random.random() < 0.3
    if isolani_ostili:
        return personaggi_selezionati, equip_scelto, cibo_scelto, settimane_rimaste
    

    if albatro_avvistato > 0 and not albatro_ucciso:
        guadagno = random.randint(20, 40)
    else:
        guadagno = random.randint(3, 15)
    
    for nome in ["verdura", "frutta", "carne", "acqua"]:
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if cibo:
            cibo["stats"]["saturazione"] += guadagno
    
    return personaggi_selezionati, equip_scelto, cibo_scelto, settimane_rimaste

def calcola_paga_totale(personaggi_selezionati, settimane_totali):
    return sum(p.get("stats", {}).get("cost", 0) for p in personaggi_selezionati) * settimane_totali

def controllo_scorte_settimanali(cibo_scelto, personaggi_selezionati, settimane_rimaste):
    num_membri = conta_membri_vivi(personaggi_selezionati)
    delta_morale = 0
    
    consumi_base = {
        "verdura": 0.5,
        "frutta": 1.0,
        "carne": 1.0,
        "acqua": 3.0
    }
    
    for nome, consumo_base in consumi_base.items():
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if not cibo:
            continue
        
        quantita = cibo["stats"]["saturazione"]
        consumo_settimanale = num_membri * consumo_base
        consumo_totale = consumo_settimanale * settimane_rimaste
        
        if quantita <= 0:
            delta_morale -= 5  # MALUS_MORALE_SCORTE_ESAURITE
        elif quantita < consumo_totale:
            # Offerta dimezzare razioni
            delta_morale -= 3  # MALUS_MORALE_DIMEZZA_RAZIONI
    
    return delta_morale

def verifica_ammutinamento(personaggi_selezionati, albatro_ucciso, settimane_passate):
    membri_basso_morale = sum(1 for p in personaggi_selezionati 
                             if p.get("stats", {}).get("alive", True) and p.get("morale", 100) < 50)
    
    if membri_basso_morale > conta_membri_vivi(personaggi_selezionati) / 2:
        return True
    return False
