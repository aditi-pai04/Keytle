from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Define the path to the temporary keys file
TMP_PATH = "/tmp/keys.json"

# Default keys to initialize if the file does not exist
DEFAULT_KEYS = [
    {"key": "A123", "name": "John Doe", "contact": "1234567890"},
    {"key": "B456", "name": "Jane Smith", "contact": "9876543210"},
    {"key": "B456", "name": "Jane Smith", "contact": "9876543210"}
]

# Function to load keys from the JSON file
def load_keys():
    if os.path.exists(TMP_PATH):
        with open(TMP_PATH, 'r') as file:
            return json.load(file)
    return DEFAULT_KEYS

# Function to save keys to the JSON file
def save_keys(keys):
    with open(TMP_PATH, 'w') as file:
        json.dump(keys, file, indent=4)

# Initialize the keys file on startup
def initialize_tmp_file():
    if not os.path.exists(TMP_PATH):
        save_keys(DEFAULT_KEYS)

initialize_tmp_file()

@app.route('/')
def index():
    keys = load_keys()
    return render_template('index.html', keys=keys)

@app.route('/update', methods=['POST'])
def update_key():
    keys = load_keys()
    key_id = int(request.form['key_id'])
    name = request.form['name']
    contact = request.form['contact']

    keys[key_id]['name'] = name
    keys[key_id]['contact'] = contact

    save_keys(keys)
    return jsonify({'success': True, 'message': 'Key updated successfully!'})

@app.route('/clear/<int:key_id>', methods=['POST'])
def clear_key(key_id):
    keys = load_keys()
    keys[key_id]['name'] = ""
    keys[key_id]['contact'] = ""

    save_keys(keys)
    return jsonify({'success': True, 'message': 'Key cleared successfully!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
