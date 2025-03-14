from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulated storage (in-memory list)
stored_files = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def get_files():
    return jsonify({"files": stored_files})

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    filename = data.get('filename')
    if filename and filename not in stored_files:
        stored_files.append(filename)
    return jsonify({"message": "File uploaded"})

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if old_name in stored_files and new_name and new_name not in stored_files:
        stored_files[stored_files.index(old_name)] = new_name
    return jsonify({"message": "File updated"})

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    filename = data.get('filename')
    if filename in stored_files:
        stored_files.remove(filename)
    return jsonify({"message": "File deleted"})

if __name__ == '__main__':
    app.run(debug=True)
