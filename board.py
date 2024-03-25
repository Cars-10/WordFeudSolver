from dawg import *
import regex as re
import random
import copy

class Square:
    def __init__(self, letter=None, modifier="Normal", sentinel=1):
        self.letter = letter
        self.cross_checks_0 = [sentinel] * 26
        self.cross_checks_1 = [sentinel] * 26
        self.cross_checks = self.cross_checks_0
        self.modifier = modifier
        self.visible = True
        if sentinel == 0:
            self.visible = False

    def __str__(self):
        if not self.visible:
            return ""
        if not self.letter:
            return "_"
        else:
            return self.letter

    def check_switch(self, is_transpose):
        """
        Switches the cross_checks attribute based on the value of is_transpose.

        Args:
            is_transpose (bool): A boolean value indicating whether the switch is for transpose or not.

        Returns:
            None
        """
        if is_transpose:
            self.cross_checks = self.cross_checks_1
        else:
            self.cross_checks = self.cross_checks_0

class ScrabbleBoard:
    """
    Represents a Scrabble board.

    Attributes:
        board (list): A list of lists representing the Scrabble board.
        point_dict (dict): A dictionary mapping each letter to its corresponding point value.
        words_on_board (list): A list of words already placed on the board.
        is_transpose (bool): A flag indicating whether the board is transposed.
        dawg_root (Node): The root node of the DAWG (Directed Acyclic Word Graph).
        word_rack (list): A list of letters in the player's rack.
        word_score_dict (dict): A dictionary mapping words to their corresponding scores.
        best_word (str): The highest-scoring word found so far.
        highest_score (int): The score of the highest-scoring word found so far.
        dist_from_anchor (int): The distance of the leftmost placed tile from the anchor.
        letters_from_rack (list): A list of letters used from the player's rack to form the best word.
        best_row (int): The row of the highest-scoring word found so far.
        best_col (int): The column of the highest-scoring word found so far.
        upper_cross_check (list): A list of squares that need updated cross-checks in the upper direction.
        lower_cross_check (list): A list of squares that need updated cross-checks in the lower direction.
    """
    def __init__(self, dawg_root):

        row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8,row_9, row_10, row_11, row_12, \
        row_13, row_14, row_15, row_16 = self._setup_board()

        # variables to describe board state
        self.board = [row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8,
                      row_9, row_10, row_11, row_12, row_13, row_14, row_15, row_16]

        self._setup_colors()

        self.point_dict = {"A": 1, "B": 3, "C": 3, "D": 2,
                           "E": 1, "F": 4, "G": 2, "H": 4,
                           "I": 1, "J": 8, "K": 5, "L": 1,
                           "M": 3, "N": 1, "O": 1, "P": 3,
                           "Q": 10, "R": 1, "S": 1, "T": 1,
                           "U": 1, "V": 4, "W": 4, "X": 8,
                           "Y": 8, "Z": 10, "%": 0}

        self.words_on_board = []

        self.is_transpose = False

        # variables to encode best word on a given turn
        self.dawg_root = dawg_root
        self.word_rack = []
        self.word_score_dict = {}
        self.best_word = ""
        self.highest_score = 0
        self.dist_from_anchor = 0
        self.letters_from_rack = []

        # rows and columns of highest-scoring word found so far.
        # these are the rows and columns of the tile already on the board
        self.best_row = 0
        self.best_col = 0

        # store squares that need updated cross-checks
        self.upper_cross_check = []
        self.lower_cross_check = []

    def _setup_colors(self):
        self.bgcolor = (255, 215, 0)
        self.fgcolor = (0, 0, 0)
        self.TILE_bgcolor = (255, 215, 0)
        self.TILE_fgcolor = (0, 0, 0)
        self.TLS_bgcolor = (0, 100, 200)
        self.TWS_bgcolor =  (237, 28, 36)
        self.DLS_bgcolor = (173, 216, 230)
        self.DWS_bgcolor =  (190, 120, 30)
        self.BLANK_bgcolor =   (210, 180, 140)
        self.SQUARE_fgcolor = (255, 255, 255)

    def _setup_board(self):
        row_1 = \
            [Square(modifier="3WS"), Square(), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="3WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(), Square(modifier="3WS"),
             Square(sentinel=0)]
        row_15 = copy.deepcopy(row_1)

        row_2 = \
            [Square(), Square(modifier="2WS"), Square(), Square(), Square(),
             Square(modifier="3LS"), Square(), Square(), Square(), Square(modifier="3LS"),
             Square(), Square(), Square(), Square(modifier="2WS"), Square(),
             Square(sentinel=0)]
        row_14 = copy.deepcopy(row_2)

        row_3 = \
            [Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(sentinel=0)]
        row_13 = copy.deepcopy(row_3)

        row_4 = \
            [Square(modifier="2LS"), Square(), Square(), Square(modifier="2WS"), Square(),
             Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(), Square(modifier="2WS"), Square(), Square(), Square(modifier="2LS"),
             Square(sentinel=0)]
        row_12 = copy.deepcopy(row_4)

        row_5 = \
            [Square(), Square(), Square(), Square(), Square(modifier="2WS"),
             Square(), Square(), Square(), Square(), Square(),
             Square(modifier="2WS"), Square(), Square(), Square(), Square(),
             Square(sentinel=0)]
        row_11 = copy.deepcopy(row_5)

        row_6 = \
            [Square(), Square(modifier="3LS"), Square(), Square(), Square(),
             Square(modifier="3LS"), Square(), Square(), Square(), Square(modifier="3LS"),
             Square(), Square(), Square(), Square(modifier="3LS"), Square(),
             Square(sentinel=0)]
        row_10 = copy.deepcopy(row_6)

        row_7 = \
            [Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(sentinel=0)]
        row_9 = copy.deepcopy(row_7)

        row_8 = \
            [Square(modifier="3WS"), Square(), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(), Square(modifier="3WS"),
             Square(sentinel=0)]

        row_16 = [Square(sentinel=0) for _ in range(16)]

        return row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8,row_9, row_10, row_11, row_12, \
        row_13, row_14, row_15, row_16


    # transpose method that modifies self.board inplace
    def _transpose(self):
        """
        Transposes the board by swapping rows and columns.

        This method transposes the current board by swapping rows and columns. It uses the `zip` function to transpose the
        list of lists and then updates the `self.board` attribute with the transposed board. It also toggles the
        `self.is_transpose` attribute to indicate that the board has been transposed.

        Returns:
            None
        """
        transposed_tuples = copy.deepcopy(list(zip(*self.board)))
        self.board = [list(sublist) for sublist in transposed_tuples]
        self.is_transpose = not self.is_transpose

    # TODO: fix scoring errors
    def _score_word(self, word, squares, dist_from_anchor):
        score = 0
        score_multiplier = 1

        if self.is_transpose:
            cross_sum_ind = "-"
        else:
            cross_sum_ind = "+"

        # word that will be inserted onto board shouldn't have wildcard indicator
        board_word = word.replace("%", "")

        # don't add words that are already on the board
        #print(f"board_word: {board_word}  words_on_board: {self.words_on_board}")
        if board_word in self.words_on_board:
            return board_word, 0

        # remove letters before wildcard indicators
        word = re.sub("[A-Z]%", "%", word)

        # maintain list of which tiles were pulled from word rack
        rack_tiles = []
        for letter, square in zip(word, squares):
            # add cross-sum by adding first and second letter scores from orthogonal two-letter word
            if cross_sum_ind in square.modifier:
                score += int(square.modifier[-1])
            if square.modifier:
                rack_tiles.append(letter)
            if "2LS" in square.modifier:
                score += (self.point_dict[letter] * 2)
            elif "3LS" in square.modifier:
                score += (self.point_dict[letter] * 3)
            elif "2WS" in square.modifier:
                score_multiplier *= 2
                score += self.point_dict[letter]
            elif "3WS" in square.modifier:
                score_multiplier *= 3
                score += self.point_dict[letter]
            else:
                score += self.point_dict[letter]

        score *= score_multiplier

        # check for bingo
        if len(rack_tiles) == 7:
            # TODO This should be 2WS Bonus
            score += 50

        if score > self.highest_score:
            self.best_word = board_word
            self.highest_score = score
            #print(f"best_word: {self.best_word}  highest_score: {self.highest_score}")
            # distance of leftmost placed tile from anchor. if anchor is leftmost tile distance will be 0.
            self.dist_from_anchor = dist_from_anchor
            self.letters_from_rack = rack_tiles

    def _extend_right(self, start_node, square_row, square_col, rack, word, squares, dist_from_anchor):
        """
        Extends the current word to the right by recursively exploring the possible letter combinations.

        Args:
            start_node (Node): The starting node of the word in the trie.
            square_row (int): The row index of the current square on the board.
            square_col (int): The column index of the current square on the board.
            rack (list): The available letters in the player's rack.
            word (str): The current word being formed.
            squares (list): The list of squares occupied by the current word.
            dist_from_anchor (int): The distance of the current square from the anchor square.

        Returns:
            None
        """
        square = self.board[square_row][square_col]
        square.check_switch(self.is_transpose)

        # execute if square is empty
        if not square.letter:
            if start_node.is_terminal:
                self._score_word(word, squares, dist_from_anchor)
            for letter in start_node.children:
                # if square already has letters above and below it, don't try to extend
                if self.board[square_row + 1][square_col].letter and self.board[square_row - 1][square_col].letter:
                    continue

                # conditional for blank squares
                if letter in rack:
                    wildcard = False
                elif "%" in rack:
                    wildcard = True
                else:
                    continue
                if letter in rack and self._cross_check(letter, square):
                    new_node = start_node.children[letter]
                    new_rack = rack.copy()
                    if wildcard:
                        new_word = word + letter + "%"
                        new_rack.remove("%")
                    else:
                        new_word = word + letter
                        new_rack.remove(letter)
                    new_squares = squares + [square]
                    self._extend_right(new_node, square_row, square_col + 1, new_rack, new_word, new_squares,
                                       dist_from_anchor)
        else:
            if square.letter in start_node.children:
                new_node = start_node.children[square.letter]
                new_word = word + square.letter
                new_squares = squares + [square]
                self._extend_right(new_node, square_row, square_col + 1, rack, new_word, new_squares,
                                   dist_from_anchor)

    def _left_part(self, start_node, anchor_square_row, anchor_square_col, rack, word, squares, limit, dist_from_anchor):
        """
        Recursive helper method for extending the word towards the left of the anchor square.

        Args:
            start_node (Node): The starting node of the trie representing the current prefix of the word.
            anchor_square_row (int): The row index of the anchor square.
            anchor_square_col (int): The column index of the anchor square.
            rack (list): The current rack of letters available for forming the word.
            word (str): The current partial word being formed.
            squares (list): The list of squares visited so far in the word formation.
            limit (int): The maximum number of squares that can be used to extend the word.
            dist_from_anchor (int): The distance from the anchor square to the current square being considered.

        Returns:
            None
        """
        potential_square = self.board[anchor_square_row][anchor_square_col - dist_from_anchor]
        potential_square.check_switch(self.is_transpose)
        if potential_square.letter:
            return
        self._extend_right(start_node, anchor_square_row, anchor_square_col, rack, word, squares, dist_from_anchor)
        if 0 in potential_square.cross_checks:
            return
        if limit > 0:
            for letter in start_node.children:
                # conditional for blank squares
                if letter in rack:
                    wildcard = False
                elif "%" in rack:
                    wildcard = True
                else:
                    continue

                new_node = start_node.children[letter]
                new_rack = rack.copy()
                if wildcard:
                    new_word = word + letter + "%"
                    new_rack.remove("%")
                else:
                    new_word = word + letter
                    new_rack.remove(letter)
                new_squares = squares + [potential_square]
                self._left_part(new_node, anchor_square_row, anchor_square_col, new_rack, new_word, new_squares,
                                limit - 1, dist_from_anchor + 1)

    def _update_cross_checks(self):
        """
        Updates the cross checks for each square on the board.

        This method iterates over the upper and lower cross checks and performs the following steps:
        1. Switches the check mode of the current square based on whether the board is transposed or not.
        2. Adds the point value of the lower or upper letter to the modifier of the current square.
        3. Prevents cross stacking deeper than 2 layers by resetting the cross checks of adjacent squares.
        4. Checks if the current square has a letter. If not, it checks the validity of each cross check using a DAWG data structure.
        5. Updates the cross checks of the current square based on the validity of each cross check.

        Note: The cross checks are represented as a list of integers, where 1 indicates a valid cross check and 0 indicates an invalid cross check.

        """
        while self.upper_cross_check:
            curr_square, lower_letter, lower_row, lower_col = self.upper_cross_check.pop()
            curr_square.check_switch(self.is_transpose)

            # add to modifier for computing cross-sum
            if self.is_transpose:
                curr_square.modifier += f"-{self.point_dict[lower_letter]}"
            else:
                curr_square.modifier += f"+{self.point_dict[lower_letter]}"
            #print(f"curren square: {curr_square.modifier}")
            chr_val = 65
            # prevent cross stacking deeper than 2 layers
            if curr_square.letter:
                if not self.is_transpose:
                    self.board[lower_row - 2][lower_col].cross_checks_0 = [0] * 26
                    self.board[lower_row + 1][lower_col].cross_checks_0 = [0] * 26

                else:
                    self.board[lower_row - 2][lower_col].cross_checks_1 = [0] * 26
                    self.board[lower_row + 1][lower_col].cross_checks_1 = [0] * 26
                continue

            for i, ind in enumerate(curr_square.cross_checks):
                if ind == 1:
                    test_node = self.dawg_root.children[chr(chr_val)]
                    if (lower_letter not in test_node.children) or (not test_node.children[lower_letter].is_terminal):
                        curr_square.cross_checks[i] = 0
                chr_val += 1

        while self.lower_cross_check:
            curr_square, upper_letter, upper_row, upper_col = self.lower_cross_check.pop()
            curr_square.check_switch(self.is_transpose)

            # add to modifier for computing cross-sum
            if self.is_transpose:
                curr_square.modifier += f"-{self.point_dict[upper_letter]}"
            else:
                curr_square.modifier += f"+{self.point_dict[upper_letter]}"
            #print(f"curren square: {curr_square.modifier}")

            chr_val = 65
            # prevent cross stacking deeper than 2 layers
            if curr_square.letter:
                if not self.is_transpose:
                    self.board[upper_row - 1][upper_col].cross_checks_0 = [0] * 26
                    self.board[upper_row + 2][upper_col].cross_checks_0 = [0] * 26
                else:
                    self.board[upper_row - 1][upper_col].cross_checks_1 = [0] * 26
                    self.board[upper_row + 2][upper_col].cross_checks_1 = [0] * 26
                continue

            for i, ind in enumerate(curr_square.cross_checks):
                if ind == 1:
                    test_node = self.dawg_root.children[upper_letter]
                    if (chr(chr_val) not in test_node.children) or (not test_node.children[chr(chr_val)].is_terminal):
                        curr_square.cross_checks[i] = 0
                chr_val += 1

    def _cross_check(self, letter, square):
        #print(f"_cross_check: {letter}, {square}")
        """
        Checks if the given letter is a valid cross-check for the specified square.

        Args:
            letter (str): The letter to check.
            square (Square): The square to check against.

        Returns:
            bool: True if the letter is a valid cross-check, False otherwise.
        """
        square.check_switch(self.is_transpose)
        chr_val = 65
        for i, ind in enumerate(square.cross_checks):
            if ind == 1:
                if chr(chr_val) == letter:
                    return True
            chr_val += 1
        return False

    def print_board(self):
            """
            Prints the current state of the board.
            """
            print("    ", end="")
            [print(str(num).zfill(2), end=" ") for num in range(0, 15)]
            print()
            for i, row in enumerate(self.board):
                if i != 15:
                    print(str(i).zfill(2), end="  ")
                [print(square, end="  ") for square in row]
                print()
            print()

    # method to insert words into board by row and column number
    # using 1-based indexing for user input
    def insert_word(self, row, col, word):
        print(f"Inserting word: {word} at column {col}, row {row}\n")
        """
        Inserts a word onto the game board at the specified row and column.

        Args:
            row (int): The row index (0-based) where the word should be inserted.
            col (int): The column index (0-based) where the word should be inserted.
            word (str): The word to be inserted onto the board.

        Returns:
            None

        Raises:
            None

        """
        row -= 1
        col -= 1

        if len(word) + col > 15:
            print(f'Cannot insert word "{word}" at column {col+1}, '
                  f'row {row+1} not enough space')
            return
        curr_col = col
        modifiers = []
        for i, letter in enumerate(word):
            curr_square_letter = self.board[row][curr_col].letter
            modifiers.append(self.board[row][curr_col].modifier)
            if curr_square_letter:
                if curr_square_letter == letter:
                    if row >= 0:
                        self.upper_cross_check.append((self.board[row - 1][curr_col], letter, row, curr_col))
                    if row < 15:
                        self.lower_cross_check.append((self.board[row + 1][curr_col], letter, row, curr_col))
                    curr_col += 1
                else:
                    print(f'Failed to insert letter "{letter}" of "{word}" at column {curr_col+1}, '
                          f'row {row+1}. Square is occupied by letter "{curr_square_letter}"')
                    self.upper_cross_check = []
                    self.lower_cross_check = []
                    for _ in range(i):
                        curr_col -= 1
                        self.board[row][curr_col].letter = None
                        self.board[row][curr_col].modifier = modifiers.pop()
                    return
            else:
                self.board[row][curr_col].letter = letter
                self.board[row][curr_col].modifier = ""

                if row > 0:
                    self.upper_cross_check.append((self.board[row - 1][curr_col], letter, row, curr_col))
                if row < 15:
                    self.lower_cross_check.append((self.board[row + 1][curr_col], letter, row, curr_col))

                curr_col += 1

        if curr_col < 15:
            if self.is_transpose:
                self.board[row][curr_col].cross_checks_0 = [0] * 26
            else:
                self.board[row][curr_col].cross_checks_1 = [0] * 26
        if col >= 0 :
            if self.is_transpose:
                self.board[row][col - 1].cross_checks_0 = [0] * 26
            else:
                self.board[row][col - 1].cross_checks_1 = [0] * 26

        self._update_cross_checks()
        self.words_on_board.append(word)


    # gets all words that can be made using a selected filled square and the current word rack
    def get_all_words(self, square_row, square_col, rack):
        #print(f"get_all_words: {square_row}, {square_col}, {rack}")
        """
        Retrieves all possible words that can be formed on the game board starting from a specific square,
        using the given rack of letters.

        Args:
            square_row (int): The row index of the starting square.
            square_col (int): The column index of the starting square.
            rack (list): The list of letters available in the player's rack.

        Returns:
            None

        Raises:
            None
        """
        # TODO should add check if the final word is the existing word
        square_row -= 1
        square_col -= 1

        # get all words that start with the filled letter
        self._extend_right(self.dawg_root, square_row, square_col, rack, "", [], 0)

        # create anchor square only if the space is empty
        if self.board[square_row][square_col-1].letter:
            return
        # try every letter in rack as possible anchor square
        for i, letter in enumerate(rack):
            #print(f"i: {i}, letter: {letter}")
            # Only allow anchor square with trivial cross-checks
            potential_square = self.board[square_row][square_col - 1]
            potential_square.check_switch(self.is_transpose)
            #print(f"Cross checks: {potential_square.cross_checks}   Letter: {potential_square.letter}")
            if 0 in potential_square.cross_checks or potential_square.letter:
                continue
            temp_rack = rack[:i] + rack[i + 1:]
            self.board[square_row][square_col - 1].letter = letter
            #print(f"Square row,col {square_row}, {square_col} : Anchor square: {letter} temp_rack: {temp_rack}  ")
            self._left_part(self.dawg_root, square_row, square_col - 1, temp_rack, "", [], 6, 1)

        # reset anchor square spot to blank after trying all combinations
        self.board[square_row][square_col - 1].letter = None

    def is_word_playable(self, word):
        playable = True
        self.words_on_board = self.all_board_words(self.board)
        for word in self.words_on_board:
            #print(f"Checking {word}")
            if not find_in_dawg(word, self.dawg_root) and word:
                playable = False
        return playable

    def all_board_words(self, board):
        """
        Retrieves all the words present on the game board.

        Args:
            board (list): A 2D list representing the game board.

        Returns:
            list: A list of words found on the game board.
        """
        board_words = []

        # check regular board
        for row in range(15):
            temp_word = ""
            for col in range(16):
                letter = board[row][col].letter
                if letter:
                    temp_word += letter
                    #print(f"temp_word = {temp_word}")
                else:
                    if len(temp_word) > 1:
                        board_words.append(temp_word)
                        #print(f"Final temp_word = {temp_word}")
                    temp_word = ""

        # check transposed board
        for col in range(16):
            temp_word = ""
            for row in range(16):
                letter = board[row][col].letter
                if letter:
                    # sums up letters till theres a space
                    temp_word += letter
                    #print(f"temp_word = {temp_word}")
                else:
                    if len(temp_word) > 1:
                        #print(f"appending {temp_word}")
                        board_words.append(temp_word)
                        #print(f"Final temp_word = {temp_word}")
                    temp_word = ""
        #print(f"board_words = {board_words}")
        return board_words

    # scan all tiles on board in both transposed and non-transposed state, find best move
    def get_best_move(self, word_rack):
        """
        Finds the best move on the board for the given word rack.

        Args:
            word_rack (list): A list of letters representing the available letters in the word rack.

        Returns:
            list: The updated word rack after making the best move.

        """
        self.word_rack = word_rack

        # clear out cross-check lists before adding new words
        self._update_cross_checks()

        # reset word variables to clear out words from previous turns
        self.best_word = ""
        self.highest_score = 0
        self.best_row = 0
        self.best_col = 0

        transposed = False
        for row in range(15):
            for col in range(15):
                curr_square = self.board[row][col]
                if curr_square.letter and (not self.board[row][col - 1].letter):
                    prev_best_score = self.highest_score
                    self.get_all_words(row + 1, col + 1, word_rack)
                    if self.highest_score > prev_best_score:
                        self.best_row = row
                        self.best_col = col

        self._transpose()
        for row in range(0, 15):
            for col in range(0, 15):
                curr_square = self.board[row][col]
                if curr_square.letter and (not self.board[row][col - 1].letter):
                    prev_best_score = self.highest_score
                    self.get_all_words(row + 1, col + 1, word_rack)
                    if self.highest_score > prev_best_score:
                        transposed = True
                        self.best_row = row
                        self.best_col = col

        # Don't try to insert word if we couldn't find one
        if not self.best_word:
            self._transpose()
            return word_rack

        #print(f"best_word: {self.best_word}  highest_score: {self.highest_score}")
        #print(f"best_row: {self.best_row}  best_col: {self.best_col}")
        if transposed:
            self.insert_word(self.best_row + 1, self.best_col + 1 - self.dist_from_anchor, self.best_word)
            self._transpose()
        else:
            self._transpose()
            self.insert_word(self.best_row + 1, self.best_col + 1 - self.dist_from_anchor, self.best_word)

        self.word_score_dict[self.best_word] = self.highest_score

        for letter in self.letters_from_rack:
            if letter in word_rack:
                word_rack.remove(letter)
        return word_rack

