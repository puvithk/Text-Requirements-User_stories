# app.py
from flask import Flask, request, jsonify,send_file,abort 
import zipfile
import io
from flask_cors import CORS
import os
import shutil
import time 
import threading
from threading import Lock
import logging
import multiprocessing
from multiprocessing import Manager
from GeneratingDoc import UserStories
from GenertingDocument import CodeGeneration, HLDDocument,LLDDocument,UserStories,SRSDocument,TOLSTestCase
from ConvertToDoc import generate_word_from_txt ,txt_to_docx ,  text_doc,create_table_doc
app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "*"}}) 
CORS(app, resources={r"/refresh": {"origins": "*"}}) 
CORS(app, resources={r"/*": {"origins": "*"}})
start_log = Lock()
logging.basicConfig(level=logging.DEBUG)
DOCUMENTS_DIR = os.path.join(os.getcwd(), "AllDocuments")
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(DOCUMENTS_DIR):
    os.makedirs(DOCUMENTS_DIR)
ALL_THREADS =[]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit


@app.route("/Document_Status", methods=["GET"])
def document_status():
    DOCUMENT_STATUS = {
    "Requirements": False,
    "UserStories": False,
    "SRS": False,
    "HLD": False,
    "LLD": False,
    "FullCode": False,
    "TestCase": False,
    "TOLs" :False
    }
    for i , j  in DOCUMENT_STATUS.items():
      
        if os.path.exists(os.path.join(DOCUMENTS_DIR, f'{i}.docx')):
        
            DOCUMENT_STATUS[i] = True
            
    if os.listdir(os.path.join(os.getcwd(), 'FullCode')):
        DOCUMENT_STATUS["FullCode"] = True

    
    return jsonify(DOCUMENT_STATUS), 200
        
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
        response = jsonify({
            'message': f"File uploaded successfully: {file.filename}",
            'filename': filename
        })
        response.status_code = 200
        thread = multiprocessing.Process(target=generate_All_file , args=(filename,))
        #thread = threading.Thread(target=generate_All_file , args=(filename,))
        ALL_THREADS.append(thread)
        thread.start()
        time.sleep(5)
        return response


def generate_All_file(filename ):
    #Generating Userstory
        global requirements,user_stories,srs,hld,lld,full_code
        UserOutput = UserStories(filename)
        Requirements =UserOutput.read_file()
        generate_word_from_txt(Requirements , "Requirements.txt")
        requirements = True
        
        if not UserOutput.preprocessing():
            return jsonify({'error': 'An error occured in server'}), 500
        Userprocessed ,UserUnProcessed = UserOutput.GenerateUserStories()
        if not Userprocessed:
            return jsonify({'error': 'An error occured in server'}), 500
        
        generate_word_from_txt(UserUnProcessed.text , "UserStories.txt")
        

        #Generating SRS Document 
        srsDoc = SRSDocument(Userprocessed)
        srsOutput,SRSUnProcessed = srsDoc.GenerateSRS()
        if not srsOutput:
            return jsonify({'error': 'An error occured in server'}), 500
        generate_word_from_txt(SRSUnProcessed.text  , "SRS.txt")
       
        #Generating HLD Document 
        hldDoc = HLDDocument(srsOutput)
        hldOutput,hldUnProcessed =hldDoc.GenerateHLD()
        if not hldOutput:
            return jsonify({'error': 'An error occured in server'}), 500
        generate_word_from_txt(hldUnProcessed.text , "HLD.txt")
       

        #Generating LLD Document 
        lldDoc = LLDDocument(hldOutput)
        lldOutput,lldUnProcessed =lldDoc.GenerateLLD() 
        if not lldOutput:
            return jsonify({'error': 'An error occured in server'}), 500
        generate_word_from_txt(lldUnProcessed.text , "LLd.txt")
        TOLDoc = TOLSTestCase(lldOutput)
        TOLOutput , TOLUnprocessed = TOLDoc.GenerateTOL()
        text_doc(TOLOutput , "TOLs.txt")


        TestCase ,TestUnprocessed = TOLDoc.GenerateTestCase()
        text_doc(TestCase , "TestCase.txt")
        time.sleep(10)
        #Generating Code 
        output =CodeGeneration(lldOutput)
        if not output.CreateCode():
            return jsonify({'error': 'An error occured in server'}), 500
        
        with open(os.path.join(os.getcwd(),"AllDocuments","UserStories.txt") , "w") as file :
            file.write(Userprocessed)
        
        with open(os.path.join("AllDocuments","srsOutput.txt" ), "w")as file :
            file.write(srsOutput)
        with open(os.path.join("AllDocuments","hldOutput.txt" ), "w") as file :
            file.write(hldOutput)
        with open(os.path.join("AllDocuments","lldOutput.txt" ), "w") as file :
            file.write(lldOutput)



