from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

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
        node.frequency += 1

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
            suggestions.append((current_prefix, node.frequency))

        for char, child_node in node.children.items():
            self._get_suggestions(child_node, current_prefix + char, suggestions)
    
    def get_all_words_with_prefix(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))

        for char, child_node in node.children.items():
            self.get_all_words_with_prefix(child_node, prefix + char, suggestions)

product_data = ["apple", "banana", "orange", "grape", "mango", "strawberry", "blueberry", "kiwi", "pineapple"]

trie = Trie()
for product in product_data:
    trie.insert(product)

def get_autocomplete_suggestions(prefix):
    suggestions = []
    node = trie.root
    for char in prefix.lower():
        if char in node.children:
            node = node.children[char]
        else:
            return suggestions

    trie.get_all_words_with_prefix(node, prefix.lower(), suggestions)
    sorted_suggestions = sorted(suggestions, key=lambda x: x[1], reverse=True)
    return [word for word in sorted_suggestions]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = get_autocomplete_suggestions(prefix)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
