"""
Module for managing the game window
"""
import datetime
import random
import tkinter as tk
import utils
import stats

main_board = []
board_dimensions = []
game_start_time = datetime.datetime.now()
game_status = ""

# Otherwise linter gets mad
global turn
global result_text

def start_game(width, height, mines, main_window):
    """
    Starts the game, creates and manages the game window
    :param width: width of the board
    :param height: height of the board
    :param mines: amount of mines
    :param main_window: root window of the program
    """
    global main_board
    global board_dimensions
    global turn
    global result_text
    global game_start_time
    global game_status

    turn = tk.StringVar()
    result_text = tk.StringVar()
    turn.set("Turn #1")
    result_text.set("")
    game_status = "GAME_ONGOING"

    game_window = tk.Toplevel(main_window)
    game_window.title("Game of Minesweeper")

    board_frame = tk.Frame(game_window)
    top_frame = tk.Frame(game_window)

    result_label = tk.Label(top_frame, textvariable=result_text)
    title_label = tk.Label(top_frame, text="Minesweeper", font=("Bauhaus 93", 12))
    turn_label = tk.Label(top_frame, textvariable=turn)

    result_label.pack(side="left")
    title_label.pack(side="left")
    turn_label.pack(side="left")

    # Create the logical and actual boards and set the dimensions
    main_board = prepare_logical_board(width, height, mines)
    tiles = prepare_tiles(width, height, board_frame)
    board_dimensions = [width, height]

    # Merge the logical and actual boards
    for x in range(len(main_board)):
        for y in range(len(main_board[x])):
            main_board[x][y]["tile"] = tiles[x][y]

    top_frame.pack(side="top")
    board_frame.pack()

    game_start_time = datetime.datetime.now()

    game_window.mainloop()


def increase_turn():
    """
    Increases the turn number
    """
    current_turn = turn.get()
    next_turn = int(current_turn.split("#")[1]) + 1
    turn.set(f'Turn #{next_turn}')


def end_game(result):
    """
    Ends the game
    :param result: result of the game (WIN or LOSE)
    """
    global game_status
    global result_text

    final_turn = int(turn.get().split("#")[1]) - 1
    game_duration = utils.get_game_duration(game_start_time, datetime.datetime.now())

    if result == "WIN":
        game_status = "GAME_ENDED"
        result_text.set("You win!")

        stats.write_stats_data([game_start_time.date(), game_duration, final_turn, "WIN", 0])
    else:
        game_status = "GAME_ENDED"
        result_text.set("You lose :c")

        mines_left = get_mines_left()
        stats.write_stats_data([str(game_start_time.date()), game_duration, final_turn, "LOST", mines_left])


def get_mines_left():
    """
    Returns the number of mines left in the game
    :return: number of mines left
    """
    mines_counter = 0

    for i in main_board:
        for j in i:
            if j["state"] == -1 and not j["flagged"]:
                mines_counter += 1

    return mines_counter


def prepare_logical_board(width, height, mines):
    """
    Prepares the logical board for the game
    :param width: width of the board
    :param height: height of the board
    :param mines: amount of mines
    :return: logical board of the game as a two-dimensional list of dictionaries
    """

    # Create starting board
    logical_board = []
    for i in range(width):
        tmp_board = []
        for j in range(height):
            tmp_board.append({"state": 0, "tile": tk.Label(), "uncovered": False, "flagged": False})
        logical_board.append(tmp_board)

    # Shuffle all possible coordinates
    available_tiles = []
    for x in range(width):
        for y in range(height):
            available_tiles.append((x, y))
    random.shuffle(available_tiles)

    # Mark fields with mines
    mine_indexes = []
    for i in range(mines):
        x = available_tiles[i][0]
        y = available_tiles[i][1]
        logical_board[x][y]["state"] = -1
        mine_indexes.append(available_tiles[i])

    # Add numbers to tiles bordering mines
    for mine in mine_indexes:
        x = mine[0]
        y = mine[1]
        for k in range(-1, 2):
            if 0 <= x + k < width:
                for j in range(-1, 2):
                    if 0 <= y + j < height:
                        if logical_board[x + k][y + j]["state"] != -1:
                            logical_board[x + k][y + j]["state"] += 1

    return logical_board


def prepare_tiles(width, height, board):
    """
    Prepares the actual board for the game
    :param width: width of the board
    :param height: height of the board
    :param board: logical board of the game (from the prepare_logical_board function)
    :return: board of the game as a two-dimensional list of Labels in a grid
    """
    tiles_array = []
    for i in range(width):
        tmp_array = []
        for j in range(height):
            tile = tk.Label(board, width=2, height=1, bg="lightgray", bd=1, relief="sunken")
            tile.bind("<Button-1>", left_click_on_tile)
            tile.bind("<Button-3>", right_click_on_tile)
            tile.bind("<Button-2>", right_click_on_tile)
            tile.grid(row=i, column=j)
            tmp_array.append(tile)
        tiles_array.append(tmp_array)
    return tiles_array


def right_click_on_tile(event):
    """
    Handles the right click on a tile
    :param event: generic event parameter
    """
    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]

    if game_status == "GAME_ONGOING":
        toggle_flag(x, y)


def left_click_on_tile(event):
    """
    Handles the left click on a tile
    :param event: generic event parameter
    """
    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]

    if game_status == "GAME_ONGOING" and not main_board[x][y]["uncovered"]:
        increase_turn()
        uncover_tile(x, y)


def uncover_tile(x, y):
    """
    Uncovers the clicked file and uses DFS to uncover adjacent tiles (if applicable)
    :param x: x coordinate of the tile
    :param y: y coordinate of the tile
    """
    clicked_tile = main_board[x][y]
    if clicked_tile["state"] == -1:
        # Clicked on a mine, end game with a "LOSE" status
        clicked_tile["tile"].config(bg="red")
        end_game("LOSE")
    elif clicked_tile["state"] == 0 and not clicked_tile["flagged"]:
        # Clicked on an empty tile, uncover and start DFS
        clicked_tile["tile"].config(bg="white", relief="flat", text="0", fg="white")
        clicked_tile["uncovered"] = True

        # DFS for empty tiles to uncover
        for k in range(-1, 2):
            if 0 <= x + k < board_dimensions[0]:
                for j in range(-1, 2):
                    if 0 <= y + j < board_dimensions[1]:
                        if main_board[x + k][y + j]["tile"]["text"] == "":
                            uncover_tile(x + k, y + j)
    else:
        # Clicked on a border tile, uncover it
        clicked_tile["tile"].config(text=str(clicked_tile["state"]), fg=utils.pick_color(clicked_tile["state"]))
        clicked_tile["uncovered"] = True
        check_win()


def check_win():
    """
    Checks the win condition of the game
    """
    for row in main_board:
        for tile in row:
            if not tile["uncovered"] and tile["state"] != -1:
                return

    end_game("WIN")


def toggle_flag(x, y):
    """
    Toggles the flag of the selected tile
    :param x: x coordinate of the tile
    :param y: y coordinate of the tile
    """
    clicked_tile = main_board[x][y]
    if clicked_tile["flagged"]:
        clicked_tile["tile"].config(text="")
        clicked_tile["flagged"] = False
    else:
        clicked_tile["tile"].config(text="🚩")
        clicked_tile["flagged"] = True
