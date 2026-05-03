import random

SOGLIA_EPIDEMIA          = 0.7
MALUS_MORALE_SCORTE_ESAURITE  = 20
MALUS_MORALE_DIMEZZA_RAZIONI  = 10
BONUS_MORALE_RADDOPPIA_RAZIONI = 10
MARINAI_MAX              = 12
SOGLIA_MORALE_BASSO      = 25

EVENTO_UOMO_MARE          = "UOMO IN MARE"
EVENTO_VERDURA_MARE       = "VERDURA IN MARE"
EVENTO_FRUTTA_MARE        = "FRUTTA IN MARE"
EVENTO_CARNE_MARE         = "CARNE IN MARE"
EVENTO_ACQUA_MARE         = "ACQUA IN MARE"
EVENTO_PESCA_MIRACOLOSA   = "PESCA MIRACOLOSA"
EVENTO_TEMPESTA_MIRACOLOSA= "TEMPESTA MIRACOLOSA"
EVENTO_VENTI_FAVOREVOLI   = "VENTI FAVOREVOLI"
EVENTO_CATTIVO_TEMPO      = "CATTIVO TEMPO"
EVENTO_ONDATA             = "ONDATA"
EVENTO_INFESTAZIONE_RATTI = "INFESTAZIONE RATTI"
EVENTO_AVVISTAMENTO_ALBATRO = "AVVISTAMENTO ALBATRO"
EVENTO_SCIALUPPA          = "AVVISTAMENTO SCIALUPPA"
EVENTO_EPIDEMIA           = "EPIDEMIA"
EVENTO_ATTACCO_PIRATA     = "ATTACCO PIRATA"
EVENTO_DANNI_TIMONE       = "DANNI AL TIMONE"
EVENTO_RAFFICHE_VENTO     = "RAFFICHE DI VENTO"
EVENTO_AVVISTAMENTO_ISOLA = "AVVISTAMENTO ISOLA"



def conta_membri_vivi(personaggi):
    return sum(1 for p in personaggi if p.get("stats", {}).get("alive", True))

def presenza_ruolo(personaggi, ruolo):
    return any(
        p.get("info", {}).get("ruolo") == ruolo and p.get("stats", {}).get("alive", True)
        for p in personaggi
    )

def trova_cibo_per_nome(cibo_lista, nome):
    for c in cibo_lista:
        if c.get("info", {}).get("name") == nome:
            return c
    return None

def trova_equip_per_tipo(equip_lista, tipo):
    for e in equip_lista:
        if e.get("stats", {}).get("tipo") == tipo:
            return e
    return None

def get_saturazione(cibo):
    return cibo["stats"]["saturazione"]

def set_saturazione(cibo, valore):
    cibo["stats"]["saturazione"] = max(0.0, valore)

def get_quantita_equip(equip, campo="danno_nave"):
    return equip["stats"].get(campo, 0)

def set_quantita_equip(equip, valore, campo="danno_nave"):
    equip["stats"][campo] = max(0, valore)

def get_heal(equip):
    return equip["stats"].get("heal", 0)

def set_heal(equip, valore):
    equip["stats"]["heal"] = max(0, valore)


def evento_uomo_in_mare(personaggi_selezionati):
    vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
    if not vivi:
        return personaggi_selezionati, None
    vittima = random.choice(vivi)
    vittima["stats"]["alive"] = False
    return personaggi_selezionati, vittima.get("info", {}).get("name", "Membro sconosciuto")

def _perdita_scorta(cibo_scelto, nome_cibo):

    cibo = trova_cibo_per_nome(cibo_scelto, nome_cibo)
    if cibo is None:
        return cibo_scelto, None
    quota = random.choice([2, 3, 4, 5])
    perdita = get_saturazione(cibo) * (1 / quota)
    set_saturazione(cibo, get_saturazione(cibo) - perdita)
    return cibo_scelto, f"1/{quota}"

def evento_verdura_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "verdura")

