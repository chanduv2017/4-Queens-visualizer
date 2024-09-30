import random
import tkinter as tk
from PIL import Image, ImageTk
import time


def initial_state(board_size):
    return [i for i in range(board_size)]


def conflicts(state, row, col):
    count = 0
    for i in range(len(state)):
        if i != row:
            if state[i] == col or abs(i - row) == abs(state[i] - col):
                count += 1
    return count


def total_conflicts(state):
    total = 0
    for i in range(len(state)):
        total += conflicts(state, i, state[i])
    return total


def min_conflict_value(state, row):
    min_conflict_count = float('inf')
    min_conflict_col = -1
    for col in range(len(state)):
        conflict_count = conflicts(state, row, col)
        if conflict_count < min_conflict_count:
            min_conflict_count = conflict_count
            min_conflict_col = col
    return min_conflict_col


def min_conflict(state, max_steps, update_board_func, update_step_func):
    for step in range(1, max_steps + 1):
        if total_conflicts(state) == 0:
            return state, step  # Solution found
        row = random.randint(0, len(state) - 1)
        col = min_conflict_value(state, row)
        state[row] = col
        update_board_func(state)
        update_step_func(step)
        root.update()
        time.sleep(0.5)  # Adjust delay for better visualization
    return None, step


def update_board(state):
    for row in range(len(state)):
        for col in range(len(state)):
            cell = board[row][col]
            if state[row] == col:
                if queen_image:
                    cell.config(image=queen_image, bg="lightblue")
                    cell.image = queen_image
                else:
                    cell.config(text='Q', bg="lightblue", fg="black")
            else:
                cell.config(image="", text="", bg="lightgrey")
                cell.image = None


def update_step(step):
    step_label.config(text=f"Steps: {step}")

def solve():
    """Start the solving process."""
    result_label.config(text="")
    initial_board = initial_state(board_size)
    solution, steps = min_conflict(
        initial_board,
        max_steps=100,  # Increased steps for larger boards
        update_board_func=update_board,
        update_step_func=update_step
    )
    if solution:
        result_label.config(text="Solution Found!")
    else:
        result_label.config(text="No solution found within the given steps.")


def create_gui(board_size):
    global board, step_label, result_label, solve_button, root, queen_image

    root = tk.Tk()
    root.title(f"{board_size}-Queens Problem")

    try:
        original_image = Image.open("img.png")
        resized_image = original_image.resize((50, 50), Image.LANCZOS)  # Adjust size as needed
        queen_image = ImageTk.PhotoImage(resized_image)
    except FileNotFoundError:
        print("Error: 'image.png' not found. Proceeding without images.")
        queen_image = None

    board = []

    for row in range(board_size):
        row_cells = []
        for col in range(board_size):
            # Avoid specifying width and height for images
            cell = tk.Label(
                root,
                width=6,  # Set a fixed width in text units (not pixels)
                height=3,  # Set a fixed height in text units (not pixels)
                borderwidth=2,
                relief="solid",
                bg="lightgrey",
                anchor='center'
            )
            cell.grid(row=row, column=col, sticky="nsew")  # Ensure it stretches to fill the grid
            row_cells.append(cell)
        board.append(row_cells)

    for i in range(board_size):
        root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(i, weight=1)

    # Label to display steps
    step_label = tk.Label(root, text="Steps: 0", font=('Arial', 16))
    step_label.grid(row=board_size, column=0, columnspan=board_size//2)

    # Label to display result
    result_label = tk.Label(root, text="", font=('Arial', 16))
    result_label.grid(row=board_size, column=board_size//2, columnspan=(board_size +1)//2)

    # Button to start solving
    solve_button = tk.Button(root, text="Solve", command=solve)
    solve_button.grid(row=board_size + 1, column=0, columnspan=board_size)

    root.mainloop()


if __name__ == "__main__":
    board_size = 4
    create_gui(board_size)
