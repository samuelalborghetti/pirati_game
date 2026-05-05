import random
from utility import MOD,HEIGHT,WIDTH, font_numeri,title_font,info_font, BIANCO
import pygame
import copy
pygame.init()
SOGLIA_EPIDEMIA          = 0.7
MALUS_MORALE_SCORTE_ESAURITE  = 10
MALUS_MORALE_DIMEZZA_RAZIONI  = 5
BONUS_MORALE_RADDOPPIA_RAZIONI = 5
MARINAI_MAX              = 12
SOGLIA_MORALE_BASSO      = 30

PUNTI_RAZIONI_RIDOTTE    = 30
PUNTI_NO_CUOCO           = 30
PUNTI_ALBATRO_UCCISO     = 30
PUNTI_ALBATRO_RISPARMIATO = -20
PUNTI_NAVE_AFFOLLATA     = 30
PUNTI_SETTIMANA_EXTRA    = 10
SOGLIA_AMMUTINAMENTO     = 100

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


def ui_generale_schermata_nera(schermo, txt_title, txt_domanda, txt_motivo, lista_scelte, font_title=title_font, font_domanda=font_numeri, font_scelte=font_numeri, font_motivo=info_font, colore_testo=BIANCO, colore_sfondo=(0, 0, 0), pos_title=(WIDTH//2, HEIGHT//4), pos_domanda=(WIDTH//2, HEIGHT//2), pos_scelte=(WIDTH//2, HEIGHT//2 + 100*MOD), spazio_tra_scelte=50*MOD, presenza_scelte=True, mouse=None, click=False):
    schermo.fill(colore_sfondo)
    
    title = font_title.render(txt_title, True, colore_testo)
    title_rect = title.get_rect(center=pos_title)
    schermo.blit(title, title_rect)
    
    domanda = font_domanda.render(txt_domanda, True, colore_testo)
    domanda_rect = domanda.get_rect(center=pos_domanda)
    schermo.blit(domanda, domanda_rect)
    
    motivo = font_motivo.render(txt_motivo, True, colore_testo)
    motivo_rect = motivo.get_rect(center=(pos_domanda[0], pos_domanda[1] + 50*MOD))
    schermo.blit(motivo, motivo_rect)
    
    scelta_cliccata = None
    
    if presenza_scelte:
        for i, scelta in enumerate(lista_scelte):
            testo_scelta = font_scelte.render(scelta, True, colore_testo)
            rect_scelta = testo_scelta.get_rect(center=(pos_scelte[0], pos_scelte[1] + i * spazio_tra_scelte))
            schermo.blit(testo_scelta, rect_scelta)
            
            if mouse and click and rect_scelta.collidepoint(mouse):
                scelta_cliccata = scelta
                
    return scelta_cliccata
    
    
def mostra_messaggio_evento(titolo, domanda, motivo, scelte=["Continua"]):
    schermo = pygame.display.get_surface()
    start = True
    
    while start:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return scelte[0]

        scelta = ui_generale_schermata_nera(
            schermo=schermo,
            txt_title=titolo,
            txt_domanda=domanda,
            txt_motivo=motivo,
            lista_scelte=scelte,
            presenza_scelte=True,
            mouse=mouse_pos,
            click=mouse_click
        )
        
        if scelta:
            return scelta
            
        pygame.display.flip()


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


# ─── EVENTI ────────────────────────────────────────────────────────────────────

def evento_uomo_in_mare(personaggi_selezionati):
    schermo = pygame.display.get_surface()
    vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
    if not vivi:
        return personaggi_selezionati, None
    vittima = random.choice(vivi)
    vittima["stats"]["alive"] = False
    
    mostra_messaggio_evento(
        titolo="UOMO IN MARE!",
        domanda=f"{vittima.get('info', {}).get('name', 'Membro sconosciuto')} e' caduto in mare!",
        motivo="Speriamo che sappia nuotare...",
    )
    
    return personaggi_selezionati, vittima.get("info", {}).get("name", "Membro sconosciuto")


def _perdita_scorta(cibo, nome_cibo):
    quota = random.choice([2, 3, 4, 5])
    perdita = cibo * (1.0 / quota)
    mostra_messaggio_evento(
        titolo=f"{nome_cibo.upper()} IN MARE!",
        domanda="Una violenta tempesta ha colpito la nave!",
        motivo=f"1/{quota} delle scorte di {nome_cibo} e' finita in mare."
    )
    if perdita <= 0:
        return 0
    return perdita

def evento_verdura_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "verdura")

def evento_frutta_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "frutta")

