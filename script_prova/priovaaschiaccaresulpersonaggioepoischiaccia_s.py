import pygame
import json

pygame.init()

pers = 1
IMPOSTAZIONI = "./dati/setting.json"
ROSSO = (255, 0, 0)
NERO  = (0, 0, 0)
BIANCO = (255, 255, 255)

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.load(file)
    file.close()
    return dati["width"], dati["height"], dati["audio"], dati["mod"]

WIDTH, HEIGHT, VOLUME, MOD = CaricaSettings(IMPOSTAZIONI)

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the see")

bg = pygame.image.load("assets/sfondi/default1.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_piccolo    = pygame.font.SysFont(None, 16)
font_zoom       = pygame.font.SysFont(None, 38)
font_istruzioni = pygame.font.SysFont(None, 20)

PERSONAGGI = [
    #--------------------------------------------------------------------------------------------capitano---------------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/capitano/idle/capitanoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png").convert_alpha() for i in range(1, 6)],
        },
        "info": {
            "name":        "Capitano",
            "descrizione": "Ormai dopo tante avventure pericolose in cui si rischia la pelle, la ha persa veramente. Ma la morte stessa ha rifiutato di tenerlo — troppo testardo anche per l'aldilà. Ora naviga senza carne, senza paura, senza niente da perdere. Il mare lo teme ancora.",
            "abilita":     "non mangia, non beve potrebe improvvisamente ridursi a poche ossa",
        },
    },
    #-------------------------------------------------------------------------------------cuoco--------------------------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/cuoco/idle/cuocoidle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png").convert_alpha() for i in range(1, 3)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
        },
        "info": {
            "name":        "Cuoco",
            "descrizione": "Un piccolo maiale che prepara piatti stellati. Menomale che non è grosso sennò li mangerebbe anche. Nessuno sa come un maiale abbia imparato a cucinare, nessuno osa chiederglielo — non quando è lui a decidere cosa finisce nel piatto e cosa finisce come piatto.",
            "abilita":     "se mangi con il cuoco a bordo le porzioni valgono doppio. Il cibo dura il doppio con metà delle scorte.",
        },
    },
    #--------------------------------------------------------------------------------------------guardone--------------------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)],
        },
        "info": {
            "name":        "Guardone",
            "descrizione": "Un piccolo occhio molto fortunato. Se dovesse tirare una freccetta centrerebbe sicuramente il centro, peccato non abbia le mani. Vede tutto — tempeste in arrivo, navi nemiche all'orizzonte, il futuro stesso. L'unico problema è che per indicare la rotta deve ammiccare nella direzione giusta e sperare che qualcuno capisca.",
            "abilita":     "Ogni settimana rivela l'evento prima che accada. Puoi prepararti o evitarlo completamente una volta per run.",
        },
    },
    #--------------------------------------------------------------------------------------------medico---------------------------------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/medico/idle/medicoidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/medico/camminata_in_avanti/medico{i}_camminatainavanti.png").convert_alpha() for i in range(1, 9)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
        },
        "info": {
            "name":        "Medico",
            "descrizione": "Piccolo, rotondo, con quel cappello che sembra più un fungo che una divisa da medico — il che in realtà ha senso. Ha guarito più malattie con i suoi funghi magici che qualsiasi medicina convenzionale. L'unico dottore al mondo che invece di prescrivere pillole ti lancia un fungo in faccia e giura che funziona. E funziona.",
            "abilita":     "Ogni membro curato da lui riceve +1 HP massimo permanente per il resto della run.",
        },
    },
    #----------------------------------------------------------------------------------------------------mozzo----------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png").convert_alpha() for i in range(1, 4)],
        },
        "info": {
            "name":        "Mozzo",
            "descrizione": "Il pirata più sfigato dei sette mari. Ha provato a fare il capitano — la nave è affondata. Ha provato a fare il cannoniere — si è sparato su un piede. Ora fa il mozzo e stranamente in questo riesce, probabilmente perché l'unica cosa che gli viene chiesta è di non combinare disastri troppo grossi. Ci riesce. A malapena.",
            "abilita":     "Anni di pasti orribili lo hanno temprato. Consuma solo 0.5 porzioni e non si ammala mai di scorbuto — il suo corpo ha rinunciato ad avere standard.",
        },
    },
    #-------------------------------------------------------------------------------------------carpentiere-------------------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 5)],
        },
        "info": {
            "name":        "Carpentiere",
            "descrizione": "Non parla. Non esprime emozioni. Non fa domande. Gli dai dei blocchi di legno e in trenta secondi hai una nave nuova — non chiedergli come, non chiedergli perché. È arrivato a bordo dal nulla, probabilmente scavando dal basso, e da quel giorno la nave non ha mai avuto un buco che durasse più di un turno. L'unico membro dell'equipaggio che guarda un albero e vede già una scialuppa.",
            "abilita":     "La vita della nave non scende mai sotto 1 finché Steve è vivo. Ripara tutto in silenzio prima che affondi davvero.",
        },
    },
    #--------------------------------------------------------------------------------------------bardo---------------------------------------------------------------------------------------------------
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x":      WIDTH//10,
            "y":      (HEIGHT//2) + (HEIGHT//10),
            "x_fine": (WIDTH//2) + (WIDTH//10),
            "y_fine": (HEIGHT//2) - (HEIGHT//16)
        },
        "sprites": {
            "idle":            [pygame.image.load(f"assets/personaggi/bardo/idle/bardoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward":    [pygame.image.load(f"assets/personaggi/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle":      [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 4)],
        },
        "info": {
            "name":        "Bardo",
            "descrizione": "Non sa combattere, non sa navigare, non sa riparare niente. Sa però cantare — e stranamente a bordo di una nave in mezzo all'oceano, dopo settimane di tempeste e razioni dimezzate, una buona canzone vale quanto un medikit. Nessuno lo ammetterebbe mai. Ma quando smette di suonare il morale crolla e tutti lo sanno.",
            "abilita":     "Il morale non scende mai sotto 2 finché il Bardo è vivo e in salute.",
        },
    },
]

# posizione del personaggio di prova nella schermata 0
debug_pos_x = 0.0
debug_pos_y = 0.0
debug_x_fine = float(WIDTH - 100)
debug_y_fine = float(HEIGHT - 100)


# ------------------------------------------------------------------------------- funzioni comuni -------------------------------------------------------------------------------

def prendi_frame(lista_frame: list, durata_frame_ms: int, inizio_ms: int = 0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]


def disegna_animazione(schermo: pygame.Surface, sprites: dict, animazione: str, durata_ms: int, pos: tuple, dimensione: tuple = (64, 78), flip: bool = False):
    frame_grezzo   = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato  = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    rect = frame_flippato.get_rect(topleft=pos)
    schermo.blit(frame_flippato, rect.topleft)
    return rect


def disegna_spostamento_pos_to_pos(x: int, x_fine: int, y: int, y_fine: int, velocita: int, sprites: dict, durata_ms: int, schermo: pygame.Surface, personaggio: int, dimensione: tuple = (64, 78)):
    if x != x_fine:
        if x < x_fine:
            x += velocita
            if x > x_fine:
                x = x_fine
        elif x > x_fine:
            x -= velocita
            if x < x_fine:
                x = x_fine
        disegna_animazione(schermo, sprites[personaggio]["sprites"], "walk_cycle", durata_ms, (x, y), dimensione, False)

    elif y != y_fine:
        if y < y_fine:
            y += velocita
            if y > y_fine:
                y = y_fine
        elif y > y_fine:
            y -= velocita
            if y < y_fine:
                y = y_fine
        disegna_animazione(schermo, sprites[personaggio]["sprites"], "walk_forward", durata_ms, (x, y), dimensione, False)

    else:
        disegna_animazione(schermo, sprites[personaggio]["sprites"], "idle", durata_ms, (x, y), dimensione, False)

    return x, y


def spostamento_pos_to_pos(x_iniz, x_fine, y_iniz, y_fine, velocita):
    x = x_iniz
    y = y_iniz

    if x < x_fine:
        x += velocita
        if x > x_fine:
            x = x_fine
    elif x > x_fine:
        x -= velocita
        if x < x_fine:
            x = x_fine

    if x == x_fine:
        if y < y_fine:
            y += velocita
            if y > y_fine:
                y = y_fine
        elif y > y_fine:
            y -= velocita
            if y < y_fine:
                y = y_fine

    return (int(x), int(y))


# ------------------------------------------------------------------------------- funzioni schermata 0 (debug) -------------------------------------------------------------------------------

def disegna_etichetta(rect, testo, font):
    surf = font.render(testo, True, NERO)
    padding_x = 4
    padding_y = 2
    box = pygame.Rect(0, 0, surf.get_width() + padding_x * 2, surf.get_height() + padding_y * 2)
    box.midbottom = (rect.centerx, rect.top - 3)
    pygame.draw.rect(schermo, BIANCO, box, border_radius=5)
    pygame.draw.rect(schermo, NERO,   box, width=1, border_radius=5)
    schermo.blit(surf, (box.x + padding_x, box.y + padding_y))


def disegna_testo_wrapped(testo, x, y, larghezza_max, font, colore=NERO, line_spacing=3):
    parole = testo.split(" ")
    riga   = ""
    y_corr = y

    for p in parole:
        tentativo = (riga + " " + p).strip()
        w, _ = font.size(tentativo)
        if w <= larghezza_max:
            riga = tentativo
        else:
            surf = font.render(riga, True, colore)
            schermo.blit(surf, (x, y_corr))
            y_corr += surf.get_height() + line_spacing
            riga = p

    if riga:
        surf = font.render(riga, True, colore)
        schermo.blit(surf, (x, y_corr))
        y_corr += surf.get_height() + line_spacing

    return y_corr


def disegna_slot(idx_personaggio, anim, durata, pos, dim, flip, hitboxes):
    rect = disegna_animazione(
        schermo,
        PERSONAGGI[idx_personaggio]["sprites"],
        anim,
        durata,
        pos,
        dimensione=dim,
        flip=flip,
    )
    disegna_etichetta(rect, PERSONAGGI[idx_personaggio]["info"]["name"], font_piccolo)
    hitboxes.append({
        "personaggio": idx_personaggio,
        "anim":        anim,
        "durata":      durata,
        "dim":         dim,
        "flip":        flip,
        "rect":        rect,
    })


def disegna_pannello_info(selezionato):
    idx  = selezionato["personaggio"]
    info = PERSONAGGI[idx]["info"]

    zoom     = 3.0
    w, h     = selezionato["dim"]
    dim_zoom = (int(w * zoom), int(h * zoom))

    rect_zoom = disegna_animazione(
        schermo,
        PERSONAGGI[idx]["sprites"],
        selezionato["anim"],
        selezionato["durata"],
        (60, 140),
        dimensione=dim_zoom,
        flip=selezionato["flip"],
    )
    disegna_etichetta(rect_zoom, info["name"], font_zoom)

    pannello_x = rect_zoom.right + 30
    pannello_y = 120
    pannello_w = WIDTH - pannello_x - 40
    pannello_h = 560

    box = pygame.Rect(pannello_x - 12, pannello_y - 12, pannello_w + 24, pannello_h)
    pygame.draw.rect(schermo, BIANCO, box, border_radius=10)
    pygame.draw.rect(schermo, NERO,   box, width=2, border_radius=10)

    y = pannello_y

    titolo2 = font_istruzioni.render(info["name"], True, NERO)
    schermo.blit(titolo2, (pannello_x, y))
    y += titolo2.get_height() + 10

    label_desc = font_istruzioni.render("Descrizione:", True, NERO)
    schermo.blit(label_desc, (pannello_x, y))
    y += label_desc.get_height() + 6
    y = disegna_testo_wrapped(info["descrizione"], pannello_x, y, pannello_w, font_istruzioni)
    y += 10

    label_abi = font_istruzioni.render("Abilità:", True, NERO)
    schermo.blit(label_abi, (pannello_x, y))
    y += label_abi.get_height() + 6
    disegna_testo_wrapped(info["abilita"], pannello_x, y, pannello_w, font_istruzioni)

    istr = font_istruzioni.render("Premi 'S' per tornare alla schermata normale", True, BIANCO)
    schermo.blit(istr, (20, 15))


# ------------------------------------------------------------------------------- game loop -------------------------------------------------------------------------------

schermata   = 0
selezionato = None
gameOver    = False

while not gameOver:
    hitboxes  = []
    click_pos = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                selezionato = None
            if event.key == pygame.K_F1:
                schermata = 0 if schermata == 1 else 1
                selezionato = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos

    # ---------------------------------------------------------------- schermata 0: debug interattivo ----------------------------------------------------------------
    if schermata == 0:
        schermo.blit(bg, (0, 0))

        if selezionato is None:
            titolo = font_istruzioni.render(
                "Clicca su un personaggio per i dettagli  |  S = torna indietro  |  F1 = gioco",
                True, BIANCO,
            )
            schermo.blit(titolo, (20, 15))

            # CAPITANO
            disegna_slot(0, "walk_forward",    150, (50,  50), (64, 78), False, hitboxes)
            disegna_slot(0, "walk_cycle",      150, (150, 50), (64, 78), False, hitboxes)
            disegna_slot(0, "walk_cycle",      150, (250, 50), (64, 78), True,  hitboxes)
            disegna_slot(0, "idle",            200, (350, 50), (64, 78), False, hitboxes)
            disegna_slot(0, "walk_cycle_sick", 150, (450, 50), (64, 78), False, hitboxes)
            disegna_slot(0, "walk_cycle_sick", 150, (550, 50), (64, 78), True,  hitboxes)

            # CUOCO
            disegna_slot(1, "walk_forward",    200, (650,  50), (54, 74), False, hitboxes)
            disegna_slot(1, "walk_cycle",      170, (750,  50), (54, 74), False, hitboxes)
            disegna_slot(1, "walk_cycle",      170, (850,  50), (54, 74), True,  hitboxes)
            disegna_slot(1, "idle",            150, (945,  50), (54, 74), False, hitboxes)
            disegna_slot(1, "walk_cycle_sick", 170, (1040, 50), (54, 74), False, hitboxes)
            disegna_slot(1, "walk_cycle_sick", 170, (1140, 50), (54, 74), True,  hitboxes)

            # GUARDONE
            disegna_slot(2, "walk_forward",    150, (50,  150), (64, 78), False, hitboxes)
            disegna_slot(2, "walk_cycle",      110, (150, 150), (64, 78), True,  hitboxes)
            disegna_slot(2, "walk_cycle",      110, (250, 150), (64, 78), False, hitboxes)
            disegna_slot(2, "idle",            150, (350, 150), (64, 78), False, hitboxes)
            disegna_slot(2, "walk_cycle_sick", 110, (550, 150), (64, 78), False, hitboxes)
            disegna_slot(2, "walk_cycle_sick", 110, (450, 150), (64, 78), True,  hitboxes)

            # MEDICO
            disegna_slot(3, "walk_forward",    120, (650,  150), (60, 74), False, hitboxes)
            disegna_slot(3, "walk_cycle",      140, (750,  150), (60, 80), False, hitboxes)
            disegna_slot(3, "walk_cycle",      140, (850,  150), (60, 80), True,  hitboxes)
            disegna_slot(3, "idle",            135, (945,  147), (66, 76), False, hitboxes)
            disegna_slot(3, "walk_cycle_sick", 140, (1040, 150), (60, 80), False, hitboxes)
            disegna_slot(3, "walk_cycle_sick", 140, (1140, 150), (60, 80), True,  hitboxes)

            # MOZZO
            disegna_slot(4, "walk_forward",    150, (50,  250), (58, 63), False, hitboxes)
            disegna_slot(4, "walk_cycle",      150, (150, 250), (62, 68), True,  hitboxes)
            disegna_slot(4, "walk_cycle",      150, (250, 250), (62, 68), False, hitboxes)
            disegna_slot(4, "idle",            150, (350, 250), (58, 68), False, hitboxes)
            disegna_slot(4, "walk_cycle_sick", 150, (450, 250), (62, 68), True,  hitboxes)
            disegna_slot(4, "walk_cycle_sick", 150, (550, 250), (62, 68), False, hitboxes)

            # CARPENTIERE
            disegna_slot(5, "walk_forward",    150, (50,  350), (64, 78), False, hitboxes)
            disegna_slot(5, "walk_cycle",      150, (150, 350), (64, 78), False, hitboxes)
            disegna_slot(5, "walk_cycle",      150, (250, 350), (64, 78), True,  hitboxes)
            disegna_slot(5, "idle",            150, (350, 350), (64, 78), False, hitboxes)
            disegna_slot(5, "walk_cycle_sick", 150, (450, 350), (64, 78), False, hitboxes)
            disegna_slot(5, "walk_cycle_sick", 150, (550, 350), (64, 78), True,  hitboxes)

            # BARDO
            disegna_slot(6, "walk_forward",    150, (50,  450), (58, 78), False, hitboxes)
            disegna_slot(6, "walk_cycle",      150, (150, 450), (58, 78), False, hitboxes)
            disegna_slot(6, "walk_cycle",      150, (250, 450), (58, 78), True,  hitboxes)
            disegna_slot(6, "idle",            150, (350, 450), (70, 78), False, hitboxes)
            disegna_slot(6, "walk_cycle_sick", 150, (450, 450), (58, 78), False, hitboxes)
            disegna_slot(6, "walk_cycle_sick", 150, (550, 450), (58, 78), True,  hitboxes)

            # personaggio di prova in movimento
            debug_pos_x, debug_pos_y = spostamento_pos_to_pos(debug_pos_x, debug_x_fine, debug_pos_y, debug_y_fine, 3)
            disegna_animazione(schermo, PERSONAGGI[6]["sprites"], "walk_cycle_sick", 150, (debug_pos_x, debug_pos_y), (58, 78))

            if click_pos is not None:
                for hb in hitboxes:
                    if hb["rect"].collidepoint(click_pos):
                        selezionato = hb
                        break

        else:
            disegna_pannello_info(selezionato)

    # ---------------------------------------------------------------- schermata 1: gioco ----------------------------------------------------------------
    else:
        schermo.blit(bg, (0, 0))

        p = PERSONAGGI[pers]
        p["pos"]["x"], p["pos"]["y"] = disegna_spostamento_pos_to_pos(
            p["pos"]["x"], p["pos"]["x_fine"],
            p["pos"]["y"], p["pos"]["y_fine"],
            3, PERSONAGGI, 150, schermo, pers, (64, 78)
        )

        istr = font_istruzioni.render("F1 = schermata debug", True, BIANCO)
        schermo.blit(istr, (20, 15))

    pygame.display.update()
    clock.tick(60)

pygame.quit()