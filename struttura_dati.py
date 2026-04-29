import random
import pygame
import json
import gestione_eventi
IMPOSTAZIONI = "./dati/setting.json"

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads(info)
    file.close()
    return dati["height"], dati["width"], dati["audio"], dati["mod"]

HEIGHT, WIDTH, VOLUME, MOD = CaricaSettings(IMPOSTAZIONI)

WIDTH_BUTTON = 85 * MOD
HEIGHT_BUTTON = 95 * MOD
WIDTH_INFO_CHARACHTER = 380 * MOD
HEIGHT_INFO_CHARACHETER = 220 * MOD

WIDHT_BUTTON = 180 * MOD
HEIGH_BUTTON = 90 * MOD
WIDHT_VOLUME_BAR = 200 * MOD
HEIGHT_VOLUME_BAR = 10 * MOD
WIDTH_SLIDER = 18 * MOD
HEIGHT_SLIDER = 30 * MOD
AUDIO_BUTTON_SIZE = 60 * MOD
WIDHT_EMPTY = 220 * MOD
HEIGHT_EMPTY = 75 * MOD
ARROW_SIZE = 50 * MOD

VOLUME_BAR = pygame.Rect(WIDTH/2 - WIDHT_VOLUME_BAR/2,HEIGH_BUTTON * 3, WIDHT_VOLUME_BAR, HEIGHT_VOLUME_BAR)
VOLUME_BAR_COLLISION = pygame.Rect(VOLUME_BAR.centerx - (WIDHT_VOLUME_BAR * 1.2)/2, VOLUME_BAR.centery - (HEIGHT_VOLUME_BAR * 4), WIDHT_VOLUME_BAR * 1.2, HEIGHT_VOLUME_BAR * 8)

BUTTONS = {
    "play":     [pygame.transform.scale(pygame.image.load("assets/tasti/play.png"), (WIDHT_BUTTON, HEIGH_BUTTON)), pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2, HEIGH_BUTTON * 3,WIDHT_BUTTON, HEIGH_BUTTON)],
    "options": [pygame.transform.scale(pygame.image.load("assets/tasti/settings.png"), (WIDHT_BUTTON, HEIGH_BUTTON)), pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2, HEIGH_BUTTON * 4.5, WIDHT_BUTTON, HEIGH_BUTTON)],
    "quit":     [pygame.transform.scale(pygame.image.load("assets/tasti/exit.png"), (WIDHT_BUTTON, HEIGH_BUTTON)), pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2, HEIGH_BUTTON * 6, WIDHT_BUTTON, HEIGH_BUTTON)],
    "audio_full": [pygame.transform.scale(pygame.image.load("assets/tasti/audio_full.png"), (AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)), pygame.Rect(VOLUME_BAR.x - HEIGH_BUTTON, VOLUME_BAR.y - AUDIO_BUTTON_SIZE/2, AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)],
    "no_audio": [pygame.transform.scale(pygame.image.load("assets/tasti/no_audio.png"), (AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)), pygame.Rect(VOLUME_BAR.x - HEIGH_BUTTON, VOLUME_BAR.y - AUDIO_BUTTON_SIZE/2, AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)],
    "empty": [pygame.transform.scale(pygame.image.load("assets/tasti/empty_button.png"), (WIDHT_EMPTY, HEIGHT_EMPTY)), pygame.Rect(WIDTH/2 - WIDHT_EMPTY/2, HEIGHT/2 + HEIGHT_EMPTY/2, WIDHT_EMPTY, HEIGHT_EMPTY)],
    "arr_right": [pygame.transform.scale(pygame.image.load("assets/tasti/arrow_right.png"), (ARROW_SIZE, ARROW_SIZE)), pygame.Rect(WIDTH/2 + WIDHT_EMPTY/2 + ARROW_SIZE /2, HEIGHT/2 + HEIGHT_EMPTY/1.6, ARROW_SIZE, ARROW_SIZE)],
    "resolution": [pygame.transform.scale(pygame.image.load("assets/tasti/resolution.png"), (AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)), pygame.Rect(WIDTH/2 - WIDHT_EMPTY/2 - ARROW_SIZE*1.5, HEIGHT/2 + HEIGHT_EMPTY/1.8, AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)],
    "back": [pygame.transform.scale(pygame.image.load("assets/tasti/back.png"), (WIDHT_BUTTON, HEIGH_BUTTON)), pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2, HEIGHT - HEIGH_BUTTON * 1.5, WIDHT_BUTTON, HEIGH_BUTTON)]
}