def evento_carne_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "carne")

def evento_acqua_in_mare(cibo_scelto):
    return _perdita_scorta(cibo_scelto, "acqua")


def aggiungi_cibo(cibo_scelto):
    quantita = random.randint(11, 20)
    cibo = cibo_scelto + quantita
    return cibo, quantita

def evento_pesca_miracolosa(cibo_scelto):
    cibo, quantita = aggiungi_cibo(cibo_scelto)
    mostra_messaggio_evento(
        titolo="PESCA MIRACOLOSA!",
        domanda="Una giornata fortunata in mare!",
        motivo=f"Le scorte di carne sono aumentate di {quantita} kg!")
    return cibo

def evento_tempesta_miracolosa(cibo_scelto):
    cibo, quantita = aggiungi_cibo(cibo_scelto)
    mostra_messaggio_evento(
        titolo="TEMPESTA MIRACOLOSA!",
        domanda="Una tempesta ha rinfrescato la nave!",
        motivo=f"Le scorte di acqua sono aumentate di {quantita} litri!")
    return cibo


def evento_venti_favorevoli(settimane_supplementari, personaggi_selezionati):
    bonus_morale = random.randint(5, 15)
    settimane_supplementari = max(0, settimane_supplementari - 1)
    for p in personaggi_selezionati:
        if p.get("stats", {}).get("alive", True):
            morale_attuale = p.get("morale", 100)
            p["morale"] = min(100, morale_attuale + bonus_morale)
    mostra_messaggio_evento(
        titolo="VENTI FAVOREVOLI!",
        domanda="Il vento e' cambiato in nostro favore!",
        motivo=f"Il viaggio sara' piu' veloce e l'equipaggio guadagna {bonus_morale} morale!"
    )
    return settimane_supplementari, bonus_morale


def evento_cattivo_tempo(equip_scelto):
    n_medicinali = 0
    for p in equip_scelto:
        if p.get("stats", {}).get("tipo") == "medicinale":
            n_medicinali += 1

    if n_medicinali == 0:
        mostra_messaggio_evento(
            titolo="CATTIVO TEMPO!",
            domanda="Il tempo e' peggiorato!",
            motivo="Per fortuna non avevamo medicinali da poter perdere."
        )
        return equip_scelto

    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_medicinali * (1.0 / quota))

    for i in range(perdita):
        for p in equip_scelto:
            if p.get("stats", {}).get("tipo") == "medicinale":
                equip_scelto.remove(p)
                break

    mostra_messaggio_evento(
        titolo="CATTIVO TEMPO!",
        domanda="I violenti sobbalzi della nave hanno fatto danni!",
        motivo=f"Si sono rovesciate e rotte {perdita} bottiglie di medicinale (1/{quota})."
    )
    return equip_scelto


def evento_ondata(equip_scelto):
    n_armi = 0
    for p in equip_scelto:
        if p.get("stats", {}).get("tipo") == "arma":
            n_armi += 1
    if n_armi == 0:
        mostra_messaggio_evento(
            titolo="ONDATA!",
            domanda="Un'onda improvvisa ha colpito la nave!",
            motivo="Per fortuna non avevamo armi da poter perdere."
        )
        return equip_scelto
    
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_armi * (1.0 / quota))
    for i in range(perdita):
        for p in equip_scelto:
            if p.get("stats", {}).get("tipo") == "arma":
                equip_scelto.remove(p)
                break
    mostra_messaggio_evento(
        titolo="ONDATA!",
        domanda="Un'onda improvvisa ha colpito la nave!",
        motivo=f"Si sono rotte {perdita} armi a causa dell'onda!"
    )
    return equip_scelto