def evento_frutta_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "frutta")

def evento_carne_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "carne")

def evento_acqua_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "acqua")


def evento_pesca_miracolosa(cibo_scelto):
    quantita = random.randint(11, 20)
    carne = trova_cibo_per_nome(cibo_scelto, "carne")
    if carne is None:
        # fallback: cerca "pesce" (scorta alternativa presente in struttura_dati.py)
        carne = trova_cibo_per_nome(cibo_scelto, "pesce")
    if carne:
        set_saturazione(carne, get_saturazione(carne) + quantita)
    return cibo_scelto, quantita

def evento_tempesta_miracolosa(cibo_scelto):
    quantita = random.randint(11, 20)
    acqua = trova_cibo_per_nome(cibo_scelto, "acqua")
    if acqua:
        set_saturazione(acqua, get_saturazione(acqua) + quantita)
    return cibo_scelto, quantita


def evento_venti_favorevoli(settimane_supplementari, personaggi_selezionati):
    bonus_morale = random.randint(5, 15)
    settimane_supplementari = max(0, settimane_supplementari - 1)
    for p in personaggi_selezionati:
        if p.get("stats", {}).get("alive", True):
            morale_attuale = p.get("morale", 100)
            p["morale"] = min(100, morale_attuale + bonus_morale)
    return settimane_supplementari, personaggi_selezionati, bonus_morale

def evento_cattivo_tempo(equip_scelto):
    medicinale = trova_equip_per_tipo(equip_scelto, "medicinale")
    if medicinale is None:
        return equip_scelto, None
    quota = random.choice([2, 3, 4, 5])
    perdita = int(get_heal(medicinale) * (1 / quota))
    set_heal(medicinale, get_heal(medicinale) - perdita)
    return equip_scelto, f"1/{quota}"

def evento_ondata(equip_scelto):
    arma = trova_equip_per_tipo(equip_scelto, "arma")
    if arma is None:
        return equip_scelto, None
    quota = random.choice([2, 3, 4, 5])
    perdita = int(get_quantita_equip(arma) * (1 / quota))
    set_quantita_equip(arma, get_quantita_equip(arma) - perdita)
    return equip_scelto, f"1/{quota}"

def evento_infestazione_ratti(equip_scelto):
    stoffa = trova_equip_per_tipo(equip_scelto, "strumento")  # "stoffa" è di tipo "strumento"
    for e in equip_scelto:
        if e.get("info", {}).get("name") == "stoffa":
            stoffa = e
            break
    if stoffa is None:
        return equip_scelto, None
    quota = random.choice([2, 3, 4, 5])
    campo = "heal" if "heal" in stoffa["stats"] else "cost"
    valore_attuale = stoffa["stats"].get(campo, 0)
    perdita = int(valore_attuale * (1 / quota))
    stoffa["stats"][campo] = max(0, valore_attuale - perdita)
    return equip_scelto, f"1/{quota}"


def evento_avvistamento_albatro(
    personaggi_selezionati, equip_scelto, cibo_scelto,
    albatro_avvistato, albatro_ucciso
):
    if albatro_avvistato >= 3:
        return equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso, False, "Evento albatro già avvenuto 3 volte."

    albatro_avvistato += 1

    arma = trova_equip_per_tipo(equip_scelto, "arma")
    numero_armi = get_quantita_equip(arma) if arma else 0
    numero_uomini = conta_membri_vivi(personaggi_selezionati)
    numero_colpi = min(numero_armi, numero_uomini)

    if numero_armi == 0 or numero_colpi == 0:
        return equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso, False, "Nessuna arma disponibile."

    abbattuto = False
    for _ in range(numero_colpi):
        if random.randint(1, 10) > 7:
            abbattuto = True
            break

    if abbattuto:
        guadagno_carne = numero_colpi * 5
        carne = trova_cibo_per_nome(cibo_scelto, "carne")
        if carne is None:
            carne = trova_cibo_per_nome(cibo_scelto, "pesce")
        if carne:
            set_saturazione(carne, get_saturazione(carne) + guadagno_carne)
        # Le armi usate vengono rimosse
        set_quantita_equip(arma, get_quantita_equip(arma) - numero_colpi)
        albatro_ucciso = True
        esito = f"Albatro abbattuto! +{guadagno_carne} kg di carne. Armi usate: {numero_colpi}."
    else:
        albatro_ucciso = False
        esito = "Nessun colpo è andato a segno."

    return equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso, True, esito

