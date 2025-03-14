from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

stored_files = []

@app.route('/')
def index():
    return render_template('htmldoc.html')

@app.route('/files')
def get_files():
    return jsonify({"files": stored_files})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get("file")
    if file and file.filename:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        stored_files.append(file.filename)
        return jsonify({"message": "Uploaded!"})
    return jsonify({"message": "No file selected"}), 400

@app.route('/rename', methods=['POST'])
def rename():
    data = request.json
    old, new = data["oldName"], data["newName"]
    old_path, new_path = os.path.join(UPLOAD_FOLDER, old), os.path.join(UPLOAD_FOLDER, new)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        stored_files[stored_files.index(old)] = new
        return jsonify({"message": "Renamed successfully!"})
    
    return jsonify({"message": "File not found"}), 404

@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    file = data["fileName"]
    path = os.path.join(UPLOAD_FOLDER, file)
    
    if os.path.exists(path):
        os.remove(path)
        stored_files.remove(file)
        return jsonify({"message": "Deleted!"})
    
    return jsonify({"message": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
