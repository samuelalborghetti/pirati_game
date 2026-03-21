import pygame

pygame.init()

LARGHEZZA = 1200
ALTEZZA = 800
NERO = (155, 0, 0)



personaggi = [
    {
        "nome": "Capitano",
        "costo": 380,
        "hp": 3,
        "vivo": True,
        "sprites": {
            "idle":             [pygame.image.load(f"allframe/capitano/idle/capitanoidle{i}.png") for i in range(1, 3)], 
            "cammino_avanti":   [pygame.image.load(f"allframe/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png") for i in range(1, 5)],
            "cammino_laterale": [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png") for i in range(1, 5)],
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

inizio_ms = pygame.time.get_ticks()  # opzionale, per sincronizzare l'animazione con un punto di partenza specifico





gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    schermo.fill(NERO)

    frame_coerrente = prendi_frame(personaggi[0]["sprites"]["idle"], 200, inizio_ms)
    frame_coerente = pygame.transform.scale(frame_coerrente, ( 64,78) )  # Ridimensiona il frame a 64x78 pixel
    frame_coerente_due = prendi_frame(personaggi[0]["sprites"]["cammino_avanti"], 150, inizio_ms)
    frame_coerente_due = pygame.transform.scale(frame_coerente_due, ( 64,78) )  # Flip orizzontale per cammino laterale
    frame_coerente_tre = prendi_frame(personaggi[0]["sprites"]["cammino_laterale"], 150, inizio_ms)
    frame_coerente_tre = pygame.transform.scale(frame_coerente_tre, ( 64,78) )  # Flip orizzontale per cammino laterale
    schermo.blit(frame_coerente,     (100, 100))  # idle — scalato ✓
    schermo.blit(frame_coerente_due, (300, 100))  # cammino avanti — scalato ✓
    schermo.blit(frame_coerente_tre, (500, 100))

    pygame.display.update()
    clock.tick(60)

pygame.quit()