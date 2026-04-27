import random
import pygame
import json


albatro_avvistato = 0
albatro_ucciso = False

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.loads(file.read())
    file.close()
    return dati["width"], dati["height"], dati["audio"], dati["mod"]

pygame.font.init()
HEIGHT, WIDTH, VOLUME, MOD = CaricaSettings("dati/setting.json")
FONT_BOLD = pygame.font.Font("./assets/fonts/PixelifySans-Bold.ttf", int(50 * MOD))
def Drawtext(schermo, text: list, y_in, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        testo_rect = testo.get_rect(center=(schermo.get_width() // 2, y))
        schermo.blit(testo, testo_rect)
        y += spazio_tra_righe

def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = int(tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo  = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

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

def anima_topo(schermo, clock, sprites_topo, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD):
    frame = prendi_frame(sprites_topo["run right"], 120)
    frame_scalato = pygame.transform.scale(frame, (int(64 * MOD), int(64 * MOD)))
    topo_w = frame_scalato.get_width()
    topo_h = frame_scalato.get_height()

    x = random.randint(0, WIDTH_S - topo_w)
    y = random.randint(0, HEIGHT_S - topo_h)

    direzioni = ["run right", "run left", "run up", "run down"]
    direzione = random.choice(direzioni)
    velocita = 1 * MOD
    tempo_cambio = pygame.time.get_ticks()

    inizio = pygame.time.get_ticks()
    colpito_bordo = False
    while pygame.time.get_ticks() - inizio < durata_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if not colpito_bordo and pygame.time.get_ticks() - tempo_cambio > 1500:
            direzione = random.choice(direzioni)
            tempo_cambio = pygame.time.get_ticks()
        if direzione == "run right":
            x += velocita
        elif direzione == "run left":
            x -= velocita
        elif direzione == "run up":
            y -= velocita
        elif direzione == "run down":
            y += velocita
        frame = prendi_frame(sprites_topo[direzione], 120)
        frame_scalato = pygame.transform.scale(frame, (int(64 * MOD), int(64 * MOD)))
        topo_w = frame_scalato.get_width()
        topo_h = frame_scalato.get_height()
        colpito_bordo = False
        if x < 320*MOD+topo_w:
            x = 320*MOD+topo_w
            direzione = random.choice(["run right", "run up", "run down"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        elif x > 710*MOD-topo_w:
            x = 710*MOD-topo_w
            direzione = random.choice(["run left", "run down", "run up"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        if y < 485*MOD-topo_h:
            y = 485*MOD-topo_h
            direzione = random.choice(["run down", "run right", "run left"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        elif y > 565*MOD-topo_h:
            y = 565*MOD-topo_h
            direzione = random.choice(["run up", "run right", "run left"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            disegna_animazione(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(frame_scalato, (x, y))
        Drawtext(schermo, ["Un infestazione si è diffusa!"], int((HEIGHT_S // 2)- HEIGHT_S//4), FONT_BOLD, (255, 255, 255), 40*MOD)
        pygame.display.update()
        clock.tick(60)
        
        
def animazione_epidemia(schermo, clock, personaggi, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD, HEIGHT_S=HEIGHT):
    # Salva le posizioni originali per resetarle alla fine
    posizioni_originali = {
        id(p): (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"])
        for p in personaggi
    }

    # Direzioni possibili come nel topo
    DIREZIONI = ["right", "left", "up", "down"]
    VELOCITA = 2 * MOD
    tempo_cambio = pygame.time.get_ticks()
    stati = {}
    for p in personaggi:
        direzione = random.choice(DIREZIONI)
        stati[id(p)] = {
            "direzione": direzione,
            "flip": direzione == "left",
            "colpito_bordo": False,
        }

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        # Cambio direzione globale ogni 1.5s (solo per chi non ha colpito un bordo)
        cambia_ora = pygame.time.get_ticks() - tempo_cambio > 1500
        if cambia_ora:
            tempo_cambio = pygame.time.get_ticks()

        schermo.blit(bg, (0, 0))

        for p in personaggi:
            stato = stati[id(p)]
            x = p["pos"]["main"]["x_attuale"]
            y = p["pos"]["main"]["y_attuale"]
            direzione = stato["direzione"]
            colpito_bordo = stato["colpito_bordo"]

            # Cambia direzione tutti insieme ogni 1.5s se non hanno colpito un bordo
            if cambia_ora and not colpito_bordo:
                direzione = random.choice(DIREZIONI)
                stato["direzione"] = direzione

            # Movimento in base alla direzione
            if direzione == "right":
                x += VELOCITA
                stato["flip"] = False
            elif direzione == "left":
                x -= VELOCITA
                stato["flip"] = True
            elif direzione == "up":
                y -= VELOCITA
            elif direzione == "down":
                y += VELOCITA

            # Dimensione frame per i boundary
            w = int(64 * MOD)
            h = int(78 * MOD)

            # Boundary identici ad anima_topo
            colpito_bordo = False
            if x < 320 * MOD + w:
                x = 320 * MOD + w
                direzione = random.choice(["right", "up", "down"])
                stato["flip"] = False
                colpito_bordo = True
            elif x > 710 * MOD - w:
                x = 710 * MOD - w
                direzione = random.choice(["left", "up", "down"])
                stato["flip"] = True
                colpito_bordo = True
            if y < 485 * MOD - h:
                y = 485 * MOD - h
                direzione = random.choice(["down", "right", "left"])
                colpito_bordo = True
            elif y > 565 * MOD - h:
                y = 565 * MOD - h
                direzione = random.choice(["up", "right", "left"])
                colpito_bordo = True

            # Aggiorna stato e dizionario personaggio
            stato["direzione"] = direzione
            stato["colpito_bordo"] = colpito_bordo
            p["pos"]["main"]["x_attuale"] = x
            p["pos"]["main"]["y_attuale"] = y

            # Disegna con walk_cycle_sick e flip orizzontale in base alla direzione
            disegna_animazione(
                schermo, p["sprites"], "walk_cycle_sick", 120,
                (x, y), flip=stato["flip"]
            )
            Drawtext(schermo, ["L'epidemia si è diffusa!"], int((HEIGHT_S // 2)- HEIGHT_S//4), FONT_BOLD, (255, 255, 255), 40*MOD)

        pygame.display.update()
        clock.tick(60)
    
    
def animazione_albatro(schermo, clock, sprites_albatro, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD):
    frame = prendi_frame(sprites_albatro["run right"], 120)
    frame_scalato = pygame.transform.scale(frame, (int(64 * MOD), int(64 * MOD)))
    albatro_w = frame_scalato.get_width()
    albatro_h = frame_scalato.get_height()

    x = ((WIDTH_S // 2) - (albatro_w // 2)) - 90*MOD
    y = 80

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        frame = prendi_frame(sprites_albatro["run right"], 120)
        frame_scalato = pygame.transform.scale(frame, (int(300 * MOD), int(150 * MOD)))
        schermo.blit(bg, (0, 0))
        
        for p in PERSONAGGI_SCELTI:
            disegna_animazione(schermo, p["sprites"], "idle", 135,(p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        Drawtext(schermo, ["Un albatro si avvicina alla nave!"], int((HEIGHT_S // 2)- HEIGHT_S//4), FONT_BOLD, (255, 255, 255), 40*MOD)
        schermo.blit(frame_scalato, (x, y))
        
        pygame.display.update()
        clock.tick(60)
    
def avvistamentoAlbatros(personaggi: list, armi: float, carne: float) -> tuple:
    global albatro_avvistato, albatro_ucciso
    
    if albatro_avvistato >= 3:
        return armi, carne
    
    albatro_avvistato += 1
    
    if armi <= 0:
        return armi, carne
    
    scelta = input("Vuoi tentare di abbattere l'albatro? (s/n): ").strip().lower()
    if scelta != "s":
        return armi, carne
    
    tentativi = int(min(armi, len(personaggi)))
    armi_usate = tentativi
    armi -= tentativi
    
    abbattuto = any(random.random() < 0.5 for _ in range(tentativi))
    
    if abbattuto:
        carne += random.randint(10, 15)
        albatro_ucciso = True
        print(f"Albatro abbattuto! Carne +10/15 kg. Armi usate: {armi_usate}")
    
    return armi, carne

def avvistamentoScialuppa(personaggi: list, armi: float, stoffe: float, sale: float, coltelli: float, diamanti: float) -> tuple:
    RUOLI = ["cuoco", "navigatore", "medico", "meccanico", "marinaio", "bardo", "tesoriere"]
    
    scelta = input("Vuoi salvare i 4 naufraghi? (s/n): ").strip().lower()
    if scelta != "s":
        return personaggi, armi, stoffe, sale, coltelli, diamanti
    
    for _ in range(4):
        nuovo_membro = {
            "ruolo": random.choice(RUOLI),
            "morale": random.randint(25, 75),
            "pagato": False
        }
        personaggi.append(nuovo_membro)
    
    guadagno = random.randint(10, 20)
    armi += guadagno
    stoffe += guadagno
    sale += guadagno
    coltelli += guadagno
    diamanti += guadagno
    
    print(f"Naufraghi salvati: +4 membri. Merci: +{guadagno} di ogni tipo.")
    
    return personaggi, armi, stoffe, sale, coltelli, diamanti

def epidemia(personaggi: list, medicinali: float) -> tuple:
    medici = [p for p in personaggi if p.get("ruolo") == "medico"]
    non_medici = [p for p in personaggi if p.get("ruolo") != "medico"]
    
    malati = [p for p in non_medici if random.random() < 0.7]
    curati = []
    morti = []
    
    for malato in malati:
        if medici and medicinali >= 1:
            medicinali -= 1
            curati.append(malato)
        else:
            morti.append(malato)
            personaggi.remove(malato)
    
    print(f"Epidemia: {len(malati)} malati, {len(curati)} curati, {len(morti)} morti. Medicinali rimasti: {medicinali}")
    
    return personaggi, medicinali

def attaccoPirata(personaggi: list, armi: float) -> tuple:
    num_pirati = random.randint(3, 10)
    num_difensori = int(min(armi, len(personaggi)))
    armi_usate = num_difensori
    armi -= num_difensori
    uomini_persi = min(num_pirati - num_difensori, len(personaggi))
    if uomini_persi > 0:
        for _ in range(uomini_persi):
            if personaggi:
                personaggi.remove(random.choice(personaggi))
        print(f"Uomini persi: {uomini_persi}")
    else:
        print("Vittoria! Nessun uomo perso.")
    
    return personaggi, armi

def danniAlTimone(settimane_rimaste: int, personaggi: list) -> int:
    ha_meccanico = any(p.get("ruolo") == "meccanico" for p in personaggi)
    if ha_meccanico:
        ritardo = 1
        print("Meccanico presente: riparazione rapida. Viaggio +1 settimana.")
    else:
        ritardo = random.randint(2, 4)
        print("Nessun meccanico: riparazione difficile. Viaggio +{} settimane.".format(ritardo))
    return settimane_rimaste + ritardo

def animazione_divento(schermo, clock, sprites_vento, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=None, favorevole=True):
    inizio = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - inizio < durata_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        frame = prendi_frame(sprites_vento["vento"], 120)
        frame_scalato = pygame.transform.scale(frame, (int(160 * MOD), int(110 * MOD)))
    
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
             disegna_animazione(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        if favorevole:
            schermo.blit(frame_scalato, ((WIDTH_S // 2)-100*MOD, (HEIGHT_S // 2)- 200*MOD))
            Drawtext(schermo, ["venti favorevoli!"], int((HEIGHT_S // 2)- HEIGHT_S//3), FONT_BOLD, (255, 255, 255), 40*MOD)
        else:
            schermo.blit(frame_scalato, ((WIDTH_S // 2)-100*MOD, (HEIGHT_S // 2)- 200*MOD))
            Drawtext(schermo, ["venti contrari!"], int((HEIGHT_S // 2)- HEIGHT_S//3), FONT_BOLD, (255, 255, 255), 40*MOD)
        

        pygame.display.update()
        clock.tick(60)
def rafficheDiVento(settimane_rimaste: int, personaggi: list) -> int:
    ha_navigatore = any(p.get("ruolo") == "navigatore" for p in personaggi)
    if ha_navigatore:
        ritardo = 1
        print("Navigatore presente: rotta corretta. Viaggio +1 settimana.")
    else:
        ritardo = random.randint(2, 4)
        print("Nessun navigatore: persi in mare. Viaggio +{} settimane.".format(ritardo))
    return settimane_rimaste + ritardo

def animazione_isola(schermo, clock, sprites_isola, WIDTH_S, HEIGHT_S, durata_ms=6000, FONT_BOLD=FONT_BOLD):
    frame = prendi_frame(sprites_isola["isola"], 500)
    frame_scalato = pygame.transform.scale(frame, (WIDTH_S, HEIGHT_S))
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        frame = prendi_frame(sprites_isola["isola"], 500)
        frame_scalato = pygame.transform.scale(frame, (WIDTH_S, HEIGHT_S))
        schermo.blit(frame_scalato, (0, 0))
        Drawtext(schermo, ["Intravedi un isola Misteriosa..."], int((HEIGHT_S // 2)- HEIGHT_S//3), FONT_BOLD, (255, 255, 255), 40*MOD)
        pygame.display.update()
        clock.tick(60)
        
def avvistamentoIsola(personaggi: list, armi: float, stoffe: float, sale: float, coltelli: float, diamanti: float, settimane_rimaste: int) -> tuple:
    global albatro_avvistato, albatro_ucciso
    
    scelta = input("Vuoi approdare sull'isola? (s/n): ").strip().lower()
    if scelta != "s":
        return personaggi, armi, stoffe, sale, coltelli, diamanti, settimane_rimaste
    
    settimane_rimaste += random.randint(1, 2)
    abitata = random.random() < 0.5
    
    if not abitata:
        print("Isola disabitata. Nessun beneficio.")
        return personaggi, armi, stoffe, sale, coltelli, diamanti, settimane_rimaste
    
    ostili = random.random() < 0.5
    if ostili:
        print("Isola abitata ma isolani ostili! Nausea.")
        return personaggi, armi, stoffe, sale, coltelli, diamanti, settimane_rimaste
    
    if albatro_avvistato > 0 and not albatro_ucciso:
        guadagno = random.randint(20, 40)
        print("Albatro avvistato (non ucciso): bonus fortuna! +{} unità.".format(guadagno))
    else:
        guadagno = random.randint(5, 20)
        print("Isola amichevole: +{} unità di ogni merce.".format(guadagno))
    
    armi += guadagno
    stoffe += guadagno
    sale += guadagno
    coltelli += guadagno
    diamanti += guadagno
    
    return personaggi, armi, stoffe, sale, coltelli, diamanti, settimane_rimaste

def nessunoImprevisto():
    pass

def controllo_scorte(scorte: dict, num_membri: int, settimane_rimaste: int) -> dict:
    delta_morale = 0
    razioni_attuali = scorte.get("razione_corrente", 1.0)
    
    for tipo in ["verdura", "frutta", "carne", "acqua"]:
        quantita = scorte.get(tipo, 0)
        consumo_base = {"verdura": 0.5, "frutta": 1.0, "carne": 1.0, "acqua": 0.5}[tipo]
        
        consumo_settimanale = num_membri * consumo_base * razioni_attuali
        consumo_totale = consumo_settimanale * settimane_rimaste
        
        if quantita < consumo_totale:
            print(f"ATTENZIONE: {tipo} insufficiente per le settimane rimanenti!")
            scelta = input(f"Vuoi dimezzare la razione di {tipo}? (s/n): ").strip().lower()
            if scelta == "s":
                scorte["razione_corrente"] = razioni_attuali * 0.5
                delta_morale -= 5
                print(f"Razione {tipo} dimezzata. Morale -5.")
        
        if quantita >= consumo_totale * 2:
            print(f"ECCELLENTE: {tipo} sufficiente per il doppio delle settimane!")
            scelta = input(f"Vuoi raddoppiare la razione di {tipo}? (s/n): ").strip().lower()
            if scelta == "s":
                scorte["razione_corrente"] = razioni_attuali * 2
                delta_morale += 5
                print(f"Razione {tipo} raddoppiata. Morale +5.")
        
        if quantita <= 0:
            delta_morale -= 10
            print(f"{tipo} esaurito! Morale -10.")
    
    scorte["delta_morale"] = delta_morale
    return scorte

def calcolo_ammutinamento(scorte: dict, personaggi: list, settimane_passate: int, albatro_ucciso: bool, albatro_avvistato: int) -> int:
    punti = 0
    
    if scorte.get("razione_corrente", 1.0) < 1.0:
        punti += 30
        print("+30: Razioni cibo ridotte")
    
    ha_cuoco = any(p.get("ruolo") == "cuoco" for p in personaggi)
    if not ha_cuoco:
        punti += 30
        print("+30: Nessun cuoco a bordo")
    
    if albatro_avvistato > 0 and albatro_ucciso:
        punti += 30
        print("+30: Presagio di sfiga (albatro ucciso)")
    
    if albatro_avvistato > 0 and not albatro_ucciso:
        punti -= 20
        print("-20: Ottimismo (albatro avvistato, non ucciso)")
    
    if len(personaggi) > 12:
        punti += 30
        print("+30: Nave troppo affollata")
    
    if settimane_passate > 8:
        punti += (settimane_passate - 8) * 10
        print("+{}: Viaggio troppo lungo".format((settimane_passate - 8) * 10))
    elif settimane_passate < 8:
        punti -= (8 - settimane_passate) * 10
        print("-{}: Viaggio più breve del previsto".format((8 - settimane_passate) * 10))
    
    print("Punteggio ammutinamento totale: {}".format(punti))
    return punti

def aggiorna_morale(personaggi: list, delta_morale: int) -> list:
    for p in personaggi:
        p["morale"] = p.get("morale", 100) + delta_morale
        if p["morale"] <= 0:
            print("{} è morto (morale 0)!".format(p.get("ruolo", "membro")))
            personaggi.remove(p)
    return personaggi

def scelta_evento(EVENTI: list):
    evento = random.choice(EVENTI)
    return evento

def infestazioneRatti(list):
    pass