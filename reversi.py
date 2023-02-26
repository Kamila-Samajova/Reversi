from typing import List, Optional, Tuple
Playground = List[List[str]]


# Reversi
# 1. Game plan representation
def new_playground(size: int) -> Playground:
    return [size * [" "] for _ in range(size)]


def init_playground(playground: Playground) -> None:
    mid = len(playground) // 2
    for row, col in [(mid - 1, mid - 1), (mid, mid)]:
        set_symbol(playground, row, col, "X")
    for row, col in [(mid - 1, mid), (mid, mid - 1)]:
        set_symbol(playground, row, col, "O")


def get(playground: Playground, row: int, col: int) -> str:
    return playground[row][col]


def set_symbol(playground: Playground, row: int, col: int,
               symbol: str) -> None:
    playground[row][col] = symbol


# 2. Draw the game plan
def draw_numbers_line(size: int) -> None:
    print(end="     ")
    for i in range(size):
        if i < 10:
            print(str(i), end="   ")
        else:
            print(str(i), end="  ")
    print()


def draw_lines(playground: Playground) -> None:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    size = len(playground)
    for i in range(size):
        print("   " + size * "+---" + "+")
        print(" " + alphabet[i], end=" ")
        for j in range(size):
            print("| " + playground[i][j], end=" ")
        print("|")
    print("   " + size * "+---" + "+")


def draw(playground: Playground) -> None:
    draw_numbers_line(len(playground))
    draw_lines(playground)


# 3. Making a move
def is_in_playground(row: int, col: int, size: int) -> bool:
    return 0 <= row < size and 0 <= col < size


# This procedure recolours stones in a given direction. (Row_change and
# col_change are numbers -1, 0 or 1 and they give the direction in which the
# opponent´s stones on the playground will be recoloured. It returns the
# number of stones recoloured.
def modify_playground(playground: Playground, row: int, col: int, symbol: str,
                      row_change: int, col_change: int) -> int:
    num_of_recoloured = 0
    size = len(playground)
    opp_symbol = "O" if symbol == "X" else "X"
    var_row = row + row_change
    var_col = col + col_change

    while is_in_playground(var_row, var_col, size) and \
            get(playground, var_row, var_col) == opp_symbol:
        set_symbol(playground, var_row, var_col, symbol)
        var_row += row_change
        var_col += col_change
        num_of_recoloured += 1

    if (not is_in_playground(var_row, var_col, size) or
            get(playground, var_row, var_col) != symbol):
        return 0

    return num_of_recoloured


# This procedure recolours the opponent´s stones in one direction if the
# variable change is True. Else it just returns the number of the stones
# recoloured.
def recolour_one_dir(playground: Playground, row: int, col: int, symbol: str,
                     change: bool, row_change: int, col_change: int) -> int:
    playground_copy = [row[:] for row in playground[:]]
    num_of_recoloured = modify_playground(playground_copy, row, col, symbol,
                                          row_change, col_change)

    if change and num_of_recoloured != 0:
        playground.clear()
        for row_copy in playground_copy:
            playground.append(row_copy)

    return num_of_recoloured


# This procedure recolours the opponent´s stones in all 8 direction and puts
# the player´s stone on the playground if the variable change is True. Else it
# just returns the number of the stones recoloured. If the given move is not
# possible to play, it returns None.
def recolour(playground: Playground, row: int, col: int,
             symbol: str, change: bool = True) -> Optional[int]:
    num_of_recoloured = 0
    for row_change in [-1, 0, 1]:
        for col_change in [-1, 0, 1]:
            num_of_recoloured += \
                recolour_one_dir(playground, row, col, symbol, change,
                                 row_change, col_change)
    if num_of_recoloured <= 0:
        return None
    if change:
        set_symbol(playground, row, col, symbol)
    return num_of_recoloured


# This procedure make the player´s move if the move is valid and returns the
# number of the stones recoloured (or None if the move is invalid).
def play(playground: Playground, row: int, col: int,
         symbol: str) -> Optional[int]:
    if (not is_in_playground(row, col, len(playground)) or
            get(playground, row, col) != " "):
        return None
    return recolour(playground, row, col, symbol)


# 4. computer strategy and counting stones

# This function returns a valid computer´s move. If there are more valid moves,
# it returns the one with the most opponent´s stones recoloured.
def strategy(playground: Playground, symbol: str) -> Optional[Tuple[int, int]]:
    size = len(playground)
    best_move = None
    max_recoloured = -1
    for row in range(size):
        for col in range(size):
            if get(playground, row, col) != " ":
                continue
            recoloured = recolour(playground, row, col, symbol, False)
            if recoloured is not None and recoloured > max_recoloured:
                best_move = row, col
                max_recoloured = recoloured
    return best_move


# This function returns the count of X and O symbols on the playground.
def count(playground: Playground) -> Tuple[int, int]:
    count_x, count_o = 0, 0
    for row in playground:
        for symbol in row:
            if symbol == "X":
                count_x += 1
            elif symbol == "O":
                count_o += 1
    return count_x, count_o


# 5. game
def who_starts() -> bool:
    start = input("Do you want to start? (YES/NO) ")
    if start == "YES":
        return True
    elif start == "NO":
        return False
    print("You have to write YES or NO in capital letters, "
          "nothing else is allowed, try again: ")
    return who_starts()


def players_symbol() -> str:
    players_sym = input("Which symbol do you want to play with? (X/O) ")
    if players_sym == "X":
        return "X"
    elif players_sym == "O":
        return "O"
    print("You have to write X or O in capital letters, "
          "nothing else is allowed, try again: ")
    return players_symbol()


