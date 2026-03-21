import pygame
import random

#TODO aggiungere oggetti che cadono dallaltro e fungono da perk per i personaggi

personaggio_buono = 1
personaggio_cattivo = 1
salvo = False
VELOCITA_ZORO = 4
VELOCITA_LUFFY = 4
DURATA_STORDIMENTO = 1000
TEMPO_RICARICA_TORNADO = 10000 
TEMPO_RICARICA_SOTTOTERRA = 10000

pygame.init()

# SFONDO
i = 0
tempo_sfondo = 0
frames_sfondo = [pygame.image.load('framessfondo/onepice.png')]
for n in range(2, 11):
    frames_sfondo.append(pygame.image.load(f'framessfondo/framessfondo{n}.jpg'))

# CARDS 
frames_cards = [
    pygame.transform.scale_by(pygame.image.load('cards/lufycard.png'), 0.8),
    pygame.transform.scale_by(pygame.image.load('cards/zorocard.png'), 0.8),
    pygame.transform.scale_by(pygame.image.load('cards/sanjicard.gif'), 0.8),
    pygame.transform.scale_by(pygame.image.load('cards/crocodilecard.png'), 0.8)
]

# VITA 
frames_vita = [
    pygame.transform.scale_by(pygame.image.load('framesvita/framevita.png'), 1.5),
    pygame.transform.scale_by(pygame.image.load('framesvita/framevitapersa.png'), 1.4),
]

# MORTO 
morto_frames = [
    pygame.transform.scale_by(pygame.image.load('framesmortozoro/framesmortozoro7.png'), 1.8),
    pygame.transform.scale_by(pygame.image.load('framesmortozoro/framesmortozoro8.png'), 2.4),
    pygame.transform.scale_by(pygame.image.load('framesmortozoro/mortosanji.png'), 2.4),
    pygame.transform.scale_by(pygame.image.load('framesmortozoro/mortocrocodile.png'), 1.8)
]
# Freccie
freccie_menu = [    
    pygame.transform.scale_by(pygame.image.load('freccie/frecciaingiu.png'), 0.1),
    pygame.transform.scale_by(pygame.image.load('freccie/frecciaingiu1.png'), 0.1),
    pygame.transform.scale_by(pygame.image.load('freccie/frecciainsu.png'), 0.1),
    pygame.transform.scale_by(pygame.image.load('freccie/frecciainsu1.png'), 0.1)
]

sfondo = frames_sfondo[i]
larghezzaSfondo = sfondo.get_width()
altezzaSfondo = sfondo.get_height()
schermo = pygame.display.set_mode((larghezzaSfondo, altezzaSfondo))
pygame.display.set_caption('gioco di combattimento one piece')
terreno = pygame.image.load("terreno.png")
pygame.transform.scale_by(terreno, 0.5)
larghezzaterreno = terreno.get_width()
altezzaterreno = terreno.get_height()

clock = pygame.time.Clock()

# TORNADO
tornado_frames = []
for n in range(1, 4):
    tornado_frames.append(pygame.transform.scale_by(pygame.image.load(f'framestornado/framestornado{n}.png'), 1.8))

# ZORO
zoro_base = []
for n in range(1, 6):
    zoro_base.append(pygame.transform.scale_by(pygame.image.load(f'spritezoro/zoro{n}.png'), 1.8))

pugno_zoro_base = []
for n in range(1, 7):
    pugno_zoro_base.append(pygame.transform.scale_by(pygame.image.load(f'pugno/pugno{n}.png'), 1.8))

special_zoro_base = []
for n in range(1, 8):
    special_zoro_base.append(pygame.transform.scale_by(pygame.image.load(f'special/speciale{n}.png'), 1.8))

sottoterra_zoro_base = []
for n in range(1, 4):
    sottoterra_zoro_base.append(pygame.transform.scale_by(pygame.image.load(f'sottoterra/sottoterra{n}.png'), 1.2))

colpito_zoro_base = []
for n in range(1, 6):
    colpito_zoro_base.append(pygame.transform.scale_by(pygame.image.load(f'colpitozoro/colpitozoro{n}.png'), 1.8))

# CROCODILE
crocodile_base = []
for n in range(1, 9):
    crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'spritecrocodile/crocodile{n}.png'), 1.8))

pugno_crocodile_base = []
for n in range(1, 12):
    pugno_crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'pugnocrocodile/pugnocrocodile{n}.png'), 1.8))

special_crocodile_base = []
for n in range(1, 10):
    special_crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'specialcrocodile/specialcrocodile{n}.png'), 1.8))

sottoterra_crocodile_base = []
for n in range(1, 4):
    sottoterra_crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'paratacrocodile/paratacrocodile{n}.png'), 1.8))

colpito_crocodile_base = []
for n in range(1, 5):
    colpito_crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'colpitocrocodile/colpitocrocodile{n}.png'), 1.8))
for n in range(5, 10):
    colpito_crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'colpitocrocodile/colpitocrocodile{n}.png'), 0.9))

if personaggio_cattivo == 1:
    zoro_frames = zoro_base
    pugno_frames = pugno_zoro_base
    special_frames = special_zoro_base
    sottoterra_frames = sottoterra_zoro_base
    colpitozoro_frames = colpito_zoro_base
else:
    zoro_frames = crocodile_base
    pugno_frames = pugno_crocodile_base
    special_frames = special_crocodile_base
    sottoterra_frames = sottoterra_crocodile_base
    colpitozoro_frames = colpito_crocodile_base


#----------------------------------------------PERSONAGGIO SCELTO-----------------------------------------------------

# FISSE
fisse_zoro_base = []
for n in range(1, 9):
    fisse_zoro_base.append(pygame.transform.scale_by(pygame.image.load(f'fissezoro/fisso{n}.png'), 1.8))

fisse_crocodile_base = []
for n in range(1, 9):
    fisse_crocodile_base.append(pygame.transform.scale_by(pygame.image.load(f'fissecrocodile/fissecrocodile{n}.png'), 1.8))

# FERMO
fermo_luffy_base = []
for n in range(1, 8):
    fermo_luffy_base.append(pygame.transform.scale_by(pygame.image.load(f'fermolufy/fermolufy{n}.png'), 1.8))

fermo_sanji_base = []
for n in range(1, 15):
    fermo_sanji_base.append(pygame.transform.scale_by(pygame.image.load(f'fermosanji/fermosanji{n}.png'), 1.8))

# LUFFY
corsa_luffy_base = []
for n in range(1, 7):
    corsa_luffy_base.append(pygame.transform.scale_by(pygame.image.load(f'corsalufy/corsalufy{n}.png'), 1.8))

parata_luffy_base = []
for n in range(1, 8):
    parata_luffy_base.append(pygame.transform.scale_by(pygame.image.load(f'paratalufy/paratalufy{n}.png'), 1.8))

pugno_luffy_base = []
for n in range(1, 11):
    pugno_luffy_base.append(pygame.transform.scale_by(pygame.image.load(f'pugnolufy/pugnolufy{n}.png'), 1.8))

special_luffy_base = []
for n in range(1, 12):
    special_luffy_base.append(pygame.transform.scale_by(pygame.image.load(f'speciallufy/speciallufy{n}.png'), 1.8))

colpito_luffy_base = []
for n in range(1, 9):
    colpito_luffy_base.append(pygame.transform.scale_by(pygame.image.load(f'colpitolufy/colpitolufy{n}.png'), 1.8))

# SANJI
corsa_sanji_base = []
for n in range(1, 11):
    corsa_sanji_base.append(pygame.transform.scale_by(pygame.image.load(f'corsasanji/corsasanji{n}.png'), 1.8))

parata_sanji_base = []
for n in range(1, 8):
    parata_sanji_base.append(pygame.transform.scale_by(pygame.image.load(f'paratasanji/paratasanji{n}.png'), 1.8))

pugno_sanji_base = []
for n in range(1, 6):
    pugno_sanji_base.append(pygame.transform.scale_by(pygame.image.load(f'pugnosanji/pugnosanji{n}.png'), 1.8))

special_sanji_base = []
for n in range(1, 14):
    special_sanji_base.append(pygame.transform.scale_by(pygame.image.load(f'specialsanji/specialsanji{n}.png'), 1.8))

colpito_sanji_base = []
for n in range(1, 9):
    colpito_sanji_base.append(pygame.transform.scale_by(pygame.image.load(f'colpitosanji/colpitosanji{n}.png'), 1.8))


if personaggio_cattivo == 1:
    fissezoro_frames = fisse_zoro_base
else:
    fissezoro_frames = fisse_crocodile_base

if personaggio_buono == 1:
    fermolufy_frames = fermo_luffy_base
    corsalufy_frames = corsa_luffy_base
    paratalufy_frames = parata_luffy_base
    pugnolufy_frames = pugno_luffy_base
    speciallufy_frames = special_luffy_base
    colpitolufy_frames = colpito_luffy_base
else:
    fermolufy_frames = fermo_sanji_base
    corsalufy_frames = corsa_sanji_base
    paratalufy_frames = parata_sanji_base
    pugnolufy_frames = pugno_sanji_base
    speciallufy_frames = special_sanji_base
    colpitolufy_frames = colpito_sanji_base

vs_frames = []
for n in range(1, 16):
    vs_frames.append(pygame.image.load(f'menu/framesvs{n}.png'))


#sound
tornado_sound = pygame.mixer.Sound("sound/tornado.mp3")
pugno_sound = pygame.mixer.Sound("sound/pugno.mp3")
teletrasporto_sound = pygame.mixer.Sound("sound/teletrasporto.mp3")
sound_base= pygame.mixer.Sound("sound/soundbase.mp3")


tornado_sound.set_volume(1.0)    
pugno_sound.set_volume(1.0)        
teletrasporto_sound.set_volume(1.0) 
sound_base.set_volume(0.3)
sound_base.play(-1)  # Musica di sottofondo sempre attiva in loop

#ciclo principale
probabilita = True

larghezz_ZORO = zoro_frames[0].get_width()
altezz_ZORO = zoro_frames[0].get_height()
larghezz_LUFFY = corsalufy_frames[0].get_width()
altezz_LUFFY = corsalufy_frames[0].get_height()
altezza_TORNADO = tornado_frames[0].get_height()
y_tornado = altezzaSfondo - altezzaterreno - altezza_TORNADO + 10
y_luffy = altezzaSfondo - altezzaterreno - altezz_LUFFY + 10  
y_zoro = altezzaSfondo - altezzaterreno - altezz_ZORO + 10  

     
#ZORO
morto_zoro = False
giro = True
gameOver = False
x_zoro = 0
x_zoro_posizione_pre_attacco = 0

mosse_zoro = 1
tpugno_zoro = 0
animazione_pugno_in_corso_zoro = False
animazione_special_in_corso_zoro = False
tspecial_zoro = 0
animazione_sottoterra_in_corso_zoro = False
tsottoterra_zoro = 0

