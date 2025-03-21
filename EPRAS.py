import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Page Replacement Simulation
class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithm Simulator")
        self.root.geometry("700x500")

        # Dropdown for Algorithm Selection
        self.algo_label = ttk.Label(root, text="Select Algorithm:")
        self.algo_label.pack()
        self.algo_choice = ttk.Combobox(root, values=["FIFO", "LRU", "Optimal"])
        self.algo_choice.pack()
        self.algo_choice.set("FIFO")

        # Start Button
        self.start_button = ttk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.start_button.pack()

        # Frame for Graph
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.frames = 3  # Number of frames
        self.pages = [random.randint(1, 5) for _ in range(10)]  # Random page references

    def fifo_algorithm(self):
        queue = []
        page_faults = 0
        history = []

        for page in self.pages:
            if page not in queue:
                if len(queue) < self.frames:
                    queue.append(page)
                else:
                    queue.pop(0)
                    queue.append(page)
                page_faults += 1
            history.append(queue.copy())

        return history, page_faults

    def animate(self, i):
        self.ax.clear()
        self.ax.set_title(f"Page Replacement: {self.algo_choice.get()}")
        self.ax.set_xlabel("Time Step")
        self.ax.set_ylabel("Page Frames")
        
        # Get frame-by-frame data
        if i < len(self.history):
            y_data = self.history[i]
            self.ax.bar(range(len(y_data)), y_data, color="blue")

    def run_simulation(self):
        algo = self.algo_choice.get()
        if algo == "FIFO":
            self.history, self.page_faults = self.fifo_algorithm()
        
        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=len(self.history), repeat=False, interval=700)
        self.canvas.draw()

# Run GUI
root = tk.Tk()
app = PageReplacementSimulator(root)
root.mainloop()
