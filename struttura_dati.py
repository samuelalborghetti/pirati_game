import pygame
import json
IMPOSTAZIONI = "./dati/setting.json"

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads(info)
    file.close()
    return dati["height"], dati["width"], dati["audio"], dati["mod"]

HEIGHT, WIDTH, VOLUME, MOD = CaricaSettings(IMPOSTAZIONI)

WIDTH_BUTTON = 90 * MOD
HEIGHT_BUTTON = 115 * MOD
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
            "idle": [pygame.image.load(f"assets/personaggi/capitano/idle/capitanoidle{i}.png") for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png") for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png") for i in range(1, 6)],
            "button": pygame.image.load("assets/tasti/button_capitan.png"),
        },
        "info": {
            "name": "Capitano",
            "descrizione": "Ormai dopo tante avventure pericolose in cui si rischia la pelle, la ha persa veramente. Ma la morte stessa ha rifiutato di tenerlo — troppo testardo anche per l'aldilà. Ora naviga senza carne, senza paura, senza niente da perdere. Il mare lo teme ancora.",
            "abilita": "Non mangia, non beve, potrebe improvvisamente ridursi a poche ossa",
        },
    },
    {
        "stats": {"cost": 400, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16)+(205*MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (20*MOD),
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
            "descrizione": "Un piccolo maiale che prepara piatti stellati. Menomale che non è grosso sennò li mangerebbe anche. Nessuno sa come un maiale abbia imparato a cucinare, nessuno osa chiederglielo — non quando è lui a decidere cosa finisce nel piatto e cosa finisce come piatto.",
            "abilita": "se mangi con il cuoco a bordo le porzioni valgono doppio. Il cibo dura il doppio con metà delle scorte.",
        },
    },
    {
        "stats": {"cost": 400, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (100 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (20 * MOD),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png") for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png") for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png") for i in range(1, 8)],
            "button": pygame.image.load("assets/tasti/button_guardone.png"),
        },
        "info": {
            "name": "Guardone",
            "descrizione": "Un piccolo occhio molto fortunato. Se dovesse tirare una freccetta centrerebbe sicuramente il centro, peccato non abbia le mani. Vede tutto — tempeste in arrivo, navi nemiche all'orizzonte, il futuro stesso. L'unico problema è che per indicare la rotta deve ammiccare nella direzione giusta e sperare che qualcuno capisca.",
            "abilita": "Ogni settimana rivela l'evento prima che accada. Puoi prepararti o evitarlo completamente una volta per run.",
        },
    },
    {
        "stats": {"cost": 400, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) + (230*MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (50 * MOD),
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
            "descrizione": "Piccolo, rotondo, con quel cappello che sembra più un fungo che una divisa da medico — il che in realtà ha senso. Ha guarito più malattie con i suoi funghi magici che qualsiasi medicina convenzionale. L'unico dottore al mondo che invece di prescrivere pillole ti lancia un fungo in faccia e giura che funziona. E funziona.",
            "abilita": "Ogni membro curato da lui riceve +1 HP massimo permanente per il resto della run.",
        },
    },
    {
        "stats": {"cost": 300, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (390 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (40 * MOD),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png") for i in range(1, 4)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png") for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png") for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png") for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_mozzo.png"),
        },
        "info": {
            "name": "Mozzo",
            "descrizione": "Il pirata più sfigato dei sette mari. Ha provato a fare il capitano — la nave è affondata. Ha provato a fare il cannoniere — si è sparato su un piede. Ora fa il mozzo e stranamente in questo riesce, probabilmente perché l'unica cosa che gli viene chiesta è di non combinare disastri troppo grossi. Ci riesce. A malapena.",
            "abilita": "Anni di pasti orribili lo hanno temprato. Consuma solo 0.5 porzioni e non si ammala mai di scorbuto — il suo corpo ha rinunciato ad avere standard.",
        },
    },
    {
        "stats": {"cost": 500, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (408 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16),
        },
        "sprites": {
            "idle": [pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png") for i in range(1, 5)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png") for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png") for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png") for i in range(1, 5)],
            "button": pygame.image.load("assets/tasti/button_carpentiere.png"),
        },
        "info": {
            "name": "Carpentiere",
            "descrizione": "Non parla. Non esprime emozioni. Non fa domande. Gli dai dei blocchi di legno e in trenta secondi hai una nave nuova — non chiedergli come, non chiedergli perché. È arrivato a bordo dal nulla, probabilmente scavando dal basso, e da quel giorno la nave non ha mai avuto un buco che durasse più di un turno. L'unico membro dell'equipaggio che guarda un albero e vede già una scialuppa.",
            "abilita": "La vita della nave non scende mai sotto 1 finché Steve è vivo. Ripara tutto in silenzio prima che affondi davvero.",
        },
    },
    {
        "stats": {"cost": 200, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (440 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (10*MOD),
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
            "descrizione": "Non sa combattere, non sa navigare, non sa riparare niente. Sa però cantare — e stranamente a bordo di una nave in mezzo all'oceano, dopo settimane di tempeste e razioni dimezzate, una buona canzone vale quanto un medikit. Nessuno lo ammetterebbe mai. Ma quando smette di suonare il morale crolla e tutti lo sanno.",
            "abilita": "Il morale non scende mai sotto 2 finché il Bardo è vivo e in salute.",
        },
    },
    {
        "stats": {"cost": 200, "hp": 3, "alive": True},
        "pos": {
            "x": WIDTH // 10,
            "y": (HEIGHT // 2) + (HEIGHT // 10),
            "x_fine": (WIDTH // 2) + (WIDTH // 10),
            "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            "x_barca": (HEIGHT // 2) - (HEIGHT // 16) + (510 * MOD),
            "y_barca": (HEIGHT // 2) - (HEIGHT // 16) - (79*MOD),
            "x_y_card": (10*MOD, 495*MOD),
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
            "descrizione": "ex banchiere, ha perso tutto al gioco e ora si è unito a una ciurma di pirati per cercare tesori, diamanti e ricchezze. Non è molto abile in niente, ma sa contare i soldi meglio di chiunque altro. Se c'è un tesoro da trovare, è lui che lo trova. Se c'è un tesoro da nascondere, è lui che lo nasconde. Se c'è un tesoro da spendere, è lui che lo spende.",
            "abilita": "ogni tanto trova un tesoro nascosto a bordo che contiene cibo o equipaggiamento.",
        },
    },
]

CIBO = [
    {
        "stats": {"heal": 5, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"morale": 1, "stamina": 1},
        "info": {"name": "biscotti", "descrizione": "Biscotti dolci e nutrienti"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/biscotti_png.png"), "button": pygame.image.load("assets/cibo/button/biscotti_png_button.png")}
    },
    {
        "stats": {"heal": 5, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"morale": 1},
        "info": {"name": "pane", "descrizione": "Pane fresco e nutriente"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png"), "button": pygame.image.load("assets/cibo/button/pane_button.png")}
    },
    {
        "stats": {"heal": 8, "cost": 20},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 2},
        "info": {"name": "riso", "descrizione": "Riso basmati di alta qualità"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/riso.png"), "button": pygame.image.load("assets/cibo/button/riso_button.png")}
    },
    {
        "stats": {"heal": 7, "cost": 15},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 2, "salute_max_temp": 1},
        "info": {"name": "legumi", "descrizione": "Legumi secchi ricchi di proteine",},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/legumi(piselli).png"), "button": pygame.image.load("assets/cibo/button/legumi(piselli)_button.png")}
    },
    {
        "stats": {"heal": 10, "cost": 25},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 3},
        "info": {"name": "carne", "descrizione": "Carne salata conservata per i lunghi viaggi"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/carne_2.png"), "button": pygame.image.load("assets/cibo/button/carne_2_button.png")}
    },
    {
        "stats": {"heal": 9, "cost": 20},
        "meta": {"rarity": "non_comune"},
        "effects": {"focus": 1, "stamina": 2},
        "info": {"name": "pesce", "descrizione": "Pesce essiccato ricco di nutrienti"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pesce.png"), "button": pygame.image.load("assets/cibo/button/pesce_button.png")}
    },
    {
        "stats": {"heal": 6, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"scorbuto_resistenza": 2},
        "info": {"name": "frutta", "descrizione": "Frutta fresca per recuperare energie"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/banane.png"), "button": pygame.image.load("assets/cibo/button/banane_button.png")}
    },
    {
        "stats": {"heal": 6, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"scorbuto_resistenza": 2, "morale": 1},
        "info": {"name": "verdura", "descrizione": "Verdura fresca per una dieta bilanciata"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/carote.png"), "button": pygame.image.load("assets/cibo/button/carote_button.png")}
    },
]

EQUIPAGGIAMENTO = [
    {
        "stats": {"heal": 15, "cost": 50},
        "meta": {"rarity": "raro"},
        "effects": {"cura_istantanea": 15, "rimuovi_malattia": 1},
        "info": {"name": "medikit", "descrizione": "Kit medico per curare ferite e malanni"},
        "sprites": {"button": pygame.image.load("assets/equip/medikit.png")}
    },
    {
        "stats": {"heal": 0, "cost": 100},
        "meta": {"rarity": "raro"},
        "effects": {"danno_nave": 12},
        "info": {"name": "cannone", "descrizione": "Arma pesante per attacchi navali"},
        "sprites": {"button": pygame.image.load("assets/equip/cannone.png")}
    },
    #{
        #"stats": {"heal": 0, "cost": 5},
        #"meta": {"rarity": "comune"},
        #"effects": {"ammo_cannone": 1},
        #"info": {"name": "palla di cannone", "descrizione": "Munizione per il cannone di bordo"},
        #"sprites": {"button": pygame.image.load("assets/equip/barile_rum.png")}
    #},
    #{
        #"stats": {"heal": 0, "cost": 20},
        #"meta": {"rarity": "non_comune"},
        #"effects": {"attacco_boarding": 4},
        #"info": {"name": "sciabole", "descrizione": "Lame da combattimento ravvicinato"},
        #"sprites": {"button": pygame.image.load("assets/equip/spade.png")}
    #},
    #{
        #"stats": {"heal": 0, "cost": 30},
        #"meta": {"rarity": "non_comune"},
        #"effects": {"attacco_distanza": 3, "precisione": 2},
        #"info": {"name": "balestra", "descrizione": "Arma a distanza precisa e silenziosa"},
        #"sprites": {"button": pygame.image.load("assets/equip/balestra_1.png")}
    #},
    {
        "stats": {"heal": 0, "cost": 15},
        "meta": {"rarity": "non_comune"},
        "effects": {"riparazione_nave": 10},
        "info": {"name": "kit di riparazione", "descrizione": "Strumenti e materiali per riparare la nave"},
        "sprites": {"button": pygame.image.load("assets/equip/attrezzi.png")}
    },
    #{
        #"stats": {"heal": 0, "cost": 10},
        #"meta": {"rarity": "comune"},
        #"effects": {"raccolta_legno": 3, "attacco_boarding": 1},
        #"info": {"name": "ascia", "descrizione": "Attrezzo robusto per lavori pesanti"},
        #"sprites": {"button": pygame.image.load("assets/equip/barile_rum.png")}
    #},
    #{
        #"stats": {"heal": 0, "cost": 10},
        #"meta": {"rarity": "comune"},
        #"effects": {"stabilita_nave": 3},
        #"info": {"name": "ancora", "descrizione": "Serve per fermare la nave in sicurezza"},
        #"sprites": {"button": pygame.image.load("assets/equip/ancora.png")}
    #},
    {
        "stats": {"heal": 0, "cost": 15},
        "meta": {"rarity": "non_comune"},
        "effects": {"errore_rotta": -2},
        "info": {"name": "bussola", "descrizione": "Strumento di navigazione per orientarsi"},
        "sprites": {"button": pygame.image.load("assets/equip/bussola.png")}
    },
    {
        "stats": {"heal": 0, "cost": 5},
        "meta": {"rarity": "comune"},
        "effects": {"visibilita_notte": 3},
        "info": {"name": "lanterna a olio", "descrizione": "Fonte di luce per la notte e gli interni"},
        "sprites": {"button": pygame.image.load("assets/equip/lanterna.png")}
    },
    {
        "stats": {"heal": 0, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"raccolta_cibo_mare": 3},
        "info": {"name": "reti da pesca", "descrizione": "Utili per catturare pesce durante il viaggio"},
        "sprites": {"button": pygame.image.load("assets/equip/rete_da_pesca.png")}
    },
    {
        "stats": {"heal": 0, "cost": 5},
        "meta": {"rarity": "comune"},
        "effects": {"perdita_cibo": -2},
        "info": {"name": "trappola per ratti", "descrizione": "Mantiene pulita la stiva eliminando infestazioni"},
        "sprites": {"button": pygame.image.load("assets/equip/trappola_topi.png")}
    },
    {
        "stats": {"heal": 0, "cost": 50},
        "meta": {"rarity": "epico"},
        "effects": {"chance_tesoro": 5},
        "info": {"name": "mappa del tesoro", "descrizione": "Indica possibili rotte e tesori nascosti"},
        "sprites": {"button": pygame.image.load("assets/equip/mappa_tesoro.png")}
    },
    #{
        #"stats": {"heal": 0, "cost": 100},
        #"meta": {"rarity": "raro"},
        #"effects": {"intimidazione": 3, "morale_ciurma": 2},
        #"info": {"name": "bandiera pirata", "descrizione": "Simbolo della ciurma e della sua fama"},
        #"sprites": {"button": pygame.image.load("assets/equip/bandiera.png")}
    #},
    {
        "stats": {"heal": 15, "cost": 50},
        "meta": {"rarity": "non_comune"},
        "effects": {"morale_ciurma": 4, "disciplina": -1},
        "info": {"name": "barile di rum", "descrizione": "Scorta di rum per la ciurma"},
        "sprites": {"button": pygame.image.load("assets/equip/barile_rum.png")}
    },
]