#LUFFY
morto_luffy = False
giro_luffy = False
x_luffy = larghezzaSfondo - larghezz_LUFFY

mosse_luffy = 1
tpugno_luffy = 0
animazione_pugno_in_corso_luffy = False
animazione_special_in_corso_luffy = False
tspecial_luffy = 0
tparata_luffy = 0
animazione_parata_in_corso_luffy = False
parata_fatta_zoro = False
parata_fatta_luffy = False
pugno_zoro_gestito = False
speciale_zoro_gestito = False
pugno_luffy_gestito = False
speciale_luffy_gestito = False
#vita
vita_zoro = 100
vita_luffy = 100

# Stordimento 
stordito_zoro = False
tempo_stordito_zoro = 0
stordito_luffy = False
tempo_stordito_luffy = 0
#schermata iniziale
schermo_iniziale = True
schermata2=0
tcfermo_menu_luffy = 0
tcfermo_menu_zoro = 0

#sanji
flag_avanti = False
massima_lunghezza_lufy = 0

#crocodile
animazione_tornado_in_corso_zoro = False
x_tornado = 0
tempo_tornado = 0
ultimo_tornado = 0  
ultimo_sottoterra = 0





font = pygame.font.SysFont(None, 18)


sfondo_scelta_personaggio = pygame.image.load('sfondosceltapersonaggio.jpg')

schermata = 0
tempo_schermata0 = 0

