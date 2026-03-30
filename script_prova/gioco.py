import pygame
import json
import random
pygame.init()

pers = []
IMPOSTAZIONI = "./dati/setting.json"
ROSSO = (255, 0, 0)
controllo = False

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
bottone_marrone = pygame.image.load("assets/tasti/arrow_left.png").convert_alpha()
clock = pygame.time.Clock()

PERSONAGGI = [
    {
        "stats": {"cost": 500, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) + (215*MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/capitano/idle/capitanoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png").convert_alpha() for i in range(1, 6)],
            "button": pygame.image.load("assets/tasti/button_capitan.png").convert_alpha(),
        },
        "info": {
            "name":        "Capitano",
            "descrizione": "Ormai dopo tante avventure pericolose in cui si rischia la pelle, la ha persa veramente. Ma la morte stessa ha rifiutato di tenerlo — troppo testardo anche per l'aldilà. Ora naviga senza carne, senza paura, senza niente da perdere. Il mare lo teme ancora.",
            "abilita":     "non mangia, non beve potrebe improvvisamente ridursi a poche ossa",
        },
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16)+(205*MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (20*MOD),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/cuoco/idle/cuocoidle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png").convert_alpha() for i in range(1, 3)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
            "button": pygame.image.load("assets/tasti/button_cuoco.png").convert_alpha(),
            
        },
        "info": {
            "name":        "Cuoco",
            "descrizione": "Un piccolo maiale che prepara piatti stellati. Menomale che non è grosso sennò li mangerebbe anche. Nessuno sa come un maiale abbia imparato a cucinare, nessuno osa chiederglielo — non quando è lui a decidere cosa finisce nel piatto e cosa finisce come piatto.",
            "abilita":     "se mangi con il cuoco a bordo le porzioni valgono doppio. Il cibo dura il doppio con metà delle scorte.",
        },
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (100 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (20 * MOD),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)],
            "button": pygame.image.load("assets/tasti/button_guardone.png").convert_alpha(),
        },
        "info": {
            "name":        "Guardone",
            "descrizione": "Un piccolo occhio molto fortunato. Se dovesse tirare una freccetta centrerebbe sicuramente il centro, peccato non abbia le mani. Vede tutto — tempeste in arrivo, navi nemiche all'orizzonte, il futuro stesso. L'unico problema è che per indicare la rotta deve ammiccare nella direzione giusta e sperare che qualcuno capisca.",
            "abilita":     "Ogni settimana rivela l'evento prima che accada. Puoi prepararti o evitarlo completamente una volta per run.",
        },
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) + (230*MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (50 * MOD),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/medico/idle/medicoidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/medico/camminata_in_avanti/medico{i}_camminatainavanti.png").convert_alpha() for i in range(1, 9)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
            "button": pygame.image.load("assets/tasti/button_medico.png").convert_alpha(),
        },
        "info": {
            "name":        "Medico",
            "descrizione": "Piccolo, rotondo, con quel cappello che sembra più un fungo che una divisa da medico — il che in realtà ha senso. Ha guarito più malattie con i suoi funghi magici che qualsiasi medicina convenzionale. L'unico dottore al mondo che invece di prescrivere pillole ti lancia un fungo in faccia e giura che funziona. E funziona.",
            "abilita":     "Ogni membro curato da lui riceve +1 HP massimo permanente per il resto della run.",
        },
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (390 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (40 * MOD)
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_mozzo.png").convert_alpha(),   
        },
        "info": {
            "name":        "Mozzo",
            "descrizione": "Il pirata più sfigato dei sette mari. Ha provato a fare il capitano — la nave è affondata. Ha provato a fare il cannoniere — si è sparato su un piede. Ora fa il mozzo e stranamente in questo riesce, probabilmente perché l'unica cosa che gli viene chiesta è di non combinare disastri troppo grossi. Ci riesce. A malapena.",
            "abilita":     "Anni di pasti orribili lo hanno temprato. Consuma solo 0.5 porzioni e non si ammala mai di scorbuto — il suo corpo ha rinunciato ad avere standard.",
        },
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (408 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 5)],
            "button": pygame.image.load("assets/tasti/button_carpentiere.png").convert_alpha(),
        },
        "info": {
            "name":        "Carpentiere",
            "descrizione": "Non parla. Non esprime emozioni. Non fa domande. Gli dai dei blocchi di legno e in trenta secondi hai una nave nuova — non chiedergli come, non chiedergli perché. È arrivato a bordo dal nulla, probabilmente scavando dal basso, e da quel giorno la nave non ha mai avuto un buco che durasse più di un turno. L'unico membro dell'equipaggio che guarda un albero e vede già una scialuppa.",
            "abilita":     "La vita della nave non scende mai sotto 1 finché Steve è vivo. Ripara tutto in silenzio prima che affondi davvero.",
        },
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (440 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (10*MOD),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/bardo/idle/bardoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_bardo.png").convert_alpha(),
        },
        "info": {
            "name":        "Bardo",
            "descrizione": "Non sa combattere, non sa navigare, non sa riparare niente. Sa però cantare — e stranamente a bordo di una nave in mezzo all'oceano, dopo settimane di tempeste e razioni dimezzate, una buona canzone vale quanto un medikit. Nessuno lo ammetterebbe mai. Ma quando smette di suonare il morale crolla e tutti lo sanno.",
            "abilita":     "Il morale non scende mai sotto 2 finché il Bardo è vivo e in salute.",
        },
    },
]
CIBO = [
    {
        "stats": {"heal": 5},
        "meta": {"rarity": "comune"},
        "effects": {"morale": 1, "stamina": 1},
        "info": {"name": "biscotti", "descrizione": "Biscotti dolci e nutrienti"},
    },
    {
        "stats": {"heal": 5},
        "meta": {"rarity": "comune"},
        "effects": {"morale": 1},
        "info": {"name": "pane", "descrizione": "Pane fresco e nutriente"},
    },
    {
        "stats": {"heal": 2},
        "meta": {"rarity": "comune"},
        "effects": {"craft_cucina": 2},
        "info": {"name": "farina", "descrizione": "Farina per impasti e preparazioni"},
    },
    {
        "stats": {"heal": 8},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 2},
        "info": {"name": "riso", "descrizione": "Riso basmati di alta qualità"},
    },
    {
        "stats": {"heal": 7},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 2, "salute_max_temp": 1},
        "info": {"name": "legumi", "descrizione": "Legumi secchi ricchi di proteine"},
    },
    {
        "stats": {"heal": 1},
        "meta": {"rarity": "raro"},
        "effects": {"morale": 2, "buff_pasto": 1},
        "info": {"name": "spezie", "descrizione": "Spezie aromatiche per migliorare i pasti"},
    },
    {
        "stats": {"heal": 10},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 3},
        "info": {"name": "carne", "descrizione": "Carne salata conservata per i lunghi viaggi"},
    },
    {
        "stats": {"heal": 9},
        "meta": {"rarity": "non_comune"},
        "effects": {"focus": 1, "stamina": 2},
        "info": {"name": "pesce", "descrizione": "Pesce essiccato ricco di nutrienti"},
    },
    {
        "stats": {"heal": 6},
        "meta": {"rarity": "comune"},
        "effects": {"scorbuto_resistenza": 2},
        "info": {"name": "frutta", "descrizione": "Frutta fresca per recuperare energie"},
    },
    {
        "stats": {"heal": 6},
        "meta": {"rarity": "comune"},
        "effects": {"scorbuto_resistenza": 2, "morale": 1},
        "info": {"name": "verdura", "descrizione": "Verdura fresca per una dieta bilanciata"},
    },
    {
        "stats": {"heal": 4},
        "meta": {"rarity": "comune"},
        "effects": {"sete": 5},
        "info": {"name": "acqua", "descrizione": "Acqua potabile essenziale per la sopravvivenza"},
    },
    {
        "stats": {"heal": 2},
        "meta": {"rarity": "non_comune"},
        "effects": {"morale": 3, "precisione": -1},
        "info": {"name": "rum", "descrizione": "Rum forte, tipico della ciurma"},
    },
    {
        "stats": {"heal": 2},
        "meta": {"rarity": "comune"},
        "effects": {"morale": 2, "sete": 1},
        "info": {"name": "birra", "descrizione": "Birra leggera da cambusa"},
    },
]
EQUIPAGGIAMENTO = [
    {
        "stats": {},
        "meta": {"rarity": "raro"},
        "effects": {"cura_istantanea": 15, "rimuovi_malattia": 1},
        "info": {"name": "medikit", "descrizione": "Kit medico per curare ferite e malanni"},
    },
    {
        "stats": {},
        "meta": {"rarity": "raro"},
        "effects": {"danno_nave": 12},
        "info": {"name": "cannone", "descrizione": "Arma pesante per attacchi navali"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"ammo_cannone": 1},
        "info": {"name": "palla di cannone", "descrizione": "Munizione per il cannone di bordo"},
    },
    {
        "stats": {},
        "meta": {"rarity": "non_comune"},
        "effects": {"attacco_boarding": 4},
        "info": {"name": "sciabole", "descrizione": "Lame da combattimento ravvicinato"},
    },
    {
        "stats": {},
        "meta": {"rarity": "non_comune"},
        "effects": {"successo_arrembaggio": 2},
        "info": {"name": "rampino", "descrizione": "Utile per arrembaggio e scalata"},
    },
    {
        "stats": {},
        "meta": {"rarity": "non_comune"},
        "effects": {"attacco_distanza": 3, "precisione": 2},
        "info": {"name": "balestra", "descrizione": "Arma a distanza precisa e silenziosa"},
    },
    {
        "stats": {},
        "meta": {"rarity": "non_comune"},
        "effects": {"riparazione_nave": 10},
        "info": {"name": "kit di riparazione", "descrizione": "Strumenti e materiali per riparare la nave"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"raccolta_legno": 2},
        "info": {"name": "sega", "descrizione": "Attrezzo da lavoro per tagliare legno"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"raccolta_legno": 3, "attacco_boarding": 1},
        "info": {"name": "ascia", "descrizione": "Attrezzo robusto per lavori pesanti"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"stabilita_nave": 3},
        "info": {"name": "ancora", "descrizione": "Serve per fermare la nave in sicurezza"},
    },
    {
        "stats": {},
        "meta": {"rarity": "non_comune"},
        "effects": {"errore_rotta": -2},
        "info": {"name": "bussola", "descrizione": "Strumento di navigazione per orientarsi"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"visibilita_notte": 3},
        "info": {"name": "lanterna a olio", "descrizione": "Fonte di luce per la notte e gli interni"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"raccolta_cibo_mare": 3},
        "info": {"name": "reti da pesca", "descrizione": "Utili per catturare pesce durante il viaggio"},
    },
    {
        "stats": {},
        "meta": {"rarity": "comune"},
        "effects": {"perdita_cibo": -2},
        "info": {"name": "trappola per ratti", "descrizione": "Mantiene pulita la stiva eliminando infestazioni"},
    },
    {
        "stats": {},
        "meta": {"rarity": "epico"},
        "effects": {"chance_tesoro": 5},
        "info": {"name": "mappa del tesoro", "descrizione": "Indica possibili rotte e tesori nascosti"},
    },
    {
        "stats": {},
        "meta": {"rarity": "raro"},
        "effects": {"intimidazione": 3, "morale_ciurma": 2},
        "info": {"name": "bandiera pirata", "descrizione": "Simbolo della ciurma e della sua fama"},
    },
    {
        "stats": {},
        "meta": {"rarity": "non_comune"},
        "effects": {"morale_ciurma": 4, "disciplina": -1},
        "info": {"name": "barile di rum", "descrizione": "Scorta di rum per la ciurma"},
    },
]
personaggi_selezionati = []
bottone_rect = bottone_marrone.get_rect(bottomright=(WIDTH - (20 * MOD), HEIGHT - (20 * MOD)))
soldi_iniziali = 2000
font = pygame.font.Font(None, 36)