def evento_infestazione_ratti(equip_scelto):
    n_stoffe = 0
    for p in equip_scelto:
        if p.get("stats", {}).get("tipo") == "strumento":
            n_stoffe += 1
    if n_stoffe == 0:
        mostra_messaggio_evento(
            titolo="INFESTAZIONE DI RATTI!",
            domanda="I ratti hanno invaso la stiva!",
            motivo="Per fortuna non c'erano stoffe da danneggiare."
        )
        return equip_scelto
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_stoffe * (1.0 / quota))
    for i in range(perdita):
        for p in equip_scelto:
            if p.get("stats", {}).get("tipo") == "strumento":
                equip_scelto.remove(p)
                break
    mostra_messaggio_evento(
        titolo="INFESTAZIONE DI RATTI!",
        domanda="I ratti hanno danneggiato le stoffe!",
        motivo=f"Si sono rovinate {perdita} stoffe!"
    )
    return equip_scelto


def evento_avvistamento_albatro(
    personaggi_selezionati, equip_scelto, carne_totale,
    albatro_avvistato, albatro_ucciso, fortuna_dellalbatro=False
):
    if albatro_avvistato >= 3:
        return carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro
    
    albatro_avvistato += 1

    armi_disponibili = []
    for e in equip_scelto:
        if e.get("stats", {}).get("tipo") == "arma":
            armi_disponibili.append(e)
            
    numero_armi = len(armi_disponibili)
    numero_uomini = conta_membri_vivi(personaggi_selezionati)
    numero_colpi = min(numero_armi, numero_uomini, 6)

    if numero_armi == 0 or numero_colpi == 0:
        mostra_messaggio_evento(
            titolo="ALBATRO AVVISTATO",
            domanda="Un maestoso albatro ci sorvola.",
            motivo="Non avendo armi pronte, possiamo solo ammirarlo volare via."
        )
        fortuna_dellalbatro = True
        return carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro

    scelta = mostra_messaggio_evento(
        titolo="ALBATRO AVVISTATO",
        domanda="Un albatro ci sorvola. Porta sfortuna ucciderlo...",
        motivo="...ma la sua carne ci farebbe molto comodo. Cosa facciamo?",
        scelte=["Spara", "Ignora"]
    )

    if scelta == "Ignora":
        mostra_messaggio_evento(
            titolo="ALBATRO RISPARMIATO",
            domanda="L'uccello si allontana all'orizzonte.",
            motivo="Speriamo che il mare ci ricompensi per avergli risparmiato la vita."
        )
        fortuna_dellalbatro = True
        return carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro

    fortuna_dellalbatro = False
    abbattuto = False
    for _ in range(numero_colpi):
        if random.random() < 0.5:
            abbattuto = True
            break

    for i in range(numero_colpi):
        if armi_disponibili:
            arma_da_rimuovere = armi_disponibili.pop()
            if arma_da_rimuovere in equip_scelto:
                equip_scelto.remove(arma_da_rimuovere)

    if abbattuto:
        guadagno_carne = random.randint(10, 15)
        carne_totale += guadagno_carne
        albatro_ucciso = True
        mostra_messaggio_evento(
            titolo="ALBATRO UCCISO!",
            domanda="Un colpo perfetto! L'albatro cade in mare.",
            motivo=f"Recuperati {guadagno_carne} kg di carne. Persi {numero_colpi} fucili."
        )
    else:
        albatro_ucciso = False
        mostra_messaggio_evento(
            titolo="COLPO MANCATO",
            domanda="L'albatro e' volato via illeso.",
            motivo=f"Abbiamo sprecato {numero_colpi} fucili sparando a vuoto."
        )

    return carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro


def evento_scialuppa(personaggi_selezionati, equip_scelto, PERSONAGGI, MERCI):
    spazio_disponibile = 16 - len(personaggi_selezionati)
    
    if spazio_disponibile <= 0:
        mostra_messaggio_evento(
            titolo="AVVISTAMENTO SCIALUPPA",
            domanda="Abbiamo avvistato 4 naufraghi alla deriva...",
            motivo="...ma la nostra nave e' gia' piena (16 membri). Dobbiamo tirar dritto."
        )
        return personaggi_selezionati, equip_scelto
        
    scelta = mostra_messaggio_evento(
        titolo="AVVISTAMENTO SCIALUPPA",
        domanda="Ci sono 4 naufraghi alla deriva con una cassa.",
        motivo=f"Li portiamo a bordo? Lavoreranno gratis. (Spazio libero: {spazio_disponibile})",
        scelte=["Salva i naufraghi", "Ignorali"]
    )
    
    if scelta == "Ignorali":
        mostra_messaggio_evento(
            titolo="NAUFRAGHI ABBANDONATI",
            domanda="Abbiamo tirato dritto.",
            motivo="Il mare e' crudele, ma le nostre scorte sono preziose."
        )
        return personaggi_selezionati, equip_scelto

    naufraghi_da_salvare = min(4, spazio_disponibile)

    RUOLI_POSSIBILI = ["capitano", "cuoco", "navigatore", "medico",
                       "marinaio", "meccanico", "bardo", "tesoriere"]

    for _ in range(naufraghi_da_salvare):
        ruolo_estratto = random.choice(RUOLI_POSSIBILI)
        
        p_originale = None
        for p in PERSONAGGI:
            if p["info"]["ruolo"] == ruolo_estratto:
                p_originale = p
                break
                
        if p_originale:
            nuovo_naufrago = {
                "stats": copy.deepcopy(p_originale["stats"]),
                "pos": copy.deepcopy(p_originale["pos"]),
                "sprites": p_originale["sprites"], 
                "info": copy.deepcopy(p_originale["info"]),
                "morale": random.randint(25, 75)
            }
            
            nuovo_naufrago["stats"]["cost"] = 0
            nuovo_naufrago["stats"]["alive"] = True
            nuovo_naufrago["info"]["name"] = "Naufrago"
            nuovo_naufrago["info"]["descrizione"] = f"Naufrago salvato - ruolo: {ruolo_estratto}"
            
            from utility import WIDTH, MOD
            nuovo_naufrago["pos"]["main"]["x_attuale"] = random.randint(int(400*MOD), int(WIDTH - 420*MOD))
            nuovo_naufrago["pos"]["main"]["y_attuale"] = random.randint(int(430*MOD), int(470*MOD))

            personaggi_selezionati.append(nuovo_naufrago)

    # Cassa: tutte le tipologie di merci +10/20 unità (da specifiche)
    oggetti_trovati = 0
    tipi_cassa = ["medicinale", "armi", "sale", "coltelli", "stoffa", "diamanti"]
    for tipo_oggetto in tipi_cassa:
        quantita_trovata = random.randint(10, 20)
        for merce in MERCI:
            if merce["info"]["name"] == tipo_oggetto:
                for _ in range(quantita_trovata):
                    nuova_merce = {
                        "stats": copy.deepcopy(merce["stats"]),
                        "info": copy.deepcopy(merce["info"]),
                        "sprites": merce.get("sprites", {})
                    }
                    equip_scelto.append(nuova_merce)
                    oggetti_trovati += 1
                break

    if naufraghi_da_salvare < 4:
        testo_uomini = f"Salvati {naufraghi_da_salvare} uomini (nave ora piena)."
    else:
        testo_uomini = "Accolti a bordo tutti e 4 gli uomini."

    mostra_messaggio_evento(
        titolo="SALVATAGGIO COMPLETATO",
        domanda="Abbiamo svuotato la loro cassa.",
        motivo=f"{testo_uomini} Trovati {oggetti_trovati} oggetti utili."
    )

    return personaggi_selezionati, equip_scelto


