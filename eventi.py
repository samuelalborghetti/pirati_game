import random
import copy
import pygame
from utility import MOD, HEIGHT, WIDTH, font_numeri, title_font, info_font, BIANCO
 
pygame.init()
 
SOGLIA_EPIDEMIA            = 0.7
MALUS_MORALE_SCORTE_ESAURITE  = 10
MALUS_MORALE_DIMEZZA_RAZIONI  = 5
BONUS_MORALE_RADDOPPIA_RAZIONI = 5
MARINAI_MAX                = 12
SOGLIA_MORALE_BASSO        = 30
 
PUNTI_RAZIONI_RIDOTTE  = 30
PUNTI_NO_CUOCO         = 30
PUNTI_ALBATRO_UCCISO   = 30
PUNTI_ALBATRO_RISPARMIATO = -20
PUNTI_NAVE_AFFOLLATA   = 30
PUNTI_SETTIMANA_EXTRA  = 10
SOGLIA_AMMUTINAMENTO   = 100
 
def leggi_nome(personaggio):
    return personaggio["info"]["name"]
 
def leggi_ruolo(personaggio):
    return personaggio["info"]["ruolo"]
 
def e_vivo(personaggio):
    return personaggio["stats"]["alive"]
 
def uccidi(personaggio):
    personaggio["stats"]["alive"] = False
 
def leggi_tipo_equip(oggetto):
    return oggetto["stats"]["tipo"]
 
def leggi_nome_equip(oggetto):
    return oggetto["info"]["name"]
 
def leggi_saturazione(cibo):
    return cibo["stats"]["saturazione"]
 
def scrivi_saturazione(cibo, valore):
    cibo["stats"]["saturazione"] = max(0.0, valore)
 
def conta_membri_vivi(personaggi):
    contatore = 0
    for p in personaggi:
        if e_vivo(p):
            contatore += 1
    return contatore
 
def presenza_ruolo(personaggi, ruolo):
    for p in personaggi:
        if e_vivo(p) and leggi_ruolo(p) == ruolo:
            return True
    return False
 
def trova_cibo_per_nome(lista_cibo, nome):
    for c in lista_cibo:
        if c["info"]["name"] == nome:
            return c
    return None
 
def conta_oggetti_per_tipo(lista_equip, tipo):
    contatore = 0
    for oggetto in lista_equip:
        if leggi_tipo_equip(oggetto) == tipo:
            contatore += 1
    return contatore
 
def conta_oggetti_per_nome(lista_equip, nome):
    contatore = 0
    for oggetto in lista_equip:
        if leggi_nome_equip(oggetto) == nome:
            contatore += 1
    return contatore
 
def rimuovi_n_oggetti_per_tipo(lista_equip, tipo, quanti):
    rimossi = 0
    indice = 0
    while indice < len(lista_equip) and rimossi < quanti:
        if leggi_tipo_equip(lista_equip[indice]) == tipo:
            lista_equip.pop(indice)
            rimossi += 1
        else:
            indice += 1
    return rimossi
 
def rimuovi_n_oggetti_per_nome(lista_equip, nome, quanti):
    rimossi = 0
    indice = 0
    while indice < len(lista_equip) and rimossi < quanti:
        if leggi_nome_equip(lista_equip[indice]) == nome:
            lista_equip.pop(indice)
            rimossi += 1
        else:
            indice += 1
    return rimossi
 
def trova_template_merce(lista_merci, nome):
    for merce in lista_merci:
        if merce["info"]["name"] == nome:
            return merce
    return None
 
 
