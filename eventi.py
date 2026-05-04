import random
from utility import MOD,HEIGHT,WIDTH, font_numeri,title_font,info_font, BIANCO
import pygame
import copy
pygame.init()
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

def ui_generale_schermata_nera(schermo, txt_title, txt_domanda, txt_motivo, lista_scelte, font_title=title_font, font_domanda=font_numeri, font_scelte=font_numeri, font_motivo=info_font, colore_testo=BIANCO, colore_sfondo=(0, 0, 0), pos_title=(WIDTH//2, HEIGHT//4), pos_domanda=(WIDTH//2, HEIGHT//2), pos_scelte=(WIDTH//2, HEIGHT//2 + 100*MOD), spazio_tra_scelte=50*MOD, presenza_scelte=True, mouse=None, click=False):
    schermo.fill(colore_sfondo)
    
    # Disegna Titolo centrato
    title = font_title.render(txt_title, True, colore_testo)
    title_rect = title.get_rect(center=pos_title)
    schermo.blit(title, title_rect)
    
    # Disegna Domanda centrata
    domanda = font_domanda.render(txt_domanda, True, colore_testo)
    domanda_rect = domanda.get_rect(center=pos_domanda)
    schermo.blit(domanda, domanda_rect)
    
    # Disegna Motivo centrato sotto la domanda
    motivo = font_motivo.render(txt_motivo, True, colore_testo)
    motivo_rect = motivo.get_rect(center=(pos_domanda[0], pos_domanda[1] + 50*MOD))
    schermo.blit(motivo, motivo_rect)
    
    scelta_cliccata = None
    
    if presenza_scelte:
        for i, scelta in enumerate(lista_scelte):
            testo_scelta = font_scelte.render(scelta, True, colore_testo)
            # Centra anche i pulsanti delle scelte
            rect_scelta = testo_scelta.get_rect(center=(pos_scelte[0], pos_scelte[1] + i * spazio_tra_scelte))
            schermo.blit(testo_scelta, rect_scelta)
            
            # Controlla se il mouse è sopra e se c'è stato un click
            if mouse and click and rect_scelta.collidepoint(mouse):
                scelta_cliccata = scelta
                
    return scelta_cliccata
    
    
def mostra_messaggio_evento(titolo, domanda, motivo, scelte=["Continua"]):
    schermo = pygame.display.get_surface()
    start = True
    scelta_fatta = None
    
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


def evento_uomo_in_mare(personaggi_selezionati):
    schermo = pygame.display.get_surface()
    start = True
    vivi = [p for p in personaggi_selezionati if p.get("stats", {}).get("alive", True)]
    if not vivi:
        return personaggi_selezionati, None
    vittima = random.choice(vivi)
    vittima["stats"]["alive"] = False
    
    while start:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        # Gestione eventi ESCLUSIVA per questa schermata
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                start = False # Permetti di premere Invio per continuare

        # Disegna la UI e ottieni la scelta
        scelta = mostra_messaggio_evento(
            titolo="UOMO IN MARE!",
            domanda=f"Un membro dell'equipaggio: {vittima.get('info', {}).get('name', 'Membro sconosciuto')} è caduto in mare!",
            motivo="Speriamo che sappia nuotare...",
        )
        
        # Se l'utente clicca sul pulsante "Continua", esci dal ciclo
        if scelta == "Continua":
            start = False
            
        pygame.display.flip()

    # Logica dell'evento
    
    return personaggi_selezionati, vittima.get("info", {}).get("name", "Membro sconosciuto")

def _perdita_scorta(cibo, nome_cibo):# puo essere acqu verdura o non verdura
    quota = random.choice([2, 3, 4])
    perdita =  cibo* (1 / quota)
    if perdita <= 0 :
        mostra_messaggio_evento(
        titolo=f"{nome_cibo.upper()} IN MARE!",
        domanda="Una violenta tempesta ha colpito la nave!",
        motivo=f"Una parte delle scorte di {nome_cibo} è finita in mare."
    )
        return 0
    else:
        mostra_messaggio_evento(
            titolo=f"{nome_cibo.upper()} IN MARE!",
            domanda="Una violenta tempesta ha colpito la nave!",
            motivo=f"Una parte delle scorte di {nome_cibo} è finita in mare."
        )
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
        motivo=f"Le scorte di carne sono aumentate di {quantita} kg grazie a una pesca miracolosa!")
    return cibo

def evento_tempesta_miracolosa(cibo_scelto):
    cibo,quantita = aggiungi_cibo(cibo_scelto)
    mostra_messaggio_evento(
        titolo="TEMPESTA MIRACOLOSA!",
        domanda="Una tempesta ha rinfrescato la nave!",
        motivo=f"Le scorte di acqua sono aumentate di {quantita} litri grazie alla tempesta miracolosa!")
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
        domanda="Il vento è cambiato in nostro favore!",
        motivo=f"Il viaggio sarà più veloce e l'equipaggio guadagna {bonus_morale} morale!"
    )
    return settimane_supplementari