def evento_epidemia(personaggi_selezionati, equip_scelto):
    medicinali_disponibili = []
    for e in equip_scelto:
        if e.get("stats", {}).get("tipo") == "medicinale":
            medicinali_disponibili.append(e)
            
    numero_medicinali = len(medicinali_disponibili)
    ha_medico = presenza_ruolo(personaggi_selezionati, "medico")

    malati = 0
    curati = 0
    morti = 0
    bottiglie_usate = 0

    for p in personaggi_selezionati:
        is_vivo = p.get("stats", {}).get("alive", True)
        is_medico = p.get("info", {}).get("ruolo") == "medico"
        
        if is_vivo and not is_medico:
            if random.random() < SOGLIA_EPIDEMIA:
                malati += 1
                if ha_medico and numero_medicinali > 0:
                    curati += 1
                    bottiglie_usate += 1
                    numero_medicinali -= 1
                    med_da_rimuovere = medicinali_disponibili.pop()
                    equip_scelto.remove(med_da_rimuovere)
                else:
                    p["stats"]["alive"] = False
                    morti += 1

    report = {
        "malati": malati,
        "curati": curati,
        "morti": morti,
        "bottiglie_usate": bottiglie_usate,
    }

    if report["malati"] == 0:
        mostra_messaggio_evento(
            titolo="NESSUN MALATO!",
            domanda="Un'epidemia ha sfiorato la nave...",
            motivo="...fortunatamente l'equipaggio ha anticorpi di ferro. Nessun malato."
        )
    elif report["morti"] > 0:
        if not ha_medico:
            motivo_morte = "Senza un medico a bordo, sono morti tutti i malati."
        else:
            motivo_morte = "Non avevamo abbastanza medicinali per curarli tutti."
        mostra_messaggio_evento(
            titolo="EPIDEMIA DEVASTANTE!",
            domanda=f"{report['malati']} membri si sono ammalati.",
            motivo=f"Curati: {report['curati']}. Morti: {report['morti']}. {motivo_morte}"
        )
    else:
        mostra_messaggio_evento(
            titolo="EPIDEMIA SOTTO CONTROLLO",
            domanda=f"{report['malati']} membri si sono ammalati.",
            motivo=f"Il medico li ha curati tutti usando {report['bottiglie_usate']} medicinali!"
        )
    
    return personaggi_selezionati, equip_scelto


def evento_attacco_pirata(personaggi_selezionati, equip_scelto):
    numero_pirati = random.randint(3, 10)
    
    n_armi = 0
    for e in equip_scelto:
        if e.get("stats", {}).get("tipo") == "arma":
            n_armi += 1
    numero_membri = conta_membri_vivi(personaggi_selezionati)

    # numero_difensori = min(armi, membri vivi) - da specifiche
    numero_difensori = min(n_armi, numero_membri)

    perdite = max(0, numero_pirati - numero_difensori)
    perdite = min(perdite, numero_membri)
    vittoria = perdite <= 0

    if perdite > 0:
        vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
        random.shuffle(vivi)
        for i in range(min(perdite, len(vivi))):
            vivi[i]["stats"]["alive"] = False

    # Rimuovi armi usate (= numero_difensori)
    armi_usate = numero_difensori
    rimossi = 0
    for e in list(equip_scelto):
        if rimossi >= armi_usate:
            break
        if e.get("stats", {}).get("tipo") == "arma":
            equip_scelto.remove(e)
            rimossi += 1

    if vittoria:
        mostra_messaggio_evento(
            titolo="ATTACCO RESPINTO!",
            domanda=f"I pirati erano {numero_pirati}, noi {numero_difensori} difensori.",
            motivo=f"Abbiamo vinto! Usate {armi_usate} armi."
        )
    else:
        mostra_messaggio_evento(
            titolo="ATTACCO PIRATA!",
            domanda=f"I pirati erano {numero_pirati}, noi solo {numero_difensori} difensori.",
            motivo=f"Persi {perdite} uomini. Usate {armi_usate} armi."
        )

    return personaggi_selezionati, equip_scelto


def evento_danni_timone(settimane_supplementari, personaggi_selezionati):
    ha_meccanico = presenza_ruolo(personaggi_selezionati, "meccanico")
    if ha_meccanico:
        ritardo = 1
    else:
        ritardo = random.randint(2, 4)
    
    mostra_messaggio_evento(
        titolo="DANNI AL TIMONE!",
        domanda="L'urto con uno scoglio ha danneggiato il timone.",
        motivo=f"{'Il meccanico lo aggiusta in fretta:' if ha_meccanico else 'Senza meccanico ci vuole piu tempo:'} +{ritardo} settimane."

    )
    print(f"DEBUG: ha_meccanico={ha_meccanico}, ritardo={ritardo}, settimane_supplementari={settimane_supplementari}")
    settimane_tornare = int(settimane_supplementari + ritardo)
    return settimane_tornare