def disegna_schermata_nera(schermo, titolo, domanda, motivo, scelte, font_titolo=title_font, font_domanda=font_numeri, font_scelte=font_numeri, font_motivo=info_font, colore_testo=BIANCO, colore_sfondo=(0, 0, 0), pos_titolo=None, pos_domanda=None, pos_scelte=None, spazio_scelte=50, mouse=None, click=False):
 
    if pos_titolo == None:
        pos_titolo = (WIDTH // 2, HEIGHT // 4)
    if pos_domanda == None:
        pos_domanda = (WIDTH // 2, HEIGHT // 2)
    if pos_scelte == None:
        pos_scelte = (WIDTH // 2, HEIGHT // 2 + int(100 * MOD))
 
    schermo.fill(colore_sfondo)
 
    surf_titolo = font_titolo.render(titolo, True, colore_testo)
    schermo.blit(surf_titolo, surf_titolo.get_rect(center=pos_titolo))
 
    surf_domanda = font_domanda.render(domanda, True, colore_testo)
    schermo.blit(surf_domanda, surf_domanda.get_rect(center=pos_domanda))
 
    surf_motivo = font_motivo.render(motivo, True, colore_testo)
    schermo.blit(surf_motivo, surf_motivo.get_rect(center=(pos_domanda[0], pos_domanda[1] + int(50 * MOD))))
 
    scelta_cliccata = None
    for i in range(len(scelte)):
        surf_scelta = font_scelte.render(scelte[i], True, colore_testo)
        rect_scelta = surf_scelta.get_rect(center=(pos_scelte[0], pos_scelte[1] + i * int(spazio_scelte * MOD)))
        schermo.blit(surf_scelta, rect_scelta)
        if mouse is not None and click and rect_scelta.collidepoint(mouse):
            scelta_cliccata = scelte[i]
 
    return scelta_cliccata
def disegna_schermata_nera_riepilogo_settimana(pers, razioni_attuali, consumi_attuali, merci_attuali):
    schermo = pygame.display.get_surface()
    continua = True
    
    while continua:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                continua = False 

        schermo.fill((0, 0, 0))
        
        y_cambia = 50 * MOD
        
        for p in pers:
            nome = p["info"]["name"]
            ruolo = p["info"]["ruolo"]
            if e_vivo(p):
                colore = (255, 255, 255)
                testo = f"{nome} ({ruolo}) - Morale: {p['stats']['morale']}"
            else:
                colore = (255, 0, 0)
                testo = f"{nome} ({ruolo}) - MORTO"
            
            img = info_font.render(testo, True, colore)
            schermo.blit(img, (50 * MOD, y_cambia))
            y_cambia += 30 * MOD

        y_cambia += 40 * MOD
        
        for tipo in ["verdura", "frutta", "carne", "acqua"]:
            testo_merce = f"{tipo.capitalize()}: {razioni_attuali[tipo]} razioni (Consumo: {consumi_attuali[tipo]}/sett)"
            img = info_font.render(testo_merce, True, (200, 200, 200))
            schermo.blit(img, (50 * MOD, y_cambia))
            y_cambia += 30 * MOD
            
        y_cambia += 40 * MOD
            
        testo_merci = f"Medicinali: {merci_attuali['medicinali']} | Armi: {merci_attuali['armi']} | Totale: {merci_attuali['totale']}"
        txt_merci = info_font.render(testo_merci, True, (255, 215, 0))
        schermo.blit(txt_merci, (50 * MOD, y_cambia))

        y_cambia += 60 * MOD
        msg_uscita = info_font.render("Premi un tasto per continuare...", True, (100, 100, 100))
        schermo.blit(msg_uscita, (50 * MOD, y_cambia))

        pygame.display.flip()
    
 
 
def mostra_messaggio_evento(titolo, domanda, motivo, scelte=None):
    if scelte is None:
        scelte = ["Continua"]
 
 
    schermo = pygame.display.get_surface()
 
    while True:
        pos_mouse = pygame.mouse.get_pos()
        click = False
 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                click = True
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return scelte[0]
 
        scelta = disegna_schermata_nera( schermo=schermo, titolo=titolo, domanda=domanda, motivo=motivo, scelte=scelte, mouse=pos_mouse, click=click)
        if scelta != None:
            return scelta
 
        pygame.display.flip()
 
def calcola_perdita_scorta(quantita_totale, nome_cibo):
    quota = random.choice([2, 3 ,4, 5])
    perdita = quantita_totale * (1.0 / quota)
    if perdita <= 0:
        return 0, quota
    return perdita, quota
 
def mostra_perdita_scorta(nome_cibo, quota, perdita):
    mostra_messaggio_evento(
        titolo=nome_cibo.upper() + " IN MARE!",
        domanda="Una violenta tempesta ha colpito la nave!",
        motivo="1/" + str(quota) + " delle scorte di " + nome_cibo + " e' finita in mare."
    )
 
def rimuovi_oggetti_per_quota(lista_equip, tipo_o_nome, cerca_per_tipo, nome_evento):
    """Rimuove 1/quota degli oggetti. Restituisce la lista modificata."""
    if cerca_per_tipo:
        n_totale = conta_oggetti_per_tipo(lista_equip, tipo_o_nome)
    else:
        n_totale = conta_oggetti_per_nome(lista_equip, tipo_o_nome)
 
    if n_totale == 0:
        mostra_messaggio_evento(
            titolo=nome_evento,
            domanda="Non abbiamo " + tipo_o_nome + " a bordo.",
            motivo="Nessun danno subito."
        )
        return lista_equip
 
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_totale * (1.0 / quota))
 
    if cerca_per_tipo:
        rimuovi_n_oggetti_per_tipo(lista_equip, tipo_o_nome, perdita)
    else:
        rimuovi_n_oggetti_per_nome(lista_equip, tipo_o_nome, perdita)
 
    return lista_equip, quota, perdita
 
def aggiungi_scorta(quantita_attuale):
    """Aggiunge tra 11 e 20 unita. Restituisce nuova quantita e quantita aggiunta."""
    guadagno = random.randint(11, 20)
    return quantita_attuale + guadagno, guadagno
 
def mostra_aggiunta_settimane(ha_specialista, nome_ruolo, ritardo, titolo, domanda):
    if ha_specialista:
        motivo = "Il " + nome_ruolo + " risolve in fretta: +" + str(ritardo) + " settimane."
    else:
        motivo = "Senza " + nome_ruolo + " ci vuole piu tempo: +" + str(ritardo) + " settimane."
    mostra_messaggio_evento(titolo=titolo, domanda=domanda, motivo=motivo)
 
def evento_uomo_in_mare(personaggi):
    vivi = []
    for p in personaggi:
        if e_vivo(p):
            vivi.append(p)
 
    if len(vivi) == 0:
        return personaggi, None
 
    vittima = random.choice(vivi)
    uccidi(vittima)
    nome_vittima = leggi_nome(vittima)
 
    mostra_messaggio_evento(
        titolo="UOMO IN MARE!",
        domanda=nome_vittima + " e' caduto in mare!",
        motivo="Speriamo che sapesse nuotare..."
    )
 
    return personaggi, nome_vittima
 
 
def evento_verdura_in_mare(verdura_totale):
    perdita, quota = calcola_perdita_scorta(verdura_totale, "verdura")
    mostra_perdita_scorta("verdura", quota, perdita)
    return perdita
 
def evento_frutta_in_mare(frutta_totale):
    perdita, quota = calcola_perdita_scorta(frutta_totale, "frutta")
    mostra_perdita_scorta("frutta", quota, perdita)
    return perdita
 
def evento_carne_in_mare(carne_totale):
    perdita, quota = calcola_perdita_scorta(carne_totale, "carne")
    mostra_perdita_scorta("carne", quota, perdita)
    return perdita
 
def evento_acqua_in_mare(acqua_totale):
    perdita, quota = calcola_perdita_scorta(acqua_totale, "acqua")
    mostra_perdita_scorta("acqua", quota, perdita)
    return perdita
 
 
def evento_pesca_miracolosa(carne_totale):
    nuova_carne, guadagno = aggiungi_scorta(carne_totale)
    mostra_messaggio_evento(
        titolo="PESCA MIRACOLOSA!",
        domanda="Una giornata di pesca fortunatissima!",
        motivo="Le scorte di carne sono aumentate di " + str(guadagno) + " kg."
    )
    return nuova_carne
 
def evento_tempesta_miracolosa(acqua_totale):
    nuova_acqua, guadagno = aggiungi_scorta(acqua_totale)
    mostra_messaggio_evento(
        titolo="TEMPESTA MIRACOLOSA!",
        domanda="Una tempesta ha portato acqua piovana abbondante!",
        motivo="Le scorte di acqua sono aumentate di " + str(guadagno) + " barili."
    )
    return nuova_acqua
 
def evento_venti_favorevoli(settimane_totali, bonus):
    nuove_settimane = max(0, settimane_totali - 1)
    bonus_morale = bonus + random.randint (5,15)
    mostra_messaggio_evento(
        titolo="VENTI FAVOREVOLI!",
        domanda="Il vento e' cambiato in nostro favore!",
        motivo="Viaggio di 1 settimana piu breve. Morale +" + str(bonus_morale) + " da ora in poi."
    )
 
    return nuove_settimane, bonus_morale
 
 
def evento_cattivo_tempo(lista_equip):
    n_medicinali = conta_oggetti_per_tipo(lista_equip, "medicinale")
 
    if n_medicinali == 0:
        mostra_messaggio_evento(
            titolo="CATTIVO TEMPO!",
            domanda="Il tempo e' peggiorato bruscamente!",
            motivo="Per fortuna non avevamo medicinali da poter perdere."
        )
        return lista_equip
 
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_medicinali * (1.0 / quota))
    rimuovi_n_oggetti_per_tipo(lista_equip, "medicinale", perdita)
 
    mostra_messaggio_evento(
        titolo="CATTIVO TEMPO!",
        domanda="I sobbalzi della nave hanno fatto danni in stiva!",
        motivo="Si sono rotte " + str(perdita) + " bottiglie di medicinale (1/" + str(quota) + ")."
    )
    return lista_equip
 
 
def evento_ondata(lista_equip):
    n_armi = conta_oggetti_per_tipo(lista_equip, "arma")
 
    if n_armi == 0:
        mostra_messaggio_evento(
            titolo="ONDATA!",
            domanda="Un'onda improvvisa ha colpito la nave!",
            motivo="Per fortuna non avevamo armi che potessero rovesciarsi."
        )
        return lista_equip
 
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_armi * (1.0 / quota))
    rimuovi_n_oggetti_per_tipo(lista_equip, "arma", perdita)
 
    mostra_messaggio_evento(
        titolo="ONDATA!",
        domanda="Un'onda improvvisa ha colpito la nave!",
        motivo="Si sono rotte " + str(perdita) + " armi a causa dell'onda (1/" + str(quota) + ")."
    )
    return lista_equip
 
 
