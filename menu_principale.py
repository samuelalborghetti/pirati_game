import pygame
import json
import subprocess
import sys

IMPOSTAZIONI = "./dati/setting.json"

def CaricaSettings (percorso):
    file = open (percorso, "r", encoding="utf-8")
    info = file.read()
    dati = json.loads (info)
    return dati["height"], dati["width"], dati["audio"], dati["mod"]

def SalvaSettings(percorso, height, width, audio, mod):
    dati = {"height": height,"width": width,"audio": audio,"mod": mod}
    file = open(percorso, "w", encoding="utf-8")
    info = json.dumps(dati)
    file.write(info)
    file.close()

HEIGHT, WIDTH, volume, MOD = CaricaSettings (IMPOSTAZIONI)

print (HEIGHT, WIDTH, MOD)

widht_prov = WIDTH
height_prov = HEIGHT
mod_prov = MOD

pygame.init()

bg = pygame.image.load ("./assets/sfondi/menu.jpeg")
bg = pygame.transform.scale (bg, (WIDTH, HEIGHT))

screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Pirates of the see")
clock = pygame.time.Clock()

pygame.mixer.music.load("./assets/music/GLOVO.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)


FONT_BOLD = pygame.font.Font ("./assets/fonts/PixelifySans-Bold.ttf", int(50 * MOD))
FONT_REGULAR = pygame.font.Font ("./assets/fonts/PixelifySans-Regular.ttf", int(40 * MOD))
FONT_AVVISI = pygame.font.Font ("./assets/fonts/PixelifySans-Regular.ttf", int(30 * MOD))

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

DIMENSIONI_SCHERMO = ["1920x1280", "1080x720"]

SCHERMATA_PRINCIPALE = "main"
SCHERMATA_OPTIONS = "options"

schermata = "main"
slider_x = VOLUME_BAR.x + (VOLUME_BAR.width - WIDTH_SLIDER) * volume
cambio_volume = False

def DrawButtons(schermo, to_button):
    for button in to_button:
        if button in BUTTONS.keys():
            schermo.blit (BUTTONS[button][0], (BUTTONS[button][1].x, BUTTONS[button][1].y))

def Drawtext (schermo, text: list, y_in, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        testo_rect = testo.get_rect(center=(schermo.get_width() // 2, y))
        schermo.blit (testo, testo_rect)
        y += spazio_tra_righe

menu_on = True
while menu_on:
    mouse = pygame.mouse.get_pos()

    #gestione eventi -> collisione mouse
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            menu_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if schermata == SCHERMATA_PRINCIPALE:
                if BUTTONS["play"][1].collidepoint (mouse):
                    subprocess.Popen([sys.executable, "script_prova/gioco.py"])
                    sys.exit()
                elif BUTTONS["options"][1].collidepoint (mouse):
                    schermata = SCHERMATA_OPTIONS
                elif BUTTONS["quit"][1].collidepoint (mouse):
                    menu_on = False
            elif schermata == SCHERMATA_OPTIONS:
                if VOLUME_BAR.collidepoint(mouse):
                    cambio_volume = True
                elif BUTTONS["audio_full"][1].collidepoint (mouse):
                    if volume == 0:
                        volume = 0.5
                        slider_x = VOLUME_BAR.x + VOLUME_BAR.width /2
                    else:
                        volume = 0
                        slider_x = VOLUME_BAR.x
                elif BUTTONS["arr_right"][1].collidepoint (mouse):
                    if height_prov == 1280:
                        widht_prov = 1080
                        height_prov = 720
                        mod_prov = 1
                    else:
                        widht_prov = 1920
                        height_prov = 1280
                        mod_prov = 1.77
                elif BUTTONS["back"][1].collidepoint (mouse):
                    if height_prov != HEIGHT:
                        SalvaSettings (IMPOSTAZIONI,height_prov, widht_prov, volume, mod_prov)
                        subprocess.Popen([sys.executable] + sys.argv) #zio claudio righe (questa e la prossima) -> non so come funzionino ma fanno quello che devono fare
                        sys.exit()
                    else:
                        SalvaSettings (IMPOSTAZIONI,HEIGHT, WIDTH, volume, MOD)
                        schermata = SCHERMATA_PRINCIPALE
        elif event.type == pygame.MOUSEBUTTONUP:
            if VOLUME_BAR.collidepoint(mouse):
                cambio_volume = False


    #gestione cambiamento volume
    if not VOLUME_BAR_COLLISION.collidepoint(mouse):
        cambio_volume = False
    if cambio_volume:
        slider_x = mouse[0] - WIDTH_SLIDER / 2 
        slider_x = max(VOLUME_BAR.x, min(slider_x, VOLUME_BAR.x + VOLUME_BAR.width - WIDTH_SLIDER))
        volume = (slider_x - VOLUME_BAR.x) / (VOLUME_BAR.width - WIDTH_SLIDER)
        pygame.mixer.music.set_volume(volume)
    
    #gestione schermo
    screen.blit (bg, (0,0))
    if schermata == SCHERMATA_PRINCIPALE: #menu principale
        Drawtext (screen, ["Pirates", "of the see!"], HEIGH_BUTTON, FONT_BOLD, (255,255,255), HEIGH_BUTTON /1.5)
        DrawButtons (screen, ["play", "quit", "options"])
    else: #menu opzioni
        Drawtext (screen, ["OPTIONS"], HEIGH_BUTTON, FONT_BOLD, (255,255,255), HEIGH_BUTTON /1.5)
        if int(volume * 100) > 0:
            DrawButtons (screen, ["audio_full", "empty", "arr_right", "resolution", "back"])
        else:
            DrawButtons (screen, ["no_audio", "empty", "arr_right", "resolution", "back"])
        if height_prov == 1280:
            dim_schermo = DIMENSIONI_SCHERMO [0]
        else:
            dim_schermo = DIMENSIONI_SCHERMO [1]
        dim_schermo_testo = FONT_REGULAR.render(dim_schermo, True, (255,255,255))
        dim_schermo_rect = dim_schermo_testo.get_rect()
        dim_schermo_rect.center = BUTTONS["empty"][1].center
        screen.blit(dim_schermo_testo, dim_schermo_rect)
        screen.blit (FONT_REGULAR.render(str(int(volume * 100)), True, (0, 0, 0)), (VOLUME_BAR.x + VOLUME_BAR.width + WIDTH_SLIDER, VOLUME_BAR.y - HEIGHT_SLIDER/1.25))
        if height_prov != HEIGHT:
            Drawtext (screen, ["Le modifiche veranno apportate", "dopo essere tornati al menu principale"], BUTTONS["empty"][1].y + HEIGH_BUTTON, FONT_AVVISI, (255, 234, 0), HEIGH_BUTTON/2)
        pygame.draw.rect(screen, (255, 177, 27), VOLUME_BAR, border_radius=3)
        slider_rect = pygame.Rect (slider_x, VOLUME_BAR.centery - HEIGHT_SLIDER/2, WIDTH_SLIDER, HEIGHT_SLIDER)
        pygame.draw.rect(screen, (138, 95, 14), slider_rect, border_radius=2)
        #pygame.draw.rect (screen, (0,0,0), VOLUME_BAR_COLLISION) #-> debug per vedere quanto spazio c'è per cambiare volume


    pygame.display.update()
    clock.tick(60)

pygame.quit()