def bottone_personaggio(pers: list, personaggi_selezionati: list, personaggio_corrente: int, controllo: bool, bottone_img: pygame.Surface, posizione: tuple, soldi_correnti: int, dimensione: tuple = (100*MOD, 100*MOD)):

    bottone_scalato = pygame.transform.scale(bottone_img, dimensione)
    bottone_rect = pygame.Rect(posizione[0], posizione[1], dimensione[0], dimensione[1])
    schermo.blit(bottone_scalato, bottone_rect)

    mouse_pos = pygame.mouse.get_pos()
    click_sinistro = pygame.mouse.get_pressed()[0]

    if click_sinistro and bottone_rect.collidepoint(mouse_pos) and not controllo:
        controllo = True
        if personaggio_corrente not in pers:
            costo = PERSONAGGI[personaggio_corrente]["stats"]["cost"] or 0
            if soldi_correnti >= costo:
                pers.append(personaggio_corrente)
                personaggi_selezionati.append(PERSONAGGI[personaggio_corrente])
                soldi_correnti -= costo

    if not click_sinistro:
        controllo = False

    return controllo, soldi_correnti

def prendi_frame(lista_frame: list, durata_frame_ms: int, inizio_ms: int = 0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo: pygame.Surface, sprites: dict, animazione: str, durata_ms: int, pos: tuple, dimensione: tuple = (64*MOD, 78*MOD), flip: bool = False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

def disegna_spostamento_personaggio(p: dict, velocita: float, durata_ms: int, schermo: pygame.Surface, dimensione: tuple = (64*MOD, 78*MOD), flip: bool = False):
    x = p["pos"]["x"]
    y = p["pos"]["y"]
    x_fine = p["pos"]["x_fine"]
    y_fine = p["pos"]["y_fine"]

    if x != x_fine:
        if x < x_fine:
            x += velocita
            if p["info"]["name"] in ["Mozzo","Guardone"]:
                flip = True
            if x > x_fine:
                x = x_fine
        elif x > x_fine:
            x -= velocita
            flip = True
        disegna_animazione(schermo, p["sprites"], "walk_cycle", durata_ms, (x, y), flip=flip)

    elif y != y_fine:
        if y < y_fine:
            y += velocita
            if y > y_fine:
                y = y_fine
        elif y > y_fine:
            y -= velocita
        disegna_animazione(schermo, p["sprites"], "walk_forward", durata_ms, (x, y), flip=flip)

    else:
        disegna_animazione(schermo, p["sprites"], "idle", durata_ms, (x, y), flip=flip)

    p["pos"]["x"] = x
    p["pos"]["y"] = y

    arrivato = (x == x_fine and y == y_fine)
    return arrivato

def riordina_per_profondita(pers: list, personaggi: list):
    for i in range(len(pers)):
        for j in range(i + 1, len(pers)):
            if personaggi[pers[i]]["pos"]["y"] > personaggi[pers[j]]["pos"]["y"]:
                pers[i], pers[j] = pers[j], pers[i]

def nuova_destinazione(p: dict, pers: list, personaggi: list):
    riordina_per_profondita(pers, personaggi)
    p["pos"]["x_fine"] = p["pos"]["x_barca"]
    p["pos"]["y_fine"] = p["pos"]["y_barca"]
    

def disegna_soldi(screen: pygame.Surface, soldi_correnti: int) -> None:
    testo = font.render(f"Soldi: {soldi_correnti}", True, (255, 215, 0))
    rett = testo.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(testo, rett)


schermata = 1
gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    schermo.blit(bg, (0, 0))
    disegna_soldi(schermo, soldi_iniziali)
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 0, controllo, PERSONAGGI[0]["sprites"]["button"], (10*MOD, 10*MOD), soldi_iniziali, (90*MOD, 115*MOD))
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 3, controllo, PERSONAGGI[3]["sprites"]["button"], (115*MOD, 10*MOD), soldi_iniziali, (90*MOD, 120*MOD))
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 1, controllo, PERSONAGGI[1]["sprites"]["button"], (10*MOD, 135*MOD), soldi_iniziali, (90*MOD, 115*MOD))
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 2, controllo, PERSONAGGI[2]["sprites"]["button"], (115*MOD, 135*MOD), soldi_iniziali, (90*MOD, 115*MOD))
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 5, controllo, PERSONAGGI[5]["sprites"]["button"], (10*MOD, 265*MOD), soldi_iniziali, (90*MOD, 115*MOD))
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 4, controllo, PERSONAGGI[4]["sprites"]["button"], (115*MOD, 260*MOD), soldi_iniziali, (98*MOD, 123*MOD))
    controllo, soldi_iniziali = bottone_personaggio(pers, personaggi_selezionati, 6, controllo, PERSONAGGI[6]["sprites"]["button"], (10*MOD, 385*MOD), soldi_iniziali, (98*MOD, 123*MOD))
    if len(pers) != 0:
        arrivato = False
        for n in pers:
            arrivato = disegna_spostamento_personaggio(PERSONAGGI[n], 5, 150, schermo)
            if arrivato:
                nuova_destinazione(PERSONAGGI[n], pers, PERSONAGGI)
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()