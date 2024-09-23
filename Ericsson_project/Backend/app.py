# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from GeneratingDoc import UserStroies
app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://127.0.0.1:5500"}})

# Set up logging
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        return '', 204
    
    app.logger.info("Received upload request")
    app.logger.debug(f"Request files: {request.files}")
    
    if 'file' not in request.files:
        app.logger.warning("No file part in the request")
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        app.logger.warning("No selected file")
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    if file and file.filename.endswith('.txt'):
        #fileName : puvith.txt
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)#Uploads/puvith.txt
        file.save(filename)
        print(filename)
        app.logger.info(f"File saved: {filename}")
        UserStory = UserStroies(filename)
        UserStory.preprocessing()
        UserStory.GenerateUserStories()
        print(UserStory.UserStory)
        return jsonify({'message': 'File successfully uploaded'}), 200
    else:
        app.logger.warning("Invalid file type")
        return jsonify({'error': 'Allowed file type is txt'}), 400

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5000)