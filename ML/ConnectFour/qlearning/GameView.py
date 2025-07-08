import pygame
import random
import argparse


# define some global variables
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BOARD_SIZE = (7,6)

class ColumnFullException(Exception):
    """An exception that will be thrown if a column of the board is full"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GameView(object):
    """A class that represents the displays in the game"""

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 20, bold=True)
        self.trainedComputer = None
        self.win_list = [0,0]

    def initialize_game_variables(self, game_mode):
        """
        Initialize the game board and the GameLogic object
        """
        self.game_board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
        (self.board_rows, self.board_cols) = self.game_board.get_dimensions()
        self.game_logic = GameLogic(self.game_board)
        first_coin_type = random.randint(1,2)
        second_coin_type = 2 if first_coin_type == 1 else 1

        if game_mode == "single":
            self.p1 = HumanPlayer(first_coin_type)
            if (self.trainedComputer == None):
                self.p2 = ComputerPlayer(second_coin_type, "qlearner")
                self.trainedComputer = self.p2
            else:
                self.trainedComputer.set_coin_type(second_coin_type)
                self.p2 = self.trainedComputer
        elif game_mode == "two_player":
            self.p1 = HumanPlayer(first_coin_type)
            self.p2 = HumanPlayer(second_coin_type)
        else:
            self.trainedComputer = None
            self.win_list = [0,0]
            self.p1 = ComputerPlayer(first_coin_type, "qlearner")
            self.p2 = ComputerPlayer(second_coin_type, "qlearner")


    def main_menu(self, iterations=20):
        """
        Display the main menu screen
        """
        main_menu = True
        play_game = False
        self.background.fill(WHITE)
        self.draw_menu()

        while main_menu:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.rect1.collidepoint(pos):
                        play_game = True
                        main_menu = False
                        game_mode = "two_player"

                    elif self.rect2.collidepoint(pos):
                        play_game = True
                        main_menu = False
                        game_mode = "single"

                    elif self.rect3.collidepoint(pos):
                        play_game = True
                        main_menu = False
                        game_mode = "train"

                    elif self.rect4.collidepoint(pos):
                        main_menu = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu = False


            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        if not play_game:
            pygame.quit()

        elif game_mode == "train":
            self.run(game_mode, iterations)

        else:
            self.run(game_mode)


    def run(self, game_mode, iterations=1):
        """
        Main loop in the game
        """
        while (iterations > 0):
            self.initialize_game_variables(game_mode)
            self.background.fill(BLACK)
            self.game_board.draw(self.background)
            game_over = False
            turn_ended = False
            uninitialized = True
            current_type = random.randint(1,2)
            if game_mode == "single":
                human_turn = (self.p1.get_coin_type() == current_type)

            elif game_mode == "two_player":
                human_turn = True

            else:
                human_turn = False

            p1_turn = (self.p1.get_coin_type() == current_type)

            (first_slot_X, first_slot_Y) = self.game_board.get_slot(0,0).get_position()
            coin = Coin(current_type)
            game_over_screen = False
            while not game_over:

                if uninitialized:
                    coin = Coin(current_type)
                    coin.set_position(first_slot_X, first_slot_Y - Slot.SIZE)
                    coin.set_column(0)
                    uninitialized = False
                    coin_inserted = False

                coin.draw(self.background)

                current_player = self.p1 if p1_turn else self.p2

                if not human_turn:
                    game_over = current_player.complete_move(coin, self.game_board, self.game_logic, self.background)
                    coin_inserted = True
                    uninitialized = True

                # handle the keyboard events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_over = True
                        if event.key == pygame.K_RIGHT and human_turn:
                            if (coin.get_column() + 1 < self.board_cols):
                                coin.move_right(self.background)

                        elif event.key == pygame.K_LEFT and human_turn:
                            if (coin.get_column() - 1 >= 0):
                                coin.move_left(self.background)

                        elif event.key == pygame.K_RETURN and human_turn and not coin_inserted:
                            try:
                                game_over = self.game_board.insert_coin(coin, self.background, self.game_logic)
                                current_player.complete_move()
                                uninitialized = True
                                coin_inserted = True

                            except ColumnFullException as e:
                                pass

                if game_over:
                    winner = self.game_logic.determine_winner_name()
                    winner_value = self.game_logic.get_winner()
                    if (winner_value > 0 and game_mode == "train"):
                        self.win_list[winner_value - 1] += 1
                    game_over_screen = True

                if coin_inserted:
                    if game_mode == "single":
                        human_turn = not human_turn
                    current_type = 1 if current_type == 2 else 2
                    p1_turn = not p1_turn


                milliseconds = self.clock.tick(self.fps)
                self.playtime += milliseconds / 1000.0
                pygame.display.flip()
                self.screen.blit(self.background, (0, 0))

            iterations -= 1

        if game_mode == "train":
            index = self.win_list.index(max(self.win_list))
            self.trainedComputer = self.p1 if index == 0 else self.p2
            self.main_menu()

        else:
            self.game_over_view(winner)

    def draw_menu(self):
        """
        Draw the elements for the main menu screen
        """
        font = pygame.font.SysFont('mono', 60, bold=True)
        self.title_surface = font.render('CONNECT 4', True, BLACK)
        fw, fh = font.size('CONNECT 4')
        self.background.blit(self.title_surface, ((self.width - fw) // 2, 150))
        two_player_text = '2 Player Mode'
        computer_player_text = 'vs Computer'
        train_text = 'Train Computer'
        quit_text = 'QUIT'
        font = pygame.font.SysFont('mono', 40, bold=True)

        self.play_surface = font.render(two_player_text, True, BLACK)
        fw, fh = font.size(two_player_text)
        self.rect1 = self.play_surface.get_rect(topleft=((self.width - fw) // 2, 300))
        self.background.blit(self.play_surface, ((self.width - fw) // 2, 300) )

        computer_play_surface = font.render(computer_player_text, True, BLACK)
        fw, fh = font.size(computer_player_text)
        self.rect2 = computer_play_surface.get_rect(topleft=((self.width - fw) // 2, 350))
        self.background.blit(computer_play_surface, ((self.width - fw) // 2, 350) )

        self.train_surface = font.render(train_text, True, BLACK)
        fw, fh = font.size(train_text)
        self.rect3 = self.train_surface.get_rect(topleft=((self.width - fw) // 2, 400))
        self.background.blit(self.train_surface, ((self.width - fw) // 2, 400) )

        self.quit_surface = font.render(quit_text, True, BLACK)
        fw, fh = font.size(quit_text)
        self.rect4 = self.quit_surface.get_rect(topleft=((self.width - fw) // 2, 450))
        self.background.blit(self.quit_surface, ((self.width - fw) // 2, 450) )

    def game_over_view(self, winner):
        """
        Display the game over screen
        """
        game_over_screen = True
        main_menu = False
        self.background.fill(WHITE)
        self.draw_game_over(winner)

        while game_over_screen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect1.collidepoint(pygame.mouse.get_pos()):
                        main_menu = True
                        game_over_screen = False

                    elif self.rect2.collidepoint(pygame.mouse.get_pos()):
                        game_over_screen = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over_screen = False


            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        if not main_menu:
            pygame.quit()

        else:
            self.main_menu()


    def draw_game_over(self, winner):
        """
        Draw the elements for the game over screen
        """
        font = pygame.font.SysFont('mono', 60, bold=True)
        game_over_text = 'GAME OVER'
        self.title_surface = font.render(game_over_text, True, GREEN)
        fw, fh = font.size(game_over_text)
        self.background.blit(self.title_surface, ((self.width - fw) // 2, 150))
        play_again_text = 'Return to Main Menu'
        quit_text = 'Quit'
        if winner != 'TIE':
            winner_text = winner + " wins!"
        else:
            winner_text = "It was a " + winner + "!"
        font = pygame.font.SysFont('mono', 40, bold=True)
        winner_surface = font.render(winner_text, True, BLACK)
        fw, fh = font.size(winner_text)
        self.background.blit(winner_surface, ((self.width - fw) // 2, 300) )

        font = pygame.font.SysFont('mono', 40, bold=False)
        self.play_surface = font.render(play_again_text, True, (0,  0, 0))
        fw, fh = font.size(play_again_text)
        self.rect1 = self.play_surface.get_rect(topleft=((self.width - fw) // 2, 360))
        self.background.blit(self.play_surface, ((self.width - fw) // 2, 360) )

        self.quit_surface = font.render(quit_text, True, (0,  0, 0))
        fw, fh = font.size(quit_text)
        self.rect2 = self.quit_surface.get_rect(topleft=((self.width - fw) // 2, 410))
        self.background.blit(self.quit_surface, ((self.width - fw) // 2, 410) )