while probabilita:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            probabilita = False
            schermata = 0
        if event.type == pygame.KEYDOWN and schermata == 0:
            if event.key == pygame.K_a:
                schermata = 1
            elif event.key == pygame.K_b:
                probabilita = False
                schermata = 7
            elif event.key == pygame.K_w:
                if personaggio_cattivo == 2:
                    personaggio_cattivo = 1
                else:
                    personaggio_cattivo = 2
                if personaggio_cattivo == 1:
                    fissezoro_frames = fisse_zoro_base
                    zoro_frames = zoro_base
                    pugno_frames = pugno_zoro_base
                    special_frames = special_zoro_base
                    sottoterra_frames = sottoterra_zoro_base
                    colpitozoro_frames = colpito_zoro_base
                else:
                    fissezoro_frames = fisse_crocodile_base
                    zoro_frames = crocodile_base
                    pugno_frames = pugno_crocodile_base
                    special_frames = special_crocodile_base
                    sottoterra_frames = sottoterra_crocodile_base
                    colpitozoro_frames = colpito_crocodile_base
            elif event.key == pygame.K_s:
                if personaggio_cattivo == 2:
                    personaggio_cattivo = 1
                else:
                    personaggio_cattivo = 2
                if personaggio_cattivo == 1:
                    fissezoro_frames = fisse_zoro_base
                    zoro_frames = zoro_base
                    pugno_frames = pugno_zoro_base
                    special_frames = special_zoro_base
                    sottoterra_frames = sottoterra_zoro_base
                    colpitozoro_frames = colpito_zoro_base
                else:
                    fissezoro_frames = fisse_crocodile_base
                    zoro_frames = crocodile_base
                    pugno_frames = pugno_crocodile_base
                    special_frames = special_crocodile_base
                    sottoterra_frames = sottoterra_crocodile_base
                    colpitozoro_frames = colpito_crocodile_base
            elif event.key == pygame.K_i:
                if personaggio_buono == 1:
                    personaggio_buono = 2
                else:
                    personaggio_buono = 1
                if personaggio_buono == 1:
                    fermolufy_frames = fermo_luffy_base
                    corsalufy_frames = corsa_luffy_base
                    paratalufy_frames = parata_luffy_base
                    pugnolufy_frames = pugno_luffy_base
                    speciallufy_frames = special_luffy_base
                    colpitolufy_frames = colpito_luffy_base
                else:
                    fermolufy_frames = fermo_sanji_base
                    corsalufy_frames = corsa_sanji_base
                    paratalufy_frames = parata_sanji_base
                    pugnolufy_frames = pugno_sanji_base
                    speciallufy_frames = special_sanji_base
                    colpitolufy_frames = colpito_sanji_base
                if personaggio_buono ==1:
                    giro_luffy = False
                elif personaggio_buono ==2:
                    giro_luffy = True
            elif event.key == pygame.K_k:
                if personaggio_buono == 2:
                    personaggio_buono = 1
                else:
                    personaggio_buono = 2
                if personaggio_buono == 1:
                    fermolufy_frames = fermo_luffy_base
                    corsalufy_frames = corsa_luffy_base
                    paratalufy_frames = parata_luffy_base
                    pugnolufy_frames = pugno_luffy_base
                    speciallufy_frames = special_luffy_base
                    colpitolufy_frames = colpito_luffy_base
                else:
                    fermolufy_frames = fermo_sanji_base
                    corsalufy_frames = corsa_sanji_base
                    paratalufy_frames = parata_sanji_base
                    pugnolufy_frames = pugno_sanji_base
                    speciallufy_frames = special_sanji_base
                    colpitolufy_frames = colpito_sanji_base
                if personaggio_buono ==1:
                    giro_luffy = False
                elif personaggio_buono ==2:
                    giro_luffy = True
            elif event.key == pygame.K_r and schermata == 0:
                # Reset tutte le variabili come all'inizio del gioco
                personaggio_buono = 1
                personaggio_cattivo = 1
                morto_zoro = False
                giro = True
                gameOver = False
                x_zoro = 0
                x_zoro_posizione_pre_attacco = 0
                mosse_zoro = 1
                tpugno_zoro = 0
                animazione_pugno_in_corso_zoro = False
                animazione_special_in_corso_zoro = False
                tspecial_zoro = 0
                animazione_sottoterra_in_corso_zoro = False
                tsottoterra_zoro = 0
                morto_luffy = False
                giro_luffy = False
                x_luffy = larghezzaSfondo - larghezz_LUFFY
                mosse_luffy = 1
                tpugno_luffy = 0
                animazione_pugno_in_corso_luffy = False
                animazione_special_in_corso_luffy = False
                tspecial_luffy = 0
                tparata_luffy = 0
                animazione_parata_in_corso_luffy = False
                parata_fatta_zoro = False
                parata_fatta_luffy = False
                pugno_zoro_gestito = False
                speciale_zoro_gestito = False
                pugno_luffy_gestito = False
                speciale_luffy_gestito = False
                vita_zoro = 100
                vita_luffy = 100
                stordito_zoro = False
                tempo_stordito_zoro = 0
                stordito_luffy = False
                tempo_stordito_luffy = 0
                animazione_tornado_in_corso_zoro = False
                x_tornado = 0
                tempo_tornado = 0
                ultimo_tornado = 0
                ultimo_sottoterra = 0
                schermata2 = 0
                schermo_iniziale = True
                tcfermo_menu_luffy = 0
                tcfermo_menu_zoro = 0
                flag_avanti = False
                massima_lunghezza_lufy = 0
                tempo_sfondo = 0
                i = 0
                # Reset frame personaggi
                if personaggio_cattivo == 1:
                    fissezoro_frames = fisse_zoro_base
                    zoro_frames = zoro_base
                    pugno_frames = pugno_zoro_base
                    special_frames = special_zoro_base
                    sottoterra_frames = sottoterra_zoro_base
                    colpitozoro_frames = colpito_zoro_base
                else:
                    fissezoro_frames = fisse_crocodile_base
                    zoro_frames = crocodile_base
                    pugno_frames = pugno_crocodile_base
                    special_frames = special_crocodile_base
                    sottoterra_frames = sottoterra_crocodile_base
                    colpitozoro_frames = colpito_crocodile_base
                if personaggio_buono == 1:
                    fermolufy_frames = fermo_luffy_base
                    corsalufy_frames = corsa_luffy_base
                    paratalufy_frames = parata_luffy_base
                    pugnolufy_frames = pugno_luffy_base
                    speciallufy_frames = special_luffy_base
                    colpitolufy_frames = colpito_luffy_base
                else:
                    fermolufy_frames = fermo_sanji_base
                    corsalufy_frames = corsa_sanji_base
                    paratalufy_frames = parata_sanji_base
                    pugnolufy_frames = pugno_sanji_base
                    speciallufy_frames = special_sanji_base
                    colpitolufy_frames = colpito_sanji_base
                sfondo = frames_sfondo[0]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and schermata == 3:
            # Reset completo tutte le variabili come all'inizio del gioco
            personaggio_buono = 1
            personaggio_cattivo = 1
            morto_zoro = False
            giro = True
            gameOver = False
            x_zoro = 0
            x_zoro_posizione_pre_attacco = 0
            mosse_zoro = 1
            tpugno_zoro = 0
            animazione_pugno_in_corso_zoro = False
            animazione_special_in_corso_zoro = False
            tspecial_zoro = 0
            animazione_sottoterra_in_corso_zoro = False
            tsottoterra_zoro = 0
            morto_luffy = False
            giro_luffy = False
            x_luffy = larghezzaSfondo - larghezz_LUFFY
            mosse_luffy = 1
            tpugno_luffy = 0
            animazione_pugno_in_corso_luffy = False
            animazione_special_in_corso_luffy = False
            tspecial_luffy = 0
            tparata_luffy = 0
            animazione_parata_in_corso_luffy = False
            parata_fatta_zoro = False
            parata_fatta_luffy = False
            pugno_zoro_gestito = False
            speciale_zoro_gestito = False
            pugno_luffy_gestito = False
            speciale_luffy_gestito = False
            vita_zoro = 100
            vita_luffy = 100
            stordito_zoro = False
            tempo_stordito_zoro = 0
            stordito_luffy = False
            tempo_stordito_luffy = 0
            animazione_tornado_in_corso_zoro = False
            x_tornado = 0
            tempo_tornado = 0
            ultimo_tornado = 0
            ultimo_sottoterra = 0
            schermata2 = 0
            schermo_iniziale = True
            tcfermo_menu_luffy = 0
            tcfermo_menu_zoro = 0
            flag_avanti = False
            massima_lunghezza_lufy = 0
            tempo_sfondo = 0
            i = 0
            # Reset frame personaggi
            if personaggio_cattivo == 1:
                fissezoro_frames = fisse_zoro_base
                zoro_frames = zoro_base
                pugno_frames = pugno_zoro_base
                special_frames = special_zoro_base
                sottoterra_frames = sottoterra_zoro_base
                colpitozoro_frames = colpito_zoro_base
            else:
                fissezoro_frames = fisse_crocodile_base
                zoro_frames = crocodile_base
                pugno_frames = pugno_crocodile_base
                special_frames = special_crocodile_base
                sottoterra_frames = sottoterra_crocodile_base
                colpitozoro_frames = colpito_crocodile_base
            if personaggio_buono == 1:
                fermolufy_frames = fermo_luffy_base
                corsalufy_frames = corsa_luffy_base
                paratalufy_frames = parata_luffy_base
                pugnolufy_frames = pugno_luffy_base
                speciallufy_frames = special_luffy_base
                colpitolufy_frames = colpito_luffy_base
            else:
                fermolufy_frames = fermo_sanji_base
                corsalufy_frames = corsa_sanji_base
                paratalufy_frames = parata_sanji_base
                pugnolufy_frames = pugno_sanji_base
                speciallufy_frames = special_sanji_base
                colpitolufy_frames = colpito_sanji_base
            sfondo = frames_sfondo[0]
            schermata = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and schermata == 3:
            probabilita = False
            schermata = 7
    
    if schermata == 0:

        if personaggio_buono == 1:
            moodulo_personaggiobuono = 1050 
        elif personaggio_buono == 2:
            moodulo_personaggiobuono = 1600
        tcfermo_s0_buono = pygame.time.get_ticks() % moodulo_personaggiobuono
        tcfermo_s0_nemico = pygame.time.get_ticks() % 1000

        
        schermo.blit(sfondo_scelta_personaggio, (0, 0))

        
        if 0 <= tcfermo_s0_nemico < 150:
            frame_nemico = fissezoro_frames[0]
        elif 150 <= tcfermo_s0_nemico < 300:
            frame_nemico = fissezoro_frames[1]
        elif 300 <= tcfermo_s0_nemico < 450:
            frame_nemico = fissezoro_frames[2]
        elif 450 <= tcfermo_s0_nemico < 600:
            frame_nemico = fissezoro_frames[3]
        elif 600 <= tcfermo_s0_nemico < 750:
            frame_nemico = fissezoro_frames[4]
        elif 750 <= tcfermo_s0_nemico < 900:
            frame_nemico = fissezoro_frames[5]
        else:
            frame_nemico = fissezoro_frames[6]
        if personaggio_cattivo == 1:
            frame_nemico = pygame.transform.flip(frame_nemico, True, False)
            schermo.blit(frame_nemico, (210, 100))
        else:
            frame_nemico = pygame.transform.scale_by(frame_nemico, 0.9)
            schermo.blit(frame_nemico, (204, 115))

        
        if personaggio_buono == 1:
            if 0 <= tcfermo_s0_buono < 150:
                frame_buono = fermolufy_frames[0]
            elif 150 <= tcfermo_s0_buono < 300:
                frame_buono = fermolufy_frames[1]
            elif 300 <= tcfermo_s0_buono < 450:
                frame_buono = fermolufy_frames[2]
            elif 450 <= tcfermo_s0_buono < 600:
                frame_buono = fermolufy_frames[3]
            elif 600 <= tcfermo_s0_buono < 750:
                frame_buono = fermolufy_frames[4]
            elif 750 <= tcfermo_s0_buono < 900:
                frame_buono = fermolufy_frames[5]
            else:
                frame_buono = fermolufy_frames[6]
        else:
            if 0 <= tcfermo_s0_buono < 114:
                frame_buono = fermolufy_frames[0]
            elif 114 <= tcfermo_s0_buono < 228:
                frame_buono = fermolufy_frames[1]
            elif 228 <= tcfermo_s0_buono < 342:
                frame_buono = fermolufy_frames[2]
            elif 342 <= tcfermo_s0_buono < 456:
                frame_buono = fermolufy_frames[3]
            elif 456 <= tcfermo_s0_buono < 570:
                frame_buono = fermolufy_frames[4]
            elif 570 <= tcfermo_s0_buono < 684:
                frame_buono = fermolufy_frames[5]
            elif 684 <= tcfermo_s0_buono < 798:
                frame_buono = fermolufy_frames[6]
            else:
                frame_buono = fermolufy_frames[6]

        if personaggio_buono == 1:
            x_buono = larghezzaSfondo - frame_buono.get_width() - 225
            schermo.blit(frame_buono, (x_buono, 130))
        elif personaggio_buono == 2:
            frame_buono = pygame.transform.flip(frame_buono, True, False)
            x_buono = larghezzaSfondo - frame_buono.get_width() - 230
            schermo.blit(frame_buono, (x_buono, 115))
        schermo.blit(freccie_menu[2], (100, 100))
        schermo.blit(freccie_menu[1], (100, 250))
        schermo.blit(freccie_menu[3], (larghezzaSfondo - 200, 100))
        schermo.blit(freccie_menu[0], (larghezzaSfondo - 200, 250))

        pygame.display.update()
        clock.tick(60)
    
    
    elif schermata == 1:
        
        if personaggio_buono ==1:
            modulo_lufy = 1050
        else:
            modulo_lufy = 1600
            for frame in fermolufy_frames:
                if frame.get_width() > massima_lunghezza_lufy:
                    massima_lunghezza_lufy = frame.get_width()
                    luffy_x = (larghezzaSfondo - massima_lunghezza_lufy) // 2
        
        
        # Timer animazioni
        tcfermo_menu_luffy = pygame.time.get_ticks() % modulo_lufy
        tcfermo_menu_zoro = pygame.time.get_ticks() % 1000
        tcfermo_menu_vs = pygame.time.get_ticks() % 1300
        
        # Sfondo
        schermo.blit(pygame.image.load('menu/sfondo_menu.gif'), (0, 0))
        
        if personaggio_buono ==1:
            if 0 <= tcfermo_menu_luffy < 150:
                frame_menu_luffy = fermolufy_frames[0]
            elif 150 <= tcfermo_menu_luffy < 300:
                frame_menu_luffy = fermolufy_frames[1]
            elif 300 <= tcfermo_menu_luffy < 450:
                frame_menu_luffy = fermolufy_frames[2]
            elif 450 <= tcfermo_menu_luffy < 600:
                frame_menu_luffy = fermolufy_frames[3]
            elif 600 <= tcfermo_menu_luffy < 750:
                frame_menu_luffy = fermolufy_frames[4]
            elif 750 <= tcfermo_menu_luffy < 900:
                frame_menu_luffy = fermolufy_frames[5]
            else:
                frame_menu_luffy = fermolufy_frames[6]
        else:
            if 0 <= tcfermo_menu_luffy < 114:
                frame_menu_luffy = fermolufy_frames[0]
            elif 114 <= tcfermo_menu_luffy < 228:
                frame_menu_luffy = fermolufy_frames[1]
            elif 228 <= tcfermo_menu_luffy < 342:
                frame_menu_luffy = fermolufy_frames[2]
            elif 342 <= tcfermo_menu_luffy < 456:
                frame_menu_luffy = fermolufy_frames[3]
            elif 456 <= tcfermo_menu_luffy < 570:
                frame_menu_luffy = fermolufy_frames[4]
            elif 570 <= tcfermo_menu_luffy < 684:
                frame_menu_luffy = fermolufy_frames[5]
            elif 684 <= tcfermo_menu_luffy < 798:
                frame_menu_luffy = fermolufy_frames[6]
            elif 798 <= tcfermo_menu_luffy < 912:
                frame_menu_luffy = fermolufy_frames[7]
            elif 912 <= tcfermo_menu_luffy < 1026:
                frame_menu_luffy = fermolufy_frames[8]
            elif 1026 <= tcfermo_menu_luffy < 1140:
                frame_menu_luffy = fermolufy_frames[9]
            elif 1140 <= tcfermo_menu_luffy < 1254:
                frame_menu_luffy = fermolufy_frames[10]
            elif 1254 <= tcfermo_menu_luffy < 1368:
                frame_menu_luffy = fermolufy_frames[11]
            elif 1368 <= tcfermo_menu_luffy < 1482:
                frame_menu_luffy = fermolufy_frames[12]
            elif tcfermo_menu_luffy >= 1482:
                frame_menu_luffy = fermolufy_frames[13]
        if personaggio_buono ==1:
            luffy_x = (larghezzaSfondo - frame_menu_luffy.get_width()) // 2 
            schermo.blit(frame_menu_luffy, (luffy_x - 40, 233))       
        elif personaggio_buono ==2 :
            #onesto lo ha fatto chat gpt
            frame_menu_luffy = pygame.transform.flip(frame_menu_luffy, True, False)
            offset = massima_lunghezza_lufy - frame_menu_luffy.get_width()
            schermo.blit(frame_menu_luffy, (luffy_x + offset - 40, 233))
            #fine onesto lo ha fatto chat gpt
            
        
        if 0 <= tcfermo_menu_zoro < 125:
            frame_menu_zoro = fissezoro_frames[0]
        elif 125 <= tcfermo_menu_zoro < 250:
            frame_menu_zoro = fissezoro_frames[1]
        elif 250 <= tcfermo_menu_zoro < 375:
            frame_menu_zoro = fissezoro_frames[2]
        elif 375 <= tcfermo_menu_zoro < 500:
            frame_menu_zoro = fissezoro_frames[3]
        elif 500 <= tcfermo_menu_zoro < 625:
            frame_menu_zoro = fissezoro_frames[4]
        elif 625 <= tcfermo_menu_zoro < 750:
            frame_menu_zoro = fissezoro_frames[5]
        elif 750 <= tcfermo_menu_zoro < 875:
            frame_menu_zoro = fissezoro_frames[6]
        else:
            frame_menu_zoro = fissezoro_frames[7]
        if personaggio_cattivo ==1:
            frame_menu_zoro = pygame.transform.flip(frame_menu_zoro, True, False)
        elif personaggio_cattivo ==2:
            pass
        
        schermo.blit(frame_menu_zoro, (40 , 210))
        
        if 0 <= tcfermo_menu_vs < 87:
            frame_menu_vs = vs_frames[0]
        elif 87 <= tcfermo_menu_vs < 174:
            frame_menu_vs = vs_frames[1]
        elif 174 <= tcfermo_menu_vs < 261:
            frame_menu_vs = vs_frames[2]
        elif 261 <= tcfermo_menu_vs < 348:
            frame_menu_vs = vs_frames[3]
        elif 348 <= tcfermo_menu_vs < 435:
            frame_menu_vs = vs_frames[4]
        elif 435 <= tcfermo_menu_vs < 522:
            frame_menu_vs = vs_frames[5]
        elif 522 <= tcfermo_menu_vs < 609:
            frame_menu_vs = vs_frames[6]
        elif 609 <= tcfermo_menu_vs < 696:
            frame_menu_vs = vs_frames[7]
        elif 696 <= tcfermo_menu_vs < 783:
            frame_menu_vs = vs_frames[8]
        elif 783 <= tcfermo_menu_vs < 870:
            frame_menu_vs = vs_frames[9]
        elif 870 <= tcfermo_menu_vs < 957:
            frame_menu_vs = vs_frames[10]
        elif 957 <= tcfermo_menu_vs < 1044:
            frame_menu_vs = vs_frames[11]
        elif 1044 <= tcfermo_menu_vs < 1131:
            frame_menu_vs = vs_frames[12]
        elif 1131 <= tcfermo_menu_vs < 1218:
            frame_menu_vs = vs_frames[13] 
        else:
            frame_menu_vs = vs_frames[14]
            schermata2 +=1
            
        schermo.blit(frame_menu_vs, ((larghezzaSfondo - 420) // 2, 240))
        
        
            
        pygame.display.update()
        clock.tick(60)
        
        if schermata2 >= 25:
            schermata = 2
            schermata2 = 0

    
    elif schermata == 2:
        tasti = pygame.key.get_pressed()
        
        # Cambio sfondo con fecceta in su
        if tasti[pygame.K_UP]:
            tempo_iniziale = pygame.time.get_ticks()
            if tempo_sfondo == 0 or tempo_iniziale - tempo_sfondo >= 300:
                ok = 0
                while ok == 0:
                    sfondo2 = random.choice(frames_sfondo)
                    if sfondo2 != sfondo:
                        sfondo = sfondo2
                        ok = 1
                tempo_sfondo = tempo_iniziale
        
        #pungno di zoro
        if tasti[pygame.K_e] and not animazione_pugno_in_corso_zoro and not animazione_special_in_corso_zoro and not animazione_sottoterra_in_corso_zoro and not stordito_zoro:
            animazione_pugno_in_corso_zoro = True
            parata_fatta_zoro = False
            pugno_zoro_gestito = False
            tpugno_zoro = 0
            mosse_zoro = 2
            posizione_pre_attacco_zoro = x_zoro
        #special di zoro
        if tasti[pygame.K_q] and not animazione_special_in_corso_zoro and not animazione_pugno_in_corso_zoro and not animazione_sottoterra_in_corso_zoro and not stordito_zoro:
            tempo_attuale = pygame.time.get_ticks()
            if personaggio_cattivo == 1:
                if tempo_attuale - ultimo_sottoterra >= TEMPO_RICARICA_SOTTOTERRA:
                    animazione_special_in_corso_zoro = True
                    parata_fatta_zoro = False
                    speciale_zoro_gestito = False
                    tspecial_zoro = 0
                    mosse_zoro = 3
                    ultimo_sottoterra = tempo_attuale
                    teletrasporto_sound.play(-1)  # Suono teletrasporto in loop
                    x_zoro = x_luffy+larghezz_LUFFY
                    giro = False

                    if personaggio_buono == 1:
                        # Luffy normale
                        if giro_luffy:
                            # Luffy guarda a destra -> Zoro si sovrappone a Luffy
                            x_zoro = x_luffy
                            giro = True  # Zoro guarda a destra verso il nemico
                        else:
                            # Luffy guarda a sinistra -> Zoro si sovrappone a Luffy
                            x_zoro = x_luffy
                            giro = False  # Zoro guarda a sinistra
                    else: 
                        # Per Sanji il giro è invertito
                        if giro_luffy:
                            # Sanji guarda a sinistra -> Zoro si sovrappone
                            x_zoro = x_luffy
                            giro = False
                        else:
                            # Sanji guarda a destra -> Zoro si sovrappone
                            x_zoro = x_luffy
                            giro = True
            elif personaggio_cattivo == 2:
                if tempo_attuale - ultimo_tornado >= TEMPO_RICARICA_TORNADO:
                    animazione_special_in_corso_zoro = True
                    parata_fatta_zoro = False
                    speciale_zoro_gestito = False
                    tspecial_zoro = 0
                    mosse_zoro = 3
                    animazione_tornado_in_corso_zoro = True
                    tempo_tornado = 0
                    ultimo_tornado = tempo_attuale
                    tornado_sound.play(-1)  # Suono tornado in loop
                    # fissa la direzione del tornado verso la posizione di Luffy al momento del lancio
                    tornado_direzione = 1 if x_luffy > x_zoro else -1
                    if tornado_direzione == 1:
                        x_tornado = x_zoro + larghezz_ZORO
                    else:
                        x_tornado = x_zoro - larghezz_ZORO
                
        if not animazione_pugno_in_corso_zoro and not animazione_special_in_corso_zoro and not stordito_zoro and not animazione_pugno_in_corso_zoro:
            if tasti[pygame.K_w] and not animazione_sottoterra_in_corso_zoro:
                animazione_sottoterra_in_corso_zoro = True
                tsottoterra_zoro = 0
                mosse_zoro = 4
            elif tasti[pygame.K_a]:
                if not animazione_sottoterra_in_corso_zoro:
                    mosse_zoro = 0
                x_zoro -= VELOCITA_ZORO
                giro = False
            elif tasti[pygame.K_d]:
                if not animazione_sottoterra_in_corso_zoro:
                    mosse_zoro = 0
                x_zoro += VELOCITA_ZORO
                giro = True
            elif not animazione_sottoterra_in_corso_zoro:
                mosse_zoro = 1

        if x_zoro < 0:
            x_zoro = 0
        if x_zoro > larghezzaSfondo - larghezz_ZORO:
            x_zoro = larghezzaSfondo - larghezz_ZORO

        # ------------------- CONTROLLI LUFFY -------------------
        if tasti[pygame.K_o] and not animazione_pugno_in_corso_luffy and not animazione_special_in_corso_luffy and not animazione_parata_in_corso_luffy and not stordito_luffy:
            animazione_pugno_in_corso_luffy = True
            parata_fatta_luffy = False
            pugno_luffy_gestito = False
            tpugno_luffy = 0
            mosse_luffy = 2

        if tasti[pygame.K_u] and not animazione_special_in_corso_luffy and not animazione_pugno_in_corso_luffy and not animazione_parata_in_corso_luffy and not stordito_luffy:
            animazione_special_in_corso_luffy = True
            parata_fatta_luffy = False
            speciale_luffy_gestito = False
            tspecial_luffy = 0
            mosse_luffy = 3
            posizione_pre_attacco_luffy = x_luffy  

        if tasti[pygame.K_i] and not animazione_parata_in_corso_luffy and not animazione_pugno_in_corso_luffy and not animazione_special_in_corso_luffy and not stordito_luffy:
            animazione_parata_in_corso_luffy = True
            tparata_luffy = 0
            mosse_luffy = 4

        if not animazione_pugno_in_corso_luffy and not animazione_special_in_corso_luffy and not animazione_parata_in_corso_luffy and not stordito_luffy:
            if tasti[pygame.K_j]:
                mosse_luffy = 0
                x_luffy -= VELOCITA_LUFFY
                if personaggio_buono ==1:
                    giro_luffy = False
                elif personaggio_buono ==2:
                    giro_luffy = True
            elif tasti[pygame.K_l]:
                mosse_luffy = 0
                x_luffy += VELOCITA_LUFFY
                if personaggio_buono ==1:
                    giro_luffy = True
                elif personaggio_buono ==2:
                    giro_luffy = False
            else:
                mosse_luffy = 1

        # ---------- GESTIONE TEMPI ANIMAZIONI ----------
        if personaggio_cattivo == 1:
            tc_zoro = pygame.time.get_ticks() % 650
        elif personaggio_cattivo == 2:
            tc_zoro = pygame.time.get_ticks() % 800
        tcfermo_zoro = pygame.time.get_ticks() % 1000
        if personaggio_buono ==1:
            tc_luffy = pygame.time.get_ticks() % 600
        elif personaggio_buono ==2:
            tc_luffy = pygame.time.get_ticks() % 1000
        if personaggio_buono ==1:
            tcfermo_luffy = pygame.time.get_ticks() % 1050
        elif personaggio_buono ==2:
            tcfermo_luffy = pygame.time.get_ticks() % modulo_lufy
        # ---------- ANIMAZIONE ZORO ----------
        if animazione_pugno_in_corso_zoro:
            tpugno_zoro += clock.get_time()
            if tpugno_zoro < 800:
                if giro:
                    # Zoro guarda a destra: avanza poi ritrarre
                    if tpugno_zoro <= 200:
                        x_zoro += 2
                    elif tpugno_zoro < 400:
                        x_zoro += 2
                    elif tpugno_zoro < 600:
                        x_zoro += 1
                    elif tpugno_zoro < 700:
                        x_zoro -= 2
                    elif tpugno_zoro < 800:
                        x_zoro -= 2
                        
                else:
                    # Zoro guarda a sinistra: inverso
                    if tpugno_zoro <= 200:
                        x_zoro -= 2
                        
                    elif tpugno_zoro < 400:
                        x_zoro -= 2
                    elif tpugno_zoro < 600:
                        x_zoro -= 1
                        
                    elif tpugno_zoro < 700:
                        x_zoro += 2
                    elif tpugno_zoro < 800:
                        x_zoro += 2
                        
                    
                if x_zoro < 0:
                    x_zoro = 0
                if x_zoro > larghezzaSfondo - larghezz_ZORO:
                    x_zoro = larghezzaSfondo - larghezz_ZORO
            else:
                mosse_zoro = 1
                animazione_pugno_in_corso_zoro = False
                if posizione_pre_attacco_zoro is not None:
                    x_zoro = posizione_pre_attacco_zoro
                posizione_pre_attacco_zoro = None
                tpugno_zoro = 0
        if personaggio_cattivo == 2 and animazione_tornado_in_corso_zoro:
            tempo_tornado += clock.get_time()
            
            # Movimento del tornado: usa la direzione fissata al lancio
            x_tornado += 3 * tornado_direzione
            if tornado_direzione == 1 and x_tornado > larghezzaSfondo:
                animazione_tornado_in_corso_zoro = False
                tempo_tornado = 0
                tornado_sound.stop()  # Fermo il suono del tornado
            elif tornado_direzione == -1 and x_tornado < -100:
                animazione_tornado_in_corso_zoro = False
                tempo_tornado = 0
                tornado_sound.stop()  # Fermo il suono del tornado
                    

                
        if animazione_special_in_corso_zoro:
            tspecial_zoro += clock.get_time()
            if personaggio_cattivo == 1:
                if tspecial_zoro >= 651:
                    mosse_zoro = 1
                    animazione_special_in_corso_zoro = False
                    tspecial_zoro = 0
                    teletrasporto_sound.stop()  # Fermo il suono del teletrasporto
            elif personaggio_cattivo == 2:
                if tspecial_zoro >= 1000:
                    mosse_zoro = 1
                    animazione_special_in_corso_zoro = False
                    tspecial_zoro = 0
                
        if animazione_sottoterra_in_corso_zoro:
            tsottoterra_zoro += clock.get_time()
            if tsottoterra_zoro >= 400:
                mosse_zoro = 1
                animazione_sottoterra_in_corso_zoro = False
                tsottoterra_zoro = 0

        if mosse_zoro == 0:
            if personaggio_cattivo == 1:
                if 0 <= tc_zoro < 130:
                    frame_zoro = zoro_frames[0]
                elif 130 <= tc_zoro < 260:
                    frame_zoro = zoro_frames[1]
                elif 260 <= tc_zoro < 390:
                    frame_zoro = zoro_frames[2]
                elif 390 <= tc_zoro < 520:
                    frame_zoro = zoro_frames[3]
                else:
                    frame_zoro = zoro_frames[4]
            elif personaggio_cattivo == 2:
                if 0 <= tc_zoro < 100:
                    frame_zoro = zoro_frames[0]
                elif 100 <= tc_zoro < 200:
                    frame_zoro = zoro_frames[1]
                elif 200 <= tc_zoro < 300:
                    frame_zoro = zoro_frames[2]
                elif 300 <= tc_zoro < 400:
                    frame_zoro = zoro_frames[3]
                elif 400 <= tc_zoro < 500:
                    frame_zoro = zoro_frames[4]
                elif 500 <= tc_zoro < 600:
                    frame_zoro = zoro_frames[5]
                elif 600 <= tc_zoro < 700:
                    frame_zoro = zoro_frames[6]
                else:
                    frame_zoro = zoro_frames[7]
   
        elif mosse_zoro == 1:
            if 0 <= tcfermo_zoro < 125:
                frame_zoro = fissezoro_frames[0]
            elif 125 <= tcfermo_zoro < 250:
                frame_zoro = fissezoro_frames[1]
            elif 250 <= tcfermo_zoro < 375:
                frame_zoro = fissezoro_frames[2]
            elif 375 <= tcfermo_zoro < 500:
                frame_zoro = fissezoro_frames[3]
            elif 500 <= tcfermo_zoro < 625:
                frame_zoro = fissezoro_frames[4]
            elif 625 <= tcfermo_zoro < 750:
                frame_zoro = fissezoro_frames[5]
            elif 750 <= tcfermo_zoro < 875:
                frame_zoro = fissezoro_frames[6]
            else:
                frame_zoro = fissezoro_frames[7]
        elif mosse_zoro == 2:
            if personaggio_cattivo == 1:
                if 0 <= tpugno_zoro < 133:
                    frame_zoro = pugno_frames[0]
                elif 133 <= tpugno_zoro < 266:
                    frame_zoro = pugno_frames[1]
                elif 266 <= tpugno_zoro < 399:
                    frame_zoro = pugno_frames[2]
                elif 399 <= tpugno_zoro < 532:
                    frame_zoro = pugno_frames[3]
                elif 532 <= tpugno_zoro < 665:
                    frame_zoro = pugno_frames[4]
                else:
                    frame_zoro = pugno_frames[5]
            elif personaggio_cattivo == 2:
                if 0 <= tpugno_zoro < 82:
                    frame_zoro = pugno_frames[0]
                elif 82 <= tpugno_zoro < 164:
                    frame_zoro = pugno_frames[1]
                elif 164 <= tpugno_zoro < 246:
                    frame_zoro = pugno_frames[2]
                elif 246 <= tpugno_zoro < 328:
                    frame_zoro = pugno_frames[3]
                elif 328 <= tpugno_zoro < 410:
                    frame_zoro = pugno_frames[4]
                elif 410 <= tpugno_zoro < 492:
                    frame_zoro = pugno_frames[5]
                elif 492 <= tpugno_zoro < 574:
                    frame_zoro = pugno_frames[6]
                elif 574 <= tpugno_zoro < 656:
                    frame_zoro = pugno_frames[7]
                elif 656 <= tpugno_zoro < 738:
                    frame_zoro = pugno_frames[8]
                elif 738 <= tpugno_zoro < 820:
                    frame_zoro = pugno_frames[9]
                else:
                    frame_zoro = pugno_frames[10]

        elif mosse_zoro == 3:
            if personaggio_cattivo == 1:
                if 0 <= tspecial_zoro < 93:
                    frame_zoro = special_frames[0]
                elif 93 <= tspecial_zoro < 186:
                    frame_zoro = special_frames[1]
                elif 186 <= tspecial_zoro < 279:
                    frame_zoro = special_frames[2]
                elif 279 <= tspecial_zoro < 372:
                    frame_zoro = special_frames[3]
                elif 372 <= tspecial_zoro < 465:
                    frame_zoro = special_frames[4]
                elif 465 <= tspecial_zoro < 558:
                    frame_zoro = special_frames[5]
                else:
                    frame_zoro = special_frames[6]
            elif personaggio_cattivo == 2:
                if 0 <= tspecial_zoro < 111:
                    frame_zoro = special_frames[0]
                elif 111 <= tspecial_zoro < 222:
                    frame_zoro = special_frames[1]
                elif 222 <= tspecial_zoro < 333:
                    frame_zoro = special_frames[2]
                elif 333 <= tspecial_zoro < 444:
                    frame_zoro = special_frames[3]
                elif 444 <= tspecial_zoro < 555:
                    frame_zoro = special_frames[4]
                elif 555 <= tspecial_zoro < 666:
                    frame_zoro = special_frames[5]
                elif 666 <= tspecial_zoro < 777:
                    frame_zoro = special_frames[6]
                elif 777 <= tspecial_zoro < 888:
                    frame_zoro = special_frames[7]
                else:
                    frame_zoro = special_frames[8]

        elif mosse_zoro == 4:
            if 0 <= tsottoterra_zoro < 133:
                frame_zoro = sottoterra_frames[0]
            elif 133 <= tsottoterra_zoro < 266:
                frame_zoro = sottoterra_frames[1]
            elif 266 <= tsottoterra_zoro < 400:
                frame_zoro = sottoterra_frames[2]
            else:
                frame_zoro = sottoterra_frames[0]
        elif mosse_zoro == 5:
            if personaggio_cattivo == 1:
                if 0 <= tempo_stordito_zoro < 125:
                    frame_zoro = colpitozoro_frames[0]
                elif 125 <= tempo_stordito_zoro < 250:
                    frame_zoro = colpitozoro_frames[1]
                elif 250 <= tempo_stordito_zoro < 375:
                    frame_zoro = colpitozoro_frames[2]
                elif 375 <= tempo_stordito_zoro < 500:
                    frame_zoro = colpitozoro_frames[3]
                elif 500 <= tempo_stordito_zoro < 625:
                    frame_zoro = colpitozoro_frames[4]
                else:
                    frame_zoro = colpitozoro_frames[4]
            elif personaggio_cattivo == 2:
                if 0 <= tempo_stordito_zoro < 100:
                    frame_zoro = colpitozoro_frames[0]
                elif 100 <= tempo_stordito_zoro < 200:
                    frame_zoro = colpitozoro_frames[1]
                elif 200 <= tempo_stordito_zoro < 300:
                    frame_zoro = colpitozoro_frames[2]
                elif 300 <= tempo_stordito_zoro < 400:
                    frame_zoro = colpitozoro_frames[3]
                elif 400 <= tempo_stordito_zoro < 500:
                    frame_zoro = colpitozoro_frames[4]
                elif 500 <= tempo_stordito_zoro < 600:
                    frame_zoro = colpitozoro_frames[5]
                elif 600 <= tempo_stordito_zoro < 700:
                    frame_zoro = colpitozoro_frames[6]
                elif 700 <= tempo_stordito_zoro < 800:
                    frame_zoro = colpitozoro_frames[7]
                elif 800 <= tempo_stordito_zoro < 900:
                    frame_zoro = colpitozoro_frames[8]
                elif 900 <= tempo_stordito_zoro < 1000:
                    frame_zoro = colpitozoro_frames[8]  # rimane l'ultimo frame
                else:
                    frame_zoro = colpitozoro_frames[8]


        # ---------- ANIMAZIONE LUFFY ----------
        # ---------- GESTIONE ANIMAZIONE PUGNO LUFFY ----------
        if animazione_pugno_in_corso_luffy:
            tpugno_luffy += clock.get_time()
            if tpugno_luffy < 800:
                if personaggio_buono ==1:
                    if giro_luffy:
                        if tpugno_luffy <= 200:
                            x_luffy += 2
                        elif tpugno_luffy < 400:
                            x_luffy += 2
                        elif tpugno_luffy < 600:
                            x_luffy += 2
                        elif tpugno_luffy < 700:
                            x_luffy -= 2
                        elif tpugno_luffy < 800:
                            x_luffy -= 2
                    else:
                        if tpugno_luffy <= 200:
                            x_luffy -= 2
                        elif tpugno_luffy < 400:
                            x_luffy -= 2
                        elif tpugno_luffy < 600:
                            x_luffy -= 2
                        elif tpugno_luffy < 700:
                            x_luffy += 2
                        elif tpugno_luffy < 800:
                            x_luffy += 2
                elif personaggio_buono ==2:
                    if not giro_luffy:
                        if tpugno_luffy <= 200:
                            x_luffy += 2
                        elif tpugno_luffy < 400:
                            x_luffy += 2
                        elif tpugno_luffy < 600:
                            x_luffy += 2
                        elif tpugno_luffy < 700:
                            x_luffy -= 2
                        elif tpugno_luffy < 800:
                            x_luffy -= 2
                    else:
                        if tpugno_luffy <= 200:
                            x_luffy -= 2
                        elif tpugno_luffy < 400:
                            x_luffy -= 2
                        elif tpugno_luffy < 600:
                            x_luffy -= 2
                        elif tpugno_luffy < 700:
                            x_luffy += 2
                        elif tpugno_luffy < 800:
                            x_luffy += 2
            else:
                mosse_luffy = 1
                animazione_pugno_in_corso_luffy = False
                tpugno_luffy = 0

        # ---------- GESTIONE ANIMAZIONE SPECIAL LUFFY ----------
        if animazione_special_in_corso_luffy:
            tspecial_luffy += clock.get_time()
            if tspecial_luffy < 803:
                if personaggio_buono ==1:
                    if giro_luffy:
                        # Luffy guarda a destra: avanzamento poi ritrazione
                        if tspecial_luffy <= 200:
                            x_luffy += 5
                        elif tspecial_luffy  < 300:
                            x_luffy += 2
                        elif tspecial_luffy < 400:
                            x_luffy += 4
                        elif tspecial_luffy < 500:
                            x_luffy += 2
                        elif tspecial_luffy < 600:
                            x_luffy += 3
                        elif tspecial_luffy < 700:
                            x_luffy -= 10
                        elif tspecial_luffy < 750:
                            x_luffy -= 3
                        elif tspecial_luffy < 800:
                            x_luffy -= 4
                    else:
                        # Luffy guarda a sinistra: stesso timing ma segni invertiti
                        if tspecial_luffy <= 200:
                            x_luffy -= 5
                        elif tspecial_luffy < 400:
                            x_luffy -= 4
                        elif tspecial_luffy < 600:
                            x_luffy -= 3
                        elif tspecial_luffy < 700:
                            x_luffy += 10
                        elif tspecial_luffy < 750:
                            x_luffy += 3
                        elif tspecial_luffy < 800:
                            x_luffy += 4
                elif personaggio_buono ==2:
                    if not giro_luffy:
                        # Luffy guarda a destra: avanzamento poi ritrazione
                        if tspecial_luffy <= 200:
                            x_luffy += 5
                        elif tspecial_luffy  < 300:
                            x_luffy += 2
                        elif tspecial_luffy < 400:
                            x_luffy += 4
                        elif tspecial_luffy < 500:
                            x_luffy += 2
                        elif tspecial_luffy < 600:
                            x_luffy += 3
                        elif tspecial_luffy < 700:
                            x_luffy -= 10
                        elif tspecial_luffy < 750:
                            x_luffy -= 3
                        elif tspecial_luffy < 800:
                            x_luffy -= 4
                    else:
                        # Luffy guarda a sinistra: stesso timing ma segni invertiti
                        if tspecial_luffy <= 200:
                            x_luffy -= 5
                        elif tspecial_luffy < 400:
                            x_luffy -= 4
                        elif tspecial_luffy < 600:
                            x_luffy -= 3
                        elif tspecial_luffy < 700:
                            x_luffy += 10
                        elif tspecial_luffy < 750:
                            x_luffy += 3
                        elif tspecial_luffy < 800:
                            x_luffy += 4      
            else:
                mosse_luffy = 1
                animazione_special_in_corso_luffy = False
                tspecial_luffy = 0
                
        if animazione_parata_in_corso_luffy:
            tparata_luffy += clock.get_time()
            if tparata_luffy >= 700:
                mosse_luffy = 1
                animazione_parata_in_corso_luffy = False
                tparata_luffy = 0
        # ---------- STUN ZORO ----------
        if stordito_zoro:

            tempo_stordito_zoro += clock.get_time()
            if personaggio_buono ==1:
                if not giro_luffy:
                    if tempo_stordito_zoro <= 200:
                        x_zoro -= 7
                    elif tempo_stordito_zoro < 400:
                        x_zoro -= 3
                    elif tempo_stordito_zoro < 600:
                        x_zoro -= 2
                    elif tempo_stordito_zoro < 700:
                        x_zoro -= 1
                    elif tempo_stordito_zoro < 750:
                        x_zoro -= 1
                    elif tempo_stordito_zoro < 800:
                        x_zoro -= 1
                else:   
                    if tempo_stordito_zoro <= 100:
                        x_zoro += 6
                    elif tempo_stordito_zoro < 400:
                        x_zoro += 3
                    elif tempo_stordito_zoro < 600:
                        x_zoro += 2
                    elif tempo_stordito_zoro < 700:
                        x_zoro += 1
                    elif tempo_stordito_zoro < 750:
                        x_zoro += 1
                    elif tempo_stordito_zoro < 800:
                        x_zoro += 1
            elif personaggio_buono ==2:
                if giro_luffy:
                    if tempo_stordito_zoro <= 200:
                        x_zoro -= 7
                    elif tempo_stordito_zoro < 400:
                        x_zoro -= 3
                    elif tempo_stordito_zoro < 600:
                        x_zoro -= 2
                    elif tempo_stordito_zoro < 700:
                        x_zoro -= 1
                    elif tempo_stordito_zoro < 750:
                        x_zoro -= 1
                    elif tempo_stordito_zoro < 800:
                        x_zoro -= 1
                else:   
                    if tempo_stordito_zoro <= 100:
                        x_zoro += 6
                    elif tempo_stordito_zoro < 400:
                        x_zoro += 3
                    elif tempo_stordito_zoro < 600:
                        x_zoro += 2
                    elif tempo_stordito_zoro < 700:
                        x_zoro += 1
                    elif tempo_stordito_zoro < 750:
                        x_zoro += 1
                    elif tempo_stordito_zoro < 800:
                        x_zoro += 1
            # mantieni Zoro entro i bordi
            if x_zoro < 0:
                x_zoro = 0
            if x_zoro > larghezzaSfondo - larghezz_ZORO:
                x_zoro = larghezzaSfondo - larghezz_ZORO
            # fine dello stordimento
            if tempo_stordito_zoro >= DURATA_STORDIMENTO:
                stordito_zoro = False
                tempo_stordito_zoro = 0
                mosse_zoro = 1
        # ---------- STUN LUFFY ----------
        if stordito_luffy:
            tempo_stordito_luffy += clock.get_time()
            if direzione_stordito_luffy == 1:
                if tempo_stordito_luffy < 250:
                    x_luffy += 4
                elif 250 <= tempo_stordito_luffy < 500:
                    x_luffy += 3
                elif 500 <= tempo_stordito_luffy < 750:
                    x_luffy += 2
                elif 750 <= tempo_stordito_luffy < 1000:
                    x_luffy += 2
            else:
                if tempo_stordito_luffy < 250:
                    x_luffy -= 4
                elif 250 <= tempo_stordito_luffy < 500:
                    x_luffy -= 3
                elif 500 <= tempo_stordito_luffy < 750:
                    x_luffy -= 2
                elif 750 <= tempo_stordito_luffy < 1000:
                    x_luffy -= 2

            # alla fine del timer di stordimento, ripristina lo stato di Luffy
            if tempo_stordito_luffy >= DURATA_STORDIMENTO:
                stordito_luffy = False
                tempo_stordito_luffy = 0
                mosse_luffy = 1
                

        if mosse_luffy == 0:
            if personaggio_buono ==1:
                if 0 <= tc_luffy < 100:
                    frame_luffy = corsalufy_frames[0]
                elif 100 <= tc_luffy < 200:
                    frame_luffy = corsalufy_frames[1]
                elif 200 <= tc_luffy < 300:
                    frame_luffy = corsalufy_frames[2]
                elif 300 <= tc_luffy < 400:
                    frame_luffy = corsalufy_frames[3]
                elif 400 <= tc_luffy < 500:
                    frame_luffy = corsalufy_frames[4]
                else:
                    frame_luffy = corsalufy_frames[5]
            elif personaggio_buono ==2:
                if 0 <= tc_luffy < 100:
                    frame_luffy = corsalufy_frames[0]
                elif 100 <= tc_luffy < 200:
                    frame_luffy = corsalufy_frames[1]
                elif 200 <= tc_luffy < 300:
                    frame_luffy = corsalufy_frames[2]
                elif 300 <= tc_luffy < 400:
                    frame_luffy = corsalufy_frames[3]
                elif 400 <= tc_luffy < 500:
                    frame_luffy = corsalufy_frames[4]
                elif 500 <= tc_luffy < 600:
                    frame_luffy = corsalufy_frames[5]
                elif 600 <= tc_luffy < 700:
                    frame_luffy = corsalufy_frames[6]
                elif 700 <= tc_luffy < 800:
                    frame_luffy = corsalufy_frames[7]
                elif 800 <= tc_luffy < 900:
                    frame_luffy = corsalufy_frames[8]
                elif 900 <= tc_luffy < 1000:
                    frame_luffy = corsalufy_frames[9]
                else:
                    frame_luffy = corsalufy_frames[9]
                
        elif mosse_luffy == 1:
            if personaggio_buono ==1:
                if 0 <= tcfermo_luffy < 150:
                    frame_luffy = fermolufy_frames[0]
                elif 150 <= tcfermo_luffy < 300:
                    frame_luffy = fermolufy_frames[1]
                elif 300 <= tcfermo_luffy < 450:
                    frame_luffy = fermolufy_frames[2]
                elif 450 <= tcfermo_luffy < 600:
                    frame_luffy = fermolufy_frames[3]
                elif 600 <= tcfermo_luffy < 750:
                    frame_luffy = fermolufy_frames[4]
                elif 750 <= tcfermo_luffy < 900:
                    frame_luffy = fermolufy_frames[5]
                else:
                    frame_luffy = fermolufy_frames[6]
            elif personaggio_buono ==2:
                if 0 <= tcfermo_luffy < 114:
                    frame_luffy = fermolufy_frames[0]
                elif 114 <= tcfermo_luffy < 228:
                    frame_luffy = fermolufy_frames[1]
                elif 228 <= tcfermo_luffy < 342:
                    frame_luffy = fermolufy_frames[2]
                elif 342 <= tcfermo_luffy < 456:
                    frame_luffy = fermolufy_frames[3]
                elif 456 <= tcfermo_luffy < 570:
                    frame_luffy = fermolufy_frames[4]
                elif 570 <= tcfermo_luffy < 684:
                    frame_luffy = fermolufy_frames[5]
                elif 684 <= tcfermo_luffy < 798:
                    frame_luffy = fermolufy_frames[6]
                elif 798 <= tcfermo_luffy < 912:
                    frame_luffy = fermolufy_frames[7]
                elif 912 <= tcfermo_luffy < 1026:
                    frame_luffy = fermolufy_frames[8]
                elif 1026 <= tcfermo_luffy < 1140:
                    frame_luffy = fermolufy_frames[9]
                elif 1140 <= tcfermo_luffy < 1254:
                    frame_luffy = fermolufy_frames[10]
                    
                elif 1254 <= tcfermo_luffy < 1368:
                    frame_luffy = fermolufy_frames[11]
                   
                elif 1368 <= tcfermo_luffy < 1482:
                    frame_luffy = fermolufy_frames[12]
                    
                elif 1482 <= tcfermo_luffy <= 1600:
                    frame_luffy = fermolufy_frames[13]
                    
        elif mosse_luffy == 2:
            if personaggio_buono ==1:
                if 0 <= tpugno_luffy < 80:
                    frame_luffy = pugnolufy_frames[0]
                elif 80 <= tpugno_luffy < 160:
                    frame_luffy = pugnolufy_frames[1]
                elif 160 <= tpugno_luffy < 240:
                    frame_luffy = pugnolufy_frames[2]
                elif 240 <= tpugno_luffy < 320:
                    frame_luffy = pugnolufy_frames[3]
                elif 320 <= tpugno_luffy < 400:
                    frame_luffy = pugnolufy_frames[4]
                elif 400 <= tpugno_luffy < 480:
                    frame_luffy = pugnolufy_frames[5]
                elif 480 <= tpugno_luffy < 560:
                    frame_luffy = pugnolufy_frames[6]
                elif 560 <= tpugno_luffy < 640:
                    frame_luffy = pugnolufy_frames[7]
                elif 640 <= tpugno_luffy < 720:
                    frame_luffy = pugnolufy_frames[8]
                else:
                    frame_luffy = pugnolufy_frames[9]
            elif personaggio_buono ==2:
                if 0 <= tpugno_luffy < 110:
                    frame_luffy = pugnolufy_frames[0]
                elif 110 <= tpugno_luffy < 220:
                    frame_luffy = pugnolufy_frames[1]
                elif 220 <= tpugno_luffy < 330:
                    frame_luffy = pugnolufy_frames[2]
                elif 330 <= tpugno_luffy < 440:
                    frame_luffy = pugnolufy_frames[3]
                elif 440 <= tpugno_luffy < 580:
                    frame_luffy = pugnolufy_frames[4]
                else:
                    frame_luffy = pugnolufy_frames[3]
                    
                
        elif mosse_luffy == 3:
            if personaggio_buono ==1:
                if 0 <= tspecial_luffy < 73:
                    frame_luffy = speciallufy_frames[0]
                elif 73 <= tspecial_luffy < 146:
                    frame_luffy = speciallufy_frames[1]
                elif 146 <= tspecial_luffy < 219:
                    frame_luffy = speciallufy_frames[2]
                elif 219 <= tspecial_luffy < 292:
                    frame_luffy = speciallufy_frames[3]
                elif 292 <= tspecial_luffy < 365:
                    frame_luffy = speciallufy_frames[4]
                elif 365 <= tspecial_luffy < 438:
                    frame_luffy = speciallufy_frames[5]
                elif 438 <= tspecial_luffy < 550:
                    frame_luffy = speciallufy_frames[6]
                elif 550 <= tspecial_luffy < 600:
                    frame_luffy = speciallufy_frames[7]
                elif 600 <= tspecial_luffy < 657:
                    frame_luffy = speciallufy_frames[8]
                elif 657 <= tspecial_luffy < 730:
                    frame_luffy = speciallufy_frames[9]
                else:
                    frame_luffy = speciallufy_frames[10]
            elif personaggio_buono ==2:
                if 0 <= tspecial_luffy < 73:
                    frame_luffy = speciallufy_frames[0]
                elif 73 <= tspecial_luffy < 146:
                    frame_luffy = speciallufy_frames[1]
                elif 146 <= tspecial_luffy < 219:
                    frame_luffy = speciallufy_frames[2]
                elif 219 <= tspecial_luffy < 292:
                    frame_luffy = speciallufy_frames[3]
                elif 292 <= tspecial_luffy < 365:
                    frame_luffy = speciallufy_frames[4]
                elif 365 <= tspecial_luffy < 438:
                    frame_luffy = speciallufy_frames[5]
                elif 438 <= tspecial_luffy < 511:
                    frame_luffy = speciallufy_frames[6]
                elif 511 <= tspecial_luffy < 584:
                    frame_luffy = speciallufy_frames[7]
                elif 584 <= tspecial_luffy < 657:
                    frame_luffy = speciallufy_frames[8]
                elif 657 <= tspecial_luffy < 730:
                    frame_luffy = speciallufy_frames[9]
                elif 730 <= tspecial_luffy < 803:
                    frame_luffy = speciallufy_frames[10]
                elif 803 <= tspecial_luffy < 876:
                    frame_luffy = speciallufy_frames[11]
                else:
                    frame_luffy = speciallufy_frames[12]
        elif mosse_luffy == 4:
            if 0 <= tparata_luffy < 100:
                frame_luffy = paratalufy_frames[0]
            elif 100 <= tparata_luffy < 200:
                frame_luffy = paratalufy_frames[1]
            elif 200 <= tparata_luffy < 300:
                frame_luffy = paratalufy_frames[2]
            elif 300 <= tparata_luffy < 400:
                frame_luffy = paratalufy_frames[3]
            elif 400 <= tparata_luffy < 500:
                frame_luffy = paratalufy_frames[4]
            elif 500 <= tparata_luffy < 600:
                frame_luffy = paratalufy_frames[5]
            else:
                frame_luffy = paratalufy_frames[6]
        elif mosse_luffy == 5:  
            if 0 <= tempo_stordito_luffy < 125:
                frame_luffy = colpitolufy_frames[0]
            elif 125 <= tempo_stordito_luffy < 250:
                frame_luffy = colpitolufy_frames[1]
            elif 250 <= tempo_stordito_luffy < 375:
                frame_luffy = colpitolufy_frames[2]
            elif 375 <= tempo_stordito_luffy < 500:
                frame_luffy = colpitolufy_frames[3]
            elif 500 <= tempo_stordito_luffy < 625:
                frame_luffy = colpitolufy_frames[4]
            elif 625 <= tempo_stordito_luffy < 750:
                frame_luffy = colpitolufy_frames[5]
            elif 750 <= tempo_stordito_luffy < 875:
                frame_luffy = colpitolufy_frames[6]
            elif 875 <= tempo_stordito_luffy < 1000:
                frame_luffy = colpitolufy_frames[7]
            else:
                frame_luffy = colpitolufy_frames[7]

     
        # ---------- CALCOLO POSIZIONI ----------
        larghezz_ZORO = frame_zoro.get_width()
        altezz_ZORO = frame_zoro.get_height()
        y_zoro = altezzaSfondo - altezzaterreno - altezz_ZORO + 10
        larghezz_LUFFY_nuova = frame_luffy.get_width()
        altezz_LUFFY = frame_luffy.get_height()
        y_luffy = altezzaSfondo - altezzaterreno - altezz_LUFFY + 10

        if personaggio_buono == 2 and (mosse_luffy == 1 or mosse_luffy == 4) and giro_luffy:
            x_luffy = x_luffy + (larghezz_LUFFY - larghezz_LUFFY_nuova)
            
        larghezz_LUFFY = larghezz_LUFFY_nuova
        

    
        if personaggio_cattivo == 2:
            if giro:
                frame_zoro = pygame.transform.flip(frame_zoro, False, False)
            else:
                frame_zoro = pygame.transform.flip(frame_zoro, True, False)
        else:
            if giro:
                frame_zoro = pygame.transform.flip(frame_zoro, True, False)
            else:
                frame_zoro = pygame.transform.flip(frame_zoro, False, False)
        if giro_luffy:
            frame_luffy = pygame.transform.flip(frame_luffy, True, False)
        if personaggio_buono ==2 and animazione_parata_in_corso_luffy:
            frame_luffy = pygame.transform.flip(frame_luffy, True, False)
        if stordito_luffy and personaggio_buono ==2:
            frame_luffy = pygame.transform.flip(frame_luffy, True, False)
            
            
            
        if x_luffy < 0:
            x_luffy = 0
        if x_luffy > larghezzaSfondo - larghezz_LUFFY:
            x_luffy = larghezzaSfondo - larghezz_LUFFY
        if x_zoro < 0:
            x_zoro = 0
        if x_zoro > larghezzaSfondo - larghezz_ZORO:
            x_zoro = larghezzaSfondo - larghezz_ZORO

        distanza_dal_terreno = altezzaterreno - 28

        testo_parata_zoro = font.render("Parata: W", True, (0, 0, 0)) 
        testo_pugno_zoro = font.render("Pugno: E", True, (0, 0, 0))
        testo_special_zoro = font.render("Teletrasporto: Q", True, (0, 0, 0))

        if personaggio_cattivo == 2:
            tempo_trascorso = pygame.time.get_ticks() - ultimo_tornado
            pronto = tempo_trascorso >= TEMPO_RICARICA_TORNADO
            if pronto:
                testo_special_zoro = font.render("Tornado: Q (pronto)", True, (0, 255, 0))
            else:
                tempo_rimanente = (TEMPO_RICARICA_TORNADO - tempo_trascorso) // 1000
                testo_special_zoro = font.render(f"Tornado: Q ({tempo_rimanente}s)", True, (255, 0, 0))
        elif personaggio_cattivo == 1:
            tempo_trascorso = pygame.time.get_ticks() - ultimo_sottoterra
            pronto = tempo_trascorso >= TEMPO_RICARICA_SOTTOTERRA
            if pronto:
                testo_special_zoro = font.render("Teletrasporto: Q (pronto)", True, (0, 255, 0))
            else:
                tempo_rimanente = (TEMPO_RICARICA_SOTTOTERRA - tempo_trascorso) // 1000
                testo_special_zoro = font.render(f"Teletrasporto: Q ({tempo_rimanente}s)", True, (255, 0, 0))

        pos_y_parata_zoro = altezzaSfondo - distanza_dal_terreno
        pos_y_pugno_zoro = pos_y_parata_zoro + 16
        pos_y_special_zoro = pos_y_pugno_zoro + 16

        testo_parata_luffy = font.render("Parata: I", True, (0, 0, 0))
        if personaggio_buono == 1:
            testo_pugno_luffy = font.render("Pugno: O", True, (0, 0, 0))
            testo_special_luffy = font.render("getpistol: U", True, (0, 0, 0))
        elif personaggio_buono == 2:
            testo_pugno_luffy = font.render("Calcio: O", True, (0, 0, 0))
            testo_special_luffy = font.render("Rotante: U", True, (0, 0, 0))
        
        
        # ---------- DISEGNO SCHERMO ----------
        schermo.blit(sfondo, (0, 0))
        schermo.blit(terreno, (0, altezzaSfondo - altezzaterreno))
        schermo.blit(frame_zoro, (x_zoro, y_zoro))
        schermo.blit(frame_luffy, (x_luffy, y_luffy))
        schermo.blit(testo_pugno_zoro, (10, pos_y_pugno_zoro))
        schermo.blit(testo_parata_zoro, (10, pos_y_parata_zoro))
        schermo.blit(testo_special_zoro, (10, pos_y_special_zoro))
        schermo.blit(testo_pugno_luffy, (larghezzaSfondo - 90, pos_y_pugno_zoro))
        schermo.blit(testo_parata_luffy, (larghezzaSfondo - 90, pos_y_parata_zoro))
        schermo.blit(testo_special_luffy, (larghezzaSfondo - 100, pos_y_special_zoro))
       
        if personaggio_cattivo == 2 and animazione_tornado_in_corso_zoro:
            tempo_ciclico = tempo_tornado % 400
            
            if 0 <= tempo_ciclico < 133:
                frame_tornado = tornado_frames[0]
            elif 133 <= tempo_ciclico < 266:
                frame_tornado = tornado_frames[1]
            else:
                frame_tornado = tornado_frames[2]
            
            schermo.blit(frame_tornado, (x_tornado, y_tornado))
        if personaggio_cattivo == 1:
            schermo.blit(frames_cards[1], (0, 0))
        elif personaggio_cattivo == 2:
            schermo.blit(frames_cards[3], (0, 0))
        if personaggio_buono == 1:
            schermo.blit(frames_cards[0], (larghezzaSfondo - frames_cards[1].get_width(), 0))
        elif personaggio_buono == 2:
            schermo.blit(frames_cards[2], (larghezzaSfondo - frames_cards[1].get_width(), 0))
        
        # Vita Zoro
        if vita_zoro == 100:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[0], (152, 47))
            schermo.blit(frames_vita[0], (165, 47))
            schermo.blit(frames_vita[0], (178, 47))
            schermo.blit(frames_vita[0], (191, 47))
            schermo.blit(frames_vita[0], (204, 47))
            schermo.blit(frames_vita[0], (217, 47))

        elif vita_zoro == 90:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[0], (152, 47))
            schermo.blit(frames_vita[0], (165, 47))
            schermo.blit(frames_vita[0], (178, 47))
            schermo.blit(frames_vita[0], (191, 47))
            schermo.blit(frames_vita[0], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 80:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[0], (152, 47))
            schermo.blit(frames_vita[0], (165, 47))
            schermo.blit(frames_vita[0], (178, 47))
            schermo.blit(frames_vita[0], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 70:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[0], (152, 47))
            schermo.blit(frames_vita[0], (165, 47))
            schermo.blit(frames_vita[0], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 60:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[0], (152, 47))
            schermo.blit(frames_vita[0], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 50:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[0], (152, 47))
            schermo.blit(frames_vita[1], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 40:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[0], (139, 47))
            schermo.blit(frames_vita[1], (152, 47))
            schermo.blit(frames_vita[1], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 30:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[0], (126, 47))
            schermo.blit(frames_vita[1], (139, 47))
            schermo.blit(frames_vita[1], (152, 47))
            schermo.blit(frames_vita[1], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 20:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[0], (113, 47))
            schermo.blit(frames_vita[1], (126, 47))
            schermo.blit(frames_vita[1], (139, 47))
            schermo.blit(frames_vita[1], (152, 47))
            schermo.blit(frames_vita[1], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        elif vita_zoro == 10:
            schermo.blit(frames_vita[0], (100, 47))
            schermo.blit(frames_vita[1], (113, 47))
            schermo.blit(frames_vita[1], (126, 47))
            schermo.blit(frames_vita[1], (139, 47))
            schermo.blit(frames_vita[1], (152, 47))
            schermo.blit(frames_vita[1], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))

        else:
            schermo.blit(frames_vita[1], (100, 47))
            schermo.blit(frames_vita[1], (113, 47))
            schermo.blit(frames_vita[1], (126, 47))
            schermo.blit(frames_vita[1], (139, 47))
            schermo.blit(frames_vita[1], (152, 47))
            schermo.blit(frames_vita[1], (165, 47))
            schermo.blit(frames_vita[1], (178, 47))
            schermo.blit(frames_vita[1], (191, 47))
            schermo.blit(frames_vita[1], (204, 47))
            schermo.blit(frames_vita[1], (217, 47))
        # Vita Luffy
        if vita_luffy == 100:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 90:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 80:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 70:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 60:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 50:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 40:  
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 30:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 20:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[0], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        elif vita_luffy == 10:
            schermo.blit(frames_vita[0], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
        else:
            schermo.blit(frames_vita[1], (larghezzaSfondo - 217 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 204 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 191 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 178 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 165 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 152 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 139 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 126 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 113 - 10, 47))
            schermo.blit(frames_vita[1], (larghezzaSfondo - 100 - 10, 47))
            
        
                
        
        #maschera
        maschera_zoro = pygame.mask.from_surface(frame_zoro)  # Zoro mask
        maschera_luffy = pygame.mask.from_surface(frame_luffy)  # Luffy mask

        offset_x = x_luffy - x_zoro
        offset_y = y_luffy - y_zoro
        
        
        danno_pugno = 10
        danno_speciale = 20 
        if personaggio_buono == 1:
            if giro_luffy:  # Luffy guarda a destra
                zoro_davanti = x_zoro > x_luffy
            else:  # Luffy guarda a sinistra
                zoro_davanti = x_zoro < x_luffy
        elif personaggio_buono == 2:
            if not giro_luffy:  # Zoro guarda a destra
                zoro_davanti = x_zoro > x_luffy
            else:  # Zoro guarda a sinistra
                zoro_davanti = x_zoro < x_luffy
        

        # Calcola se Luffy sta attaccando Zoro da davanti
        if giro:  # Zoro guarda a destra
            luffy_davanti = x_luffy > x_zoro
        else:  # Zoro guarda a sinistra
            luffy_davanti = x_luffy < x_zoro

        
        if maschera_zoro.overlap(maschera_luffy, (offset_x, offset_y)):
            
            # ----- ATTACCHI DI ZORO CONTRO LUFFY -----
            # PUGNO DI ZORO
            if animazione_pugno_in_corso_zoro and 266 <= tpugno_zoro < 532 and not pugno_zoro_gestito:
                if not stordito_luffy:
                    if animazione_parata_in_corso_luffy and zoro_davanti:
                        if not parata_fatta_zoro:
                            parata_fatta_zoro = True
                        pugno_zoro_gestito = True
                    else:
                        # Altrimenti subisce danno
                        vita_luffy -= danno_pugno
                        pugno_sound.play()  # Suono del pugno
                        stordito_luffy = True
                        direzione_stordito_luffy = 1 if giro else -1
                        tempo_stordito_luffy = 0
                        mosse_luffy = 5
                        pugno_zoro_gestito = True

            # SPECIALE DI ZORO
            if animazione_special_in_corso_zoro and 279 <= tspecial_zoro < 465 and not speciale_zoro_gestito:
                if not stordito_luffy:
                    if animazione_parata_in_corso_luffy and zoro_davanti:
                        if not parata_fatta_zoro:
                            parata_fatta_zoro = True
                        speciale_zoro_gestito = True
                    else:
                        vita_luffy -= danno_speciale
                        pugno_sound.play()  # Suono del pugno
                        stordito_luffy = True
                        direzione_stordito_luffy = 1 if giro else -1
                        tempo_stordito_luffy = 0
                        mosse_luffy = 5
                        speciale_zoro_gestito = True


            # ----- ATTACCHI DI LUFFY CONTRO ZORO -----
            # PUGNO DI LUFFY
            if animazione_pugno_in_corso_luffy and 160 <= tpugno_luffy < 320 and not pugno_luffy_gestito:
                if not stordito_zoro:
                    
                    if animazione_sottoterra_in_corso_zoro and luffy_davanti:
                        if not parata_fatta_luffy:
                            parata_fatta_luffy = True
                        pugno_luffy_gestito = True
                    else:
                        # Altrimenti subisce danno
                        vita_zoro -= danno_pugno
                        pugno_sound.play()  
                        stordito_zoro = True
                        tempo_stordito_zoro = 0
                        mosse_zoro = 5
                        pugno_luffy_gestito = True

            # SPECIALE DI LUFFY
            if animazione_special_in_corso_luffy and 219 <= tspecial_luffy < 365 and not speciale_luffy_gestito:
                if not stordito_zoro:
                    if animazione_sottoterra_in_corso_zoro and luffy_davanti:
                        if not parata_fatta_luffy:
                            parata_fatta_luffy = True
                        speciale_luffy_gestito = True
                    else:
                        vita_zoro -= danno_speciale
                        pugno_sound.play()  # Suono del pugno
                        stordito_zoro = True
                        tempo_stordito_zoro = 0
                        mosse_zoro = 5
                        speciale_luffy_gestito = True
                        
        
                                    
        # COLLISIONE CON IL TORNADO DI CROCODILE 
        if personaggio_cattivo == 2 and animazione_tornado_in_corso_zoro and not stordito_luffy:
            if 0 <= tempo_tornado < 133:
                frame_tornado_collisione = tornado_frames[0]
            elif 133 <= tempo_tornado < 266:
                frame_tornado_collisione = tornado_frames[1]
            else:
                frame_tornado_collisione = tornado_frames[2]

            maschera_tornado = pygame.mask.from_surface(frame_tornado_collisione)
            offset_tornado_x = x_luffy - x_tornado
            offset_tornado_y = y_luffy - y_tornado
            
            if maschera_tornado.overlap(maschera_luffy, (offset_tornado_x, offset_tornado_y)):
                if personaggio_buono == 1:
                    if giro_luffy:  # Luffy guarda a destra
                        tornado_davanti = x_tornado > x_luffy
                    else:           # Luffy guarda a sinistra
                        tornado_davanti = x_tornado < x_luffy
                elif personaggio_buono == 2:
                    if not giro_luffy: 
                        tornado_davanti = x_tornado > x_luffy
                    else:               # Sanji guarda a sinistra
                        tornado_davanti = x_tornado < x_luffy

                if animazione_parata_in_corso_luffy and tornado_davanti:
                    animazione_tornado_in_corso_zoro = False
                    tempo_tornado = 0
                    tornado_sound.stop()  # Fermo il suono del tornado
                    animazione_parata_in_corso_luffy = False
                    tparata_luffy = 0
                    stordito_luffy = True
                    direzione_stordito_luffy = 1 if tornado_direzione == 1 else -1
                    tempo_stordito_luffy = 0
                    mosse_luffy = 5
                else:
                    vita_luffy -= danno_speciale  
                    pugno_sound.play()  # Suono del colpo
                    stordito_luffy = True
                    direzione_stordito_luffy = 1 if tornado_direzione == 1 else -1
                    tempo_stordito_luffy = 0
                    mosse_luffy = 5
                    animazione_tornado_in_corso_zoro = False 
                    tempo_tornado = 0
                    tornado_sound.stop()  # Fermo il suono del tornado

        if vita_zoro <= 0 :
            gameOver = True
            morto_zoro = True
            schermata = 3
        if vita_luffy <= 0 :
            gameOver = True
            morto_luffy = True
            schermata = 3

        pygame.display.update()
        clock.tick(60)

    elif schermata == 3:
        tempo_morto_zoro = pygame.time.get_ticks() % 1000
        frame_morto_zoro = morto_frames[0]
        altezza_morto_zoro = frame_morto_zoro.get_height()
        lunghezza_morto_zoro = frame_morto_zoro.get_width()
        if morto_zoro:
            if personaggio_cattivo == 1:
                frame_morto_zoro = morto_frames[0]
                altezza_morto_zoro = frame_morto_zoro.get_height()
                lunghezza_morto_zoro = frame_morto_zoro.get_width()   
            elif personaggio_cattivo == 2:
                frame_morto_zoro = morto_frames[3]
                altezza_morto_zoro = morto_frames[3].get_height()
                lunghezza_morto_zoro = morto_frames[3].get_width()
        elif morto_luffy:
            if personaggio_buono == 1:
                frame_morto_zoro = morto_frames[1]
                altezza_morto_zoro = morto_frames[1].get_height()
                lunghezza_morto_zoro = morto_frames[1].get_width()
            elif personaggio_buono == 2:
                frame_morto_zoro = morto_frames[2]
                altezza_morto_zoro = morto_frames[2].get_height()
                lunghezza_morto_zoro = morto_frames[2].get_width() 

        schermo.blit(pygame.image.load('GAMEOVER.jpg'), (0, 0))
        if morto_luffy:
            schermo.blit(frame_morto_zoro, ((larghezzaSfondo - lunghezza_morto_zoro)//2 + 20, (altezzaSfondo - altezza_morto_zoro)//2))
        elif morto_zoro:
            schermo.blit(frame_morto_zoro, ((larghezzaSfondo - lunghezza_morto_zoro)//2, (altezzaSfondo - altezza_morto_zoro)//2))
            
        testo_rigioca = font.render("Premi R per rigiocare", True, (0, 0, 0))
        schermo.blit(testo_rigioca, ((larghezzaSfondo - testo_rigioca.get_width())//2, (altezzaSfondo - testo_rigioca.get_height())//2 + 100))
        testo_esci = font.render("Premi ESC per uscire", True, (0, 0, 0))
        schermo.blit(testo_esci, ((larghezzaSfondo - testo_esci.get_width())//2 , (altezzaSfondo - testo_esci.get_height())//2 + 130))
        
        pygame.display.update()
        clock.tick(60)

pygame.quit()