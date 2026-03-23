import pygame

pygame.init()

LARGHEZZA = 1200
ALTEZZA = 800
ROSSO = (255, 0, 0)
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)

sfondo = pygame.image.load("generale/sfondo_pirati.jpg")
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo ROSSO")
clock = pygame.time.Clock()

# Font: più piccolo
font_piccolo = pygame.font.SysFont(None, 16)
font_istruzioni = pygame.font.SysFont(None, 20)

personaggi = [
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "sprites": {
            "idle": [pygame.image.load(f"allframe/capitano/idle/capitanoidle{i}.png").convert_alpha() for i in range(1, 3)],
            "walk_forward": [pygame.image.load(f"allframe/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle_sick": [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png").convert_alpha() for i in range(1, 6)],
        },
        "info": {"name": "Capitano", "descrizione": "", "abilita": ""},
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "sprites": {
            "idle": [pygame.image.load(f"allframe/cuoco/idle/cuocoidle{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_forward": [pygame.image.load(f"allframe/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png").convert_alpha() for i in range(1, 3)],
            "walk_cycle": [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
        },
        "info": {"name": "Cuoco", "descrizione": "", "abilita": ""},
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "sprites": {
            "idle": [pygame.image.load(f"allframe/guardone/idle/guardoneidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png").convert_alpha() for i in range(1, 5)],
            "walk_cycle": [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png").convert_alpha() for i in range(1, 8)],
            "walk_cycle_sick": [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)],
        },
        "info": {"name": "Guardone", "descrizione": "", "abilita": ""},
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "sprites": {
            "idle": [pygame.image.load(f"allframe/medico/idle/medicoidle{i}.png").convert_alpha() for i in range(1, 9)],
            "walk_forward": [pygame.image.load(f"allframe/medico/camminata_in_avanti/medico{i}_camminatainavanti.png").convert_alpha() for i in range(1, 9)],
            "walk_cycle": [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png").convert_alpha() for i in range(1, 7)],
            "walk_cycle_sick": [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)],
        },
        "info": {"name": "Medico", "descrizione": "", "abilita": ""},
    },
    {
        "stats": {"cost": None, "hp": 3, "alive": True},
        "sprites": {
            "idle": [pygame.image.load(f"allframe/mozzo/idle/mozzoidle{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_forward": [pygame.image.load(f"allframe/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle": [pygame.image.load(f"allframe/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png").convert_alpha() for i in range(1, 4)],
            "walk_cycle_sick": [pygame.image.load(f"allframe/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png").convert_alpha() for i in range(1, 4)],
        },
        "info": {"name": "Mozzo", "descrizione": "", "abilita": ""},
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
    rect = frame_flippato.get_rect(topleft=pos)
    schermo.blit(frame_flippato, rect.topleft)
    return rect


def disegna_etichetta(rect, testo, font, colore_testo=NERO):
    surf = font.render(testo, True, colore_testo)
    padding_x = 4
    padding_y = 2

    box = pygame.Rect(0, 0, surf.get_width() + padding_x * 2, surf.get_height() + padding_y * 2)
    box.midbottom = (rect.centerx, rect.top - 3)

    pygame.draw.rect(schermo, BIANCO, box, border_radius=5)
    pygame.draw.rect(schermo, NERO, box, width=1, border_radius=5)
    schermo.blit(surf, (box.x + padding_x, box.y + padding_y))


def disegna_slot(idx_personaggio, anim, durata, pos, dim, flip, hitboxes, etichetta):
    rect = disegna_animazione(
        schermo,
        personaggi[idx_personaggio]["sprites"],
        anim,
        durata,
        pos,
        dimensione=dim,
        flip=flip,
    )
    # in modalità normale: scritte piccole
    disegna_etichetta(rect, etichetta, font_piccolo)

    hitboxes.append({
        "personaggio": idx_personaggio,
        "anim": anim,
        "durata": durata,
        "dim": dim,
        "flip": flip,
        "rect": rect,
        "etichetta": etichetta,
    })


selezionato = None
gameOver = False

while not gameOver:
    hitboxes = []

    click_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                selezionato = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos

    schermo.fill(ROSSO)

    if selezionato is None:
        # Istruzioni
        titolo = font_istruzioni.render("Clicca su un personaggio per ingrandirlo — Premi 'S' per tornare indietro", True, BIANCO)
        schermo.blit(titolo, (20, 15))

        # ------------------------ modalità normale ------------------------
        # (ho spostato le y un po' più in basso per lasciare spazio alle scritte sopra)

        # CAPITANO
        disegna_slot(0, "walk_forward", 150, (50, 70),  (64, 78), False, hitboxes, "Capitano: avanti")
        disegna_slot(0, "walk_cycle",   150, (150, 70), (64, 78), False, hitboxes, "Capitano: laterale")
        disegna_slot(0, "walk_cycle",   150, (250, 70), (64, 78), True,  hitboxes, "Capitano: laterale (flip)")
        disegna_slot(0, "idle",         200, (350, 70), (64, 78), False, hitboxes, "Capitano: fermo")
        disegna_slot(0, "walk_cycle_sick", 150, (450, 70), (64, 78), False, hitboxes, "Capitano: malato")
        disegna_slot(0, "walk_cycle_sick", 150, (550, 70), (64, 78), True,  hitboxes, "Capitano: malato (flip)")

        # CUOCO
        disegna_slot(1, "walk_forward", 200, (650, 70),  (54, 74), False, hitboxes, "Cuoco: avanti")
        disegna_slot(1, "walk_cycle",   170, (750, 70),  (54, 74), False, hitboxes, "Cuoco: laterale")
        disegna_slot(1, "walk_cycle",   170, (850, 70),  (54, 74), True,  hitboxes, "Cuoco: laterale (flip)")
        disegna_slot(1, "idle",         150, (945, 70),  (54, 74), False, hitboxes, "Cuoco: fermo")
        disegna_slot(1, "walk_cycle_sick", 170, (1040, 70), (54, 74), False, hitboxes, "Cuoco: malato")
        disegna_slot(1, "walk_cycle_sick", 170, (1140, 70), (54, 74), True,  hitboxes, "Cuoco: malato (flip)")

        # GUARDONE
        disegna_slot(2, "walk_forward", 150, (50, 220), (64, 78), False, hitboxes, "Guardone: avanti")
        disegna_slot(2, "walk_cycle",   110, (150, 220), (64, 78), True,  hitboxes, "Guardone: laterale (flip)")
        disegna_slot(2, "walk_cycle",   110, (250, 220), (64, 78), False, hitboxes, "Guardone: laterale")
        disegna_slot(2, "idle",         150, (350, 220), (64, 78), False, hitboxes, "Guardone: fermo")
        disegna_slot(2, "walk_cycle_sick", 110, (450, 220), (64, 78), True,  hitboxes, "Guardone: malato (flip)")
        disegna_slot(2, "walk_cycle_sick", 110, (550, 220), (64, 78), False, hitboxes, "Guardone: malato")

        # MEDICO
        disegna_slot(3, "walk_forward", 120, (650, 220), (60, 74), False, hitboxes, "Medico: avanti")
        disegna_slot(3, "walk_cycle",   140, (750, 220), (60, 80), False, hitboxes, "Medico: laterale")
        disegna_slot(3, "walk_cycle",   140, (850, 220), (60, 80), True,  hitboxes, "Medico: laterale (flip)")
        disegna_slot(3, "idle",         135, (945, 217), (66, 76), False, hitboxes, "Medico: fermo")
        disegna_slot(3, "walk_cycle_sick", 140, (1040, 220), (60, 80), False, hitboxes, "Medico: malato")
        disegna_slot(3, "walk_cycle_sick", 140, (1140, 220), (60, 80), True,  hitboxes, "Medico: malato (flip)")

        # MOZZO
        disegna_slot(4, "walk_forward", 150, (50, 380), (58, 63), False, hitboxes, "Mozzo: avanti")
        disegna_slot(4, "walk_cycle",   150, (150, 380), (62, 68), True,  hitboxes, "Mozzo: laterale (flip)")
        disegna_slot(4, "walk_cycle",   150, (250, 380), (62, 68), False, hitboxes, "Mozzo: laterale")
        disegna_slot(4, "idle",         150, (350, 380), (58, 68), False, hitboxes, "Mozzo: fermo")
        disegna_slot(4, "walk_cycle_sick", 150, (450, 380), (62, 68), True,  hitboxes, "Mozzo: malato (flip)")
        disegna_slot(4, "walk_cycle_sick", 150, (550, 380), (62, 68), False, hitboxes, "Mozzo: malato")

        # gestione click dopo aver creato hitboxes
        if click_pos is not None:
            for hb in hitboxes:
                if hb["rect"].collidepoint(click_pos):
                    selezionato = hb
                    break

    else:
        # ------------------------ modalità zoom ------------------------
        idx = selezionato["personaggio"]

        zoom = 3.0
        w, h = selezionato["dim"]
        dim_zoom = (int(w * zoom), int(h * zoom))
        pos_zoom = (LARGHEZZA // 2 - dim_zoom[0] // 2, ALTEZZA // 2 - dim_zoom[1] // 2)

        rect_zoom = disegna_animazione(
            schermo,
            personaggi[idx]["sprites"],
            selezionato["anim"],
            selezionato["durata"],
            pos_zoom,
            dimensione=dim_zoom,
            flip=selezionato["flip"],
        )

        # Quando ingrandisci: anche la scritta si ingrandisce (font più grande solo nello zoom)
        font_zoom = pygame.font.SysFont(None, 40)
        disegna_etichetta(rect_zoom, selezionato["etichetta"], font_zoom)

        istr = font_istruzioni.render("Premi 'S' per tornare alla schermata normale", True, BIANCO)
        schermo.blit(istr, (20, 15))

    pygame.display.update()
    clock.tick(60)

pygame.quit()