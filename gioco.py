import pygame

pygame.init()

LARGHEZZA = 1200
ALTEZZA = 800
ROSSO = (255, 0, 0)

sfondo = pygame.image.load("generale/sfondo_pirati.jpg")
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo ROSSO")
clock = pygame.time.Clock()

#------
pos_x, pos_y = 0.0, 0.0
x_fine, y_fine = 1100.0, 700.0
personaggi = [
    #--------------------------------------------------------------------------------------------capitano---------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/capitano/idle/capitanoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"allframe/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick":   [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png").convert_alpha() for i in range(1, 6)]
            
        },
        "info": {
            "name":        "Capitano",
            "descrizione": "Ormai dopo tante avventure pericolose in cui si rischia la pelle, la ha persa veramente. Ma la morte stessa ha rifiutato di tenerlo — troppo testardo anche per l'aldilà. Ora naviga senza carne, senza paura, senza niente da perdere. Il mare lo teme ancora.",
            "abilita":     "non mangia, non beve potrebe improvvisamente ridursi a poche ossa"
        }
    },
    #-------------------------------------------------------------------------------------el maiale 1--------------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/cuoco/idle/cuocoidle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"allframe/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png").convert_alpha() for i in range(1, 3)],
            "walk_cycle":   [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick":   [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)]
        },
        "info": {
            "name":        "Cuoco",
            "descrizione": "Un piccolo maiale che prepara piatti stellati. Menomale che non è grosso sennò li mangerebbe anche. Nessuno sa come un maiale abbia imparato a cucinare, nessuno osa chiederglielo — non quando è lui a decidere cosa finisce nel piatto e cosa finisce come piatto.",
            "abilita":     "se mangi con il cuoco a bordo le porzioni valgono doppio. Il cibo dura il doppio con metà delle scorte."
        }
    },
    #--------------------------------------------------------------------------------------------guardone--------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/guardone/idle/guardoneidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick":   [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)]
        },
        "info": {
            "name":        "Guardone",
            "descrizione": "Un piccolo occhio molto fortunato. Se dovesse tirare una freccetta centrerebbe sicuramente il centro, peccato non abbia le mani. Vede tutto — tempeste in arrivo, navi nemiche all'orizzonte, il futuro stesso. L'unico problema è che per indicare la rotta deve ammiccare nella direzione giusta e sperare che qualcuno capisca.",
            "abilita":     "Ogni settimana rivela l'evento prima che accada. Puoi prepararti o evitarlo completamente una volta per run."
        }
    },
    #--------------------------------------------------------------------------------------------medico---------------------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/medico/idle/medicoidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/medico/camminata_in_avanti/medico{i}_camminatainavanti.png").convert_alpha() for i in range(1, 9)],
            "walk_cycle":   [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick":   [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)]
        },
        "info": {
            "name":        "Medico",
            "descrizione": "Piccolo, rotondo, con quel cappello che sembra più un fungo che una divisa da medico — il che in realtà ha senso. Ha guarito più malattie con i suoi funghi magici che qualsiasi medicina convenzionale. L'unico dottore al mondo che invece di prescrivere pillole ti lancia un fungo in faccia e giura che funziona. E funziona.",
            "abilita":     "Ogni membro curato da lui riceve +1 HP massimo permanente per il resto della run."
        }
    },
    #----------------------------------------------------------------------------------------------------mozzo----------------------------------------------------------------------------
        {
            "stats": {
                "cost": None,
                "hp": 3,
                "alive": True
            },
            "sprites": {
                "idle":         [pygame.image.load(f"allframe/mozzo/idle/mozzoidle{i}.png").convert_alpha() for i in range(1, 4)],
                "walk_forward": [pygame.image.load(f"allframe/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png").convert_alpha() for i in range(1, 4)],
                "walk_cycle":   [pygame.image.load(f"allframe/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png").convert_alpha() for i in range(1, 4)],
                "walk_cycle_sick":   [pygame.image.load(f"allframe/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png").convert_alpha() for i in range(1, 4)]
            },
            "info": {
                "name":        "Mozzo", 
                "descrizione": "Il pirata più sfigato dei sette mari. Ha provato a fare il capitano — la nave è affondata. Ha provato a fare il cannoniere — si è sparato su un piede. Ora fa il mozzo e stranamente in questo riesce, probabilmente perché l'unica cosa che gli viene chiesta è di non combinare disastri troppo grossi. Ci riesce. A malapena.",
                "abilita":     "Anni di pasti orribili lo hanno temprato. Consuma solo 0.5 porzioni e non si ammala mai di scorbuto — il suo corpo ha rinunciato ad avere standard."
            }
        },
        #-------------------------------------------------------------------------------------------carpentiere-------------------------------------------------------------------------------------
        {
            "stats": {
                "cost": None,
                "hp": 3,
                "alive": True
            },
            "sprites": {
                "idle":         [pygame.image.load(f"allframe/carpentiere/idle/carpidle{i}.png").convert_alpha() for i in range(1, 5)],
                "walk_forward": [pygame.image.load(f"allframe/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png").convert_alpha() for i in range(1, 5)],
                "walk_cycle":   [pygame.image.load(f"allframe/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png").convert_alpha() for i in range(1, 5)],
                "walk_cycle_sick":   [pygame.image.load(f"allframe/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 5)]
            },
            "info": {
                "name":        "Carpentiere",
                "descrizione": "Non parla. Non esprime emozioni. Non fa domande. Gli dai dei blocchi di legno e in trenta secondi hai una nave nuova — non chiedergli come, non chiedergli perché. È arrivato a bordo dal nulla, probabilmente scavando dal basso, e da quel giorno la nave non ha mai avuto un buco che durasse più di un turno. L'unico membro dell'equipaggio che guarda un albero e vede già una scialuppa.",
                "abilita":     "La vita della nave non scende mai sotto 1 finché Steve è vivo. Ripara tutto in silenzio prima che affondi davvero."
            }
        },
        #--------------------------------------------------------------------------------------------bardo---------------------------------------------------------------------------------------------------
        {
            "stats": {
                "cost": None,
                "hp": 3,
                "alive": True
            },
            "sprites": {
                "idle":              [pygame.image.load(f"allframe/bardo/idle/bardoidle{i}.png").convert_alpha() for i in range(1, 3)],
                "walk_forward":      [pygame.image.load(f"allframe/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png").convert_alpha() for i in range(1, 4)],
                "walk_cycle":        [pygame.image.load(f"allframe/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png").convert_alpha() for i in range(1, 4)],
                "walk_cycle_sick":   [pygame.image.load(f"allframe/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png").convert_alpha() for i in range(1, 4)]
            },
            "info": {
                "name":        "Bardo",
                "descrizione": "Non sa combattere, non sa navigare, non sa riparare niente. Sa però cantare — e stranamente a bordo di una nave in mezzo all'oceano, dopo settimane di tempeste e razioni dimezzate, una buona canzone vale quanto un medikit. Nessuno lo ammetterebbe mai. Ma quando smette di suonare il morale crolla e tutti lo sanno.",
                "abilita":     "Il morale non scende mai sotto 2 finché il Bardo è vivo e in salute."
            }
        },
]



def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64, 78), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)
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
    



gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    schermo.fill(ROSSO)
    #---------------------------------------------------------------------------capitano----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_forward", 150, (50, 50))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle",   150, (150, 50))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle",   150, (250, 50), flip=True)
    disegna_animazione(schermo, personaggi[0]["sprites"], "idle",         200, (350, 50))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle_sick", 150, (450, 50))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle_sick", 150, (550, 50), flip = True)

    #---------------------------------------------------------------------------maile----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_forward", 200, (650, 50), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle",   170, (750, 50), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle",   170, (850, 50), (54, 74), flip=True)
    disegna_animazione(schermo, personaggi[1]["sprites"], "idle",         150, (945, 50), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle_sick",   170, (1040, 50), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle_sick",   170, (1140, 50), (54, 74), flip=True)

    #---------------------------------------------------------------------------guardone----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_forward", 150, (50, 150), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle",   110, (150, 150), (64, 78), flip=True)
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle",   110, (250, 150), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "idle",         150, (350, 150), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle_sick",   110, (550, 150), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle_sick",   110, (450, 150), (64, 78), flip=True)

    #---------------------------------------------------------------------------medico----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_forward", 120, (650, 150), (60, 74))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle",   140, (750, 150), (60, 80))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle",   140, (850, 150), (60, 80), flip=True)
    disegna_animazione(schermo, personaggi[3]["sprites"], "idle",         135, (945, 147), (66, 76))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle_sick", 140, (1040, 150), (60, 80))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle_sick", 140, (1140, 150), (60, 80), flip = True)
    #---------------------------------------------------------------------------mozzo----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[4]["sprites"], "walk_forward", 150, (50, 250), (58, 63))
    disegna_animazione(schermo, personaggi[4]["sprites"], "walk_cycle",   150, (150, 250), (62, 68), flip=True)
    disegna_animazione(schermo, personaggi[4]["sprites"], "walk_cycle",   150, (250, 250), (62, 68))
    disegna_animazione(schermo, personaggi[4]["sprites"], "idle",         150, (350, 250), (58, 68))
    disegna_animazione(schermo, personaggi[4]["sprites"], "walk_cycle_sick",   150, (450, 250), (62, 68),flip=True)
    disegna_animazione(schermo, personaggi[4]["sprites"], "walk_cycle_sick",   150, (550, 250), (62, 68))
#---------------------------------------------------------------------------carpentiere----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[5]["sprites"], "walk_forward",    150, (50,  350), (64, 78))
    disegna_animazione(schermo, personaggi[5]["sprites"], "walk_cycle",      150, (150, 350), (64, 78))
    disegna_animazione(schermo, personaggi[5]["sprites"], "walk_cycle",      150, (250, 350), (64, 78), flip=True)
    disegna_animazione(schermo, personaggi[5]["sprites"], "idle",            150, (350, 350), (64, 78))
    disegna_animazione(schermo, personaggi[5]["sprites"], "walk_cycle_sick", 150, (450, 350), (64, 78))
    disegna_animazione(schermo, personaggi[5]["sprites"], "walk_cycle_sick", 150, (550, 350), (64, 78), flip=True)
    #---------------------------------------------------------------------------bardo----------------------------------------------------------------------------------------------------
    disegna_animazione(schermo, personaggi[6]["sprites"], "walk_forward",    150, (50,  450), (58, 78))
    disegna_animazione(schermo, personaggi[6]["sprites"], "walk_cycle",      150, (150, 450), (58, 78))
    disegna_animazione(schermo, personaggi[6]["sprites"], "walk_cycle",      150, (250, 450), (58, 78), flip=True)
    disegna_animazione(schermo, personaggi[6]["sprites"], "idle",            150, (350, 450), (70, 78))
    disegna_animazione(schermo, personaggi[6]["sprites"], "walk_cycle_sick", 150, (450, 450), (58, 78))
    disegna_animazione(schermo, personaggi[6]["sprites"], "walk_cycle_sick", 150, (550, 450), (58, 78), flip=True)
    (pos_x, pos_y) = spostamento_pos_to_pos(pos_x, x_fine, pos_y, y_fine, 3)
    disegna_animazione(schermo, personaggi[6]["sprites"], "walk_cycle_sick", 150,(pos_x,pos_y), (58, 78))
    pygame.display.update()
    clock.tick(60)

pygame.quit()