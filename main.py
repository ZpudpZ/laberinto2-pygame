import pygame
from algoritmos import dfs, bfs, greedy, a_star

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
TRANSPARENTE = (255, 255, 0, 100)  # Amarillo con 100 de alfa (transparente)

# Tamaño de la pantalla
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Títulos y reloj
pygame.display.set_caption("Juego de Laberinto - Punto A al Punto B")
reloj = pygame.time.Clock()

# Función para cargar laberinto desde un archivo
def cargar_laberinto(nivel):
    laberinto = []
    posicion_inicio = None
    archivo_nivel = f"laberintos/laberinto{nivel}.txt"
    with open(archivo_nivel, 'r') as archivo:
        for fila, linea in enumerate(archivo):
            laberinto.append(list(linea.strip()))
            if 'A' in linea:
                columna_inicio = linea.index('A')
                posicion_inicio = (columna_inicio, fila)
    return laberinto, posicion_inicio

# Función para dibujar el laberinto
def dibujar_laberinto(pantalla, laberinto, tam_celda, imagen_inicio, imagen_meta):
    ancho_laberinto = len(laberinto[0]) * tam_celda
    alto_laberinto = len(laberinto) * tam_celda
    offset_x = (ANCHO_VENTANA - ancho_laberinto) // 2
    offset_y = (ALTO_VENTANA - alto_laberinto) // 2

    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            celda = laberinto[fila][columna]
            x = columna * tam_celda + offset_x
            y = fila * tam_celda + offset_y

            if celda == '1':
                pygame.draw.rect(pantalla, NEGRO, pygame.Rect(x, y, tam_celda, tam_celda))
            elif celda == '0':
                pygame.draw.rect(pantalla, BLANCO, pygame.Rect(x, y, tam_celda, tam_celda))
            elif celda == 'A':
                pygame.draw.rect(pantalla, BLANCO, pygame.Rect(x, y, tam_celda, tam_celda))
                pantalla.blit(imagen_inicio, (x, y))
            elif celda == 'B':
                pygame.draw.rect(pantalla, BLANCO, pygame.Rect(x, y, tam_celda, tam_celda))
                pantalla.blit(imagen_meta, (x, y))

# Clase Jugador
class Jugador:
    def __init__(self, x, y, tam_celda, offset_x, offset_y):
        self.x = x
        self.y = y
        self.tam_celda = tam_celda
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.imagen = pygame.transform.scale(pygame.image.load('recursos/jugador.png'), (tam_celda, tam_celda))

    def mover(self, dx, dy, laberinto):
        nuevo_x = self.x + dx
        nuevo_y = self.y + dy
        if 0 <= nuevo_x < len(laberinto[0]) and 0 <= nuevo_y < len(laberinto):
            if laberinto[nuevo_y][nuevo_x] != '1':  # Verifica que la nueva posición no sea una pared
                self.x = nuevo_x
                self.y = nuevo_y

    def dibujar(self, pantalla, tam_celda, offset_x, offset_y):
        x_pos = self.x * tam_celda + offset_x
        y_pos = self.y * tam_celda + offset_y
        pantalla.blit(self.imagen, (x_pos, y_pos))

