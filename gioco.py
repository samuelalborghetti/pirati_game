import pygame

pygame.init()

LARGHEZZA = 800
ALTEZZA = 600
NERO = (155, 0, 0)
tc = 0
durata_frames = 200

schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo Nero")
clock = pygame.time.Clock()

def get_frame(frames, tc, durata_frames):
    indice = (tc // durata_frames) % len(frames)
    return frames[indice]

frames_personaggio = [pygame.image.load("frames/h1.png"), pygame.image.load("frames/h2.png"), pygame.image.load("frames/h3.png")]

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    tc += clock.get_time()
    if tc > durata_frames * len(frames_personaggio):
        tc = 0
    

    schermo.fill(NERO)
    frame_corrente = get_frame(frames_personaggio, tc, durata_frames)
    schermo.blit(frame_corrente, (100, 100))

    pygame.display.update()
    clock.tick(60)

pygame.quit()