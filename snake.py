import pygame
import random
import sys

# ── Inicialización ──────────────────────────────────────────────────────────
pygame.init()

# ── Constantes ──────────────────────────────────────────────────────────────
ANCHO, ALTO = 600, 600
CELDA       = 20
COLUMNAS    = ANCHO // CELDA
FILAS       = ALTO  // CELDA
FPS         = 12

# Paleta de colores (estética retro-oscura)
COLOR_FONDO      = (10,  10,  18)
COLOR_GRID       = (20,  20,  35)
COLOR_SERPIENTE  = (50,  220, 120)
COLOR_CABEZA     = (80,  255, 160)
COLOR_COMIDA     = (255, 60,  100)
COLOR_COMIDA2    = (255, 180,  50)   # brillo interior
COLOR_TEXTO      = (200, 200, 220)
COLOR_TITULO     = (80,  255, 160)
COLOR_GAME_OVER  = (255, 60,  100)
COLOR_PUNTOS     = (255, 210,  80)

# ── Pantalla ─────────────────────────────────────────────────────────────────
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🐍  Snake  —  Python + Pygame")
reloj = pygame.time.Clock()

# ── Fuentes ──────────────────────────────────────────────────────────────────
fuente_grande  = pygame.font.SysFont("Consolas", 48, bold=True)
fuente_media   = pygame.font.SysFont("Consolas", 28, bold=True)
fuente_pequena = pygame.font.SysFont("Consolas", 18)


# ── Helpers ──────────────────────────────────────────────────────────────────
def celda_a_px(col, fila):
    return col * CELDA, fila * CELDA


def dibujar_grid():
    for x in range(0, ANCHO, CELDA):
        pygame.draw.line(pantalla, COLOR_GRID, (x, 0), (x, ALTO))
    for y in range(0, ALTO, CELDA):
        pygame.draw.line(pantalla, COLOR_GRID, (0, y), (ANCHO, y))


def dibujar_serpiente(cuerpo):
    for i, (col, fila) in enumerate(cuerpo):
        x, y = celda_a_px(col, fila)
        color = COLOR_CABEZA if i == 0 else COLOR_SERPIENTE
        rect  = pygame.Rect(x + 1, y + 1, CELDA - 2, CELDA - 2)
        pygame.draw.rect(pantalla, color, rect, border_radius=4)
        # brillo en la cabeza
        if i == 0:
            brillo = pygame.Rect(x + 3, y + 3, CELDA // 3, CELDA // 3)
            pygame.draw.rect(pantalla, (180, 255, 210), brillo, border_radius=2)


def dibujar_comida(pos):
    col, fila = pos
    x, y = celda_a_px(col, fila)
    cx, cy = x + CELDA // 2, y + CELDA // 2
    radio  = CELDA // 2 - 2
    pygame.draw.circle(pantalla, COLOR_COMIDA,  (cx, cy), radio)
    pygame.draw.circle(pantalla, COLOR_COMIDA2, (cx - 2, cy - 2), radio // 3)


def texto_centrado(superficie, texto, fuente, color, cy):
    render = fuente.render(texto, True, color)
    rect   = render.get_rect(center=(ANCHO // 2, cy))
    superficie.blit(render, rect)


def pantalla_inicio():
    esperando = True
    while esperando:
        pantalla.fill(COLOR_FONDO)
        dibujar_grid()
        texto_centrado(pantalla, "S N A K E",    fuente_grande,  COLOR_TITULO,   180)
        texto_centrado(pantalla, "Presiona ENTER para jugar", fuente_pequena, COLOR_TEXTO, 270)
        texto_centrado(pantalla, "Usa las flechas del teclado",fuente_pequena, COLOR_TEXTO, 300)
        texto_centrado(pantalla, "ESC para salir",            fuente_pequena, COLOR_TEXTO, 330)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()


def pantalla_game_over(puntos):
    esperando = True
    while esperando:
        pantalla.fill(COLOR_FONDO)
        dibujar_grid()
        texto_centrado(pantalla, "GAME  OVER",             fuente_grande,  COLOR_GAME_OVER, 200)
        texto_centrado(pantalla, f"Puntuación: {puntos}",  fuente_media,   COLOR_PUNTOS,    280)
        texto_centrado(pantalla, "ENTER — jugar de nuevo", fuente_pequena, COLOR_TEXTO,     340)
        texto_centrado(pantalla, "ESC   — salir",          fuente_pequena, COLOR_TEXTO,     370)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()


def nueva_comida(cuerpo):
    while True:
        pos = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1))
        if pos not in cuerpo:
            return pos


# ── Bucle principal del juego ────────────────────────────────────────────────
def jugar():
    # Estado inicial
    cabeza    = (COLUMNAS // 2, FILAS // 2)
    cuerpo    = [cabeza,
                 (cabeza[0] - 1, cabeza[1]),
                 (cabeza[0] - 2, cabeza[1])]
    direccion = (1, 0)   # moviéndose a la derecha
    siguiente = direccion
    comida    = nueva_comida(cuerpo)
    puntos    = 0
    jugando   = True

    while jugando:
        # ── Eventos ──
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP    and direccion != (0,  1): siguiente = (0, -1)
                if evento.key == pygame.K_DOWN  and direccion != (0, -1): siguiente = (0,  1)
                if evento.key == pygame.K_LEFT  and direccion != (1,  0): siguiente = (-1, 0)
                if evento.key == pygame.K_RIGHT and direccion != (-1, 0): siguiente = (1,  0)
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        # ── Actualizar dirección ──
        direccion = siguiente

        # ── Mover serpiente ──
        nueva_cabeza = (
            (cuerpo[0][0] + direccion[0]) % COLUMNAS,
            (cuerpo[0][1] + direccion[1]) % FILAS,
        )

        # Colisión con sí misma
        if nueva_cabeza in cuerpo:
            jugando = False
            break

        cuerpo.insert(0, nueva_cabeza)

        # ¿Comió?
        if nueva_cabeza == comida:
            puntos += 10
            comida  = nueva_comida(cuerpo)
        else:
            cuerpo.pop()

        # ── Dibujar ──
        pantalla.fill(COLOR_FONDO)
        dibujar_grid()
        dibujar_comida(comida)
        dibujar_serpiente(cuerpo)

        # HUD — puntuación
        hud = fuente_pequena.render(f"Puntos: {puntos}   Largo: {len(cuerpo)}", True, COLOR_TEXTO)
        pantalla.blit(hud, (8, 6))

        pygame.display.flip()
        reloj.tick(FPS)

    return puntos


# ── Entrada al programa ──────────────────────────────────────────────────────
def main():
    pantalla_inicio()
    while True:
        puntos = jugar()
        pantalla_game_over(puntos)


if __name__ == "__main__":
    main()