# Función para mostrar la victoria
def mostrar_victoria(pantalla):
    fuente = pygame.font.SysFont(None, 60)
    texto = fuente.render("¡Victoria!", True, VERDE)
    pantalla.blit(texto, (ANCHO_VENTANA // 2 - texto.get_width() // 2, ALTO_VENTANA // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Función para dibujar los botones
def dibujar_botones(pantalla):
    fuente = pygame.font.SysFont(None, 40)
    # Botón DFS
    pygame.draw.rect(pantalla, AZUL, (50, ALTO_VENTANA - 80, 150, 60))
    texto_dfs = fuente.render("DFS", True, BLANCO)
    pantalla.blit(texto_dfs, (50 + 75 - texto_dfs.get_width() // 2, ALTO_VENTANA - 80 + 30 - texto_dfs.get_height() // 2))

    # Botón BFS
    pygame.draw.rect(pantalla, AZUL, (220, ALTO_VENTANA - 80, 150, 60))
    texto_bfs = fuente.render("BFS", True, BLANCO)
    pantalla.blit(texto_bfs, (220 + 75 - texto_bfs.get_width() // 2, ALTO_VENTANA - 80 + 30 - texto_bfs.get_height() // 2))

    # Botón Greedy
    pygame.draw.rect(pantalla, NARANJA, (390, ALTO_VENTANA - 80, 150, 60))
    texto_greedy = fuente.render("Greedy", True, BLANCO)
    pantalla.blit(texto_greedy, (390 + 75 - texto_greedy.get_width() // 2, ALTO_VENTANA - 80 + 30 - texto_greedy.get_height() // 2))

    # Botón A*
    pygame.draw.rect(pantalla, AMARILLO, (560, ALTO_VENTANA - 80, 150, 60))
    texto_a_star = fuente.render("A*", True, BLANCO)
    pantalla.blit(texto_a_star, (560 + 75 - texto_a_star.get_width() // 2, ALTO_VENTANA - 80 + 30 - texto_a_star.get_height() // 2))

# Función para obtener la posición del clic del mouse
def obtener_clic():
    for evento in pygame.event.get():
        if evento.type == pygame.MOUSEBUTTONDOWN:
            return pygame.mouse.get_pos()
    return None

# Función para resolver el laberinto usando Greedy
def resolver_laberinto_greedy(laberinto, inicio, meta):
    camino = greedy(laberinto, inicio, meta)
    return camino

# Función para resolver el laberinto usando A*
def resolver_laberinto_a_star(laberinto, inicio, meta):
    camino = a_star(laberinto, inicio, meta)
    return camino

# Función para dibujar el camino autocompletado
def dibujar_camino(pantalla, camino, tam_celda, offset_x, offset_y):
    if camino:
        for paso in camino:
            x, y = paso
            camino_surf = pygame.Surface((tam_celda, tam_celda), pygame.SRCALPHA)
            camino_surf.fill(TRANSPARENTE)  # Usar color con transparencia
            pantalla.blit(camino_surf, (x * tam_celda + offset_x, y * tam_celda + offset_y))

# Función principal del juego
def main():
    nivel_actual = 1
    max_niveles = 5  # Número máximo de niveles
    jugando = True
    tam_celda = 40

    # Cargar primer laberinto
    laberinto, posicion_inicio = cargar_laberinto(nivel_actual)
    imagen_inicio = pygame.transform.scale(pygame.image.load('recursos/inicio.png'), (tam_celda, tam_celda))
    imagen_meta = pygame.transform.scale(pygame.image.load('recursos/meta.png'), (tam_celda, tam_celda))

    # Calcular el tamaño y offsets del laberinto
    ancho_laberinto = len(laberinto[0]) * tam_celda
    alto_laberinto = len(laberinto) * tam_celda
    offset_x = (ANCHO_VENTANA - ancho_laberinto) // 2
    offset_y = (ALTO_VENTANA - alto_laberinto) // 2

    # Crear el jugador, que debe empezar en la posición 'A'
    jugador = Jugador(posicion_inicio[0], posicion_inicio[1], tam_celda, offset_x, offset_y)

    # Encontrar la posición de la meta (B)
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 'B':
                posicion_meta = (columna, fila)

    camino_autocompletado = []  # Aquí almacenamos el camino de solución

    while jugando:
        pantalla.fill(BLANCO)

        # Dibujar el laberinto
        dibujar_laberinto(pantalla, laberinto, tam_celda, imagen_inicio, imagen_meta)

        # Dibujar botones
        dibujar_botones(pantalla)

        # Dibujar el camino autocompletado si existe
        if camino_autocompletado:
            dibujar_camino(pantalla, camino_autocompletado, tam_celda, offset_x, offset_y)

        # Dibujar el jugador después del camino para que se vea claramente
        jugador.dibujar(pantalla, tam_celda, offset_x, offset_y)

        # Manejar los eventos de clic y teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    jugador.mover(0, -1, laberinto)
                elif evento.key == pygame.K_DOWN:
                    jugador.mover(0, 1, laberinto)
                elif evento.key == pygame.K_LEFT:
                    jugador.mover(-1, 0, laberinto)
                elif evento.key == pygame.K_RIGHT:
                    jugador.mover(1, 0, laberinto)

            # Manejo de clics en los botones
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                clic = pygame.mouse.get_pos()
                x_clic, y_clic = clic
                # Verificar si algún botón fue presionado
                if 50 <= x_clic <= 200 and ALTO_VENTANA - 80 <= y_clic <= ALTO_VENTANA - 20:
                    camino_autocompletado = dfs(laberinto, (jugador.x, jugador.y), posicion_meta)
                elif 220 <= x_clic <= 370 and ALTO_VENTANA - 80 <= y_clic <= ALTO_VENTANA - 20:
                    camino_autocompletado = bfs(laberinto, (jugador.x, jugador.y), posicion_meta)
                elif 390 <= x_clic <= 540 and ALTO_VENTANA - 80 <= y_clic <= ALTO_VENTANA - 20:
                    camino_autocompletado = resolver_laberinto_greedy(laberinto, (jugador.x, jugador.y), posicion_meta)
                elif 560 <= x_clic <= 710 and ALTO_VENTANA - 80 <= y_clic <= ALTO_VENTANA - 20:
                    camino_autocompletado = resolver_laberinto_a_star(laberinto, (jugador.x, jugador.y), posicion_meta)

        # Comprobar si el jugador llegó a la meta
        # Comprobar si el jugador llegó a la meta
        if (jugador.x, jugador.y) == posicion_meta:
            mostrar_victoria(pantalla)

            # Incrementar el nivel
            nivel_actual += 1
            if nivel_actual > max_niveles:
                # Si el jugador ha completado todos los niveles
                pantalla.fill(BLANCO)  # Limpiar la pantalla
                fuente = pygame.font.SysFont(None, 60)
                texto_final = fuente.render("¡Juego completado!", True, VERDE)
                pantalla.blit(texto_final, (
                    ANCHO_VENTANA // 2 - texto_final.get_width() // 2, 10))  # Ajustar la posición a la parte superior
                pygame.display.flip()
                pygame.time.wait(3000)  # Espera 3 segundos y luego termina el juego
                jugando = False
            else:
                # Cargar el siguiente nivel
                laberinto, posicion_inicio = cargar_laberinto(nivel_actual)

                # Recalcular el tamaño y los offsets del laberinto
                ancho_laberinto = len(laberinto[0]) * tam_celda
                alto_laberinto = len(laberinto) * tam_celda
                offset_x = (ANCHO_VENTANA - ancho_laberinto) // 2
                offset_y = (ALTO_VENTANA - alto_laberinto) // 2

                # Actualizar la posición del jugador al punto de inicio del nuevo nivel
                jugador.x, jugador.y = posicion_inicio
                jugador.offset_x = offset_x  # Asegurar que el offset del jugador también se actualiza
                jugador.offset_y = offset_y  # Asegurar que el offset del jugador también se actualiza

                # Recalcular las posiciones de la meta
                for fila in range(len(laberinto)):
                    for columna in range(len(laberinto[0])):
                        if laberinto[fila][columna] == 'B':
                            posicion_meta = (columna, fila)

                camino_autocompletado = []  # Limpiar el camino autocompletado para el nuevo nivel

        pygame.display.flip()
        reloj.tick(30)


    pygame.quit()

if __name__ == "__main__":
    main()