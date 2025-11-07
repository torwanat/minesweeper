import random
import sys
import tkinter as tk
import datetime
import stats
import utils

global main_board
global board_dimensions
global game_window
global main_menu_status
global turn
global result_text
global game_start_time

sys.setrecursionlimit(2500)

def validate_dimensions(height, width, mines):
    if not height.isdigit() or not width.isdigit() or not mines.isdigit():
        return False

    if 0 < int(height) <= 50 and 0 < int(width) <= 50 and 0 < int(mines) < int(height) * int(width):
        return True

    return False


def play_button_click(board_height, board_width, board_mines):
    if validate_dimensions(board_height, board_width, board_mines):
        start_game(int(board_height), int(board_width), int(board_mines))
    else:
        global main_menu_status
        main_menu_status.set("Invalid dimensions!")
        return


def start_game(width, height, mines):
    global main_board
    global board_dimensions
    global game_window
    global turn
    global main_menu_status
    global result_text
    global game_start_time

    turn = tk.StringVar()
    result_text = tk.StringVar()
    turn.set("Turn #1")
    result_text.set("")
    main_menu_status.set("Game ongoing...")

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

    main_board = prepare_logical_board(width, height, mines)
    tiles = prepare_tiles(width, height, board_frame)
    board_dimensions = [width, height]

    for x in range(len(main_board)):
        for y in range(len(main_board[x])):
            main_board[x][y]["tile"] = tiles[x][y]

    top_frame.pack(side="top")
    board_frame.pack()

    game_start_time = datetime.datetime.now()

    game_window.mainloop()


def increase_turn():
    current_turn = turn.get()
    next_turn = int(current_turn.split("#")[1]) + 1
    turn.set(f'Turn #{next_turn}')


def end_game(result):
    global main_menu_status
    global result_text
    global turn
    global game_start_time

    final_turn = int(turn.get().split("#")[1]) - 1
    game_duration = utils.get_game_duration(game_start_time, datetime.datetime.now())

    if result == "WIN":
        main_menu_status.set("Congratulations!")
        result_text.set("You win!")

        stats.write_stats_data([game_start_time.date(), game_duration, final_turn, "WIN", 0])
    else:
        main_menu_status.set("Game over!")
        result_text.set("You lose :c")

        mines_left = get_mines_left()
        stats.write_stats_data([str(game_start_time.date()), game_duration, final_turn, "LOST", mines_left])


def get_mines_left():
    global main_menu_status
    mines_counter = 0

    for i in main_board:
        for j in i:
            if j["state"] == -1 and not j["flagged"]:
                mines_counter += 1

    return mines_counter


def prepare_logical_board(width, height, mines):
    logical_board = []
    for i in range(width):
        tmp_board = []
        for j in range(height):
            tmp_board.append({"state": 0, "tile": tk.Label(), "uncovered": False, "flagged": False})
        logical_board.append(tmp_board)

    available_tiles = []
    for x in range(width):
        for y in range(height):
            available_tiles.append((x, y))
    random.shuffle(available_tiles)

    mine_indexes = []
    for i in range(mines):
        x = available_tiles[i][0]
        y = available_tiles[i][1]
        logical_board[x][y]["state"] = -1
        mine_indexes.append(available_tiles[i])


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
    global main_menu_status

    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]

    if main_menu_status.get() == "Game ongoing...":
        toggle_flag(x, y)


def left_click_on_tile(event):
    global main_menu_status

    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]

    if main_menu_status.get() == "Game ongoing...":
        increase_turn()
        uncover_tile(x, y)


def uncover_tile(x, y):
    clicked_tile = main_board[x][y]
    if clicked_tile["state"] == -1:
        end_game("LOSE")
    elif clicked_tile["state"] == 0 and not clicked_tile["flagged"]:
        clicked_tile["tile"].config(bg="white", relief="flat", text="0", fg="white")
        clicked_tile["uncovered"] = True
        for k in range(-1, 2):
            if 0 <= x + k < board_dimensions[0]:
                for j in range(-1, 2):
                    if 0 <= y + j < board_dimensions[1]:
                        if main_board[x + k][y + j]["tile"]["text"] == "":
                            uncover_tile(x + k, y + j)
    else:
        clicked_tile["tile"].config(text=str(clicked_tile["state"]), fg=utils.pick_color(clicked_tile["state"]))
        clicked_tile["uncovered"] = True
        check_win()


def check_win():
    for row in main_board:
        for tile in row:
            if not tile["uncovered"] and tile["state"] != -1:
                return

    end_game("WIN")


def toggle_flag(x, y):
    clicked_tile = main_board[x][y]
    if clicked_tile["flagged"]:
        clicked_tile["tile"].config(text="")
        clicked_tile["flagged"] = False
    else:
        clicked_tile["tile"].config(text="🚩")
        clicked_tile["flagged"] = True


def stats_button_click():
    stats_data = stats.get_stats_data()
    stats.show_stats(stats_data, main_window)


def main():
    global main_menu_status
    main_menu_status = tk.StringVar()

    title_label = tk.Label(main_window, text="Minesweeper", font=("Bauhaus 93", 30))
    height_label = tk.Label(main_window, text="Height")
    width_label = tk.Label(main_window, text="Width")
    mines_label = tk.Label(main_window, text="Mines")
    status_label = tk.Label(main_window, textvariable=main_menu_status)

    height_entry = tk.Entry(main_window)
    width_entry = tk.Entry(main_window)
    mines_entry = tk.Entry(main_window)

    buttons_frame = tk.Frame(main_window)

    play_button = tk.Button(buttons_frame, text="Play", command=lambda: play_button_click(height_entry.get(), width_entry.get(), mines_entry.get()))
    stats_button = tk.Button(buttons_frame, text="Stats", command=lambda: stats_button_click())
    gap_label = tk.Label(buttons_frame, width=10)

    play_button.pack(side="left")
    gap_label.pack(side="left")
    stats_button.pack(side="left")

    title_label.grid(row=0, column=1, padx=20, pady=20)
    height_label.grid(row=1, column=1, padx=20)
    height_entry.grid(row=2, column=1, padx=20)
    width_label.grid(row=3, column=1, padx=20)
    width_entry.grid(row=4, column=1, padx=20)
    mines_label.grid(row=5, column=1, padx=20)
    mines_entry.grid(row=6, column=1, padx=20)
    status_label.grid(row=7, column=1, padx=20)
    buttons_frame.grid(row=8, column=1, padx=20, pady=20)

    main_window.mainloop()


if __name__ == '__main__':
    main_window = tk.Tk()
    main_window.title("Minesweeper")
    main()