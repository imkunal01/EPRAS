import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to simulate FIFO Page Replacement Algorithm
def fifo_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    history = []

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
            page_faults += 1
        history.append(list(frame))

    return page_faults, history

# Function to simulate LRU Page Replacement Algorithm
def lru_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    history = []

    for page in pages:
        if page in frame:
            frame.remove(page)
        else:
            page_faults += 1
            if len(frame) == capacity:
                frame.pop(0)
        frame.append(page)
        history.append(list(frame))

    return page_faults, history

# Function to simulate Optimal Page Replacement Algorithm
def optimal_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    history = []

    for i in range(len(pages)):
        if pages[i] not in frame:
            if len(frame) < capacity:
                frame.append(pages[i])
            else:
                future = pages[i+1:]
                replace_idx = -1
                farthest_use = -1

                for page in frame:
                    if page in future:
                        next_use = future.index(page)
                        if next_use > farthest_use:
                            farthest_use = next_use
                            replace_idx = frame.index(page)
                    else:
                        replace_idx = frame.index(page)
                        break

                frame[replace_idx] = pages[i]
            page_faults += 1
        history.append(list(frame))

    return page_faults, history

# Function to animate page replacement step by step
def animate_page_replacement(pages, capacity, algorithm, algo_name):
    page_faults, history = algorithm(pages, capacity)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title(f"{algo_name} Page Replacement (Faults: {page_faults})")
    ax.set_xlabel("Frame Slots")
    ax.set_ylabel("Time Step")
    ax.set_xticks(range(capacity))
    ax.set_yticks(range(len(pages)))
    
    table = ax.table(cellText=[[""] * capacity for _ in range(len(pages))],
                     cellLoc='center', loc='center')
    
    def update(frame_num):
        frame_state = history[frame_num]
        for i, val in enumerate(frame_state):
            table[(frame_num, i)]._text.set_text(str(val))
        return table,

    ani = animation.FuncAnimation(fig, update, frames=len(history), repeat=False, interval=700)
    plt.show()

# Driver Code
if __name__ == "__main__":
    pages = list(map(int, input("Enter reference string (space-separated): ").split()))
    capacity = int(input("Enter the number of frames: "))

    print("\nRunning Page Replacement Algorithms...\n")

    fifo_faults, _ = fifo_page_replacement(pages, capacity)
    lru_faults, _ = lru_page_replacement(pages, capacity)
    optimal_faults, _ = optimal_page_replacement(pages, capacity)

    print(f"FIFO Page Faults: {fifo_faults}")
    print(f"LRU Page Faults: {lru_faults}")
    print(f"Optimal Page Faults: {optimal_faults}")

    # Choose algorithm for animation (FIFO, LRU, or Optimal)
    algo_map = {
        "FIFO": fifo_page_replacement,
        "LRU": lru_page_replacement,
        "Optimal": optimal_page_replacement
    }

    choice = input("\nChoose an algorithm to animate (FIFO/LRU/Optimal): ").strip().capitalize()
    if choice in algo_map:
        animate_page_replacement(pages, capacity, algo_map[choice], choice)
    else:
        print("Invalid choice! Please enter FIFO, LRU, or Optimal.")
