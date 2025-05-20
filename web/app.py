from flask import Flask, render_template, request, jsonify
from optimizer import optimizeThis, suggestNew

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('try.html') # debug try.html

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    original_text = data.get('text', '')
    optimized_text = optimizeThis(original_text)
    return jsonify({'optimized': optimized_text})

@app.route('/suggest_new', methods=['POST'])
def get_suggestion():
    data = request.get_json()
    text = data.get('text', '')
    word = data.get('word', '')
    suggestion = suggestNew(text, word)
    return jsonify({'suggestion': suggestion})

if __name__ == '__main__':
    app.run(debug=True) 