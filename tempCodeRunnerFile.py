import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithm Simulator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        # Apply theme to ttk widgets
        style = ttk.Style()
        style.theme_use('clam')  # You can try 'alt', 'clam', 'vista', 'xpnative'
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 11), padding=6)
        style.configure('TCombobox', font=('Segoe UI', 11))

        # Top Frame (Controls)
        self.top_frame = ttk.Frame(root, padding=20)
        self.top_frame.pack(fill=tk.X)

        self.algo_label = ttk.Label(self.top_frame, text="Select Algorithm:")
        self.algo_label.pack(side=tk.LEFT, padx=(0, 10))

        self.algo_choice = ttk.Combobox(self.top_frame, values=["FIFO", "LRU", "Optimal"], state="readonly")
        self.algo_choice.set("FIFO")
        self.algo_choice.pack(side=tk.LEFT, padx=(0, 20))

        self.run_button = ttk.Button(self.top_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT)

        # Add spacing
        ttk.Label(self.top_frame, text="    ").pack(side=tk.LEFT)

        self.page_fault_label = ttk.Label(self.top_frame, text="Page Faults: 0")
        self.page_fault_label.pack(side=tk.LEFT)

        # Bottom Frame (Graph)
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_frame)
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
        self.ax.set_title(f"Page Replacement: {self.algo_choice.get()}", fontsize=14)
        self.ax.set_xlabel("Frame Index", fontsize=11)
        self.ax.set_ylabel("Page Number", fontsize=11)

        if i < len(self.history):
            y_data = self.history[i]
            self.ax.bar(range(len(y_data)), y_data, color="#4a90e2")
            self.ax.set_ylim(0, max(self.pages) + 1)

    def run_simulation(self):
        algo = self.algo_choice.get()
        if algo == "FIFO":
            self.history, self.page_faults = self.fifo_algorithm()

        self.page_fault_label.config(text=f"Page Faults: {self.page_faults}")

        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=len(self.history), repeat=False, interval=700)
        self.canvas.draw()

# Run GUI
root = tk.Tk()
app = PageReplacementSimulator(root)
root.mainloop()
