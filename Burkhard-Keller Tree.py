class Node:
    def __init__(self, word = None):
        self.word = word
        self.next = {}


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


def get_similar_words(root, s):
    if not root or not root.word:
        return []

    dist = edit_distance(root.word, s)
    like_words = [root.word] if dist <= TOLERANCE else []

    start = max(1, dist - TOLERANCE)

    for i in range(max(1, dist - TOLERANCE), dist + TOLERANCE + 1):
        if i in root.next:
            like_words.extend(get_similar_words(tree[root.next[i]], s))

    return like_words


def edit_distance(w1, w2):
    m, n = len(w1), len(w2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if w1[i - 1] == w2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)

    return dp[m][n]



TOLERANCE = 1

root = Node()
tree = [root]

dictionary = ["therefore", "there", "they", "the", "them", "their","they're", "they've", "threat", "thrill", "bird"]

for word in dictionary:
    temp = Node(word)
    add_node(root, temp)

test_word = "there"
matches = get_similar_words(root, test_word)

print("Possible corrections:")
for match in matches:
    print(match)