def players_row_input(size: int) -> int:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    move_letter = input("Write your move. First, write the capital letter "
                        "of the row that you want to play: ")
    if move_letter in set(alphabet[:size]):
        return alphabet.index(move_letter)
    print("Your input does not comply with the rules, "
          "you should write only capital letters "
          "which are written on the left side of the playground, "
          "try again:")
    return players_row_input(size)


def players_col_input(size: int) -> int:
    move_row = input("Then write the number of the column: ")
    if move_row.isdecimal() and 0 <= int(move_row) < size:
        return int(move_row)
    print("Your input does not comply with the rules, "
          "you should write only numbers which are written "
          "above the playground, try again:")
    return players_col_input(size)


def players_input(size: int) -> Tuple[int, int]:
    return players_row_input(size), players_col_input(size)


def players_move(playground: Playground, symbol: str) -> None:
    if game_over(playground, symbol):
        print("You are not able to make a move. Computer plays again.")
        return None
    move = players_input(len(playground))
    # If player inputs an invalid move, he is asked to play a valid move.
    while recolour(playground, move[0], move[1], symbol, False) is None:
        print("You have played an invalid move. Try again:")
        move = players_input(len(playground))
    play(playground, move[0], move[1], symbol)


def pc_move(playground: Playground, symbol: str) -> None:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    move = strategy(playground, symbol)
    if move is not None:
        play(playground, move[0], move[1], symbol)
        print("Computer has played a move on the field",
              alphabet[move[0]], move[1])
    else:
        print("Computer is not able to make a move. You play again.")


# This function checks if there is a possible move for the actual player.
def game_over(playground: Playground, symbol: str) -> bool:
    size = len(playground)
    for row in range(size):
        for col in range(size):
            if (get(playground, row, col) == " " and
                    recolour(playground, row, col, symbol, False) is not None):
                return False
    return True


def result(playground: Playground, pc_sym: str) -> None:
    points = count(playground)
    pc = points[0] if pc_sym == "X" else points[1]
    player = points[0] if pc_sym == "O" else points[1]
    if player > pc:
        print("Congratulations! You won. You have " + str(player) +
              " points and the computer has only " + str(pc))
    elif pc > player:
        print("You lost. The computer has " + str(pc) +
              " points and you have only " + str(player) + " points."
              " Don´t worry, try to beat the computer in the next game.")
    else:
        print("It´s a draw! You both have " + str(pc) + "points.")


def play_again() -> bool:
    start = input("Do you want to play another game? (YES/NO) ")
    if start == "YES":
        return True
    elif start == "NO":
        return False
    print("You have to write YES or NO in capital letters, "
          "nothing else is allowed, try again: ")
    return play_again()


def game(size: int) -> None:
    playground = new_playground(size)
    init_playground(playground)

    players_sym = players_symbol()
    pc_sym = "X" if players_sym == "O" else "O"
    turn = who_starts()
    draw(playground)

    while (not game_over(playground, players_sym)
           or not game_over(playground, pc_sym)):
        if turn:
            players_move(playground, players_sym)
        else:
            pc_move(playground, pc_sym)
        draw(playground)
        turn = not turn

    result(playground, pc_sym)
    if play_again():
        game(size)


# Version for the possibility of playing also 2 humans against each other and
# choosing the size of the playground. (It would substitute the game function
# above.)
def person_or_computer() -> bool:
    pc_person = input("Do you want to play against computer or another person?"
                      "Write C for computer or P for person:")
    if pc_person == "C":
        return True
    elif pc_person == "P":
        return False
    print("You have to write C or P in capital letters, "
          "nothing else is allowed, try again: ")
    return person_or_computer()


def size_of_the_playground() -> int:
    size = input("Write the size of the playground you want to play on:")
    while not size.isdecimal() and not (4 <= int(size) <= 26):
        size = input("You have not written a valid size of the playground, "
                     "please, write a number the interval from 4 to 26.")
    return int(size)


def play_game() -> None:
    playground = new_playground(size_of_the_playground())
    init_playground(playground)

    players_sym = players_symbol()
    opponent_sym = "X" if players_sym == "O" else "O"
    turn = who_starts()
    opponent = person_or_computer()

    draw(playground)
    while (not game_over(playground, players_sym)
           or not game_over(playground, opponent_sym)):
        if turn:
            players_move(playground, players_sym)
        else:
            if opponent:
                pc_move(playground, opponent_sym)
            else:
                players_move(playground, opponent_sym)
        draw(playground)
        turn = not turn

    result(playground, opponent_sym)
    if play_again():
        play_game()


if __name__ == '__main__':
    # write your own tests here
    new_play = [[" ", " ", " ", " ", " ", " "],
                [" ", " ", "X", "X", " ", " "],
                [" ", " ", "X", "O", " ", " "],
                [" ", " ", "X", "O", " ", " "],
                [" ", " ", "O", "O", " ", " "],
                [" ", " ", " ", " ", " ", " "]]
    assert play(new_play, 3, 4, "X") == 2
    x = new_playground(6)
    init_playground(x)
    assert play(x, 1, 3, "X") == 1
    assert play(x, 3, 4, "O") == 1
    assert play(x, 3, 4, "O") is None
    assert play(x, 0, 3, "O") == 2
    assert play(x, 2, 4, "X") == 1
    assert play(x, 0, 2, "X") == 1
    # r, c = strategy(x, "O")
    # play(x, r, c, "O")
    # r2, c2 = strategy(x, "X")
    # assert play(x, r2, c2, "X") == 4
    # draw(x)
    play_game()
