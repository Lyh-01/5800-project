import tkinter as tk
from tkinter import messagebox

# Dynamic Programming: Edit Distance Calculation
def edit_distance(word1, word2):
    dp = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    for i in range(len(word1) + 1):
        for j in range(len(word2) + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[len(word1)][len(word2)]

# Greedy Algorithm: Find the closest word based on edit distance
def greedy_correction(word, dictionary):
    closest_word = None
    min_distance = float('inf')

    for candidate in dictionary:
        distance = edit_distance(word, candidate)
        if distance < min_distance:
            min_distance = distance
            closest_word = candidate

    return closest_word

# Example dictionary
dictionary = ["apple", "orange", "banana", "grape", "strawberry", "blueberry"]

# Function to suggest correction based on user input
def suggest_correction():
    word = entry.get().strip().lower()
    if word:
        closest_word = greedy_correction(word, dictionary)
        if closest_word:
            result_label.config(text=f"Did you mean: {closest_word}?")
        else:
            result_label.config(text="No suggestion found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a word.")

# Set up the main application window
root = tk.Tk()
root.title("Spell Checker")

# Create and place widgets
label = tk.Label(root, text="Enter a word:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

button = tk.Button(root, text="Check Spelling")
button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Start the application loop
root.mainloop()
