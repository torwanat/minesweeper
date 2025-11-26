import csv
import tkinter as tk


def get_stats_data():
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


def show_stats(stats_data, main_window):
    stats_window = tk.Toplevel(main_window)
    stats_window.title("Statistics")

    title_label = tk.Label(stats_window, text="Previous scores", font=("Bauhaus 93", 25))
    date_label = tk.Label(stats_window, text="Date")
    duration_label = tk.Label(stats_window, text="Duration")
    turns_label = tk.Label(stats_window, text="Turns")
    result_label = tk.Label(stats_window, text="Result")
    mines_left_label = tk.Label(stats_window, text="Mines left")

    title_label.grid(row=0, column=1, columnspan=3)
    date_label.grid(row=1, column=0, padx=10)
    duration_label.grid(row=1, column=1, padx=10)
    turns_label.grid(row=1, column=2, padx=10)
    result_label.grid(row=1, column=3, padx=10)
    mines_left_label.grid(row=1, column=4, padx=10)

    for i, row in enumerate(stats_data):
        game_date_label = tk.Label(stats_window, text=row[0])
        game_duration_label = tk.Label(stats_window, text=row[1])
        game_turns_label = tk.Label(stats_window, text=row[2])
        game_result_label = tk.Label(stats_window, text=row[3])
        game_mines_left_label = tk.Label(stats_window, text=row[4])

        game_date_label.grid(row=(i + 2), column=0)
        game_duration_label.grid(row=(i + 2), column=1)
        game_turns_label.grid(row=(i + 2), column=2)
        game_result_label.grid(row=(i + 2), column=3)
        game_mines_left_label.grid(row=(i + 2), column=4)

    stats_window.mainloop()


def write_stats_data(data):
    try:
        with open("stats.csv", "a+", encoding="UTF-8") as stats_file:
            writer = csv.writer(stats_file)
            writer.writerows([data])
    except FileNotFoundError:
        print("Stats file not found")