def evento_infestazione_ratti(lista_equip):
    n_stoffe = conta_oggetti_per_nome(lista_equip, "stoffa")
 
    if n_stoffe == 0:
        mostra_messaggio_evento(
            titolo="INFESTAZIONE DI RATTI!",
            domanda="I ratti hanno invaso la stiva!",
            motivo="Per fortuna non c'erano stoffe da danneggiare."
        )
        return lista_equip
 
    quota = random.choice([2, 3, 4, 5])
    perdita = int(n_stoffe * (1.0 / quota))
    rimuovi_n_oggetti_per_nome(lista_equip, "stoffa", perdita)
 
    mostra_messaggio_evento(
        titolo="INFESTAZIONE DI RATTI!",
        domanda="I ratti hanno fatto a brandelli le stoffe in stiva!",
        motivo="Rovinate " + str(perdita) + " stoffe (1/" + str(quota) + ")."
    )
    return lista_equip
 
 
def evento_avvistamento_albatro(personaggi, lista_equip, carne_totale, albatro_avvistato, albatro_ucciso):
    if albatro_avvistato >= 3:
        return carne_totale, albatro_avvistato, albatro_ucciso
 
    albatro_avvistato += 1
 
    armi_disponibili = []
    for oggetto in lista_equip:
        if leggi_tipo_equip(oggetto) == "arma":
            armi_disponibili.append(oggetto)
 
    numero_armi   = len(armi_disponibili)
    numero_uomini = conta_membri_vivi(personaggi)
    numero_colpi  = min(numero_armi, numero_uomini, 6)
 
    if numero_armi == 0 or numero_colpi == 0:
        mostra_messaggio_evento(
            titolo="ALBATRO AVVISTATO",
            domanda="Un maestoso albatro ci sorvola lentamente.",
            motivo="Non abbiamo armi pronte, possiamo solo ammirarlo volare via."
        )
        fortuna_dellalbatro = True
        return carne_totale, albatro_avvistato, albatro_ucciso
 
    scelta = mostra_messaggio_evento(
        titolo="ALBATRO AVVISTATO",
        domanda="Un albatro ci sorvola. Ucciderlo porta sfortuna...",
        motivo="...ma la sua carne ci farebbe comodo. Cosa facciamo?",
        scelte=["Spara", "Ignora"]
    )
 
    if scelta == "Ignora":
        mostra_messaggio_evento(
            titolo="ALBATRO RISPARMIATO",
            domanda="L'uccello si allontana verso l'orizzonte.",
            motivo="Forse il mare ci ricompensera' per avergli risparmiato la vita."
        )
        fortuna_dellalbatro = True
        return carne_totale, albatro_avvistato, albatro_ucciso
 
    fortuna_dellalbatro = False
    abbattuto = False
    for tentativo in range(numero_colpi):
        if random.randint(0, 1) == 0:
            abbattuto = True
            break
 
    for i in range(numero_colpi):
        if len(armi_disponibili) > 0:
            arma_usata = armi_disponibili.pop()
            if arma_usata in lista_equip:
                lista_equip.remove(arma_usata)
 
    if abbattuto:
        guadagno_carne = random.randint(10, 15)
        carne_totale  += guadagno_carne
        albatro_ucciso = True
        mostra_messaggio_evento(
            titolo="ALBATRO ABBATTUTO!",
            domanda="Un colpo preciso! L'albatro cade in mare.",
            motivo="Recuperati " + str(guadagno_carne) + " kg di carne. Persi " + str(numero_colpi) + " fucili."
        )
    else:
        albatro_ucciso = False
        mostra_messaggio_evento(
            titolo="COLPO MANCATO",
            domanda="L'albatro se n'e' andato illeso.",
            motivo="Abbiamo sprecato " + str(numero_colpi) + " fucili sparando a vuoto."
        )
 
    return carne_totale, albatro_avvistato, albatro_ucciso
 
 
