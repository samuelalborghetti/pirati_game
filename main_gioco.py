import pygame
import json

pygame.init()

IMPOSTAZIONI = "./dati/setting.json"
ROSSO = (255, 0, 0)

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.load(file)
    file.close()
    return dati["width"], dati["height"], dati["audio"], dati["mod"]


WIDTH, HEIGHT, VOLUME, MOD = CaricaSettings(IMPOSTAZIONI)
WIDTH_BUTTON = 90 * MOD
HEIGHT_BUTTON = 115 * MOD
WIDTH_INFO_CHARACHTER = 380 * MOD
HEIGHT_INFO_CHARACHETER = 220 * MOD

schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the see")

pygame.mixer.music.load("./assets/music/menu_music.mp3")
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)

bg = pygame.image.load("assets/sfondi/default1.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bottone_marrone = pygame.image.load("assets/tasti/arrow_left.png").convert_alpha()
clock = pygame.time.Clock()
font_numeri = pygame.font.Font("assets/fonts/Barrio-Regular.ttf", 24 * MOD)
title_font = pygame.font.Font ("assets/fonts/PixelifySans-Medium.ttf", 18)
info_font = pygame.font.Font("assets/fonts/PixelifySans-SemiBold.ttf", 14 * MOD)

categoria_attiva = "personaggi"
cibo_scelto = []
personaggi_selezionati = []
pers_in_movimento = []
equip_scelto = []
soldi_iniziali = 2000
controllo = False
arrivato = False
timeout_cibo = 0

BUTTON_RECTS = [pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(10 * MOD, 125 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(115 * MOD, 125 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
                pygame.rect.Rect(115 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(10 * MOD, 225 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(115 * MOD, 225 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
                pygame.rect.Rect(10 * MOD, 345 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(115 * MOD, 345 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON), pygame.rect.Rect(10 * MOD, 445 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)]

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
            "idle": [pygame.image.load(f"assets/personaggi/cuoco/idle/cuocoidle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png").convert_alpha() for i in range(1, 3)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
            "button": pygame.image.load("assets/tasti/button_cuoco.png").convert_alpha(),
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
            "idle": [pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)],
            "button": pygame.image.load("assets/tasti/button_guardone.png").convert_alpha(),
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
            "idle": [pygame.image.load(f"assets/personaggi/medico/idle/medicoidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/medico/camminata_in_avanti/medico{i}_camminatainavanti.png").convert_alpha() for i in range(1, 9)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
            "button": pygame.image.load("assets/tasti/button_medico.png").convert_alpha(),
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
            "idle": [pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_mozzo.png").convert_alpha(),
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
            "idle": [pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 5)],
            "button": pygame.image.load("assets/tasti/button_carpentiere.png").convert_alpha(),
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
            "idle": [pygame.image.load(f"assets/personaggi/bardo/idle/bardoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 4)],
            "button": pygame.image.load("assets/tasti/button_bardo.png").convert_alpha(),
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
            "idle": [pygame.image.load(f"assets/personaggi/tesoriere/idle/cercatore_di_tesori_idle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"assets/personaggi/tesoriere/camminata_in_avanti/camminata_in_avanti{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle": [pygame.image.load(f"assets/personaggi/tesoriere/camminata_a_destrasinistra_con_flip/camminata_lateralec{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"assets/personaggi/tesoriere/camminata_a_destrasinistra_con_flip_ammalato/camminata_lateralecmalato{i}.png").convert_alpha() for i in range(1, 8)],
            "button": pygame.image.load("assets/tasti/button_tesoriere.png").convert_alpha(),
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
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/biscotti_png.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/biscotti_png_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 5, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"morale": 1},
        "info": {"name": "pane", "descrizione": "Pane fresco e nutriente"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pane.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/pane_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 8, "cost": 20},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 2},
        "info": {"name": "riso", "descrizione": "Riso basmati di alta qualità"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/riso.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/riso_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 7, "cost": 15},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 2, "salute_max_temp": 1},
        "info": {"name": "legumi", "descrizione": "Legumi secchi ricchi di proteine",},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/legumi(piselli).png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/legumi(piselli)_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 10, "cost": 25},
        "meta": {"rarity": "non_comune"},
        "effects": {"stamina": 3},
        "info": {"name": "carne", "descrizione": "Carne salata conservata per i lunghi viaggi"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/carne_2.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/carne_2_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 9, "cost": 20},
        "meta": {"rarity": "non_comune"},
        "effects": {"focus": 1, "stamina": 2},
        "info": {"name": "pesce", "descrizione": "Pesce essiccato ricco di nutrienti"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/pesce.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/pesce_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 6, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"scorbuto_resistenza": 2},
        "info": {"name": "frutta", "descrizione": "Frutta fresca per recuperare energie"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/banane.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/banane_button.png").convert_alpha()}
    },
    {
        "stats": {"heal": 6, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"scorbuto_resistenza": 2, "morale": 1},
        "info": {"name": "verdura", "descrizione": "Verdura fresca per una dieta bilanciata"},
        "sprites": {"sprite": pygame.image.load("assets/cibo/trasparenti/carote.png").convert_alpha(), "button": pygame.image.load("assets/cibo/button/carote_button.png").convert_alpha()}
    },
]

EQUIPAGGIAMENTO = [
    {
        "stats": {"heal": 15, "cost": 50},
        "meta": {"rarity": "raro"},
        "effects": {"cura_istantanea": 15, "rimuovi_malattia": 1},
        "info": {"name": "medikit", "descrizione": "Kit medico per curare ferite e malanni", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_medikit.png").convert_alpha()}
    },
    {
        "stats": {"heal": 0, "cost": 100},
        "meta": {"rarity": "raro"},
        "effects": {"danno_nave": 12},
        "info": {"name": "cannone", "descrizione": "Arma pesante per attacchi navali", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_cannone.png").convert_alpha()}
    },
    #{
        #"stats": {"heal": 0, "cost": 5},
        #"meta": {"rarity": "comune"},
        #"effects": {"ammo_cannone": 1},
        #"info": {"name": "palla di cannone", "descrizione": "Munizione per il cannone di bordo", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        #"sprites": {"button": pygame.image.load("assets/equip/barile_rum.png").convert_alpha()}
    #},
    #{
        #"stats": {"heal": 0, "cost": 20},
        #"meta": {"rarity": "non_comune"},
        #"effects": {"attacco_boarding": 4},
        #"info": {"name": "sciabole", "descrizione": "Lame da combattimento ravvicinato", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        #"sprites": {"button": pygame.image.load("assets/equip/spade.png").convert_alpha()}
    #},
    #{
        #"stats": {"heal": 0, "cost": 30},
        #"meta": {"rarity": "non_comune"},
        #"effects": {"attacco_distanza": 3, "precisione": 2},
        #"info": {"name": "balestra", "descrizione": "Arma a distanza precisa e silenziosa", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        #"sprites": {"button": pygame.image.load("assets/equip/balestra_1.png").convert_alpha()}
    #},
    {
        "stats": {"heal": 0, "cost": 15},
        "meta": {"rarity": "non_comune"},
        "effects": {"riparazione_nave": 10},
        "info": {"name": "kit di riparazione", "descrizione": "Strumenti e materiali per riparare la nave", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_atrezzi.png").convert_alpha()}
    },
    #{
        #"stats": {"heal": 0, "cost": 10},
        #"meta": {"rarity": "comune"},
        #"effects": {"raccolta_legno": 3, "attacco_boarding": 1},
        #"info": {"name": "ascia", "descrizione": "Attrezzo robusto per lavori pesanti", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        #"sprites": {"button": pygame.image.load("assets/equip/barile_rum.png").convert_alpha()}
    #},
    #{
        #"stats": {"heal": 0, "cost": 10},
        #"meta": {"rarity": "comune"},
        #"effects": {"stabilita_nave": 3},
        #"info": {"name": "ancora", "descrizione": "Serve per fermare la nave in sicurezza", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        #"sprites": {"button": pygame.image.load("assets/equip/ancora.png").convert_alpha()}
    #},
    {
        "stats": {"heal": 0, "cost": 15},
        "meta": {"rarity": "non_comune"},
        "effects": {"errore_rotta": -2},
        "info": {"name": "bussola", "descrizione": "Strumento di navigazione per orientarsi", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_bussola.png").convert_alpha()}
    },
    {
        "stats": {"heal": 0, "cost": 5},
        "meta": {"rarity": "comune"},
        "effects": {"visibilita_notte": 3},
        "info": {"name": "lanterna a olio", "descrizione": "Fonte di luce per la notte e gli interni", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_lanterna.png").convert_alpha()}
    },
    {
        "stats": {"heal": 0, "cost": 10},
        "meta": {"rarity": "comune"},
        "effects": {"raccolta_cibo_mare": 3},
        "info": {"name": "reti da pesca", "descrizione": "Utili per catturare pesce durante il viaggio", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_rete_da_pesca.png").convert_alpha()}
    },
    {
        "stats": {"heal": 0, "cost": 5},
        "meta": {"rarity": "comune"},
        "effects": {"perdita_cibo": -2},
        "info": {"name": "trappola per ratti", "descrizione": "Mantiene pulita la stiva eliminando infestazioni", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_trappola_topi.png").convert_alpha()}
    },
    {
        "stats": {"heal": 0, "cost": 50},
        "meta": {"rarity": "epico"},
        "effects": {"chance_tesoro": 5},
        "info": {"name": "mappa del tesoro", "descrizione": "Indica possibili rotte e tesori nascosti", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_mappa_tesoro.png").convert_alpha()}
    },
    #{
        #"stats": {"heal": 0, "cost": 100},
        #"meta": {"rarity": "raro"},
        #"effects": {"intimidazione": 3, "morale_ciurma": 2},
        #"info": {"name": "bandiera pirata", "descrizione": "Simbolo della ciurma e della sua fama", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        #"sprites": {"button": pygame.image.load("assets/equip/bandiera.png").convert_alpha()}
    #},
    {
        "stats": {"heal": 15, "cost": 50},
        "meta": {"rarity": "non_comune"},
        "effects": {"morale_ciurma": 4, "disciplina": -1},
        "info": {"name": "barile di rum", "descrizione": "Scorta di rum per la ciurma", "button_rect": pygame.rect.Rect(10 * MOD, 10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON)},
        "sprites": {"button": pygame.image.load("assets/equip/button/button_barile_rum.png").convert_alpha()}
    },
]

def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def reset_posizione_personaggio(personaggio_corrente):
    personaggio_corrente["pos"]["x"] = WIDTH // 10
    personaggio_corrente["pos"]["y"] = (HEIGHT // 2) + (HEIGHT // 10)
    personaggio_corrente["pos"]["x_fine"] = (WIDTH // 2) + (WIDTH // 10)
    personaggio_corrente["pos"]["y_fine"] = (HEIGHT // 2) - (HEIGHT // 16)

def riordina_per_profondita(pers):
    for i in range(len(pers)):
        for j in range(i + 1, len(pers)):
            if pers[i]["pos"]["y"] > pers[j]["pos"]["y"]:
                pers[i], pers[j] = pers[j], pers[i]

def DrawMoney(screen, soldi_correnti):
    testo = font_numeri.render(f"Soldi: {soldi_correnti}", True, (255, 215, 0))
    rett = testo.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(testo, rett)

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)

def disegna_spostamento_personaggio(p, velocita, durata_ms, schermo, flip=False):
    x = p["pos"]["x"]
    y = p["pos"]["y"]
    x_fine = p["pos"]["x_fine"]
    y_fine = p["pos"]["y_fine"]
    if x != x_fine:
        if x < x_fine:
            x += velocita
            if p["info"]["name"] in ["Mozzo", "Guardone"]:
                flip = True
            if x > x_fine:
                x = x_fine
        elif x > x_fine:
            x -= velocita
            flip = True
            if p["info"]["name"] == "Guardone":
                flip = False
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

def Drawtext (schermo, text: list, y_in, x_testo, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        schermo.blit (testo, (x_testo, y))
        y += spazio_tra_righe

def WrapText (testo: str, font_testo, rect_testo):
    parole = testo.split (" ")
    testo_fin = ""
    riga_corrente = ""
    for parola in parole:
        prova_testo = riga_corrente + parola
        width_testo, height = font_testo.size (prova_testo)
        if width_testo > rect_testo.width - 15 * MOD:
            testo_fin += riga_corrente + "|"
            riga_corrente = parola + " " 
        else:
            riga_corrente += parola + " "
    
    testo_fin += riga_corrente
    testo_lista = testo_fin.split ("|")
    return testo_lista

def ViewInfoEquip(list_info, screen, rects_pulsanti):
    mouse_pos = pygame.mouse.get_pos()
    for pos, el in enumerate(list_info):
        if rects_pulsanti[pos].collidepoint(mouse_pos):
            rect_info = pygame.Rect(rects_pulsanti[pos].x + 100 * MOD, rects_pulsanti[pos].y, WIDTH_INFO_CHARACHTER, HEIGHT_INFO_CHARACHETER)
            pygame.draw.rect(screen, (161, 88, 0), rect_info, 0, 10)
            pygame.draw.rect(screen, (0,0,0), rect_info, 3, 10)
            nome = title_font.render(el["info"]["name"].title(), True, (255, 255, 255))
            cost = font_numeri.render(str(el["stats"]["cost"]), True, (255, 133, 122))
            screen.blit (cost, (rect_info.x + rect_info.width / 4 - cost.get_width(), rect_info.y + 10 * MOD))
            screen.blit(nome, (rect_info.x + rect_info.width/2 - nome.get_width()/2, rect_info.y + 10 * MOD))
            Drawtext (screen, WrapText (el["info"]["descrizione"], info_font, rect_info), rect_info.y + nome.get_height() * 2, rect_info.x + 10 * MOD, info_font, (255,255,255), nome.get_height() / 2)
            if list_info == PERSONAGGI:
                Drawtext (screen, WrapText (el["info"]["abilita"], info_font, rect_info), rect_info.y + rect_info.height - nome.get_height() * 2.5, rect_info.x + 10 * MOD, info_font, (255,255,255), nome.get_height() / 2)

def DrawButtonEquip(list_attiva, screen, rects_pulsanti):
    for pos, el in enumerate(list_attiva):
        button_img = pygame.transform.scale(el["sprites"]["button"], (rects_pulsanti[pos].width, rects_pulsanti[pos].height))
        screen.blit(button_img, rects_pulsanti[pos])

def nuova_destinazione(p, pers):
    riordina_per_profondita(pers)
    p["pos"]["x_fine"] = p["pos"]["x_barca"]
    p["pos"]["y_fine"] = p["pos"]["y_barca"]

def SelectCharacheters(pos_pers, pers_sel, soldi, pers_move, click_mouse, lista_personaggi):
    costo = lista_personaggi[pos_pers]["stats"]["cost"]
    p = lista_personaggi [pos_pers]
    if click_mouse[0]:
        if soldi >= costo and not p in pers_sel:
            pers_move.append(p)
            pers_sel.append(p)
            soldi -= costo
    elif click_mouse[2]:
        if p in pers_move and p in pers_sel:
            pers_move.remove(p)
            pers_sel.remove(p)
            soldi += costo
            reset_posizione_personaggio(p)
    return soldi

def SelectEquipment(pos_equip, equip_sel, soldi, mouse_click, lista_equip):
    costo = lista_equip[pos_equip]["stats"]["cost"]
    e = lista_equip[pos_equip]
    if mouse_click[0]:
        if soldi >= costo and not e in equip_sel:
            equip_sel.append(e)
            soldi -= costo
    elif mouse_click[2]:
        if e in equip_sel:
            equip_sel.remove(e)
            soldi += costo
    return soldi

def SelectCibo(pos_cibi, ciboselezionato, soldi, mouse_click, lista_cibi):
    c = lista_cibi[pos_cibi]
    costo = c["stats"]["cost"]
    if mouse_click[0]:
        if soldi >= costo:
            ciboselezionato.append(c)
            soldi -= costo
    elif mouse_click[2]:
        if c in ciboselezionato:
            ciboselezionato.remove(c)
            soldi += costo

    return soldi

schermata = 1
gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                categoria_attiva = "personaggi"
            elif event.key == pygame.K_c:
                categoria_attiva = "cibo"
            elif event.key == pygame.K_e:
                categoria_attiva = "equipaggiamento"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for pos, el in enumerate (BUTTON_RECTS):
                if el.collidepoint (mouse):
                    if categoria_attiva == "personaggi":
                        soldi_iniziali = SelectCharacheters (pos, personaggi_selezionati, soldi_iniziali, pers_in_movimento, click, PERSONAGGI)
                    elif categoria_attiva == "cibo":
                        soldi_iniziali = SelectCibo (pos, cibo_scelto, soldi_iniziali, click, CIBO)
                    elif categoria_attiva == "equipaggiamento":
                        soldi_iniziali = SelectEquipment (pos, equip_scelto, soldi_iniziali, click, EQUIPAGGIAMENTO)

    if categoria_attiva == "personaggi":
        lista_attiva = PERSONAGGI
    elif categoria_attiva == "cibo":
        lista_attiva = CIBO
    elif categoria_attiva == "equipaggiamento":
        lista_attiva = EQUIPAGGIAMENTO

    schermo.blit(bg, (0, 0))
    if len(pers_in_movimento) != 0:
        for p in pers_in_movimento:
            arrivato = disegna_spostamento_personaggio(p, 5, 150, schermo)
            if arrivato:
                nuova_destinazione(p, pers_in_movimento)
    DrawMoney(schermo, soldi_iniziali)
    DrawButtonEquip(lista_attiva, schermo, BUTTON_RECTS)
    ViewInfoEquip (lista_attiva, schermo, BUTTON_RECTS)

    pygame.display.update()
    clock.tick(60)

pygame.quit()