def evento_raffiche_vento(settimane_supplementari, personaggi_selezionati):
    ha_navigatore = presenza_ruolo(personaggi_selezionati, "navigatore")
    if ha_navigatore:
        ritardo = 1
    else:
        ritardo = random.randint(2, 4)
    
    mostra_messaggio_evento(
        titolo="RAFFICHE DI VENTO!",
        domanda="Forti raffiche di vento ci allontanano dalla rotta.",
        motivo=f"{'Il navigatore ci riporta in rotta:' if ha_navigatore else 'Senza navigatore giriamo a vuoto:'} +{ritardo} settimane."
    )
    settimana_tornare = settimane_supplementari + ritardo
    return settimana_tornare

import random
import copy

def evento_avvistamento_isola(
    equip_scelto,
    n_medicinali,
    settimane_supplementari,
    albatro_avvistato: int,
    albatro_ucciso: bool,
    MERCI
):
    """
    SPEC:
    - Se "Prosegui": non succede nulla.
    - Se "Approda": viaggio +1/2 settimane (sempre).
    - 50% deserta -> fine
    - 50% abitata:
        - 50% ostili -> fine
        - 50% amichevoli -> donano MERCI (non cibo):
            +5..20 per ogni tipologia merce
            oppure +20..40 se albatro avvistato e NON ucciso

    Ritorna SOLO:
      (settimane_supplementari_aggiornate, settimane_aggiunte, medicinali_aggiunti)
    """

    scelta = mostra_messaggio_evento(
        titolo="AVVISTAMENTO ISOLA!",
        domanda="Intravediamo un'isola misteriosa all'orizzonte.",
        motivo="Vogliamo approdare per un'ispezione? (+1/2 settimane)",
        scelte=["Approda", "Prosegui"]
    )

    if scelta == "Prosegui":
        mostra_messaggio_evento(
            titolo="ISOLA IGNORATA",
            domanda="Proseguiamo la rotta.",
            motivo="Chi sa cosa c'era su quell'isola..."
        )
        return settimane_supplementari, n_medicinali

    settimane_aggiunte = random.randint(1, 2)
    settimane_supplementari += settimane_aggiunte

    # 50% isola deserta
    if random.random() < 0.5:
        mostra_messaggio_evento(
            titolo="ISOLA DESERTA",
            domanda="L'isola e' completamente disabitata.",
            motivo=f"Niente da fare qui. Viaggio +{settimane_aggiunte} settimane."
        )
        return settimane_supplementari, n_medicinali

    # 50% (delle abitate) isolani ostili
    if random.random() < 0.5:
        mostra_messaggio_evento(
            titolo="ISOLANI OSTILI!",
            domanda="Gli abitanti ci cacciano via con le armi!",
            motivo=f"Siamo fuggiti senza danni. Viaggio +{settimane_aggiunte} settimane."
        )
        return settimane_supplementari, n_medicinali

    if albatro_avvistato > 0 and not albatro_ucciso:
        bonus = random.randint(20, 40)
    else:
        bonus = random.randint(5, 20)

    # Tipologie merci (come nel tuo evento scialuppa; nota: lì avevi "armi", qui usi spesso "arma")
    tipi_merce = ["medicinale", "armi", "sale", "coltelli", "stoffa", "diamanti"]

    medicinali_aggiunti = 0

    for tipo in tipi_merce:
        template = next((m for m in MERCI if m["info"]["name"] == tipo), None)
        if template is None:
            continue

        for _ in range(bonus):
            equip_scelto.append({
                "stats": copy.deepcopy(template["stats"]),
                "info": copy.deepcopy(template["info"]),
                "sprites": template.get("sprites", {}),
            })

        if tipo == "medicinale":
            medicinali_aggiunti = bonus

    mostra_messaggio_evento(
        titolo="ISOLANI AMICHEVOLI!",
        domanda="Gli isolani ci accolgono calorosamente!",
        motivo=f"Ci donano merci! (+{bonus} per tipo). Viaggio +{settimane_aggiunte} settimane."
    )
    medicinali_tornare = n_medicinali + medicinali_aggiunti

    return settimane_supplementari, medicinali_aggiunti


# ─── STEP 2: CONTROLLO SCORTE ──────────────────────────────────────────────────

