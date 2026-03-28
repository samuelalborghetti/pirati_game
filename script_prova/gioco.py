import pygame
import json
import random
pygame.init()

pers = [0]
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
        "stats": {"cost": None, "hp": 3, "alive": True},
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
        },
        "info": {
            "name":        "Bardo",
            "descrizione": "Non sa combattere, non sa navigare, non sa riparare niente. Sa però cantare — e stranamente a bordo di una nave in mezzo all'oceano, dopo settimane di tempeste e razioni dimezzate, una buona canzone vale quanto un medikit. Nessuno lo ammetterebbe mai. Ma quando smette di suonare il morale crolla e tutti lo sanno.",
            "abilita":     "Il morale non scende mai sotto 2 finché il Bardo è vivo e in salute.",
        },
    },
]

personaggi_selezionati = []
bottone_rect = bottone_marrone.get_rect(bottomright=(WIDTH - (20 * MOD), HEIGHT - (20 * MOD)))
personaggio_corrente = 1  # il Capitano (0) è già in pers, si parte dal Cuoco

def bottone_personaggio(pers: list, personaggi_selezionati: list, personaggio_corrente: int, controllo: bool):
    schermo.blit(bottone_marrone, bottone_rect)

    mouse_pos = pygame.mouse.get_pos()
    click_sinistro = pygame.mouse.get_pressed()[0]

    if click_sinistro and bottone_rect.collidepoint(mouse_pos) and not controllo:
        controllo = True
        if personaggio_corrente not in pers:
            pers.append(personaggio_corrente)
            personaggi_selezionati.append(PERSONAGGI[personaggio_corrente])

    if not click_sinistro:
        controllo = False

    return controllo

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


schermata = 1
gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    if schermata == 0:
        schermo.fill(ROSSO)
    else:
        schermo.blit(bg, (0, 0))
        controllo = bottone_personaggio(pers, personaggi_selezionati, personaggio_corrente, controllo)
        arrivato = False
        for n in pers:
            arrivato = disegna_spostamento_personaggio(PERSONAGGI[n], 4, 150, schermo)
            if arrivato:
                nuova_destinazione(PERSONAGGI[n], pers, PERSONAGGI)

        if arrivato and (5 not in pers):
            pers.append(5)

    pygame.display.update()
    clock.tick(60)

pygame.quit()