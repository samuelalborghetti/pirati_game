import pygame
import json
import random

#TODO: struttura dati per l'equipaggiamento e il cibo

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
clock = pygame.time.Clock()

#biscotti, pane/farina, riso e legumi, spezie, carne, pesce, frutta, verdura, acqua, rum/birra
CIBO = [
    {"name": "biscotti", "description": "Biscotti dolci e nutrienti", "heal": 5, "rarity": "comune", "effects": {"morale": 1, "stamina": 1}},
    {"name": "pane", "description": "Pane fresco e nutriente", "heal": 5, "rarity": "comune", "effects": {"morale": 1}},
    {"name": "farina", "description": "Farina per impasti e preparazioni", "heal": 2, "rarity": "comune", "effects": {"craft_cucina": 2}},
    {"name": "riso", "description": "Riso basmati di alta qualità", "heal": 8, "rarity": "non_comune", "effects": {"stamina": 2}},
    {"name": "legumi", "description": "Legumi secchi ricchi di proteine", "heal": 7, "rarity": "non_comune", "effects": {"stamina": 2, "salute_max_temp": 1}},
    {"name": "spezie", "description": "Spezie aromatiche per migliorare i pasti", "heal": 1, "rarity": "raro", "effects": {"morale": 2, "buff_pasto": 1}},
    {"name": "carne", "description": "Carne salata conservata per i lunghi viaggi", "heal": 10, "rarity": "non_comune", "effects": {"stamina": 3}},
    {"name": "pesce", "description": "Pesce essiccato ricco di nutrienti", "heal": 9, "rarity": "non_comune", "effects": {"focus": 1, "stamina": 2}},
    {"name": "frutta", "description": "Frutta fresca per recuperare energie", "heal": 6, "rarity": "comune", "effects": {"scorbuto_resistenza": 2}},
    {"name": "verdura", "description": "Verdura fresca per una dieta bilanciata", "heal": 6, "rarity": "comune", "effects": {"scorbuto_resistenza": 2, "morale": 1}},
    {"name": "acqua", "description": "Acqua potabile essenziale per la sopravvivenza", "heal": 4, "rarity": "comune", "effects": {"sete": 5}},
    {"name": "rum", "description": "Rum forte, tipico della ciurma", "heal": 2, "rarity": "non_comune", "effects": {"morale": 3, "precisione": -1}},
    {"name": "birra", "description": "Birra leggera da cambusa", "heal": 2, "rarity": "comune", "effects": {"morale": 2, "sete": 1}},
]