def evento_scialuppa(personaggi_selezionati, equip_scelto, cibo_scelto):
    RUOLI_POSSIBILI = ["capitano", "cuoco", "navigatore", "medico",
                       "marinaio", "meccanico", "bardo", "tesoriere"]

    nuovi_membri = []
    for _ in range(4):
        ruolo = random.choice(RUOLI_POSSIBILI)
        nuovo = {
            "stats": {"cost": 0, "hp": 3, "alive": True},  # cost=0 → non pagato a fine viaggio
            "pos": {
                "main": {
                    "x_attuale": random.randint(400, 800),
                    "y_attuale": random.randint(430, 470),
                }
            },
            "info": {
                "name": "Naufrago",
                "ruolo": ruolo,
                "descrizione": f"Naufrago salvato - ruolo: {ruolo}",
            },
            "morale": random.randint(25, 75),
        }
        personaggi_selezionati.append(nuovo)
        nuovi_membri.append(nuovo)

    # Contenuto della cassa: +10–20 unità per ogni merce nell'equipaggiamento
    guadagno = random.randint(10, 20)
    for e in equip_scelto:
        tipo = e.get("stats", {}).get("tipo", "")
        if tipo == "medicinale":
            set_heal(e, get_heal(e) + guadagno)
        elif tipo == "arma":
            set_quantita_equip(e, get_quantita_equip(e) + guadagno)
        # altri strumenti: incrementa "cost" come proxy di quantità
        elif tipo == "strumento":
            e["stats"]["cost"] = e["stats"].get("cost", 0) + guadagno

    return personaggi_selezionati, equip_scelto, cibo_scelto, nuovi_membri, guadagno

def evento_epidemia(personaggi_selezionati, equip_scelto):
    medicinale = trova_equip_per_tipo(equip_scelto, "medicinale")
    bottiglie_disponibili = get_heal(medicinale) if medicinale else 0
    ha_medico = presenza_ruolo(personaggi_selezionati, "medico")

    malati = 0
    curati = 0
    morti = 0
    bottiglie_usate = 0

    for p in personaggi_selezionati:
        if not p.get("stats", {}).get("alive", True):
            continue
        if p.get("info", {}).get("ruolo") == "medico":
            continue

        if random.random() < SOGLIA_EPIDEMIA:
            malati += 1
            if ha_medico and bottiglie_disponibili > 0:
                curati += 1
                bottiglie_usate += 1
                bottiglie_disponibili -= 1
            else:
                p["stats"]["alive"] = False
                morti += 1

    if medicinale:
        set_heal(medicinale, get_heal(medicinale) - bottiglie_usate)

    report = {
        "malati": malati,
        "curati": curati,
        "morti": morti,
        "bottiglie_usate": bottiglie_usate,
    }
    return personaggi_selezionati, equip_scelto, report

def evento_attacco_pirata(personaggi_selezionati, equip_scelto):
    numero_pirati = random.randint(5, 15)
    arma = trova_equip_per_tipo(equip_scelto, "arma")
    numero_armi = get_quantita_equip(arma) if arma else 0
    numero_membri = conta_membri_vivi(personaggi_selezionati)

    if numero_armi > 0:
        numero_difensori = numero_armi + numero_membri
    else:
        numero_difensori = 0

    if numero_difensori >= numero_pirati:
        perdite = 0
        vittoria = True
    else:
        perdite = numero_pirati - numero_difensori
        perdite = min(perdite, numero_membri)
        vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
        random.shuffle(vivi)
        for i in range(min(perdite, len(vivi))):
            vivi[i]["stats"]["alive"] = False
        vittoria = perdite < numero_membri

    if arma and numero_armi > 0:
        armi_usate = min(numero_armi, numero_membri)
        set_quantita_equip(arma, numero_armi - armi_usate)

    return personaggi_selezionati, equip_scelto, numero_pirati, perdite, vittoria

