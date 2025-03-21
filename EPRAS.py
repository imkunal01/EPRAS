import matplotlib.pyplot as plt

# Function to simulate FIFO (First-In-First-Out) Page Replacement Algorithm
def fifo_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    history = []  # Stores the state of frames at each step

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)  # Add page if there's space
            else:
                frame.pop(0)  # Remove the oldest page
                frame.append(page)  # Insert new page
            page_faults += 1  # Increase page fault count
        history.append(list(frame))  # Store the current frame state
    
    return page_faults, history

# Function to simulate LRU (Least Recently Used) Page Replacement Algorithm
def lru_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    history = []  # Stores the state of frames at each step

    for page in pages:
        if page in frame:
            frame.remove(page)  # Move used page to the end
        else:
            page_faults += 1  # Page fault occurs
            if len(frame) == capacity:
                frame.pop(0)  # Remove least recently used page
        frame.append(page)  # Insert new page at the end
        history.append(list(frame))  # Store the current frame state

    return page_faults, history

# Function to simulate Optimal Page Replacement Algorithm
def optimal_page_replacement(pages, capacity):
    frame = []
    page_faults = 0
    history = []  # Stores the state of frames at each step

    for i in range(len(pages)):
        if pages[i] not in frame:
            if len(frame) < capacity:
                frame.append(pages[i])  # Add page if there's space
            else:
                # Find the page to be replaced
                future = pages[i+1:]  # Remaining pages
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

                frame[replace_idx] = pages[i]  # Replace the selected page
            page_faults += 1  # Increase page fault count
        history.append(list(frame))  # Store the current frame state

    return page_faults, history

# Function to visualize page replacement simulation
def visualize_simulation(pages, capacity):
    algorithms = {
        "FIFO": fifo_page_replacement,
        "LRU": lru_page_replacement,
        "Optimal": optimal_page_replacement
    }

    plt.figure(figsize=(12, 6))

    for idx, (name, algo) in enumerate(algorithms.items(), 1):
        page_faults, history = algo(pages, capacity)

        plt.subplot(1, 3, idx)
        plt.imshow(history, cmap="coolwarm", aspect="auto")
        plt.xticks(range(capacity))
        plt.yticks(range(len(pages)), pages)
        plt.title(f"{name} (Faults: {page_faults})")
        plt.xlabel("Frame Slot")
        plt.ylabel("Page Sequence")

    plt.tight_layout()
    plt.show()

# Driver Code: Takes input from the user and runs simulations
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

    # Visualize the results
    visualize_simulation(pages, capacity)
