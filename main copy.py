from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
import os
from datetime import datetime
app = Flask(__name__)

# Configure the folder to save the uploaded files
UPLOAD_FOLDER = 'static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set allowed extensions if necessary (optional)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/s')
def indexs():
    # Get list of files in the upload folder
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', filenames=filenames)

@app.route('/m')
def indexsm():
    # Get list of files in the upload folder
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload_multipart.html', filenames=filenames)


@app.route('/')
def index():
    # Get list of files in the upload folder
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    
    # Create a list of tuples containing filename and modification date
    files_with_dates = []
    for filename in filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.fromtimestamp(mod_time).strftime('%d/%m/%Y | %H:%M:%S')
        files_with_dates.append((filename, mod_date))
    
    return render_template('index.html', files_with_dates=files_with_dates)
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
      print(request.files)
      if request.method == 'POST':
            # Check if the post request has the file part
            if 'file' not in request.files:
                return 'No file part'
            file = request.files['file']
            # If the user does not select a file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return 'No selected file'
            print("file",(file))
            print(allowed_file(file.filename))
            print(file and allowed_file(file.filename))
            if file :
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("filename",filename)
                print("filepath",filepath)
                file.save(filepath)
               # return redirect(url_for('index'))
      return render_template('upload.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
      print(filename)
      return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploadMulti', methods=['GET', 'POST'])
def uploadMulti():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'

        # Get list of files from the form
        files = request.files.getlist('file')

        # If no file is selected, return an error
        if not files or files[0].filename == '':
            return 'No selected file'

        # Process each file in the list
        for file in files:
            if file :
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                print(f"Saved file: {filename} at {filepath}")

        return 'Files successfully uploaded'
    
    return render_template('upload_multipart.html')
# @app.route('/download/<filename>')
# def download_file(filename):
#       # Ensure the file exists
#         if not os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
#             abort(404)
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
#         mimetype = 'application/vnd.android.package-archive' if filename.endswith('.apk') else None
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True, mimetype=mimetype)
# @app.route('/download/<filename>')
# def download_file(filename):
#         # Ensure the file exists
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#         # Ensure the file exists
#         if not os.path.isfile(file_path):
#             abort(404)
    
#         # Use send_from_directory to send the file as an attachment
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    
@app.route('/download/<filename>')
def download_file(filename):
    # Construct the full file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Debugging output
    print(f"File path: {file_path}")
    print(f"File exists: {os.path.isfile(file_path)}")
    
    # Ensure the file exists
    if not os.path.isfile(file_path):
        abort(404)

    # Send the file as an attachment
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5010)
# pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" main.py