"""
Module for managing the stats window as well as writing / reading from a file
"""
import csv
import tkinter as tk

stats_window_opened = False

def get_stats_data():
    """
    Tries to read the stats data from the file
    :return: stats data as a list
    """
    try:
        with open("stats.csv", "r", encoding="UTF-8") as stats_file:
            stats_data = []
            csv_stats_data = csv.reader(stats_file)

            for line in csv_stats_data:
                if line:
                    stats_data.append(line)

            return stats_data
    except FileNotFoundError:
        return []


def on_frame_configure(canvas):
    """
    Reset the scroll region to encompass the inner frame
    :param canvas: tkinter Canvas object
    """
    canvas.configure(scrollregion=canvas.bbox("all"))


def fill_stats_frame(stats_frame, stats_data):
    """
    Fills the stats frame with data from file
    :param stats_frame: frame to fill with data
    :param stats_data: stats data to fill the frame with
    :return:
    """
    title_label = tk.Label(stats_frame, text="Previous scores", font=("Bauhaus 93", 25))
    date_label = tk.Label(stats_frame, text="Date")
    duration_label = tk.Label(stats_frame, text="Duration")
    turns_label = tk.Label(stats_frame, text="Turns")
    result_label = tk.Label(stats_frame, text="Result")
    mines_left_label = tk.Label(stats_frame, text="Mines left")

    title_label.grid(row=0, column=1, columnspan=3)
    date_label.grid(row=1, column=0, padx=10)
    duration_label.grid(row=1, column=1, padx=10)
    turns_label.grid(row=1, column=2, padx=10)
    result_label.grid(row=1, column=3, padx=10)
    mines_left_label.grid(row=1, column=4, padx=10)

    for i, row in enumerate(stats_data):
        game_date_label = tk.Label(stats_frame, text=row[0])
        game_duration_label = tk.Label(stats_frame, text=row[1])
        game_turns_label = tk.Label(stats_frame, text=row[2])
        game_result_label = tk.Label(stats_frame, text=row[3])
        game_mines_left_label = tk.Label(stats_frame, text=row[4])

        game_date_label.grid(row=(i + 2), column=0)
        game_duration_label.grid(row=(i + 2), column=1)
        game_turns_label.grid(row=(i + 2), column=2)
        game_result_label.grid(row=(i + 2), column=3)
        game_mines_left_label.grid(row=(i + 2), column=4)


def show_stats(stats_data, main_window):
    """
    Creates and manages the stats window
    :param stats_data: stats data as a list (from get_stats_data())
    :param main_window: root window of the program
    """
    global stats_window_opened

    stats_window = tk.Toplevel(main_window)
    stats_window.title("Statistics")

    stats_canvas = tk.Canvas(stats_window, borderwidth=0)
    stats_canvas_frame = tk.Frame(stats_canvas)
    vsb = tk.Scrollbar(stats_window, orient="vertical", command=stats_canvas.yview)
    stats_canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    stats_canvas.pack(side="left", fill="both", expand=True)
    stats_canvas.create_window((15, 0), window=stats_canvas_frame, anchor="nw")

    stats_canvas_frame.bind("<Configure>", lambda event, canvas=stats_canvas: on_frame_configure(stats_canvas))

    fill_stats_frame(stats_canvas_frame, stats_data)

    stats_window_opened = True

    stats_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(stats_window))
    stats_window.mainloop()


def write_stats_data(data):
    """
    Tries to write the stats data to the file
    :param data: data to be written to the file
    """
    try:
        with open("stats.csv", "a+", encoding="UTF-8", newline="") as stats_file:
            writer = csv.writer(stats_file)
            writer.writerows([data])
    except FileNotFoundError:
        print("Stats file not found")


def on_closing(stats_window):
    """
    Protocol handler for window closing
    :param stats_window: window to close
    """
    global stats_window_opened

    stats_window_opened = False
    stats_window.destroy()