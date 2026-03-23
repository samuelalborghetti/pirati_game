import pygame

pygame.init()

LARGHEZZA = 1200
ALTEZZA = 800
ROSSO = (255, 0, 0)

personaggi = [
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/capitano/idle/capitanoidle{i}.png") for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"allframe/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png") for i in range(1, 5)],
            "walk_cycle_sick":   [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png") for i in range(1, 6)]
            
        },
        "info": {
            "name":        "Capitano",
            "descrizione": "",
            "abilita":     ""
        }
    },
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/cuoco/idle/cuocoidle{i}.png") for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"allframe/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png") for i in range(1, 3)],
            "walk_cycle":   [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png") for i in range(1, 7)]
        },
        "info": {
            "name":        "Cuoco",
            "descrizione": "",
            "abilita":     ""
        }
    },
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/guardone/idle/guardoneidle{i}.png") for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png") for i in range(1, 8)]
        },
        "info": {
            "name":        "Guardone",
            "descrizione": "",
            "abilita":     ""
        }
    },
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {
        "stats": {
            "cost": None,
            "hp": 3,
            "alive": True
        },
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/medico/idle/medicoidle{i}.png") for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/medico/camminata_in_avanti/medico{i}_camminatainavanti.png") for i in range(1, 9)],
            "walk_cycle":   [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png") for i in range(1, 7)],
            "walk_cycle_sick":   [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png") for i in range(1, 7)]
        },
        "info": {
            "name":        "Medico",
            "descrizione": "",
            "abilita":     ""
        }
    },
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
]

sfondo = pygame.image.load("generale/sfondo_pirati.jpg")
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo ROSSO")
clock = pygame.time.Clock()


def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64, 78), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)


gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    schermo.fill(ROSSO)

    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_forward", 150, (50, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle",   150, (150, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle",   150, (250, 100), flip=True)
    disegna_animazione(schermo, personaggi[0]["sprites"], "idle",         200, (350, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle_sick", 150, (450, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle_sick", 150, (550, 100), flip = True)
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_forward", 200, (700, 100), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle",   170, (800, 100), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle",   170, (900, 100), (54, 74), flip=True)
    disegna_animazione(schermo, personaggi[1]["sprites"], "idle",         150, (1000, 100), (54, 74))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_forward", 150, (200, 200), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle",   110, (300, 200), (64, 78), flip=True)
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle",   110, (400, 200), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "idle",         150, (500, 200), (64, 78))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_forward", 120, (650, 200), (60, 74))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle",   140, (750, 200), (60, 80))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle",   140, (850, 200), (60, 80), flip=True)
    disegna_animazione(schermo, personaggi[3]["sprites"], "idle",         135, (945, 197), (66, 76))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle_sick", 140, (1040, 200), (60, 80))
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_cycle_sick", 140, (1140, 200), (60, 80), flip = True)

    pygame.display.update()
    clock.tick(60)

pygame.quit()