def evento_cattivo_tempo(equip_scelto):

    n_medicinali = 0
    for p in equip_scelto:
        if p.get("stats", {}).get("tipo") == "medicinale":
            n_medicinali += 1

    if n_medicinali == 0:
        mostra_messaggio_evento(
            titolo="CATTIVO TEMPO!",
            domanda="Il tempo è peggiorato!",
            motivo="Per fortuna non avevamo medicinali da poter perdere."
        )
        return equip_scelto

    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_medicinali * (1 / quota))

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
    perdita = int(n_armi * (1 / quota))
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
        return equip_scelto
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_stoffe * (1 / quota))
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
        if e.get("info", {}).get("name") == "armi" or e.get("stats", {}).get("tipo") == "arma":
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

    abbattuto = False
    fortuna_dellalbatro = False
    for _ in range(numero_colpi):
        if random.randint(1, 10) > 7:
            abbattuto = True
            break

    # Rimuoviamo le armi usate dalla lista
    for i in range(numero_colpi):
        if armi_disponibili:
            arma_da_rimuovere = armi_disponibili.pop()
            if arma_da_rimuovere in equip_scelto:
                equip_scelto.remove(arma_da_rimuovere)

    if abbattuto:
        guadagno_carne = numero_colpi * 5
        carne_totale += guadagno_carne
            
        albatro_ucciso = True
        
        mostra_messaggio_evento(
            titolo="ALBATRO UCCISO!",
            domanda="Un colpo perfetto! L'albatro cade in mare.",
            motivo=f"Abbiamo recuperato {guadagno_carne} kg di carne. Abbiamo perso {numero_colpi} fucili."
        )
    else:
        albatro_ucciso = False
        mostra_messaggio_evento(
            titolo="COLPO MANCATO",
            domanda="L'albatro è volato via illeso.",
            motivo=f"Abbiamo sprecato {numero_colpi} fucili sparando a vuoto."
        )

    return carne_totale, albatro_avvistato, albatro_ucciso, fortuna_dellalbatro


import copy
import random

def evento_scialuppa(personaggi_selezionati, equip_scelto, PERSONAGGI, MERCI):
    spazio_disponibile = 16 - len(personaggi_selezionati)
    
    if spazio_disponibile <= 0:
        mostra_messaggio_evento(
            titolo="AVVISTAMENTO SCIALUPPA",
            domanda="Abbiamo avvistato 4 naufraghi alla deriva...",
            motivo="...ma la nostra nave è già piena (16 membri). Dobbiamo tirar dritto."
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
            motivo="Il mare è crudele, ma le nostre scorte sono preziose."
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
            
            nuovo_naufrago["pos"]["main"]["x_attuale"] = random.randint(int(400*MOD), int(WIDTH - 420*MOD))
            nuovo_naufrago["pos"]["main"]["y_attuale"] = random.randint(int(430*MOD), int(470*MOD))

            personaggi_selezionati.append(nuovo_naufrago)


    oggetti_trovati = 0
    for _ in range(5):
        tipo_oggetto = random.choice(["medicinale", "armi", "stoffa", "sale", "coltelli", "diamanti"])
        for merce in MERCI:
            if merce["info"]["name"] == tipo_oggetto:
                nuova_merce = {
                    "stats": copy.deepcopy(merce["stats"]),
                    "info": copy.deepcopy(merce["info"]),
                    "sprites": merce.get("sprites", {})
                }
                equip_scelto.append(nuova_merce)
                oggetti_trovati += 1
                break

    if naufraghi_da_salvare < 4:
        testo_uomini = f"Abbiamo salvato {naufraghi_da_salvare} uomini (la nave è ora piena)."
    else:
        testo_uomini = "Abbiamo accolto a bordo tutti e 4 gli uomini."

    mostra_messaggio_evento(
        titolo="SALVATAGGIO COMPLETATO",
        domanda="Abbiamo svuotato la loro cassa.",
        motivo=f"{testo_uomini} Trovati {oggetti_trovati} oggetti utili."
    )

    return personaggi_selezionati, equip_scelto
def evento_epidemia(personaggi_selezionati, equip_scelto):
    # 1. Troviamo i medicinali disponibili
    medicinali_disponibili = []
    for e in equip_scelto:
        if e.get("info", {}).get("name") == "medicinale" or e.get("stats", {}).get("tipo") == "medicinale":
            medicinali_disponibili.append(e)
            
    numero_medicinali = len(medicinali_disponibili)
    ha_medico = presenza_ruolo(personaggi_selezionati, "medico")

    malati = 0
    curati = 0
    morti = 0
    bottiglie_usate = 0

    # 2. Logica dei contagi SENZA usare "continue"
    for p in personaggi_selezionati:
        is_vivo = p.get("stats", {}).get("alive", True)
        is_medico = p.get("info", {}).get("ruolo") == "medico"
        
        # Procediamo solo se il personaggio è vivo e NON è un medico
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

    # 3. CREIAMO IL REPORT
    report = {
        "malati": malati,
        "curati": curati,
        "morti": morti,
        "bottiglie_usate": bottiglie_usate,
    }

    # 4. USIAMO I DATI DEL REPORT PER L'INTERFACCIA UI
    if report["malati"] == 0:
        mostra_messaggio_evento(
            titolo="NESSUN MALATO!",
            domanda="Un'epidemia ha sfiorato la nave...",
            motivo="...ma fortunatamente l'equipaggio ha gli anticorpi di ferro. Nessun malato."
        )
    elif report["morti"] > 0:
        if not ha_medico:
            motivo_morte = "Senza un medico a bordo, sono morti tutti i malati."
        else:
            motivo_morte = "Non avevamo abbastanza medicinali per curarli tutti."
            
        mostra_messaggio_evento(
            titolo="EPIDEMIA DEVASTANTE!",
            domanda=f"{report['malati']} membri dell'equipaggio si sono ammalati.",
            motivo=f"Curati: {report['curati']}. Morti: {report['morti']}. {motivo_morte}"
        )
    else:
        mostra_messaggio_evento(
            titolo="EPIDEMIA SOTTO CONTROLLO",
            domanda=f"{report['malati']} membri dell'equipaggio si sono ammalati.",
            motivo=f"Il medico li ha curati tutti usando {report['bottiglie_usate']} medicinali!"
        )
    
    return personaggi_selezionati, equip_scelto

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
