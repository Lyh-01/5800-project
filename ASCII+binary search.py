def calculate_ascii_score(word):
    """Calculate the sum of ASCII values for all characters in a word."""
    return sum(ord(c) for c in word)

# Example dictionary
dictionary = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

# Create a dictionary with ASCII scores
ASCII_dictionary = {word: calculate_ascii_score(word) for word in dictionary}

# Sort the dictionary by ASCII scores
sorted_dict = sorted(ASCII_dictionary.items(), key=lambda x: x[1])

def levenshtein_distance(w1, w2):
    """Calculate Levenshtein distance using dynamic programming."""
    m, n = len(w1), len(w2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif w1[i - 1] == w2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def find_range(sorted_dict, target_score, threshold):
    """Find the range of scores within the threshold around the target score."""
    start, end = 0, len(sorted_dict) - 1
    for i, (_, score) in enumerate(sorted_dict):
        if target_score - threshold <= score <= target_score + threshold:
            start = i if start == 0 else start
            end = i
    return start, end

def improved_search(word, sorted_dict, threshold=10):
    """Search for words with similar ASCII scores and short edit distances."""
    target_score = calculate_ascii_score(word)
    start, end = find_range(sorted_dict, target_score, threshold)
    candidates = []

    for candidate, score in sorted_dict[start:end + 1]:
        if abs(len(candidate) - len(word)) <= 2:  # Additional length check
            distance = levenshtein_distance(word, candidate)
            if distance <= 2:  # Levenshtein distance threshold
                candidates.append(candidate)
    return candidates

# Test word
misspelled_word = "appel"
results = improved_search(misspelled_word, sorted_dict)
print(f"Suggestions for '{misspelled_word}': {results}")

# Example output
print("Sorted dictionary by ASCII score:", sorted_dict)
