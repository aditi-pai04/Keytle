import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Path to keys.json file
KEYS_FILE = os.path.join(os.path.dirname(__file__), "keys.json")

# Load keys from the JSON file
def load_keys():
    keys_json = os.getenv("KEYS_JSON")
    if keys_json:
        return json.loads(keys_json)
    return []


# Save keys to the JSON file
def save_keys(keys):
    with open(KEYS_FILE, 'w') as file:
        json.dump(keys, file, indent=4)

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
    app.run(debug=True,port=5001)