def evento_danni_timone(settimane_supplementari, personaggi_selezionati):
    ha_meccanico = presenza_ruolo(personaggi_selezionati, "meccanico")
    ritardo = 1 if ha_meccanico else random.randint(2, 4)
    return settimane_supplementari + ritardo, ritardo, ha_meccanico

def evento_raffiche_vento(settimane_supplementari, personaggi_selezionati):
    ha_navigatore = presenza_ruolo(personaggi_selezionati, "navigatore")
    ritardo = 1 if ha_navigatore else random.randint(2, 4)
    return settimane_supplementari + ritardo, ritardo, ha_navigatore

def evento_avvistamento_isola(
    personaggi_selezionati, equip_scelto, cibo_scelto,
    settimane_supplementari, albatro_avvistato, albatro_ucciso
):
    penalita = random.randint(1, 2)
    settimane_supplementari += penalita

    isola_abitata = random.random() < 0.5  #Forse cambio in 66%
    guadagno = 0

    if not isola_abitata:
        return (personaggi_selezionati, equip_scelto, cibo_scelto,
                settimane_supplementari, False, False, guadagno)

    isolani_ostili = random.random() < 0.5

    if isolani_ostili:
        return (personaggi_selezionati, equip_scelto, cibo_scelto,
                settimane_supplementari, True, True, guadagno)

    if albatro_avvistato > 0 and not albatro_ucciso:
        guadagno = random.randint(20, 40)
    else:
        guadagno = random.randint(5, 20)

    for nome in ["verdura", "frutta", "carne", "acqua"]:
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if cibo:
            set_saturazione(cibo, get_saturazione(cibo) + guadagno)

    return (personaggi_selezionati, equip_scelto, cibo_scelto,
            settimane_supplementari, True, False, guadagno)

def controllo_scorte_settimanali(cibo_scelto, personaggi_selezionati, settimane_rimaste):
    """
    Controlla le scorte alla fine di ogni settimana.
    Per ogni tipo di cibo verifica se le scorte bastano per le settimane rimanenti.

    Consumi settimanali (per membro vivo):
        verdura : 0.5 kg
        frutta  : 1.0 kg
        carne   : 1.0 kg
        acqua   : 3.0 barili

    Restituisce:
        (delta_morale, alert_list)
        dove alert_list è una lista di dict {"nome", "tipo_alert", "quantita", "consumo_necessario"}
        tipo_alert in: "esaurite", "insufficienti", "abbondanti"
    """
    num_membri = conta_membri_vivi(personaggi_selezionati)
    delta_morale = 0
    alert_list = []

    consumi_settimanali = {
        "verdura": 0.5,
        "frutta":  1.0,
        "carne":   1.0,
        "acqua":   3.0,
    }

    for nome, consumo_per_membro in consumi_settimanali.items():
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if cibo is None:
            continue

        quantita = get_saturazione(cibo)
        consumo_settimanale = consumo_per_membro * num_membri
        consumo_necessario = consumo_settimanale * settimane_rimaste

        if quantita <= 0:
            delta_morale -= MALUS_MORALE_SCORTE_ESAURITE
            alert_list.append({
                "nome": nome,
                "tipo_alert": "esaurite",
                "quantita": quantita,
                "consumo_necessario": consumo_necessario,
            })
        elif quantita < consumo_necessario:
            alert_list.append({
                "nome": nome,
                "tipo_alert": "insufficienti",
                "quantita": quantita,
                "consumo_necessario": consumo_necessario,
            })
        elif quantita > consumo_necessario * 2:
            alert_list.append({
                "nome": nome,
                "tipo_alert": "abbondanti",
                "quantita": quantita,
                "consumo_necessario": consumo_necessario,
            })


        set_saturazione(cibo, quantita - consumo_settimanale)

    return delta_morale, alert_list

