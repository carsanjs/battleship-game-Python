import pygame
from board import Board
from ship import Ship
import os
import subprocess
from network import Network
from screens.sizeScreen import screen_menu_size, screen_setting_size


def start_server():
    subprocess.Popen(["python", "server.py"])


os.environ["SDL_VIDEO_CENTERED"] = "1"
start_server()
pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

# Colors
C_BLUE = (162, 213, 252)
C_RED = (198, 8, 23)
C_GREEN = (6, 122, 16)
C_WHITE = (255, 255, 255, 0)
C_BLACK = (0, 0, 0, 255)
C_ORANGE = (255, 122, 16)
COLOR_TRANSPARENTE = (0, 0, 0, 0.1)

# Music / sounds
pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.play(-1)
play_sound = pygame.mixer.Sound("sounds/yessir.wav")
hitted_sound = pygame.mixer.Sound("sounds/canon.wav")
winner_sound = pygame.mixer.Sound("sounds/winner.wav")
lost_sound = pygame.mixer.Sound("sounds/lost.wav")

# General display settings
pygame.display.set_icon(icon)
screen4_3 = pygame.display.set_mode(screen_menu_size)
pygame.display.set_caption("Battleship - online game")


class Button:
    buttons = []
    color_txt = C_WHITE

    def __init__(self, text, x, y, width, height, color_bg):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_bg = color_bg
        Button.buttons.append(self)

    def draw(self, win):
        pygame.draw.rect(win, self.color_bg, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 22, True)
        txt = font.render(self.text, True, self.color_txt)
        win.blit(
            txt,
            (
                round(self.x + self.width / 2 - txt.get_width() / 2),
                round(self.y + self.height / 2 - txt.get_height() / 2),
            ),
        )

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                return True
        return False


def redrawWindowMenu(win, buttons):
    img_path = "./images/battleshipFondo.jpg"
    background_img = pygame.image.load(img_path)
    background_img = pygame.transform.scale(background_img, (win.get_width(), win.get_height()))
    win.blit(background_img, (0, 0))
    font = pygame.font.SysFont("Arial", 70)  # stylos del texto de la pantalla
    txt = font.render("Battleship", True, C_WHITE)
    win.blit(txt, (round(win.get_width() / 2 - txt.get_width() / 2), 100))


    font2 = pygame.font.SysFont("Arial", 30)
    txt2 = font2.render("Seleccione opcion", True, C_WHITE)
    win.blit(txt2, (round(win.get_width() / 2 - txt2.get_width() / 2), 300))

    for button in buttons:
        button.draw(win)

    pygame.display.update()


# Helper drawing functions for each game status
def redrawWindowSetting(win, my_board, ships, buttons, wins, loses):
    win.fill(C_BLUE)
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render("Cómo Jugar?", True, C_BLACK, C_BLUE)
    win.blit(txt, (80, 50))
    font2 = pygame.font.SysFont("Arial", 20)
    txt2 = font2.render("➡️ Para configurar tus barcos, dale click al barco, y arrástralo hasta un lugar correcto.", True, (0, 0, 0))
    txt4 = font2.render("➡️ Para rotar un barco de vertical/horizontal usa la tecla SPACE/ESPACIO", True, (0, 0, 0))
    txt9 = font2.render("➡️ Recuerda: No puedes dos barcos juntos!!!", True, (0, 0, 0))
    txt5 = font2.render("➡️ Después que todo este listo, dale al botón JUGAR", True, (0, 0, 0))
    txt6 = font2.render("➡️ Si posicionaste mal un barco, puedes borrar el tablero pulsando el botón BORRAR. ", True, (0, 0, 0))
    win.blit(txt2, (470, 100))
    win.blit(txt4, (470, 130))
    win.blit(txt9, (470, 165))
    win.blit(txt5, (470, 195))
    win.blit(txt6, (470, 225))
    my_board.draw(win)
    for ship in ships:
        ship.draw(win)
    for button in buttons:
        button.draw(win)
    score = font2.render("W: {} / L: {}".format(wins, loses), True, (0, 0, 0), True)
    win.blit(score, (820, 720))

    # text_input = pygame_textinput.TextInputVisualizer()
    # text_input.update(pygame.event.get())

    # win.blit(text_input.surface, (470, 650))

    pygame.display.update()


