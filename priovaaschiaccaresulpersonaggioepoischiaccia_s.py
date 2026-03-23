import pygame

pygame.init()

LARGHEZZA = 1200
ALTEZZA = 800
ROSSO = (255, 0, 0)

sfondo = pygame.image.load("generale/sfondo_pirati.jpg")
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Schermo ROSSO")
clock = pygame.time.Clock()

personaggi = [
    # --------------------------------------------------------------------------------------------capitano---------------------------------------------------------------------------------
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
            "walk_cycle_sick": [pygame.image.load(f"allframe/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png").convert_alpha() for i in range(1, 6)]
        },
        "info": {
            "name":        "Capitano",
            "descrizione": "",
            "abilita":     ""
        }
    },
    # -------------------------------------------------------------------------------------cuoco--------------------------------------------------------------------------------------------
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
            "walk_cycle_sick": [pygame.image.load(f"allframe/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)]
        },
        "info": {
            "name":        "Cuoco",
            "descrizione": "",
            "abilita":     ""
        }
    },
    # --------------------------------------------------------------------------------------------guardone--------------------------------------------------------------------------------------
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
            "walk_cycle_sick": [pygame.image.load(f"allframe/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png").convert_alpha() for i in range(1, 8)]
        },
        "info": {
            "name":        "Guardone",
            "descrizione": "",
            "abilita":     ""
        }
    },
    # --------------------------------------------------------------------------------------------medico---------------------------------------------------------------------------------------------------
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
            "walk_cycle_sick": [pygame.image.load(f"allframe/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png").convert_alpha() for i in range(1, 7)]
        },
        "info": {
            "name":        "Medico",
            "descrizione": "",
            "abilita":     ""
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
    rect = frame_flippato.get_rect(topleft=pos)
    schermo.blit(frame_flippato, rect.topleft)
    return rect  # rettangolo cliccabile

def disegna_slot(idx_personaggio, slot_name, anim, durata, pos, dim, flip, hitboxes):
    rect = disegna_animazione(
        schermo,
        personaggi[idx_personaggio]["sprites"],
        anim,
        durata,
        pos,
        dimensione=dim,
        flip=flip
    )
    hitboxes.append({
        "personaggio": idx_personaggio,
        "slot": slot_name,
        "anim": anim,
        "durata": durata,
        "pos": pos,
        "dim": dim,
        "flip": flip,
        "rect": rect
    })

selezionato = None  # dict hitbox oppure None
gameOver = False

while not gameOver:
    hitboxes = []

    # Leggi eventi (salviamo solo click_pos; la selezione si fa dopo che hitboxes è pronta)
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
        # ------------------------ DISEGNA TUTTO (e registra hitbox) ------------------------

        # Capitano
        disegna_slot(0, "cap_walk_forward", "walk_forward", 150, (50, 50),  (64, 78), False, hitboxes)
        disegna_slot(0, "cap_walk_cycle",   "walk_cycle",   150, (150, 50), (64, 78), False, hitboxes)
        disegna_slot(0, "cap_walk_cycle_f", "walk_cycle",   150, (250, 50), (64, 78), True,  hitboxes)
        disegna_slot(0, "cap_idle",         "idle",         200, (350, 50), (64, 78), False, hitboxes)
        disegna_slot(0, "cap_sick",         "walk_cycle_sick", 150, (450, 50), (64, 78), False, hitboxes)
        disegna_slot(0, "cap_sick_f",       "walk_cycle_sick", 150, (550, 50), (64, 78), True,  hitboxes)

        # Cuoco
        disegna_slot(1, "cuo_walk_forward", "walk_forward", 200, (650, 50),  (54, 74), False, hitboxes)
        disegna_slot(1, "cuo_walk_cycle",   "walk_cycle",   170, (750, 50),  (54, 74), False, hitboxes)
        disegna_slot(1, "cuo_walk_cycle_f", "walk_cycle",   170, (850, 50),  (54, 74), True,  hitboxes)
        disegna_slot(1, "cuo_idle",         "idle",         150, (945, 50),  (54, 74), False, hitboxes)
        disegna_slot(1, "cuo_sick",         "walk_cycle_sick", 170, (1040, 50), (54, 74), False, hitboxes)
        disegna_slot(1, "cuo_sick_f",       "walk_cycle_sick", 170, (1140, 50), (54, 74), True,  hitboxes)

        # Guardone
        disegna_slot(2, "gua_walk_forward", "walk_forward", 150, (50, 150), (64, 78), False, hitboxes)
        disegna_slot(2, "gua_walk_cycle_f", "walk_cycle",   110, (150, 150), (64, 78), True,  hitboxes)
        disegna_slot(2, "gua_walk_cycle",   "walk_cycle",   110, (250, 150), (64, 78), False, hitboxes)
        disegna_slot(2, "gua_idle",         "idle",         150, (350, 150), (64, 78), False, hitboxes)
        disegna_slot(2, "gua_sick",         "walk_cycle_sick", 110, (550, 150), (64, 78), False, hitboxes)
        disegna_slot(2, "gua_sick_f",       "walk_cycle_sick", 110, (450, 150), (64, 78), True,  hitboxes)

        # Medico
        disegna_slot(3, "med_walk_forward", "walk_forward", 120, (650, 150), (60, 74), False, hitboxes)
        disegna_slot(3, "med_walk_cycle",   "walk_cycle",   140, (750, 150), (60, 80), False, hitboxes)
        disegna_slot(3, "med_walk_cycle_f", "walk_cycle",   140, (850, 150), (60, 80), True,  hitboxes)
        disegna_slot(3, "med_idle",         "idle",         135, (945, 147), (66, 76), False, hitboxes)
        disegna_slot(3, "med_sick",         "walk_cycle_sick", 140, (1040, 150), (60, 80), False, hitboxes)
        disegna_slot(3, "med_sick_f",       "walk_cycle_sick", 140, (1140, 150), (60, 80), True,  hitboxes)

        # Ora che hitboxes è pronta, possiamo vedere se il click ha colpito qualcosa
        if click_pos is not None:
            selezionato = None
            for hb in hitboxes:
                if hb["rect"].collidepoint(click_pos):
                    selezionato = hb
                    break

    else:
        # ------------------------ MODALITÀ ZOOM: disegna solo il selezionato ------------------------
        idx = selezionato["personaggio"]

        zoom = 3.0  # cambia quanto vuoi (es. 2.0, 4.0)
        w, h = selezionato["dim"]
        dim_zoom = (int(w * zoom), int(h * zoom))
        pos_zoom = (LARGHEZZA // 2 - dim_zoom[0] // 2, ALTEZZA // 2 - dim_zoom[1] // 2)

        disegna_animazione(
            schermo,
            personaggi[idx]["sprites"],
            selezionato["anim"],
            selezionato["durata"],
            pos_zoom,
            dimensione=dim_zoom,
            flip=selezionato["flip"]
        )

    pygame.display.update()
    clock.tick(60)

pygame.quit()