def applica_dimezzamento_razioni(cibo_scelto, nome_cibo):
    return -MALUS_MORALE_DIMEZZA_RAZIONI

def applica_raddoppio_razioni(cibo_scelto, nome_cibo):
    return BONUS_MORALE_RADDOPPIA_RAZIONI

def aggiorna_morale_equipaggio(personaggi_selezionati, delta_morale):
    for p in personaggi_selezionati:
        if p.get("stats", {}).get("alive", True):
            morale = p.get("morale", 100)
            p["morale"] = max(0, min(100, morale + delta_morale))
    return personaggi_selezionati

def verifica_ammutinamento(
    personaggi_selezionati, albatro_ucciso,
    settimane_supplementari, ha_cuoco, razioni_ridotte
):
    fattore = 0
    motivi = []

    if razioni_ridotte:
        fattore += 1
        motivi.append("Razioni di cibo ridotte")

    if not ha_cuoco:
        fattore += 1
        motivi.append("Manca un cuoco a bordo che valorizzi il cibo")

    if albatro_ucciso:
        fattore += 1
        motivi.append("È stato ucciso un albatro (segno di maledizione)")

    if settimane_supplementari > 0:
        fattore += 1
        motivi.append("Il viaggio si è allungato oltre il previsto")

    if conta_membri_vivi(personaggi_selezionati) > MARINAI_MAX:
        fattore += 1
        motivi.append(f"La nave è troppo affollata (massimo {MARINAI_MAX} uomini)")

    return fattore >= 3, motivi

def calcola_paga_totale(personaggi_selezionati, settimane_totali):
    return sum(
        p.get("stats", {}).get("cost", 0)
        for p in personaggi_selezionati
    ) * settimane_totali