def redrawWindowDisconnected(win):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 60)
    txt = font.render("El rival se ha desconectado!!", True, (255, 0, 0), True)
    win.blit(
        txt,
        (
            round(win.get_width() / 2 - txt.get_width() / 2),
            round(win.get_height() / 2 - txt.get_height() / 2),
        ),
    )
    pygame.display.update()


def redrawWindowWinner(win, game, playerID):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 60)
    if game.winner == playerID:
        txt = font.render("GANADOR :)!", True, (255, 0, 0), True)
        win.blit(
            txt,
            (
                round(win.get_width() / 2 - txt.get_width() / 2),
                round(win.get_height() / 2 - txt.get_height() / 2),
            ),
        )
    else:
        txt = font.render("PERDEDOR :`V", True, (0, 0, 0), True)
        win.blit(
            txt,
            (
                round(win.get_width() / 2 - txt.get_width() / 2),
                round(win.get_height() / 2 - txt.get_height() / 2),
            ),
        )
    pygame.display.update()


def redrawWindowWaiting(win, my_board, ships, wins, loses):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 60)
    txt = font.render("Esperando", True, C_BLACK, C_BLUE)
    txt2 = font.render("Oponente", True, C_BLACK, C_BLUE)
    font2 = pygame.font.SysFont("Arial", 30)
    win.blit(txt, (540, 200))
    win.blit(txt2, (520, 300))
    my_board.draw(win)
    for ship in ships:
        ship.draw(win)
    score = font2.render("W: {} / L: {}".format(wins, loses), True, C_BLACK, C_BLUE)
    win.blit(score, (820, 720))
    pygame.display.update()


def redrawWindowPlaying(
    win, my_board, enemy_board, ships, playerID, game, ships_count, wins, loses
):
    win.fill((162, 213, 252))
    enemy_board.draw(win)
    my_board.draw(win)
    font = pygame.font.SysFont("Arial", 30)
    if playerID == game.turn:
        txt = font.render("Es tu turno", True, C_BLACK, C_BLUE)
        win.blit(txt, (670, 50))
    else:
        txt = font.render("Es turno de tu oponente", True, C_BLACK, C_BLUE)
        win.blit(txt, (140, 50))
    for ship in ships:
        ship.draw(win)
    score = font.render("W: {} / L: {}".format(wins, loses), True, C_BLACK, C_BLUE)
    ships_counter = font.render(
        "Ships: {} / 20".format(ships_count), True, C_BLACK, C_BLUE
    )
    win.blit(score, (820, 720))
    win.blit(ships_counter, (820, 660))
    pygame.display.update()


def controlMusic(state):
    if state:
        pygame.mixer_music.stop()
        return False
    else:
        pygame.mixer_music.play(-1)
        return True


def reDrawShips():
    return [Ship(6, 50, 530, 'images/battleship.png'), Ship(4, 280, 530, 'images/cruiser.png'), Ship(3, 50, 590, 'images/destroyer.png'), Ship(2, 180, 590, 'images/patrol boat.png'), Ship(3, 260, 590, 'images/rescue ship.png'), Ship(4, 50, 630, 'images/submarine.png')]


