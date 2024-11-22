import tkinter as tk
import tkinter as tk
from tkinter import scrolledtext
import json
import threading

# Spell checker uses 2009 Webster's English Dictionary
# https://github.com/matthewreagan/WebstersEnglishDictionary/tree/master

# 1,000 Most Common English words

# make sure to update the dictionary.json for your relative file path


# Node class definition
class Node:
    def __init__(self, word=None):
        self.word = word
        self.next = {}

# Function to add node to the tree
def add_node(root, curr):
    if not root.word:
        root.word = curr.word
        return
    dist = edit_distance(curr.word, root.word)
    if dist not in root.next:
        tree.append(curr)
        root.next[dist] = len(tree) - 1
    else:
        add_node(tree[root.next[dist]], curr)

# Edit distance function
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
    return dp[m][n]

# Function to get similar words
def get_similar_words(root, s, tolerance=1):
    if not root or not root.word:
        return []
    dist = edit_distance(root.word, s)
    like_words = [root.word] if dist <= tolerance else []
    for i in range(max(1, dist - tolerance), dist + tolerance + 1):
        if i in root.next:
            like_words.extend(get_similar_words(tree[root.next[i]], s, tolerance))
    return like_words

# Function to check text
def check_text():
    input_text = input_box.get("1.0", tk.END).strip()
    words = input_text.split()
    results = []
    for word in words: # Read the text box word by word
        if word.lower() not in all_words:  # O(1) dictionary lookup
            matches = get_similar_words(root, word.lower())
            if matches:
                results.append(f"'{word}' is misspelled. Suggestions: {', '.join(matches[:])}")
            else:
                results.append(f"'{word}' is misspelled. No suggestions found.")
        else:
            results.append(f"'{word}' is correct.")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "\n".join(results))



# Function to load dictionary and build tree
def load_dictionary():
    global root, tree, all_words
    try:
        with open('CS5800/dictionary.json', 'r') as file:
            data = json.load(file)
        with open('CS5800/common.json', 'r') as file2:
            common = json.load(file2)

        common_words = common['commonWords'] 

        dict_words = list(data.keys())
        all_words = set()

        root = Node()
        tree = [root]

        # Add commonWords first
        # 1000 most common english words at the top of the tree
        for word in common_words:
            if word not in all_words:
                temp = Node(word)
                add_node(root, temp)
                all_words.add(word)

        # Add remaining dict_words
        for word in dict_words:
            if word not in all_words:
                temp = Node(word)
                add_node(root, temp)
                all_words.add(word)
            if (word == dict_words[len(dict_words)//2]):
                loading_label.config(text="Building Burkhard-Keller Tree Dictionary...")
                
        all_words = list(all_words)
            
        loading_label.config(text="Dictionary loaded successfully!")
        loading_window.after(10, open_spell_checker)
    except FileNotFoundError:
        loading_label.config(text="Dictionary file not found.")
    except json.JSONDecodeError:
        loading_label.config(text="Invalid JSON in dictionary file.")

# Function to open spell checker GUI
def open_spell_checker():
    loading_window.destroy()
    spell_checker_window = tk.Tk()
    spell_checker_window.title("Spell Checker")

    input_label = tk.Label(spell_checker_window, text="Enter text:")
    input_label.pack()

    global input_box
    input_box = scrolledtext.ScrolledText(spell_checker_window, height=10, width=50)
    input_box.pack()

    check_button = tk.Button(spell_checker_window, text="Check Spelling", command=check_text)
    check_button.pack()

    result_label = tk.Label(spell_checker_window, text="Results:")
    result_label.pack()

    global result_box
    result_box = scrolledtext.ScrolledText(spell_checker_window, height=10, width=50)
    result_box.pack()

    spell_checker_window.mainloop()

# Create loading window
loading_window = tk.Tk()
loading_window.title("Loading Dictionary")
loading_window.geometry("300x100")

loading_label = tk.Label(loading_window, text="Dictionary is loading...")
loading_label.pack(pady=20)

# Start loading dictionary in a separate thread
threading.Thread(target=load_dictionary, daemon=True).start()

loading_window.mainloop()