def evento_scialuppa(personaggi, lista_equip, tutti_i_personaggi, tutte_le_merci):
    spazio_occupato   = conta_membri_vivi(personaggi)
    spazio_disponibile = 16 - spazio_occupato
 
    if spazio_disponibile <= 0:
        mostra_messaggio_evento(
            titolo="AVVISTAMENTO SCIALUPPA",
            domanda="Abbiamo avvistato 4 naufraghi alla deriva...",
            motivo="...ma la nave e' gia' al completo (16 membri). Dobbiamo tirar dritto."
        )
        return personaggi, lista_equip
 
    scelta = mostra_messaggio_evento(
        titolo="AVVISTAMENTO SCIALUPPA",
        domanda="Ci sono 4 naufraghi alla deriva con una cassa.",
        motivo="Li portiamo a bordo? Lavoreranno gratis. (Spazio libero: " + str(spazio_disponibile) + ")",
        scelte=["Salva i naufraghi", "Ignorali"]
    )
 
    if scelta == "Ignorali":
        mostra_messaggio_evento(
            titolo="NAUFRAGHI ABBANDONATI",
            domanda="Abbiamo tirato dritto senza fermarci.",
            motivo="Il mare e' crudele, ma le nostre scorte sono preziose."
        )
        return personaggi, lista_equip
 
    naufraghi_da_salvare = min(4, spazio_disponibile)
    ruoli_possibili = ["capitano", "cuoco", "navigatore", "medico",
                       "marinaio", "meccanico", "bardo", "tesoriere"]
 
    for i in range(naufraghi_da_salvare):
        ruolo_estratto = random.choice(ruoli_possibili)
 
        modello = None
        for p in tutti_i_personaggi:
            if p["info"]["ruolo"] == ruolo_estratto:
                modello = p
                break
 
        if modello is not None:
            nuovo_membro = {
                "stats":   copy.deepcopy(modello["stats"]),
                "pos":     copy.deepcopy(modello["pos"]),
                "sprites": modello["sprites"],
                "info":    copy.deepcopy(modello["info"]),
                "morale":  random.randint(25, 75)
            }
            nuovo_membro["stats"]["cost"]  = 0
            nuovo_membro["stats"]["alive"] = True
            nuovo_membro["info"]["name"]   = "Naufrago"
            nuovo_membro["info"]["descrizione"] = "Naufrago salvato in mare - ruolo: " + ruolo_estratto
 
            from utility import WIDTH, MOD as MOD_U
            nuovo_membro["pos"]["main"]["x_attuale"] = random.randint(int(400 * MOD_U), int(WIDTH - 420 * MOD_U))
            nuovo_membro["pos"]["main"]["y_attuale"] = random.randint(int(430 * MOD_U), int(470 * MOD_U))
 
            personaggi.append(nuovo_membro)
 
    # Contenuto della cassa: +10/20 pezzi per ogni tipo di merce
    tipi_nella_cassa = ["medicinale", "armi", "sale", "coltelli", "stoffa", "diamanti"]
    oggetti_trovati  = 0
 
    for tipo in tipi_nella_cassa:
        quantita_trovata = random.randint(10, 20)
        template = trova_template_merce(tutte_le_merci, tipo)
        if template is not None:
            for j in range(quantita_trovata):
                nuovo_oggetto = {
                    "stats":   copy.deepcopy(template["stats"]),
                    "info":    copy.deepcopy(template["info"]),
                    "sprites": template["sprites"] if "sprites" in template else {}
                }
                lista_equip.append(nuovo_oggetto)
                oggetti_trovati += 1
 
    if naufraghi_da_salvare < 4:
        testo_uomini = "Salvati " + str(naufraghi_da_salvare) + " uomini (nave ora piena)."
    else:
        testo_uomini = "Accolti a bordo tutti e 4 gli uomini."
 
    mostra_messaggio_evento(
        titolo="SALVATAGGIO COMPLETATO",
        domanda="Abbiamo svuotato la loro cassa.",
        motivo=testo_uomini + " Trovati " + str(oggetti_trovati) + " oggetti utili."
    )
 
    return personaggi, lista_equip
 
 
