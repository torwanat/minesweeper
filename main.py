import sys
import tkinter as tk
import game
import stats

global main_menu_status

sys.setrecursionlimit(2500)

def validate_dimensions(height, width, mines):
    if not height.isdigit() or not width.isdigit() or not mines.isdigit():
        return False

    if 0 < int(height) <= 50 and 0 < int(width) <= 50 and 0 < int(mines) < int(height) * int(width):
        return True

    return False


def play_button_click(board_height, board_width, board_mines):
    if validate_dimensions(board_height, board_width, board_mines):
        game.start_game(int(board_height), int(board_width), int(board_mines), main_window)
    else:
        main_menu_status.set("Invalid dimensions!")
        return


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