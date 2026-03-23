import pygame

pygame.init()

LARGHEZZA = 1200
ALTEZZA = 800
NERO = (155, 0, 0)

personaggi = [
    {
        "name": "Capitano",
        "cost": 380,
        "hp": 3,
        "alive": True,
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/capitano/idle/capitanoidle{i}.png") for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"allframe/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png") for i in range(1, 5)]
        }
    },
    {
        "name": "Cuoco",
        "cost": 380,
        "hp": 3,
        "alive": True,
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/cuoco/idle/cuocoidle{i}.png") for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"allframe/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png") for i in range(1, 3)],
            "walk_cycle":   [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png") for i in range(1, 7)]
        }
    },
    {
        "name": "guardone",
        "cost": 380,
        "hp": 3,
        "alive": True,
        "sprites": {
            "idle":         [pygame.image.load(f"allframe/guardone/idle/guardoneidle{i}.png") for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png") for i in range(1, 5)],
            "walk_cycle":   [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png") for i in range(1, 8)]
        }
    },
    {
        "name": "medico",
        "cost": 380,
        "hp": 3,
        "alive": True,
        "sprites": {
            "idle":         [],
            "walk_forward": [pygame.image.load(f"allframe/medico/camminata_in_avanti/medico{i}_camminatainavanti.png") for i in range(1,9)],
            "walk_cycle":   []
        }
    },
    
]

sfondo = pygame.image.load("generale/sfondo_pirati.jpg")
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo Nero")
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

    schermo.fill(NERO)

    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_forward", 150, (200, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle", 150, (300, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle", 150, (400, 100), flip=True)
    disegna_animazione(schermo, personaggi[0]["sprites"], "idle", 200, (500, 100))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_forward", 200, (700, 100), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle", 140, (800, 100), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle", 140, (900, 100), (54, 74), flip=True)
    disegna_animazione(schermo, personaggi[1]["sprites"], "idle", 150, (1000, 100), (54, 74))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_forward", 150, (200, 200), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle", 110, (300, 200), (64, 78), flip=True)
    disegna_animazione(schermo, personaggi[2]["sprites"], "walk_cycle", 110, (400, 200), (64, 78))
    disegna_animazione(schermo, personaggi[2]["sprites"], "idle", 150, (500, 200), (64, 78))
    
    disegna_animazione(schermo, personaggi[3]["sprites"], "walk_forward", 120, (700, 200), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle", 140, (800, 200), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle", 140, (900, 200), (54, 74), flip=True)
    disegna_animazione(schermo, personaggi[1]["sprites"], "idle", 150, (1000, 100), (54, 74))
    
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()