def evento_epidemia(personaggi, lista_equip):
    medicinali_disponibili = []
    for oggetto in lista_equip:
        if leggi_tipo_equip(oggetto) == "medicinale":
            medicinali_disponibili.append(oggetto)
 
    numero_medicinali = len(medicinali_disponibili)
    ha_medico         = presenza_ruolo(personaggi, "medico")
 
    malati      = 0
    curati      = 0
    morti       = 0
    usati       = 0
 
    for p in personaggi:
        if e_vivo(p) and leggi_ruolo(p) != "medico":
            if random.randint(1, 10) <= 7:
                malati += 1
                if ha_medico and numero_medicinali > 0:
                    curati += 1
                    usati  += 1
                    numero_medicinali -= 1
                    medicinale_usato = medicinali_disponibili.pop()
                    lista_equip.remove(medicinale_usato)
                else:
                    uccidi(p)
                    morti += 1
 
    if malati == 0:
        mostra_messaggio_evento(
            titolo="NESSUN MALATO!",
            domanda="Un'epidemia ha sfiorato la nave...",
            motivo="...per fortuna l'equipaggio gode di ottima salute. Nessun contagiato."
        )
    elif morti > 0:
        if not ha_medico:
            causa = "Senza un medico a bordo, tutti i malati sono morti."
        else:
            causa = "I medicinali non erano abbastanza per curarli tutti."
        mostra_messaggio_evento(
            titolo="EPIDEMIA DEVASTANTE!",
            domanda=str(malati) + " membri si sono ammalati.",
            motivo="Curati: " + str(curati) + "  Morti: " + str(morti) + ".  " + causa
        )
    else:
        mostra_messaggio_evento(
            titolo="EPIDEMIA SOTTO CONTROLLO",
            domanda=str(malati) + " membri si sono ammalati.",
            motivo="Il medico li ha curati tutti usando " + str(usati) + " medicinali."
        )
 
    return personaggi, lista_equip
 
 