EQUIPAGGIAMENTO = [
    {"name": "medikit", "description": "Kit medico per curare ferite e malanni", "rarity": "raro", "effects": {"cura_istantanea": 15, "rimuovi_malattia": 1}},
    {"name": "cannone", "description": "Arma pesante per attacchi navali", "rarity": "raro", "effects": {"danno_nave": 12}},
    {"name": "palla di cannone", "description": "Munizione per il cannone di bordo", "rarity": "comune", "effects": {"ammo_cannone": 1}},
    {"name": "sciabole", "description": "Lame da combattimento ravvicinato", "rarity": "non_comune", "effects": {"attacco_boarding": 4}},
    {"name": "rampino", "description": "Utile per arrembaggio e scalata", "rarity": "non_comune", "effects": {"successo_arrembaggio": 2}},
    {"name": "balestra", "description": "Arma a distanza precisa e silenziosa", "rarity": "non_comune", "effects": {"attacco_distanza": 3, "precisione": 2}},
    {"name": "kit di riparazione", "description": "Strumenti e materiali per riparare la nave", "rarity": "non_comune", "effects": {"riparazione_nave": 10}},
    {"name": "sega", "description": "Attrezzo da lavoro per tagliare legno", "rarity": "comune", "effects": {"raccolta_legno": 2}},
    {"name": "ascia", "description": "Attrezzo robusto per lavori pesanti", "rarity": "comune", "effects": {"raccolta_legno": 3, "attacco_boarding": 1}},
    {"name": "ancora", "description": "Serve per fermare la nave in sicurezza", "rarity": "comune", "effects": {"stabilita_nave": 3}},
    {"name": "bussola", "description": "Strumento di navigazione per orientarsi", "rarity": "non_comune", "effects": {"errore_rotta": -2}},
    {"name": "lanterna a olio", "description": "Fonte di luce per la notte e gli interni", "rarity": "comune", "effects": {"visibilita_notte": 3}},
    {"name": "reti da pesca", "description": "Utili per catturare pesce durante il viaggio", "rarity": "comune", "effects": {"raccolta_cibo_mare": 3}},
    {"name": "trappola per ratti", "description": "Mantiene pulita la stiva eliminando infestazioni", "rarity": "comune", "effects": {"perdita_cibo": -2}},
    {"name": "mappa del tesoro", "description": "Indica possibili rotte e tesori nascosti", "rarity": "epico", "effects": {"chance_tesoro": 5}},
    {"name": "bandiera pirata", "description": "Simbolo della ciurma e della sua fama", "rarity": "raro", "effects": {"intimidazione": 3, "morale_ciurma": 2}},
    {"name": "barile di rum", "description": "Scorta di rum per la ciurma", "rarity": "non_comune", "effects": {"morale_ciurma": 4, "disciplina": -1}},
]


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
            "idle":         [pygame.image.load(f"assets/personaggi/capitano/idle/capitanoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png").convert_alpha() for i in range(1, 6)],
        },
        "info": {"name": "Capitano", "descrizione": "...", "abilita": "..."},
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
            "idle":         [pygame.image.load(f"assets/personaggi/cuoco/idle/cuocoidle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png").convert_alpha() for i in range(1, 3)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
        },
        "info": {"name": "Cuoco", "descrizione": "...", "abilita": "..."},
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
            "idle":         [pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)],
        },
        "info": {"name": "Guardone", "descrizione": "...", "abilita": "..."},
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
            "idle":         [pygame.image.load(f"assets/personaggi/medico/idle/medicoidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/medico/camminata_in_avanti/medico{i}_camminatainavanti.png").convert_alpha() for i in range(1, 9)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
        },
        "info": {"name": "Medico", "descrizione": "...", "abilita": "..."},
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
            "idle":         [pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png").convert_alpha() for i in range(1, 4)],
        },
        "info": {"name": "Mozzo", "descrizione": "...", "abilita": "..."},
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
            "idle":         [pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 5)],
        },
        "info": {"name": "Carpentiere", "descrizione": "...", "abilita": "..."},
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
            "idle":         [pygame.image.load(f"assets/personaggi/bardo/idle/bardoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle":   [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 4)],
        },
        "info": {"name": "Bardo", "descrizione": "...", "abilita": "..."},
    },
]

def prendi_frame(lista_frame: list, durata_frame_ms: int, inizio_ms: int = 0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo: pygame.Surface, sprites: dict, animazione: str, durata_ms: int, pos: tuple, dimensione: tuple = (64, 78), flip: bool = False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

def disegna_spostamento_personaggio(p: dict, velocita: float, durata_ms: int, schermo: pygame.Surface, dimensione: tuple = (64, 78), flip : bool = False):
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

        disegna_animazione(schermo, p["sprites"], "walk_cycle", durata_ms, (x, y), dimensione, flip)

    elif y != y_fine:
        if y < y_fine:
            y += velocita
            if y > y_fine:
                y = y_fine
        elif y > y_fine:
            y -= velocita
            
            

        disegna_animazione(schermo, p["sprites"], "walk_forward", durata_ms, (x, y), dimensione, flip)

    else:
        disegna_animazione(schermo, p["sprites"], "idle", durata_ms, (x, y), dimensione, flip)

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
    riordina_per_profondita(pers,personaggi)
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
        arrivato = False
        for n in pers:
            arrivato = disegna_spostamento_personaggio(PERSONAGGI[n], 15, 150, schermo)
            if arrivato:
                nuova_destinazione(PERSONAGGI[n], pers, PERSONAGGI)


        if arrivato and (5 not in pers):
            pers.append(1)
            pers.append(2)
            pers.append(3)
            pers.append(4)
            pers.append(5)
            pers.append(6)
            
            
    pygame.display.update()
    clock.tick(60)

pygame.quit()