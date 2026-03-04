# main.py

import threading
import queue
import time
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Config import API_KEY, BASE_URL, CITIES
from worker import weather_worker
from weather_api import fetch_weather


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nepal Weather Dashboard – Multi-threaded Fetcher")
        self.root.geometry("950x650")

        self.result_queue = queue.Queue()
        self.completed = 0

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Nepal Weather Dashboard – Multi-threaded Fetcher",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        self.fetch_btn = tk.Button(
            self.root,
            text="Fetch Weather",
            font=("Arial", 12),
            command=self.start_fetch
        )
        self.fetch_btn.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Idle", fg="blue")
        self.status_label.pack(pady=5)

        columns = ("City", "Temp (°C)", "Humidity (%)", "Pressure (hPa)", "Status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(pady=10)

        self.seq_label = tk.Label(self.root, text="Sequential Time: -")
        self.seq_label.pack()

        self.par_label = tk.Label(self.root, text="Parallel Time: -")
        self.par_label.pack()

        self.figure = Figure(figsize=(5, 3))
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

    def start_fetch(self):
        self.fetch_btn.config(state="disabled")
        self.status_label.config(text="Fetching...", fg="orange")
        self.tree.delete(*self.tree.get_children())

        self.sequential_time = self.fetch_sequential()
        self.parallel_time = self.fetch_parallel()

    def fetch_sequential(self):
        start = time.time()
        for city in CITIES:
            result = fetch_weather(city, API_KEY, BASE_URL)
            self.tree.insert("", "end", values=result)
        elapsed = round(time.time() - start, 2)
        self.seq_label.config(text=f"Sequential Time: {elapsed} sec")
        return elapsed

    def fetch_parallel(self):
        self.completed = 0
        start = time.time()

        for city in CITIES:
            t = threading.Thread(
                target=weather_worker,
                args=(city, API_KEY, BASE_URL, self.result_queue)
            )
            t.start()

        self.root.after(100, lambda: self.process_queue(start))

    def process_queue(self, start_time):
        while not self.result_queue.empty():
            result = self.result_queue.get()
            self.tree.insert("", "end", values=result)
            self.completed += 1

        if self.completed < len(CITIES):
            self.root.after(100, lambda: self.process_queue(start_time))
        else:
            elapsed = round(time.time() - start_time, 2)
            self.par_label.config(text=f"Parallel Time: {elapsed} sec")
            self.draw_chart(self.sequential_time, elapsed)
            self.status_label.config(text="Done!", fg="green")
            self.fetch_btn.config(state="normal")

    def draw_chart(self, seq, par):
        self.ax.clear()
        self.ax.bar(["Sequential", "Parallel"], [seq, par])
        self.ax.set_title("Latency Comparison")
        self.ax.set_ylabel("Time (seconds)")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()