def evento_attacco_pirata(personaggi, lista_equip):
    numero_pirati   = random.randint(3, 10)
    numero_armi     = conta_oggetti_per_tipo(lista_equip, "arma")
    numero_membri   = conta_membri_vivi(personaggi)
    numero_difensori = min(numero_armi, numero_membri)
 
    perdite = max(0, numero_pirati - numero_difensori)
    perdite = min(perdite, numero_membri)
    vittoria = perdite <= 0
 
    if perdite > 0:
        vivi = []
        for p in personaggi:
            if e_vivo(p):
                vivi.append(p)
        random.shuffle(vivi)
        for i in range(min(perdite, len(vivi))):
            uccidi(vivi[i])
 
    # Le armi vengono consumate nel combattimento
    rimuovi_n_oggetti_per_tipo(lista_equip, "arma", numero_difensori)
 
    if vittoria:
        mostra_messaggio_evento(
            titolo="ATTACCO RESPINTO!",
            domanda="I pirati erano " + str(numero_pirati) + ", noi " + str(numero_difensori) + " difensori.",
            motivo="Vittoria! Abbiamo usato " + str(numero_difensori) + " armi nel combattimento."
        )
    else:
        mostra_messaggio_evento(
            titolo="ATTACCO PIRATA!",
            domanda="I pirati erano " + str(numero_pirati) + ", noi solo " + str(numero_difensori) + " difensori.",
            motivo="Persi " + str(perdite) + " uomini. Usate " + str(numero_difensori) + " armi."
        )
 
    return personaggi, lista_equip
 
 
def evento_danni_timone(settimane_totali, personaggi):
    ha_meccanico = presenza_ruolo(personaggi, "meccanico")
    if ha_meccanico:
        ritardo = 1
    else:
        ritardo = random.randint(2, 4)
 
    mostra_aggiunta_settimane(
        ha_specialista=ha_meccanico,
        nome_ruolo="meccanico",
        ritardo=ritardo,
        titolo="DANNI AL TIMONE!",
        domanda="Un urto con uno scoglio ha danneggiato il timone."
    )
 
    return settimane_totali + ritardo
 
 
def evento_raffiche_vento(settimane_totali, personaggi):
    ha_navigatore = presenza_ruolo(personaggi, "navigatore")
    if ha_navigatore:
        ritardo = 1
    else:
        ritardo = random.randint(2, 4)
 
    mostra_aggiunta_settimane(
        ha_specialista=ha_navigatore,
        nome_ruolo="navigatore",
        ritardo=ritardo,
        titolo="RAFFICHE DI VENTO!",
        domanda="Forti raffiche ci hanno allontanato dalla rotta."
    )
 
    return settimane_totali + ritardo
 
 
def evento_avvistamento_isola(lista_equip, n_medicinali, settimane_totali,
                               albatro_avvistato, albatro_ucciso, tutte_le_merci):
    scelta = mostra_messaggio_evento(
        titolo="AVVISTAMENTO ISOLA!",
        domanda="Intravediamo un'isola misteriosa all'orizzonte.",
        motivo="Vogliamo approdare per un'ispezione? (+1 o +2 settimane)",
        scelte=["Approda", "Prosegui"]
    )
 
    if scelta == "Prosegui":
        mostra_messaggio_evento(
            titolo="ISOLA IGNORATA",
            domanda="Proseguiamo la rotta senza fermarci.",
            motivo="Chissa' cosa c'era su quell'isola..."
        )
        return settimane_totali, n_medicinali
 
    settimane_aggiunte = random.randint(1, 2)
    settimane_totali  += settimane_aggiunte
 
    # 50% isola deserta
    if random.randint(0, 1) == 0:
        mostra_messaggio_evento(
            titolo="ISOLA DESERTA",
            domanda="L'isola e' completamente disabitata.",
            motivo="Niente da fare qui. Viaggio +" + str(settimane_aggiunte) + " settimane."
        )
        return settimane_totali, n_medicinali
 
    # 50% degli abitati: isolani ostili
    if random.randint(0, 1) == 0:
        mostra_messaggio_evento(
            titolo="ISOLANI OSTILI!",
            domanda="Gli abitanti ci cacciano via con le armi!",
            motivo="Siamo fuggiti senza danni. Viaggio +" + str(settimane_aggiunte) + " settimane."
        )
        return settimane_totali, n_medicinali

    if albatro_avvistato > 0 and not albatro_ucciso:
        bonus = random.randint(20, 40)
        testo_bonus = "L'albatro ha portato fortuna! (+" + str(bonus) + " per tipo)."
    else:
        bonus = random.randint(5, 20)
        testo_bonus = "Gli isolani ci donano generosamente merci (+" + str(bonus) + " per tipo)."
 
    tipi_da_donare    = ["medicinale", "armi", "sale", "coltelli", "stoffa", "diamanti"]
    medicinali_aggiunti = 0
 
    for tipo in tipi_da_donare:
        template = trova_template_merce(tutte_le_merci, tipo)
        if template is not None:
            for j in range(bonus):
                sprites_template = {}
                if "sprites" in template:
                    sprites_template = template["sprites"]
                lista_equip.append({
                    "stats":   copy.deepcopy(template["stats"]),
                    "info":    copy.deepcopy(template["info"]),
                    "sprites": sprites_template
                })
            if tipo == "medicinale":
                medicinali_aggiunti = bonus
 
    mostra_messaggio_evento(
        titolo="ISOLANI AMICHEVOLI!",
        domanda="Gli isolani ci accolgono con grande calore!",
        motivo=testo_bonus + " Viaggio +" + str(settimane_aggiunte) + " settimane."
    )
 
    return settimane_totali, n_medicinali + medicinali_aggiunti
 
 
 
