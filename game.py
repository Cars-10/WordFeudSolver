from dawg import *
from board import ScrabbleBoard, WordFeudBoard, Square
from OcrWordFeudBoard import *
from web_service import *
import pygame
import sys
import random
import pickle

# returns a list of all words played on the board



def draw_board(board):
    for y in range(15):
        for x in range(15):
            if board[x][y].letter:
                if board[x][y].letter == "I":
                    letter_x_offset = 15
                else:
                    letter_x_offset = 7
                pygame.draw.rect(screen, game.TILE_bgcolor, [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])

                letter = tile_font.render(board[x][y].letter, True, game.TILE_fgcolor)
                screen.blit(letter, ((margin + square_width) * x + margin + x_offset + letter_x_offset,
                                     (margin + square_height) * y + margin + y_offset + 7))

                letter_score = modifier_font.render(str(game.point_dict[board[x][y].letter]), True, game.TILE_fgcolor)
                screen.blit(letter_score, ((margin + square_width) * x + margin + x_offset + 31,
                                           (margin + square_height) * y + margin + y_offset + 30))

            elif "3LS" in board[x][y].modifier:
                pygame.draw.rect(screen, game.TLS_bgcolor, [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                text_top = modifier_font.render("TRIPLE", True, game.SQUARE_fgcolor)
                text_mid = modifier_font.render("LETTER", True, game.SQUARE_fgcolor)
                text_bot = modifier_font.render("SCORE", True, game.SQUARE_fgcolor)
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif "2LS" in board[x][y].modifier:
                pygame.draw.rect(screen, game.DLS_bgcolor, [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                text_top = modifier_font.render("DOUBLE", True, game.SQUARE_fgcolor)
                text_mid = modifier_font.render("LETTER", True, game.SQUARE_fgcolor)
                text_bot = modifier_font.render("SCORE", True, game.SQUARE_fgcolor)
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 3,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif "2WS" in board[x][y].modifier:
                pygame.draw.rect(screen, game.DWS_bgcolor, [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])
                text_top = modifier_font.render("DOUBLE", True, game.SQUARE_fgcolor)
                text_mid = modifier_font.render("WORD", True, game.SQUARE_fgcolor)
                text_bot = modifier_font.render("SCORE", True, game.SQUARE_fgcolor)
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 3,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            elif "3WS" in board[x][y].modifier:
                pygame.draw.rect(screen, game.TWS_bgcolor, [(margin + square_width) * x + margin + x_offset,
                                                         (margin + square_height) * y + margin + y_offset,
                                                         square_width, square_height])
                text_top = modifier_font.render("TRIPLE", True, game.fgcolor)
                text_mid = modifier_font.render("WORD", True, game.fgcolor)
                text_bot = modifier_font.render("SCORE", True, game.fgcolor)
                screen.blit(text_top, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 7))
                screen.blit(text_mid, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 17))
                screen.blit(text_bot, ((margin + square_width) * x + margin + x_offset + 5,
                                       (margin + square_height) * y + margin + y_offset + 27))

            else:
                pygame.draw.rect(screen, game.BLANK_bgcolor, [(margin + square_width) * x + margin + x_offset,
                                                           (margin + square_height) * y + margin + y_offset,
                                                           square_width, square_height])



def draw_rack(rack):
    for i, letter in enumerate(rack):
        if letter == "I":
            letter_x_offset = 15
        else:
            letter_x_offset = 7
        pygame.draw.rect(screen, game.TILE_bgcolor, [(margin + square_width) * (i + 4) + margin + x_offset,
                                                 700,
                                                 square_width, square_height])

        if letter == "%":
            tile_letter = tile_font.render(" ", True, game.TILE_fgcolor)
        else:
            tile_letter = tile_font.render(letter, True, game.TILE_fgcolor)
        screen.blit(tile_letter, ((margin + square_width) * (i + 4) + margin + x_offset + letter_x_offset,
                                  700 + 7))

        letter_score = modifier_font.render(str(game.point_dict[letter]), True, game.TILE_fgcolor)
        screen.blit(letter_score, ((margin + square_width) * (i + 4) + margin + x_offset + 31,
                                   700 + 30))

def draw_computer_score(tile_bag):
    x_start = 700
    y_start = 50
    pygame.draw.rect(screen, (45, 45, 45), [x_start, 25, 255, 50])
    score_title = score_font.render("Letters Remaining", True, game.fgcolor)
    screen.blit(score_title, (x_start + 50, 25))
    pygame.draw.rect(screen, (45, 45, 45), [x_start, y_start, 255, 700])

    for letter in tile_bag:
        if len(letter) == 1:
            #print(f"letter = {letter}")
            if y_start * (ord(letter) - ord('A') + 1) > 665:
                x_start += 130
            word = score_font.render(str(letter), True, game.fgcolor)
            screen.blit(word, (x_start + 2, y_start * (ord(letter) - ord('A') + 1)))

if __name__ == "__main__":
    pygame.init()
    # Game-level variables
    screen_width = 1000
    screen_height = 800
    #screen = pygame.display.set_mode((screen_width, screen_height))
    #clock = pygame.time.Clock()
    square_width = 40
    square_height = 40
    margin = 3
    mouse_x = 0
    mouse_y = 0
    x_offset = 20
    y_offset = 20
    modifier_font = pygame.font.Font(None, 12)
    tile_font = pygame.font.Font(None, 45)
    score_font = pygame.font.Font(None, 25)
    tile_bag = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["%"] * 2


    dictionary = "lexicon/scrabble_words_complete.pickle"
    dictionary = "lexicon/twl06 USA.pickle"
    dictionary = "lexicon/twl.pickle"
    to_load = open(dictionary, "rb")
    root = pickle.load(to_load)
    to_load.close()
    image_path = "images/WordFeudScreenshot.png"
    image_path = "images/IMG_6040 3.png"
    image_path = "images/IMG_6039 3.png"
    image_path = "images/IMG_6038 3.png"
    #image_path = "images/IMG_6041 3.png"

    wf = OcrWordfeudBoard(image_path)
    game = WordFeudBoard(root)
    word_rack = wf.get_rack_letters(image_path)
    print(f"word_rack = {word_rack}")
    [tile_bag.remove(letter) for letter in word_rack]
    wf.read_board_letters(image_path)

    # create code to transfer the contents of wf.board to game.board, skip entries that are '  '
    # game.board = wf.board
    for i in range(15):
        for j in range(15):
            if wf.read_square(i,j) != '  ':
                #print(f"game.board[{i}][{j}].letter = {wf.read_square(i,j)}")
                game.board[i][j].letter = wf.read_square(i,j).strip()
    # Check if all words on the board are valid
    game.print_board()

    for word in game.all_board_words(game.board):
        #print(f"Checking {word}")
        if not find_in_dawg(word, root) and word:
            raise Exception(f"Invalid word on board: {word} is not in my dictionary!")

    #pygame.display.set_caption("Word Feud Cheater")
    #screen.fill(game.bgcolor)
    #pygame.display.flip()
    word_rack = game.get_best_move(word_rack)

    #draw_board(game.board)
    #draw_rack(word_rack)
    #draw_computer_score(tile_bag)
    if game.is_transpose:
        game.board = game.transpose_board(game.board)
    game.print_board()
    print(f"Best word = {game.best_word}")

    for word in game.all_board_words(game.board):
        print(f"Checking {word}")
        if not find_in_dawg(word, root) and word:
            raise Exception(f"Invalid word on board: {word} is not in my dictionary!")


    if game.best_word == "":
        # draw new hand if can't find any words
        print("No words found! PASS or SWAP Tiles")
        sys.exit()

    #pygame.time.wait(75)
    # add a pause here to wait for a keypress
    print("Press Enter to continue...")
    #input()  # Program pauses here until Enter is pressed

    #pygame.quit()

# TODO: play second word from previous score, when only one letter is played
# TODO: Check that connected words are valid


