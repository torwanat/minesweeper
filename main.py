import random
import tkinter as tk

global main_board
global board_dimensions


def validate_dimensions(height, width, mines):
    if not height.isdigit() or not width.isdigit() or not mines.isdigit():
        return False

    if 0 < int(height) < 100 and 0 < int(width) < 100 and 0 < int(mines) < int(height) * int(width):
        return True

    return False


def play_button_click(board_height, board_width, board_mines, status_label):
    if validate_dimensions(board_height, board_width, board_mines):
        start_game(int(board_height), int(board_width), int(board_mines))
    else:
        status_label.config(text="Invalid dimensions!", fg="red")
        return


def start_game(width, height, mines):
    global main_board
    global board_dimensions
    board = tk.Toplevel(main_window)
    board.title("Game of Minesweeper")

    main_board = prepare_logical_board(width, height, mines)
    tiles = prepare_tiles(width, height, board)
    board_dimensions = [width, height]

    for x in range(len(main_board)):
        for y in range(len(main_board[x])):
            main_board[x][y]["tile"] = tiles[x][y]

    board.mainloop()


def prepare_logical_board(width, height, mines):
    logical_board = []
    for i in range(width):
        tmp_board = []
        for j in range(height):
            tmp_board.append({"state": 0, "tile": tk.Label()})
        logical_board.append(tmp_board)

    mine_indexes = []
    for i in range(mines):
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if logical_board[x][y]["state"] == 0:
                logical_board[x][y]["state"] = -1
                mine_indexes.append([x, y])
                break

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
    print(event.widget.grid_info())


def left_click_on_tile(event):
    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]

    uncover_tile(x, y)


def uncover_tile(x, y):
    if main_board[x][y]["state"] == -1:
        main_board[x][y]["tile"].config(bg="red")
    elif main_board[x][y]["state"] == 0:
        main_board[x][y]["tile"].config(bg="white", relief="flat", text="0", fg="white")
        for k in range(-1, 2):
            if 0 <= x + k < board_dimensions[0]:
                for j in range(-1, 2):
                    if 0 <= y + j < board_dimensions[1]:
                        if main_board[x + k][y + j]["tile"]["text"] == "":
                            uncover_tile(x + k, y + j)
    else:
        main_board[x][y]["tile"].config(text=str(main_board[x][y]["state"]))

def main():
    title_label = tk.Label(main_window, text="Minesweeper", font=("Bauhaus 93", 30))
    height_label = tk.Label(main_window, text="Height")
    width_label = tk.Label(main_window, text="Width")
    mines_label = tk.Label(main_window, text="Mines")
    status_label = tk.Label(main_window, text="")

    height_entry = tk.Entry(main_window)
    width_entry = tk.Entry(main_window)
    mines_entry = tk.Entry(main_window)

    play_button = tk.Button(main_window, text="Play", command=lambda: play_button_click(height_entry.get(), width_entry.get(), mines_entry.get(), status_label))

    title_label.grid(row=0, column=1, padx=20, pady=20)
    height_label.grid(row=1, column=1, padx=20)
    height_entry.grid(row=2, column=1, padx=20)
    width_label.grid(row=3, column=1, padx=20)
    width_entry.grid(row=4, column=1, padx=20)
    mines_label.grid(row=5, column=1, padx=20)
    mines_entry.grid(row=6, column=1, padx=20)
    status_label.grid(row=7, column=1, padx=20)
    play_button.grid(row=8, column=1, padx=20, pady=20)

    main_window.mainloop()


if __name__ == '__main__':
    main_window = tk.Tk()
    main_window.title("Minesweeper")
    main()