def controllo_scorte_settimanali(cibo_scelto, personaggi_selezionati, settimane_rimaste, razioni_attuali):
    num_membri = conta_membri_vivi(personaggi_selezionati)
    delta_morale = 0
    alert_list = []

    consumi_base = {
        "verdura": 0.5,
        "frutta":  1.0,
        "carne":   1.0,
        "acqua":   0.5,
    }

    for nome, consumo_per_membro in consumi_base.items():
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if cibo is None:
            continue

        moltiplicatore = razioni_attuali.get(nome, 1.0)
        consumo_settimanale = consumo_per_membro * moltiplicatore * num_membri
        consumo_necessario_base = consumo_per_membro * num_membri * settimane_rimaste

        quantita = get_saturazione(cibo)

        if quantita <= 0:
            delta_morale -= MALUS_MORALE_SCORTE_ESAURITE
            alert_list.append({
                "nome": nome,
                "tipo_alert": "esaurite",
                "quantita": quantita,
                "consumo_necessario": consumo_necessario_base,
            })
        else:
            consumo_futuro_necessario = consumo_per_membro * moltiplicatore * num_membri * settimane_rimaste
            consumo_doppio = consumo_per_membro * moltiplicatore * num_membri * settimane_rimaste * 2

            if quantita < consumo_futuro_necessario:
                alert_list.append({
                    "nome": nome,
                    "tipo_alert": "insufficienti",
                    "quantita": quantita,
                    "consumo_necessario": consumo_futuro_necessario,
                })
            elif quantita >= consumo_doppio:
                alert_list.append({
                    "nome": nome,
                    "tipo_alert": "abbondanti",
                    "quantita": quantita,
                    "consumo_necessario": consumo_futuro_necessario,
                })

        # Detraiamo il consumo della settimana in corso
        set_saturazione(cibo, quantita - consumo_settimanale)

    return delta_morale, alert_list, razioni_attuali


def gestisci_razioni_interattivo(cibo_scelto, personaggi_selezionati, settimane_rimaste, razioni_attuali):
    num_membri = conta_membri_vivi(personaggi_selezionati)
    consumi_base = {
        "verdura": 0.5,
        "frutta":  1.0,
        "carne":   1.0,
        "acqua":   0.5,
    }
    delta_morale = 0

    for nome, consumo_per_membro in consumi_base.items():
        cibo = trova_cibo_per_nome(cibo_scelto, nome)
        if cibo is None:
            continue

        moltiplicatore = razioni_attuali.get(nome, 1.0)
        quantita = get_saturazione(cibo)
        consumo_futuro = consumo_per_membro * moltiplicatore * num_membri * settimane_rimaste

        if quantita <= 0:
            # Scorte esaurite - malus morale già applicato in controllo_scorte
            mostra_messaggio_evento(
                titolo=f"SCORTE {nome.upper()} ESAURITE!",
                domanda=f"Non abbiamo piu' {nome} a bordo!",
                motivo=f"Il morale dell'equipaggio ne risente (-{MALUS_MORALE_SCORTE_ESAURITE} punti)."
            )
        elif quantita < consumo_futuro:
            # Scorte insufficienti - chiedi se dimezzare
            stato_attuale = "NORMALE"
            if moltiplicatore < 1.0:
                stato_attuale = "GIA' DIMEZZATA"
            
            scelta = mostra_messaggio_evento(
                titolo=f"SCORTE {nome.upper()} INSUFFICIENTI",
                domanda=f"Residuo: {quantita:.1f} - Necessario: {consumo_futuro:.1f}",
                motivo=f"Razione attuale: {stato_attuale}. Dimezzi la razione? (-{MALUS_MORALE_DIMEZZA_RAZIONI} morale/sett)",
                scelte=["Dimezza razione", "Mantieni razione"]
            )
            if scelta == "Dimezza razione":
                nuova_razione = moltiplicatore * 0.5
                razioni_attuali[nome] = nuova_razione
                delta_morale -= MALUS_MORALE_DIMEZZA_RAZIONI
                mostra_messaggio_evento(
                    titolo=f"RAZIONE {nome.upper()} DIMEZZATA",
                    domanda=f"La razione di {nome} e' stata ridotta.",
                    motivo=f"Morale dell'equipaggio -5 a settimana da ora in poi."
                )

        elif quantita >= consumo_futuro * 2:
            # Scorte abbondanti - chiedi se raddoppiare
            stato_attuale = "NORMALE"
            if moltiplicatore > 1.0:
                stato_attuale = "GIA' RADDOPPIATA"
            
            scelta = mostra_messaggio_evento(
                titolo=f"SCORTE {nome.upper()} ABBONDANTI!",
                domanda=f"Residuo: {quantita:.1f} - Doppio necessario: {consumo_futuro*2:.1f}",
                motivo=f"Razione attuale: {stato_attuale}. Raddoppi la razione? (+{BONUS_MORALE_RADDOPPIA_RAZIONI} morale/sett)",
                scelte=["Raddoppia razione", "Mantieni razione"]
            )
            if scelta == "Raddoppia razione":
                razioni_attuali[nome] = moltiplicatore * 2.0
                delta_morale += BONUS_MORALE_RADDOPPIA_RAZIONI
                mostra_messaggio_evento(
                    titolo=f"RAZIONE {nome.upper()} RADDOPPIATA!",
                    domanda=f"La razione di {nome} e' stata aumentata.",
                    motivo=f"Morale dell'equipaggio +5 a settimana da ora in poi."
                )

    return delta_morale, razioni_attuali