# Main game loop
def main():
    music_running = True
    run = True
    b = Board()
    ships = reDrawShips()  # Dibujar los barcos

    multiplayer_btn = Button("MULTIPLAYER", 150, 400, 200, 80, C_GREEN)
    quit_btn = Button("QUIT", 400, 400, 200, 80, C_RED)

    reset_btn = Button("BORRAR",590, 280, 100, 40, C_RED)
    play_btn = Button("JUGAR", 470, 280, 100, 40, C_GREEN)

    music_btn = Button("MUSICA", 950, 640, 100, 40, C_ORANGE)

    ships_count = 0
    wins = 0
    loses = 0
    status_game = "menu"
    n = None  # Para manejar la red en modo multijugador

    while run:
        if status_game == "menu":
            redrawWindowMenu(screen4_3, [multiplayer_btn, quit_btn])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if multiplayer_btn.click():
                        screenSetting = pygame.display.set_mode(screen_setting_size)
                        status_game = "setting up"
                    if quit_btn.click():
                        run = False
                        pygame.quit()
        elif status_game == "setting up":
            redrawWindowSetting(
                screenSetting, b, ships, [reset_btn, play_btn, music_btn], wins, loses
            )  # Pantalla de configuración
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    # Botón para reiniciar los barcos
                    if reset_btn.click():
                        del ships
                        ships = reDrawShips()
                        b.reset_board(ships)

                    # Botón para jugar cuando esté listo
                    if play_btn.click() and b.is_ready():
                        # print(" has presionado para jugar")
                        status_game = "connecting"
                        play_sound.play()
                        pygame.time.delay(100)

                    # Botón para controlar la música
                    if music_btn.click():
                        music_running = controlMusic(music_running)

                # Manejo de arrastrar y rotar barcos
                for ship in ships:
                    if (
                        event.type == pygame.MOUSEBUTTONUP
                        and ship.click()
                        and not ship.placed
                    ):
                        if ship.draging:
                            ship.drop(b)
                        ship.draging = not ship.draging
                    if (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE
                        and ship.draging is True
                    ):
                        ship.rotate()
                    elif event.type == pygame.MOUSEMOTION and ship.draging is True:
                        ship.drag()

        # Conexión con el servidor df
        elif status_game == "connecting":
            n = Network()
            status_game = "waiting"

        # Esperando a otro jugador
        elif status_game == "waiting":
            # print("esperano al otro jugador")
            game = n.send(b)  # Enviar tablero y recibir el estado del juego
            redrawWindowWaiting(screen4_3, b, ships, wins, loses)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            if game.both_connected:  # Si ambos jugadores están conectados
                status_game = "playing"

        # Jugando
        elif status_game == "playing":
            if not game.both_connected:
                status_game = "player disconnected"
                b.reset_board(ships)
                continue

            game = n.send("get game")  # Obtener el estado del juego actualizado
            if n.id == "0":
                b, b2 = game.boards[0], game.boards[1]
            else:
                b, b2 = game.boards[1], game.boards[0]

            b.x, b.y = 50, 100  # Tablero propio
            b2.x, b2.y = 550, 100  # Tablero enemigo

            if game.is_winner():  # Condición de victoria
                status_game = "winner"

            redrawWindowPlaying(
                screen4_3, b, b2, ships, n.id, game, ships_count, wins, loses
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP and game.turn == n.id:
                    for row in b2.fields:
                        for field in row:
                            if field.click():
                                if field.ship:
                                    b2.looking_ship(field.row, field.col)
                                    n.send(("hitted", b2))
                                    hitted_sound.play()
                                    ships_count += 1
                                    if ships_count > 19:
                                        ships_count = 0
                                else:
                                    n.send(("missed", b2))

        # Condición de victoria
        elif status_game == "winner":
            del ships
            ships = reDrawShips()
            redrawWindowWinner(screen4_3, game, n.id)

            if n.id == game.winner:
                wins += 1
                winner_sound.play()
            else:
                loses += 1
                lost_sound.play()

            pygame.time.delay(2000)
            status_game = "setting up"
            b.reset_board(ships)
            n.close()

        # Desconexión del otro jugador
        elif status_game == "player disconnected":
            del ships
            ships = reDrawShips()
            redrawWindowDisconnected(screen4_3)
            pygame.time.delay(2000)
            n.close()
            status_game = "setting up"


main()
