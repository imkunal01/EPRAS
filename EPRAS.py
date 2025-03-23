import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e2f")

        self.frames = 3
        self.pages = [random.randint(1, 5) for _ in range(10)]

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e2f")
        style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 12))
        style.configure("TButton", background="#5e60ce", foreground="white", font=("Segoe UI", 11), padding=8)
        style.map("TButton", background=[("active", "#7b7efb")])
        style.configure("TCombobox", font=("Segoe UI", 11), padding=4)
        style.map("TCombobox", fieldbackground=[("readonly", "#27293d")], foreground=[("readonly", "white")])

    def build_ui(self):
        # Controls Frame
        control_frame = ttk.Frame(self.root, padding=20)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="Select Algorithm:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.algo_choice = ttk.Combobox(control_frame, values=["FIFO", "LRU", "Optimal"], state="readonly")
        self.algo_choice.set("FIFO")
        self.algo_choice.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(control_frame, text="Page References (comma-separated):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.page_input = ttk.Entry(control_frame, width=30)
        self.page_input.insert(0, ",".join(map(str, self.pages)))
        self.page_input.grid(row=1, column=1, padx=10, pady=5)

        # Buttons Row
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.run_button = ttk.Button(btn_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(btn_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Page Faults Label
        self.page_fault_label = ttk.Label(control_frame, text="Page Faults: 0")
        self.page_fault_label.grid(row=3, column=0, columnspan=2)

        # Graph Frame
        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.fig, self.ax = plt.subplots(facecolor='#1e1e2f')
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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

    def lru_algorithm(self):
        queue = []
        recent = {}
        page_faults = 0
        history = []

        for i, page in enumerate(self.pages):
            if page not in queue:
                if len(queue) < self.frames:
                    queue.append(page)
                else:
                    lru_page = min(recent, key=recent.get)
                    queue[queue.index(lru_page)] = page
                page_faults += 1
            recent[page] = i
            history.append(queue.copy())

        return history, page_faults

    def optimal_algorithm(self):
        queue = []
        page_faults = 0
        history = []

        for i in range(len(self.pages)):
            page = self.pages[i]
            if page not in queue:
                if len(queue) < self.frames:
                    queue.append(page)
                else:
                    future = self.pages[i+1:]
                    indices = [(future.index(p) if p in future else float('inf')) for p in queue]
                    farthest = indices.index(max(indices))
                    queue[farthest] = page
                page_faults += 1
            history.append(queue.copy())

        return history, page_faults

    def animate(self, i):
        self.ax.clear()
        self.ax.set_facecolor('#1e1e2f')
        self.ax.set_title(f"{self.algo_choice.get()} Algorithm", fontsize=14, color='white')
        self.ax.set_xlabel("Frame Slot", color="white")
        self.ax.set_ylabel("Page Number", color="white")
        self.ax.tick_params(colors='white')

        if i < len(self.history):
            y = self.history[i]
            self.ax.bar(range(len(y)), y, color="#5e60ce")
            self.ax.set_ylim(0, max(self.pages) + 1)

    def run_simulation(self):
        algo = self.algo_choice.get()
        try:
            self.pages = list(map(int, self.page_input.get().strip().split(',')))
        except:
            messagebox.showerror("Invalid Input", "Please enter valid comma-separated numbers.")
            return

        # Disable run button during animation
        self.run_button.state(["disabled"])

        # Stop previous animation if running
        if hasattr(self, 'ani') and self.ani:
            try:
                self.ani.event_source.stop()
            except:
                pass

        if algo == "FIFO":
            self.history, self.page_faults = self.fifo_algorithm()
        elif algo == "LRU":
            self.history, self.page_faults = self.lru_algorithm()
        elif algo == "Optimal":
            self.history, self.page_faults = self.optimal_algorithm()
        else:
            return

        self.page_fault_label.config(text=f"Page Faults: {self.page_faults}")

        self.ax.clear()
        self.canvas.draw()

        def on_animation_complete():
            self.run_button.state(["!disabled"])

        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=len(self.history), interval=700, repeat=False)
        duration = len(self.history) * 700
        self.root.after(duration, on_animation_complete)

        self.canvas.draw()

    def reset_simulation(self):
        if hasattr(self, 'ani') and self.ani:
            try:
                self.ani.event_source.stop()
            except:
                pass

        self.ax.clear()
        self.canvas.draw()
        self.page_fault_label.config(text="Page Faults: 0")
        self.run_button.state(["!disabled"])

# Launch GUI
root = tk.Tk()
app = PageReplacementSimulator(root)
root.mainloop()