#changed from here 
@app.route("/get_requirements" , methods=['GET'])
def get_requirements():
   
    file_path = os.path.join(DOCUMENTS_DIR, "Requirements.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="Requirements.docx")
    else:
        return abort(404, description="File not found")

#Downloading Files 
@app.route('/get_user_stories', methods=['GET'])
def get_user_stories():
 
    file_path = os.path.join(DOCUMENTS_DIR, "UserStories.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="UserStories.docx")
    else:
        return abort(404, description="File not found")

# Route to get SRS file
@app.route('/get_srs', methods=['GET'])
def get_srs():
    file_path = os.path.join(DOCUMENTS_DIR, "SRS.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="SRS.docx")
    else:
        return abort(404, description="File not found")

# Route to get HLD file
@app.route('/get_hld', methods=['GET'])
def get_hld():
    file_path = os.path.join(DOCUMENTS_DIR, "HLD.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="HLD.docx")
    else:
        return abort(404, description="File not found")

# Route to get LLD file
@app.route('/get_lld', methods=['GET'])
def get_lld():
    file_path = os.path.join(DOCUMENTS_DIR, "LLd.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="LLD.docx")
    else:
        return abort(404, description="File not found")
    


@app.route('/get_TOL', methods=['GET'])
def get_TOL():
    file_path = os.path.join(DOCUMENTS_DIR, "TOLs.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="TOLs.docx")
    else:
        return abort(404, description="File not found")
@app.route('/get_testCase', methods=['GET'])
def get_TestCase():
    file_path = os.path.join(DOCUMENTS_DIR, "TestCase.docx")
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name="TestCase.docx")
    else:
        return abort(404, description="File not found")
@app.route('/get_all_documents', methods=['GET'])
def get_all_documents():
    try:
        # List of files to include in the zip
        file_list = [
            ("UserStories.docx", "UserStories.docx"),
            ("SRS.docx", "SRS.docx"),
            ("HLD.docx", "HLD.docx"),
            ("LLD.docx", "LLd.docx"),
            ("TOLs.docx", "TOLs.docx"),
            ("TestCase.docx","TestCase.docx")
        ]
        
        # Create an in-memory zip file
        zip_filename = "AllDocuments.zip"
        memory_file = io.BytesIO()

        with zipfile.ZipFile(memory_file, 'w') as zf:
            for file_name, download_name in file_list:
                file_path = os.path.join(DOCUMENTS_DIR, file_name)
                while not os.path.exists(file_path):
                    time.sleep(1)
                if os.path.exists(file_path):
                    zf.write(file_path, download_name)
                else:
                    return abort(404, description=f"File {file_name} not found")

        # Make sure the memory file is ready to be read from the start
        memory_file.seek(0)

        return send_file(memory_file, as_attachment=True, download_name=zip_filename)

    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while creating the zip file'}), 500
@app.route('/get_full_code',methods=['GET'])
def get_full_code():
    folder_path = os.path.join(os.getcwd(), 'FullCode')
    # Path to the output zip file
    while not os.listdir(folder_path):
        time.sleep(10)
    zip_filename = os.path.join(os.getcwd(), 'FullCode.zip')

    try:
        shutil.make_archive('FullCode', 'zip', folder_path) 

        return send_file(zip_filename , as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/refresh', methods=['GET'])
def refresh():
    all_code_dir = os.path.join(os.getcwd(), 'FullCode')
    all_documents_dir = os.path.join(os.getcwd(), 'AllDocuments')

    # Function to remove directory contents
    def clear_directory(directory_path):
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            try:
                # Remove all files and subdirectories inside the directory
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove subdirectories
                    else:
                        os.remove(file_path)  # Remove files
                app.logger.info(f"Successfully removed contents of {directory_path}")
            except PermissionError as e:
                app.logger.error(f"Permission denied: {str(e)}")
                return jsonify({'error': f'Permission denied: {str(e)}'}), 500
            except Exception as e:
                app.logger.error(f"An error occurred: {str(e)}")
                return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        else:
            app.logger.info(f"{directory_path} does not exist or is not a directory")

    
    clear_directory(all_code_dir)
    clear_directory(UPLOAD_FOLDER)
    global requirements,user_stories,srs,hld,lld,full_code
    requirements= False
    user_stories= False,
    srs=False
    hld= False
    lld= False
    full_code= False
    
    if ALL_THREADS:
        thread = ALL_THREADS.pop()
        thread.terminate()
    clear_directory(all_documents_dir)
    
    return jsonify({'message': 'Done'}), 200



@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({'error': 'An unexpected error occurred'}), 500
if __name__ == '__main__':
   
    app.run(debug=True,port=5000)