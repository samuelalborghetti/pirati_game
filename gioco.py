import pygame

pygame.init()

LARGHEZZA = 800
ALTEZZA = 600
NERO = (155, 0, 0)

schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo Nero")
clock = pygame.time.Clock()

def get_frame(frames, durata_frames, start_ms=0):
    t = pygame.time.get_ticks() - start_ms
    indice = (t // durata_frames) % len(frames)
    return frames[indice]

frames_personaggio = [
    pygame.image.load(f"allframe/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png").convert_alpha()
    for i in range(1, 5)
]

start_ms = pygame.time.get_ticks()  # opzionale, per sincronizzare l'animazione con un punto di partenza specifico

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    schermo.fill(NERO)

    frame_corrente = get_frame(frames_personaggio, 200, start_ms)
    frame_corrente = pygame.transform.scale(frame_corrente, (frame_corrente.get_width() * 2, frame_corrente.get_height() * 2))
    schermo.blit(frame_corrente, (100, 100))

    pygame.display.update()
    clock.tick(60)

pygame.quit()