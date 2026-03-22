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
]

sfondo = pygame.image.load("generale/sfondo_pirati.jpg")
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo Nero")
clock = pygame.time.Clock()


def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64, 78)):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    schermo.blit(frame_scalato, pos)


gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    schermo.fill(NERO)

    disegna_animazione(schermo, personaggi[0]["sprites"], "idle", 200, (100, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_forward", 150, (300, 100))
    disegna_animazione(schermo, personaggi[0]["sprites"], "walk_cycle", 150, (500, 100))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_forward", 200, (700, 100), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "walk_cycle", 135, (900, 100), (54, 74))
    disegna_animazione(schermo, personaggi[1]["sprites"], "idle", 125, (1100, 100), (54, 74))

    pygame.display.update()
    clock.tick(60)

pygame.quit()