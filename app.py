from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Define paths for temporary files
TMP_PATH = "/tmp/keys.json"
HISTORY_PATH = "/tmp/keys_history.json"

# Default keys to initialize if the file does not exist
DEFAULT_KEYS = [
    {"key": "A123", "name": "John Doe", "contact": "1234567890"},
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

# Function to log changes in the history file
def log_history(action, key_id, old_data, new_data):
    history = []
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as file:
            history = json.load(file)
    history.append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "key_id": key_id,
        "old_data": old_data,
        "new_data": new_data
    })
    with open(HISTORY_PATH, 'w') as file:
        json.dump(history, file, indent=4)

# Load history logs
def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as file:
            return json.load(file)
    return []

# Initialize files on startup
def initialize_tmp_file():
    if not os.path.exists(TMP_PATH):
        save_keys(DEFAULT_KEYS)
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'w') as file:
            json.dump([], file)

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

    old_data = keys[key_id].copy()
    keys[key_id]['name'] = name
    keys[key_id]['contact'] = contact

    save_keys(keys)
    log_history("update", key_id, old_data, keys[key_id])

    return jsonify({'success': True, 'message': 'Key updated successfully!'})

@app.route('/clear/<int:key_id>', methods=['POST'])
def clear_key(key_id):
    keys = load_keys()
    old_data = keys[key_id].copy()
    keys[key_id]['name'] = ""
    keys[key_id]['contact'] = ""

    save_keys(keys)
    log_history("clear", key_id, old_data, keys[key_id])

    return jsonify({'success': True, 'message': 'Key cleared successfully!'})

@app.route('/history')
def history():
    logs = load_history()
    return render_template('history.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
