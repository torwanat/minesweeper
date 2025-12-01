"""
Main module of the program, manages the main menu window
"""
import sys
import tkinter as tk
import game
import stats

# For large boards
sys.setrecursionlimit(2500)

def validate_dimensions(height, width, mines):
    """
    Checks if the dimensions of the board are valid
    :param height: height of the board (1 - 50)
    :param width: width of the board (1 - 50)
    :param mines: mines to place (1 - height * width - 1)
    :return: True if the dimensions of the board are valid, False otherwise
    """
    message = ""

    if not height.isdigit() or not 0 < int(height) <= 50:
        message += "Height must be between 1 and 50!\n"

    if not width.isdigit() or not 0 < int(width) <= 50:
        message += "Width must be between 1 and 50!\n"

    if not mines.isdigit() or not 0 < int(mines) < int(height) * int(width):
        message += "Mines must fit on the board and be greater than 0!\n"

    if message:
        main_menu_status.set(message)
        return False

    return True


def play_button_click(board_height, board_width, board_mines):
    """
    Handler for the play button click
    :param board_height: inputted height of the board
    :param board_width: inputted width of the board
    :param board_mines: inputted amount of mines
    """
    if validate_dimensions(board_height, board_width, board_mines):
        main_menu_status.set("")
        if game.game_status == "WINDOW_CLOSED":
            # Start the game window
            game.start_game(int(board_height), int(board_width), int(board_mines), main_window)
        else:
            main_menu_status.set("Game is already ongoing!")

def stats_button_click():
    """
    Handler for the statistics button click
    """
    if not stats.stats_window_opened:
        main_menu_status.set("")
        # Try to read stats data from the file
        stats_data = stats.get_stats_data()
        # Start the stats window
        stats.show_stats(stats_data, main_window)
    else:
        main_menu_status.set("Stats window already opened!")


def quit_button_click():
    main_window.destroy()

def main():
    """
    Main function of the module, creates and manages the main menu window
    """
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

    play_button = tk.Button(buttons_frame, text="Play",
                            command=lambda: play_button_click(height_entry.get(), width_entry.get(), mines_entry.get()))
    quit_button = tk.Button(buttons_frame, text="Quit", command=quit_button_click)
    stats_button = tk.Button(buttons_frame, text="Stats", command=stats_button_click)
    left_gap_label = tk.Label(buttons_frame, width=5)
    right_gap_label = tk.Label(buttons_frame, width=5)

    play_button.pack(side="left")
    left_gap_label.pack(side="left")
    stats_button.pack(side="left")
    right_gap_label.pack(side="left")
    quit_button.pack(side="left")

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
    main_menu_status = tk.StringVar()
    main()