PERSONAGGI = [
    # ── CAPITANO ──────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/capitano/idle/capitanoidle{i}.png") for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png") for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png") for i in range(1, 6)],
            "button": pygame.image.load("assets/tasti/button_capitan.png"),
        },
        "info": {
            "name": "Capitano",
            "descrizione": "Il leader della spedizione. La sua presenza garantisce stabilità e disciplina all'equipaggio.",
            "abilita": "Bonus al morale generale. Se muore, il morale crolla drasticamente.",
            "ruolo": "capitano",
        },
    },
    # ── CUOCO ─────────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/cuoco/idle/cuocoidle{i}.png") for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png") for i in range(1, 3)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png") for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png") for i in range(1, 7)],
            "button": pygame.image.load("assets/tasti/button_cuoco.png"),
        },
        "info": {
            "name": "Cuoco",
            "descrizione": "Specializzato nella preparazione del cibo. Senza di lui le razioni sono insipide e il morale cala.",
            "abilita": "Cuoce il cibo rendendolo più nutriente. Senza cuoco: +30 punti ammutinamento.",
            "ruolo": "cuoco",
        },
    },
    # ── NAVIGATORE ──────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 30, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png"), True, False) for i in range(1, 9)],
            "walk_forward": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png"), True, False) for i in range(1, 5)],
            "walk_cycle": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png"), True, False) for i in range(1, 8)],
            "walk_cycle_sick": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png"), True, False) for i in range(1, 8)],
            "button": pygame.image.load("assets/tasti/button_guardone.png"),
        },
        "info": {
            "name": "Navigatore",
            "descrizione": "Sa leggere le stelle e le mappe. Con lui le rotte sono più sicure e gli errori ridotti.",
            "abilita": "Riduce errori di rotta e tempi di viaggio. Evento Raffiche di vento: solo +1 settimana invece di 2-4.",
            "ruolo": "navigatore",
        },
    },
    # ── MEDICO ────────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 50, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/medico/idle/medicoidle{i}.png") for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/medico/camminata_in_avanti/medico{i}_camminatainavanti.png") for i in range(1, 9)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png") for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png") for i in range(1, 7)],
            "button": pygame.image.load("assets/tasti/button_medico.png"),
        },
        "info": {
            "name": "Medico",
            "descrizione": "Curatore dell'equipaggio. Può salvare vite durante le epidemie usando medicinali.",
            "abilita": "Durante l'epidemia: può curare i malati usando 1 bottiglia di medicinale per persona.",
            "ruolo": "medico",
        },
    },
    # ── MARINAIO ───────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png"), True, False) for i in range(1, 4)],
            "walk_forward": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png"), True, False) for i in range(1, 4)],
            "walk_cycle": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png"), True, False) for i in range(1, 4)],
            "walk_cycle_sick": [pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png"), True, False) for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_mozzo.png"),
        },
        "info": {
            "name": "Marinaio",
            "descrizione": "Forza lavoro base della nave. Necessario per le manovre e la navigazione.",
            "abilita": "Forza lavoro essenziale. Più marinai = più difensori contro i pirati.",
            "ruolo": "marinaio",
        },
    },
    # ── MECCANICO ───────────────────────────────────────────────────────────
    {
        "stats": {"cost": 10, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png") for i in range(1, 5)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png") for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png") for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png") for i in range(1, 5)],
            "button": pygame.image.load("assets/tasti/button_carpentiere.png"),
        },
        "info": {
            "name": "Meccanico",
            "descrizione": "esperto nella riparazione della nave. Gestisce i danni allo scafo e al timone.",
            "abilita": "Evento Danni al timone: solo +1 settimana invece di 2-4.",
            "ruolo": "meccanico",
        },
    },
    # ── BARDO ─────────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 10, "hp": 2, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
                
            },
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/bardo/idle/bardoidle{i}.png") for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png") for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png") for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png") for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_bardo.png"),
        },
        "info": {
            "name": "Bardo",
            "descrizione": "Intrattiene l'equipaggio con musica e storie. La sua presenza sostiene il morale durante le tempeste.",
            "abilita": "Riduce il consumo di morale durante le tempeste. Pochi HP (2 invece di 3).",
            "ruolo": "bardo",
        },
    },
    # ── TESORIERE ─────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "hp": 3, "alive": True},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
                
            },
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/tesoriere/idle/cercatore_di_tesori_idle{i}.png") for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/tesoriere/camminata_in_avanti/camminata_in_avanti{i}.png") for i in range(1, 7)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/tesoriere/camminata_a_destrasinistra_con_flip/camminata_lateralec{i}.png") for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/tesoriere/camminata_a_destrasinistra_con_flip_ammalato/camminata_lateralecmalato{i}.png") for i in range(1, 8)],
            "button": pygame.image.load("assets/tasti/button_tesoriere.png"),
        },
        "info": {
            "name": "Tesoriere",
            "descrizione": " esperto di affari e commerci. Sa come ottenere il massimo dalle trattative.",
            "abilita": "Aumenta l'efficacia del baratto nel nuovo mondo. Nessuna abilità di navigazione.",
            "ruolo": "tesoriere",
        },
    },
]