def gestisci_razioni_interattivo(personaggi, settimane_rimaste, razioni_attuali, consumi_base, bonus, flag_razioni_dimezzate):
 
    n_membrivivi = conta_membri_vivi(personaggi)
    consumi_totale = {}
    bonus_morale = bonus
   
    consumi_totale = {
        "verdura": consumi_base["verdura"] * n_membrivivi * settimane_rimaste,
        "frutta":  consumi_base["frutta"]  * n_membrivivi * settimane_rimaste,
        "carne":   consumi_base["carne"]   * n_membrivivi * settimane_rimaste,
        "acqua":   consumi_base["acqua"]   * n_membrivivi * settimane_rimaste
    }
    scelte = ["raddoppia consumi", "mantieni", "dimezza consumi"]
    for tipo in ["verdura", "frutta", "carne", "acqua"]:
        if razioni_attuali[tipo] > 0:
            scelta = mostra_messaggio_evento(
                titolo="GESTIONE RAZIONI",
                domanda="Razioni attuali di " + tipo + ": " + str(razioni_attuali[tipo]) + " unita' a settimana, consumi attuali: " + str(consumi_base[tipo]) + " unita' a settimana.",
                motivo="Consumo totale stimato per il resto del viaggio: " + str(consumi_totale[tipo]) + " unita'.",
                scelte=scelte
            )
            if scelta == "raddoppia consumi":
                consumi_base[tipo] *= 2
                flag_razioni_dimezzate[tipo] = False
                bonus_morale += 5
            elif scelta == "dimezza consumi":
                consumi_base[tipo] *= 0.5
                flag_razioni_dimezzate[tipo] = True
                bonus_morale -= 5
        else:
            mostra_messaggio_evento(
                titolo="RAZIONI ESAURITE",
                domanda="Le razioni di " + tipo + " sono esaurite!",
                motivo="Non possiamo consumare " + tipo + " se non ne abbiamo. Morale -5.",
                scelte=["Continua"]
            )
            bonus_morale -= 10
    razioni_scalate = {
        "verdura": razioni_attuali["verdura"] - consumi_base["verdura"] * n_membrivivi,
        "frutta":  razioni_attuali["frutta"]  - consumi_base["frutta"]  * n_membrivivi,
        "carne":   razioni_attuali["carne"]   - consumi_base["carne"]   * n_membrivivi,
        "acqua":   razioni_attuali["acqua"]   - consumi_base["acqua"]   * n_membrivivi
    }
    
    return razioni_scalate, consumi_base, bonus_morale, flag_razioni_dimezzate
 
# ─── AMMUTINAMENTO ────────────────────────────────────────────────────────────
 
def calcola_punteggio_ammutinamento( flag_razzione_dimezzate, pers, albatro_ucciso, n_settimane):
    punteggio = 0
    cuoco_presente = False
    motivi = []
    for p in pers:
        if e_vivo(p) and p["info"]["name"] == "Cuoco":
            cuoco_presente = True
    if cuoco_presente == False:
        punteggio += 30
        motivi.append("Cuoco assente: morale -30.")
    if flag_razzione_dimezzate["verdura"] or flag_razzione_dimezzate["frutta"] or flag_razzione_dimezzate["carne"] or flag_razzione_dimezzate["acqua"]:
        punteggio += 30
        motivi.append("Razioni dimezzate: morale -30.")
    if albatro_ucciso:
        punteggio += 30
        motivi.append("Albatro ucciso: morale +30.")
    elif albatro_ucciso == False:
        punteggio -= 20
        motivi.append("Albatro risparmiato: morale -20.")
    else:
        pass
    if len(pers) > 12:
        punteggio += 30
        motivi.append("Equipaggio numeroso: morale +30.")
    if n_settimane > 8:
        aggiunta = 10*(n_settimane - 8)
        punteggio = aggiunta
        motivi.append("Viaggio lungo: morale +" + str(aggiunta) + ".")
        
    elif n_settimane < 8:
        aggiunta_due = 10*(8 - n_settimane)
        punteggio -= aggiunta_due
        motivi.append("Viaggio breve: morale -" + str(aggiunta_due) + ".")
        
    if punteggio < 0:
        punteggio = 0
    elif punteggio > 100:
        punteggio = 100
    return punteggio, motivi