def aggiorna_morale_equipaggio(personaggi_selezionati, delta_morale):
    for p in personaggi_selezionati:
        if p.get("stats", {}).get("alive", True):
            morale = p.get("morale", 100)
            p["morale"] = max(0, min(100, morale + delta_morale))
    return personaggi_selezionati


def applica_morti_morale_zero(personaggi_selezionati):
    morti = []
    for p in personaggi_selezionati:
        if p.get("stats", {}).get("alive", True):
            if p.get("morale", 100) <= 0:
                p["stats"]["alive"] = False
                morti.append(p.get("info", {}).get("name", "?"))
    return morti



# ─── STEP 5: AMMUTINAMENTO ────────────────────────────────────────────────────

def calcola_punteggio_ammutinamento(
    personaggi_selezionati,
    albatro_avvistato,
    albatro_ucciso,
    settimane_supplementari,
    razioni_attuali
):
    """
    Calcola punteggio ammutinamento secondo le specifiche del PDF.
    Restituisce (punteggio, lista_motivi)
    """
    punteggio = 0
    motivi = []

    # Razioni ridotte: 30 punti se almeno UNA tipologia < 1.0
    ha_razioni_ridotte = False
    for nome, molt in razioni_attuali.items():
        if molt < 1.0:
            ha_razioni_ridotte = True
            break
    if ha_razioni_ridotte:
        punteggio += PUNTI_RAZIONI_RIDOTTE
        motivi.append("Razioni di cibo ridotte (+30)")

    # No cuoco: +30
    ha_cuoco = presenza_ruolo(personaggi_selezionati, "cuoco")
    if not ha_cuoco:
        punteggio += PUNTI_NO_CUOCO
        motivi.append("Manca un cuoco a bordo (+30)")

    # Albatro ucciso: +30
    if albatro_avvistato > 0 and albatro_ucciso:
        punteggio += PUNTI_ALBATRO_UCCISO
        motivi.append("E' stato ucciso un albatro - presagio di sfiga (+30)")

    # Albatro avvistato e NON ucciso: -20
    if albatro_avvistato > 0 and not albatro_ucciso:
        punteggio += PUNTI_ALBATRO_RISPARMIATO
        motivi.append("Albatro avvistato e risparmiato - ottimismo (-20)")

    # Nave affollata (>12 uomini): +30
    if conta_membri_vivi(personaggi_selezionati) > MARINAI_MAX:
        punteggio += PUNTI_NAVE_AFFOLLATA
        motivi.append(f"Nave troppo affollata (>{MARINAI_MAX} uomini) (+30)")

    # Settimane extra: +10 per ogni sett in più, -10 per ogni sett in meno
    if settimane_supplementari != 0:
        punti_sett = settimane_supplementari * PUNTI_SETTIMANA_EXTRA
        punteggio += punti_sett
        if settimane_supplementari > 0:
            motivi.append(f"Viaggio allungato di {settimane_supplementari} settimane (+{punti_sett})")
        else:
            motivi.append(f"Viaggio accorciato di {abs(settimane_supplementari)} settimane ({punti_sett})")

    return punteggio, motivi