CIBO = [
    # ── SCORTE (dal PDF "Nuovo Mondo") ─────────────────────────────────────────
    {
        "stats": {"heal": 0, "cost": 3.5, "saturazione": 1.5, "verdura": True},
        "meta": {"rarity": "comune", "categoria": "scorta"},
        "effects": {"scorbuto_resistenza": 2, "morale": 1},
        "info": {"name": "verdura", "descrizione": "Verdura fresca - 0.5kg a persona/settimana"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/carote.png"), "button": pygame.image.load("assets/cibo/button/carote_button.png")}
    },
    {
        "stats": {"heal": 0, "cost": 3.5, "saturazione": 1.0, "verdura": True},
        "meta": {"rarity": "comune", "categoria": "scorta"},
        "effects": {"scorbuto_resistenza": 2},
        "info": {"name": "frutta", "descrizione": "Frutta fresca - 1kg a persona/settimana"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/banane.png"), "button": pygame.image.load("assets/cibo/button/banane_button.png")}
    },
    {
        "stats": {"heal": 0, "cost": 7, "saturazione": 1.0, "verdura": False},
        "meta": {"rarity": "non_comune", "categoria": "scorta"},
        "effects": {"stamina": 3},
        "info": {"name": "carne", "descrizione": "Carne salata - 1kg a persona/settimana"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/carne_2.png"), "button": pygame.image.load("assets/cibo/button/carne_2_button.png")}
    },
    {
        "stats": {"heal": 0, "cost": 5, "saturazione": 2, "verdura": False},
        "meta": {"rarity": "comune", "categoria": "scorta"},
        "info": {"name": "pane", "descrizione": "Pane - da mangiare"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png"), "button": pygame.image.load("assets/cibo/button/pane_button.png")}
    },
    {
        "stats": {"heal": 0, "cost": 7, "saturazione": 3, "verdura": True},
        "meta": {"rarity": "comune", "categoria": "scorta"},
        "info": {"name": "legumi", "descrizione": "Legumi - da mangiare"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/legumi(piselli).png"), "button": pygame.image.load("assets/cibo/button/legumi(piselli)_button.png")}
    },

    {
        "stats": {"heal": 5, "cost": 3.5, "saturazione": 1.5, "verdura": False},
        "meta": {"rarity": "comune", "categoria": "cibo_extra"},
        "effects": {"morale": 1, "stamina": 1},
        "info": {"name": "biscotti", "descrizione": "Biscotti dolci e nutrienti"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/biscotti_png.png"), "button": pygame.image.load("assets/cibo/button/biscotti_png_button.png")}
    },
    {
        "stats": {"heal": 8, "cost": 5, "saturazione": 0.5, "verdura": False},
        "meta": {"rarity": "non_comune", "categoria": "cibo_extra"},
        "effects": {"stamina": 2},
        "info": {"name": "riso", "descrizione": "Riso basmati di alta qualità"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/riso.png"), "button": pygame.image.load("assets/cibo/button/riso_button.png")}
    },
    {
        "stats": {"heal": 9, "cost": 5, "saturazione": 1.0, "verdura": False},
        "meta": {"rarity": "non_comune", "categoria": "cibo_extra"},
        "effects": {"focus": 1, "stamina": 2},
        "info": {"name": "pesce", "descrizione": "Pesce essiccato ricco di nutrienti"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pesce.png"), "button": pygame.image.load("assets/cibo/button/pesce_button.png")}
    },
]

BIBITE = [
    {
        "stats": {"heal": 0, "cost": 3.5, "saturazione": 3.0},
        "meta": {"rarity": "comune", "categoria": "bibita"},
        "effects": {"stamina": 1},
        "info": {"name": "acqua", "descrizione": "Acqua potabile - 3 barili a persona/settimana"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png"), "button": pygame.image.load("assets/cibo/button/pane_button.png")}
    },
    {
        "stats": {"heal": 5, "cost": 3.5, "saturazione": 2.0},
        "meta": {"rarity": "comune", "categoria": "bibita"},
        "effects": {"morale": 2, "stamina": 1},
        "info": {"name": "birra", "descrizione": "Birra fresca - ottima per il morale"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png"), "button": pygame.image.load("assets/cibo/button/pane_button.png")}
    },
    {
        "stats": {"heal": 8, "cost": 5, "saturazione": 1.5},
        "meta": {"rarity": "non_comune", "categoria": "bibita"},
        "effects": {"morale": 3, "stamina": 2},
        "info": {"name": "mosto", "descrizione": "Mosto invecchiato - energetico"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png"), "button": pygame.image.load("assets/cibo/button/pane_button.png")}
    },
    {
        "stats": {"heal": 15, "cost": 7, "saturazione": 1.0},
        "meta": {"rarity": "raro", "categoria": "bibita"},
        "effects": {"morale": 5, "stamina": 3},
        "info": {"name": "vino", "descrizione": "Vino rosso pregiato - lusso puro"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png"), "button": pygame.image.load("assets/cibo/button/pane_button.png")}
    },
]


EQUIPAGGIAMENTO = [
    {
        "stats": {"heal": 15, "cost": 20, "tipo": "medicinale"},
        "meta": {"rarity": "raro"},
        "effects": {"cura_istantanea": 15, "rimuovi_malattia": 1},
        "info": {"name": "medicinale", "descrizione": "Medicinale - usato dal medico per curare l'epidemia (1 bottiglia per paziente)"},
        "sprites": {"button": pygame.image.load("assets/equip/medikit.png")}
    },
    {
        "stats": {"heal": 0, "cost": 15, "tipo": "arma"},
        "meta": {"rarity": "raro"},
        "effects": {"danno_nave": 12},
        "info": {"name": "cannone", "descrizione": "Cannone - arma per difendersi dagli attacchi pirata. Numero difensori = min(armi, membri)"},
        "sprites": {"button": pygame.image.load("assets/equip/cannone.png")}
    },
    {
        "stats": {"heal": 0, "cost": 15, "tipo": "strumento"},
        "meta": {"rarity": "non_comune"},
        "effects": {"riparazione_nave": 10},
        "info": {"name": "kit di riparazione", "descrizione": "Strumenti e materiali per riparare la nave"},
        "sprites": {"button": pygame.image.load("assets/equip/attrezzi.png")}
    },
    {
        "stats": {"heal": 0, "cost": 20, "tipo": "strumento"},
        "meta": {"rarity": "non_comune"},
        "effects": {"errore_rotta": -2},
        "info": {"name": "bussola", "descrizione": "Strumento di navigazione per orientarsi"},
        "sprites": {"button": pygame.image.load("assets/equip/bussola.png")}
    },
    {
        "stats": {"heal": 0, "cost": 5, "tipo": "strumento"},
        "meta": {"rarity": "comune"},
        "effects": {"visibilita_notte": 3},
        "info": {"name": "lanterna a olio", "descrizione": "Fonte di luce per la notte e gli interni"},
        "sprites": {"button": pygame.image.load("assets/equip/lanterna.png")}
    },
    {
        "stats": {"heal": 0, "cost": 5, "tipo": "strumento"},
        "meta": {"rarity": "comune"},
        "effects": {"raccolta_cibo_mare": 3},
        "info": {"name": "reti da pesca", "descrizione": "Utili per catturare pesce durante il viaggio"},
        "sprites": {"button": pygame.image.load("assets/equip/rete_da_pesca.png")}
    },
    {
        "stats": {"heal": 0, "cost": 5, "tipo": "strumento"},
        "meta": {"rarity": "comune"},
        "effects": {"perdita_cibo": -2},
        "info": {"name": "trappola per ratti", "descrizione": "Mantiene pulita la stiva eliminando infestazioni"},
        "sprites": {"button": pygame.image.load("assets/equip/trappola_topi.png")}
    },
    {
        "stats": {"heal": 0, "cost": 50, "tipo": "strumento"},
        "meta": {"rarity": "epico"},
        "effects": {"chance_tesoro": 5},
        "info": {"name": "mappa del tesoro", "descrizione": "Indica possibili rotte e tesori nascosti"},
        "sprites": {"button": pygame.image.load("assets/equip/mappa_tesoro.png")}
    },
    {
        "stats": {"heal": 15, "cost": 50, "tipo": "bevanda"},
        "meta": {"rarity": "non_comune"},
        "effects": {"morale_ciurma": 4, "disciplina": -1},
        "info": {"name": "barile di rum", "descrizione": "Scorta di rum per la ciurma"},
        "sprites": {"button": pygame.image.load("assets/equip/barile_rum.png")}
    },
]


EVENTI = [
    {
        "nome": "UOMO IN MARE",
        "descrizione": "Un membro a caso dell'equipaggio è caduto in mare e muore. La sua paga verrà corrisposta a fine viaggio.",
        "funzione": gestione_eventi.uomoInMare,
        "ruolo_richiesto": None,
        "sprites": {"idle1": [pygame.image.load(f"assets/eventi/caduta_personaggio/carpe/mozzoidle{i}.png") for i in range(1, 4)],
                    "idle2": [pygame.image.load(f"assets/eventi/caduta_personaggio/cuoco/cuocoidleg{i}.png") for i in range(1, 7)],}
    },
    {
        "nome": "VERDURA IN MARE",
        "descrizione": "Una violenta tempesta disperde una parte della quota di verdura in mare (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.verduraInMare,
        "ruolo_richiesto": None,
        "sprites": {"verdura": [pygame.image.load("assets/eventi/cadutaverdura/legumi(piselli).png")]}
    },
    {
        "nome": "FRUTTA IN MARE",
        "descrizione": "Una violenta tempesta disperde una parte della quota di frutta in mare (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.fruttaInMare,
        "ruolo_richiesto": None,
        "sprites": {"frutta": [pygame.image.load("assets/eventi/caduta_frutta/banane.png")]}
    },
    {
        "nome": "CARNE IN MARE",
        "descrizione": "Una violenta tempesta disperde una parte della quota di carne in mare (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.carneInMare,
        "ruolo_richiesto": None,
        "sprites": {"carne": [pygame.image.load("assets/eventi/caduta_carne/carne_2.png")]}
    },
    {
        "nome": "ACQUA IN MARE",
        "descrizione": "Una violenta tempesta disperde una parte della quota di acqua in mare (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.acquaInMare,
        "ruolo_richiesto": None,
        "sprites": {"acqua": [pygame.image.load("assets/eventi/caduta_acqua/acqua.png")]}
    },
    {
        "nome": "PESCA MIRACOLOSA",
        "descrizione": "Durante una settimana di quiete l'equipaggio ne approfitta per pescare. La scorta di carne viene incrementata casualmente (11-20 kg).",
        "funzione": gestione_eventi.pescaMiracolosa,
        "ruolo_richiesto": None,
    },
    {
        "nome": "TEMPESTA MIRACOLOSA",
        "descrizione": "Durante una tempesta alcuni uomini coraggiosi raccolgono acqua nei barili vuoti. La scorta di acqua viene incrementata casualmente (11-20 barili).",
        "funzione": gestione_eventi.anima_caduta_robe_in_mare,
        "ruolo_richiesto": None,
        "sprites": {"barile": [pygame.image.load("assets/eventi/tempesta_miracolosa/barile.png")]}
    },
    {
        "nome": "VENTI FAVOREVOLI",
        "descrizione": "Un vento favorevole accorcia il viaggio di una settimana. L'equipaggio guadagna tra 5 e 15 punti di morale.",
        "funzione": gestione_eventi.ventiFavorevoli,
        "ruolo_richiesto": None,
    },
    {
        "nome": "CATTIVO TEMPO",
        "descrizione": "Il cattivo tempo rovescia una parte delle bottiglie di medicinale (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.cattivoTempo,
        "ruolo_richiesto": None,
    },
    {
        "nome": "ONDATA",
        "descrizione": "Un'onda altissima rovescia una parte delle armi in mare (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.ondata,
        "ruolo_richiesto": None,
    },
    {
        "nome": "INFESTAZIONE RATTI",
        "descrizione": "I ratti rovinano alcune stoffe (1/2, 1/3, 1/4 o 1/5).",
        "funzione": gestione_eventi.infestazioneRatti,
        "ruolo_richiesto": None,
        "sprites": {"run up": [pygame.image.load(f"assets/eventi/infestazioneratti/runuptopo/runuptopo{i}.png") for i in range(1, 5)],
                    "run down": [pygame.image.load(f"assets/eventi/infestazioneratti/rundowtopo/rundowtopo{i}.png") for i in range(1, 5)],
                    "run right": [pygame.transform.flip(pygame.image.load(f"assets/eventi/infestazioneratti/rundirectiontopo/runrighttopo{i}.png"), True, False) for i in range(1, 5)],
                    "run left": [pygame.transform.flip(pygame.image.load(f"assets/eventi/infestazioneratti/rundirectiontopo/runrighttopo{i}.png"), False, False) for i in range(1, 5)],     
        }
    },
    {
        "nome": "AVVISTAMENTO ALBATRO",
        "descrizione": (
            "Segno di buon presagio. Se il giocatore ha almeno un'arma, può tentare di abbatterlo. "
            "Tentativi = min(armi, membri vivi). 50% successo per colpo. "
            "Se abbattuto: +10/15 kg di carne, ma le armi usate vengono rimosse (non barattabili). "
            "NASCOSTO: Uccidere un albatro attira sfortuna (aumenta punti ammutinamento). "
            "L'evento può capitare fino a 3 volte."
        ),
        "funzione": gestione_eventi.avvistamentoAlbatros,
        "ruolo_richiesto": None,
        "sprites": {"run right": [pygame.image.load(f"assets/eventi/albatro/animazione/albatro{i}.png") for i in range(1, 20)]},
    },
    {
        "nome": "AVVISTAMENTO SCIALUPPA",
        "descrizione": (
            "Una scialuppa alla deriva con 4 naufraghi e una cassa misteriosa. "
            "Salvataggio: +4 membri (ruolo casuale, morale 25-75, NON pagati a fine viaggio). "
            "La cassa: +10-20 unità per ogni tipo di merce (armi, stoffe, sale, coltelli, diamanti)."
        ),
        "funzione": gestione_eventi.avvistamentoScialuppa,
        "ruolo_richiesto": None,
    },
    {
        "nome": "EPIDEMIA",
        "descrizione": (
            "Ogni membro NON medico ha il 70% di contrarre l'epidemia e morire. "
            "Con almeno un medico E almeno un medicinale: 1 bottiglia cura 1 paziente. "
            "Senza medico: morte certa per i malati."
        ),
        "funzione": gestione_eventi.epidemia,
        "ruolo_richiesto": "medico",
    },
    {
        "nome": "ATTACCO PIRATA",
        "descrizione": (
            "Una banda di 3-10 pirati attacca. "
            "Difensori = min(cannoni/armi, marinai/membri vivi). "
            "Uomini persi = min(pirati - difensori, membri totali). "
            "Se <= 0: vittoria. Altrimenti perdita membri casuali. "
            "Le armi usate vengono rimosse (non barattabili)."
        ),
        "funzione": gestione_eventi.attaccoPirata,
        "ruolo_richiesto": "marinaio",
        "sprites": {"proiettile": [pygame.image.load(f"assets/eventi/attacco_pirata/proiettile{i}.png") for i in range(1, 8)]}
    },
    {
        "nome": "DANNI AL TIMONE",
        "descrizione": (
            "L'urto con uno scoglio danneggia il timone. "
            "Con Meccanico: +1 settimana. "
            "Senza Meccanico: +2-4 settimane (gli altri tentano di sistemare)."
        ),
        "funzione": gestione_eventi.danniAlTimone,
        "ruolo_richiesto": "meccanico",
    },
    {
        "nome": "RAFFICHE DI VENTO",
        "descrizione": (
            "Forti raffiche di vento allontanano la nave dalla rotta. "
            "Con Navigatore: +1 settimana. "
            "Senza Navigatore: +2-4 settimane (si gira a vuoto)."
        ),
        "funzione": gestione_eventi.rafficheDiVento,
        "ruolo_richiesto": "navigatore",
        "sprites": {"vento": [pygame.transform.flip(pygame.image.load(f"assets/eventi/venti/soffio/vento{i}.png"), True, False) for i in range(1, 9)]}
    },
    {"nome":    "VENTO FAVOREVOLE",
     "descrizione": "Un vento favorevole accorcia il viaggio di una settimana. L'equipaggio guadagna tra 5 e 15 punti di morale.",
     "sprites": {"vento": [pygame.image.load(f"assets/eventi/venti/soffio/vento{i}.png") for i in range(1, 9)]},
    },
    {
        "nome": "AVVISTAMENTO ISOLA",
        "descrizione": (
            "Isola avvistata. Approdare? (+1-2 settimane). "
            "50% abitata. Se abitata: 50% ostili (solo fuga). "
            "Se abitata e amichevole: +5-20 unità di ogni merce. "
            "Se albatro avvistato (senza uccisioni): +20-40 unità."
        ),
        "funzione": gestione_eventi.avvistamentoIsola,
        "ruolo_richiesto": None,
        "sprites": {"isola": [pygame.image.load(f"assets/eventi/isola/isola{i}.png") for i in range(1, 3)]}
    },
    {
        "nome": "NESSUN IMPREVISTO",
        "descrizione": "Non succede nulla in questa settimana.",
        "funzione": gestione_eventi.nessunoImprevisto,
        "ruolo_richiesto": None,
    },
]

BARCA_POS=[
((HEIGHT//2)-(HEIGHT//16)+(510*MOD),(HEIGHT//2)-(HEIGHT//16)-(79*MOD)),
(((HEIGHT//2)-(HEIGHT//16)+(510*MOD))+63*MOD,((HEIGHT//2)-(HEIGHT//16)-(79*MOD))-22*MOD),
(((HEIGHT//2)-(HEIGHT//16)+(510*MOD))+120*MOD,((HEIGHT//2)-(HEIGHT//16)-(79*MOD))-20*MOD),
(((HEIGHT//2)-(HEIGHT//16)+(510*MOD))+120*MOD,((HEIGHT//2)-(HEIGHT//16)-(79*MOD))+12*MOD),
(((HEIGHT//2)-(HEIGHT//16)+(510*MOD))+120*MOD,((HEIGHT//2)-(HEIGHT//16)-(79*MOD))+32*MOD),
((HEIGHT//2)+(230*MOD),(HEIGHT//2)-(HEIGHT//16)-(50*MOD)),
((HEIGHT//2)-(HEIGHT//16)+(390*MOD),(HEIGHT//2)-(HEIGHT//16)-(40*MOD)),
(((((HEIGHT//2)-(HEIGHT//16)+(440*MOD)) + ((HEIGHT//2)+(215*MOD))) // 2)-10*MOD,((HEIGHT//2)-(HEIGHT//16)-(10*MOD))-40*MOD),#cc
((HEIGHT//2)-(HEIGHT//16)+(110*MOD),(HEIGHT//2)-(HEIGHT//16)-(30*MOD)),
((HEIGHT//2)-(HEIGHT//16)+(205*MOD),(HEIGHT//2)-(HEIGHT//16)-(20*MOD)),
((HEIGHT//2)-(HEIGHT//16)+(440*MOD),(HEIGHT//2)-(HEIGHT//16)-(10*MOD)),#aa
(((((HEIGHT//2)-(HEIGHT//16)+(440*MOD)) + ((HEIGHT//2)+(215*MOD))) // 2)-10*MOD,((HEIGHT//2)-(HEIGHT//16)-(10*MOD))+15*MOD),#dd
((HEIGHT//2)+(215*MOD),(HEIGHT//2)-(HEIGHT//16)),#bb
((HEIGHT//2)-(HEIGHT//16)+(408*MOD),(HEIGHT//2)-(HEIGHT//16)),
(((HEIGHT//2)-(HEIGHT//16)+(110*MOD))-60*MOD, ((HEIGHT//2)-(HEIGHT//16)-(30*MOD))-13*MOD),
(((HEIGHT//2)-(HEIGHT//16)+(110*MOD))-60*MOD, ((HEIGHT//2)-(HEIGHT//16)-(30*MOD))-40*MOD)
]