def costruisci_testo_motivi(motivi):
    """Concatena la lista motivi in una stringa leggibile senza usare join."""
    if len(motivi) == 0:
        return "Nessuna causa rilevata."
    testo = ""
    for i in range(len(motivi)):
        if i == 0:
            testo = motivi[0]
        else:
            testo = testo + "  |  " + motivi[i]
    return testo
 
 
def step_ammutinamento(flag_razioni_dimezzate, personaggi, albatro_ucciso, settimane_totali):
    punteggio, motivi = calcola_punteggio_ammutinamento( flag_razzione_dimezzate =flag_razioni_dimezzate, pers=personaggi, albatro_ucciso=albatro_ucciso, n_settimane=settimane_totali)
 
    testo_motivi = costruisci_testo_motivi(motivi)
 
    if punteggio >= SOGLIA_AMMUTINAMENTO:
        mostra_messaggio_evento(
            titolo="AMMUTINAMENTO!",
            domanda="Punteggio ammutinamento: " + str(punteggio) + " (soglia: " + str(SOGLIA_AMMUTINAMENTO) + ")",
            motivo="L'equipaggio abbandona la nave.  " + testo_motivi,
            scelte=["Fine partita"]
        )
        return True
 
    if punteggio >= 1:
        mostra_messaggio_evento(
            titolo="RISCHIO AMMUTINAMENTO",
            domanda="Punteggio ammutinamento: " + str(punteggio) + "/" + str(SOGLIA_AMMUTINAMENTO),
            motivo=testo_motivi,
            scelte=["Continua"]
        )
        return False
 
    mostra_messaggio_evento(
        titolo="AMMUTINAMENTO EVITATO",
        domanda="Punteggio ammutinamento: " + str(punteggio) + " (sotto soglia)",
        motivo="L'equipaggio e' ancora fedele.  " + testo_motivi,
        scelte=["Continua"]
    )
    return False
 
 
def step_ricalcolo_settimane(personaggi, settimane_totali, bonus_morale_settimane):
    numero_vivi = 0
    numero_demoralizzati = 0
    lista_per_messaggio = []
    for pers in personaggi:
        if e_vivo(pers):
            pers["stats"]["morale"] += bonus_morale_settimane
            if pers["stats"]["morale"] > 100:
                pers["stats"]["morale"] = 100
    for p in personaggi:
        if e_vivo(p):
            numero_vivi += 1
            if p["stats"]["morale"] <= 30 and p["stats"]["morale"] > 0:
                numero_demoralizzati += 1
 
    if numero_vivi > 0 and numero_demoralizzati > (numero_vivi / 2):
        settimane_totali += 1
        mostra_messaggio_evento(
            titolo="EQUIPAGGIO DEMORALIZZATO!",
            domanda=str(numero_demoralizzati) + " uomini su " + str(numero_vivi) + " hanno il morale a terra.",
            motivo="Si lavora di malumore e a rilento: il viaggio si allunga di 1 settimana.",
            scelte=["Continua"]
        )

    for personaggio in personaggi:
        if e_vivo(personaggio) and personaggio["stats"]["morale"] <= 0:
            personaggio["stats"]["alive"] = False
            lista_per_messaggio.append(personaggio["info"]["name"])
            
    if len(lista_per_messaggio) > 0:
        nomi_morti = ""
        
        for i in range(len(lista_per_messaggio)):
            nomi_morti += lista_per_messaggio[i]
            
            if i < len(lista_per_messaggio) - 1:
                nomi_morti += ", "

        mostra_messaggio_evento(
            titolo="MORTE PER MORALE ZERO",
            domanda=nomi_morti + " sono morti di disperazione.",
            motivo="Il morale a zero ha portato alla morte. Speriamo che non succeda ad altri..."
        )
    mostra_messaggio_evento(
        titolo="SETTIMANE RICALCOLATE",
        domanda="Il bonus morale ha portato a un ricalcolo delle settimane totali.",
        motivo="Settimane totali ora: " + str(settimane_totali)
    )
        
 
    return settimane_totali
 
 