def esegui_evento(
    nome_evento,
    personaggi_selezionati,
    cibo_scelto,
    equip_scelto,
    settimane_supplementari,
    albatro_avvistato,
    albatro_ucciso,
):
    delta_morale = 0
    report = {"evento": nome_evento, "dettagli": {}}

    if nome_evento == EVENTO_UOMO_MARE:
        personaggi_selezionati, vittima = evento_uomo_in_mare(personaggi_selezionati)
        report["dettagli"] = {"vittima": vittima}

    elif nome_evento == EVENTO_VERDURA_MARE:
        cibo_scelto, quota = evento_verdura_in_mare(cibo_scelto)
        report["dettagli"] = {"quota_persa": quota}

    elif nome_evento == EVENTO_FRUTTA_MARE:
        cibo_scelto, quota = evento_frutta_in_mare(cibo_scelto)
        report["dettagli"] = {"quota_persa": quota}

    elif nome_evento == EVENTO_CARNE_MARE:
        cibo_scelto, quota = evento_carne_in_mare(cibo_scelto)
        report["dettagli"] = {"quota_persa": quota}

    elif nome_evento == EVENTO_ACQUA_MARE:
        cibo_scelto, quota = evento_acqua_in_mare(cibo_scelto)
        report["dettagli"] = {"quota_persa": quota}

    elif nome_evento == EVENTO_PESCA_MIRACOLOSA:
        cibo_scelto, quantita = evento_pesca_miracolosa(cibo_scelto)
        report["dettagli"] = {"carne_guadagnata": quantita}

    elif nome_evento == EVENTO_TEMPESTA_MIRACOLOSA:
        cibo_scelto, quantita = evento_tempesta_miracolosa(cibo_scelto)
        report["dettagli"] = {"acqua_guadagnata": quantita}

    elif nome_evento == EVENTO_VENTI_FAVOREVOLI:
        settimane_supplementari, personaggi_selezionati, bonus = evento_venti_favorevoli(
            settimane_supplementari, personaggi_selezionati
        )
        delta_morale += bonus
        report["dettagli"] = {"bonus_morale": bonus, "settimane_risparmiate": 1}

    elif nome_evento == EVENTO_CATTIVO_TEMPO:
        equip_scelto, quota = evento_cattivo_tempo(equip_scelto)
        report["dettagli"] = {"medicinali_persi_quota": quota}

    elif nome_evento == EVENTO_ONDATA:
        equip_scelto, quota = evento_ondata(equip_scelto)
        report["dettagli"] = {"armi_perse_quota": quota}

    elif nome_evento == EVENTO_INFESTAZIONE_RATTI:
        equip_scelto, quota = evento_infestazione_ratti(equip_scelto)
        report["dettagli"] = {"stoffe_perse_quota": quota}

    elif nome_evento == EVENTO_AVVISTAMENTO_ALBATRO:
        equip_scelto, cibo_scelto, albatro_avvistato, albatro_ucciso, ha_tentato, esito = \
            evento_avvistamento_albatro(
                personaggi_selezionati, equip_scelto, cibo_scelto,
                albatro_avvistato, albatro_ucciso
            )
        report["dettagli"] = {"ha_tentato": ha_tentato, "esito": esito,
                               "albatro_avvistato": albatro_avvistato,
                               "albatro_ucciso": albatro_ucciso}

    elif nome_evento == EVENTO_SCIALUPPA:
        personaggi_selezionati, equip_scelto, cibo_scelto, nuovi, guadagno = \
            evento_scialuppa(personaggi_selezionati, equip_scelto, cibo_scelto)
        report["dettagli"] = {"nuovi_membri": len(nuovi), "guadagno_merci": guadagno}

    elif nome_evento == EVENTO_EPIDEMIA:
        personaggi_selezionati, equip_scelto, rep = \
            evento_epidemia(personaggi_selezionati, equip_scelto)
        report["dettagli"] = rep

    elif nome_evento == EVENTO_ATTACCO_PIRATA:
        personaggi_selezionati, equip_scelto, pirati, perdite, vittoria = \
            evento_attacco_pirata(personaggi_selezionati, equip_scelto)
        report["dettagli"] = {"pirati": pirati, "perdite": perdite, "vittoria": vittoria}

    elif nome_evento == EVENTO_DANNI_TIMONE:
        settimane_supplementari, ritardo, ha_meccanico = \
            evento_danni_timone(settimane_supplementari, personaggi_selezionati)
        report["dettagli"] = {"ritardo": ritardo, "ha_meccanico": ha_meccanico}

    elif nome_evento == EVENTO_RAFFICHE_VENTO:
        settimane_supplementari, ritardo, ha_navigatore = \
            evento_raffiche_vento(settimane_supplementari, personaggi_selezionati)
        report["dettagli"] = {"ritardo": ritardo, "ha_navigatore": ha_navigatore}

    elif nome_evento == EVENTO_AVVISTAMENTO_ISOLA:
        (personaggi_selezionati, equip_scelto, cibo_scelto,
         settimane_supplementari, abitata, ostili, guadagno) = \
            evento_avvistamento_isola(
                personaggi_selezionati, equip_scelto, cibo_scelto,
                settimane_supplementari, albatro_avvistato, albatro_ucciso
            )
        report["dettagli"] = {
            "isola_abitata": abitata,
            "isolani_ostili": ostili,
            "guadagno_cibo": guadagno,
        }

    return {
        "personaggi":             personaggi_selezionati,
        "cibo":                   cibo_scelto,
        "equip":                  equip_scelto,
        "settimane_supplementari": settimane_supplementari,
        "albatro_avvistato":      albatro_avvistato,
        "albatro_ucciso":         albatro_ucciso,
        "delta_morale":           delta_morale,
        "report":                 report,
    }