class WordFeudBoard(ScrabbleBoard):
    """
    Represents a WordFeud board.

    This class inherits from the ScrabbleBoard class and provides additional functionality specific to WordFeud.

    Attributes:

    """
    def _setup_board(self):
        row_1 = \
            [Square(modifier="3LS"), Square(), Square(), Square(modifier="3WS"), Square(),
             Square(), Square(), Square(modifier="2LS"), Square(), Square(),
             Square(), Square(modifier="3WS"), Square(), Square(), Square(modifier="3LS"),
             Square(sentinel=0)]
        row_15 = copy.deepcopy(row_1)

        row_2 = \
            [Square(), Square(modifier="2LS"), Square(), Square(), Square(),
             Square(modifier="3LS"), Square(), Square(), Square(), Square(modifier="3LS"),
             Square(), Square(), Square(), Square(modifier="2LS"), Square(),
             Square(sentinel=0)]
        row_14 = copy.deepcopy(row_2)

        row_3 = \
            [Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"), Square(),
             Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(sentinel=0)]
        row_13 = copy.deepcopy(row_3)

        row_4 = \
            [Square(), Square(), Square(), Square(modifier="3LS"), Square(),
             Square(), Square(), Square(modifier="2WS"), Square(), Square(),
             Square(), Square(modifier="2LS"), Square(), Square(), Square(),
             Square(sentinel=0)]
        row_12 = copy.deepcopy(row_4)

        row_5 = \
            [Square(modifier="3WS"), Square(), Square(), Square(), Square(modifier="2WS"),
             Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"), Square(),
             Square(modifier="2WS"), Square(), Square(), Square(), Square(modifier="3WS"),
             Square(sentinel=0)]
        row_11 = copy.deepcopy(row_5)

        row_6 = \
            [Square(), Square(modifier="3LS"), Square(), Square(), Square(),
             Square(modifier="3LS"), Square(), Square(), Square(), Square(modifier="3LS"),
             Square(), Square(), Square(), Square(modifier="3LS"), Square(),
             Square(sentinel=0)]
        row_10 = copy.deepcopy(row_6)

        row_7 = \
            [Square(), Square(), Square(modifier="2LS"), Square(), Square(modifier="2LS"),
             Square(), Square(), Square(), Square(), Square(modifier="2LS"),
             Square(), Square(modifier="2LS"), Square(), Square(), Square(),
             Square(sentinel=0)]
        row_9 = copy.deepcopy(row_7)

        row_8 = \
            [Square(modifier="2LS"), Square(), Square(), Square(modifier="2WS"), Square(),
             Square(), Square(), Square(), Square(), Square(),
             Square(), Square(modifier="2WS"), Square(), Square(), Square(modifier="2LS"),
             Square(sentinel=0)]

        row_16 = [Square(sentinel=0) for _ in range(16)]

        return row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8,row_9, row_10, row_11, row_12, \
        row_13, row_14, row_15, row_16

    def _setup_colors(self):
        """
        Sets up the colors used in the WordFeud board.


        """
        self.bgcolor = (0, 0, 0)
        self.fgcolor = (255, 255, 255)
        self.TILE_bgcolor = (245, 245, 245)
        self.TILE_fgcolor = (0, 0, 0)
        self.TLS_bgcolor = (0, 100, 200)
        self.TWS_bgcolor = (130, 60, 60)
        self.DLS_bgcolor = (120, 160, 110)
        self.DWS_bgcolor = (190, 120, 30)
        self.BLANK_bgcolor = (45, 45, 45)
        self.SQUARE_fgcolor = (255, 255, 255)


