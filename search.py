import tkinter as tk

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        suggestions = []
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return suggestions  
        self._get_suggestions(node, prefix, suggestions)
        return suggestions

    def _get_suggestions(self, node, current_prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append(current_prefix)

        for char, child_node in node.children.items():
            self._get_suggestions(child_node, current_prefix + char, suggestions)

product_data = ["apple", "banana", "orange", "grape", "mango", "strawberry", "blueberry", "kiwi", "pineapple"]

trie = Trie()
for product in product_data:
    trie.insert(product)

def get_autocomplete_suggestions(prefix):
    return trie.search(prefix.lower())

def update_suggestions(*args):
    user_input = entry.get().lower()
    
    if user_input:
        autocomplete_suggestions = get_autocomplete_suggestions(user_input)
        suggestion_var.set("Are you looking for: " + ", ".join(autocomplete_suggestions))
    else:
        suggestion_var.set("")

root = tk.Tk()
root.title("Product Search")
    
entry = tk.Entry(root, width=30)
entry.pack(pady=10)
entry.bind("<KeyRelease>", update_suggestions)

suggestion_var = tk.StringVar()
suggestion_label = tk.Label(root, textvariable=suggestion_var)
suggestion_label.pack(pady=10)

root.mainloop()
