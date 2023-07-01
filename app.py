import os
from flask import Flask, redirect, url_for, render_template, request, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import datetime


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "7474747474747474747474747577477"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], timestamp + '_' + filename))
            flash('File successfully uploaded')
            #ابدا الشغل 
            return redirect('/')
        else:
            flash('Allowed file types are csv')
            return redirect(request.url)





if __name__ == '__main__':
    app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
    )
    app.run(host='0.0.0.0', debug=True)