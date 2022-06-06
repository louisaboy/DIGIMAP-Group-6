# render_template - return an html page
#  url_for - used to link the css file to the html file
import urllib.request
import os
from flask import Flask, render_template, url_for, request, flash, redirect
from werkzeug.utils import secure_filename

# import the dataset here
# SAMPLE: from sklearn.datasets import load_iris

# import the model to be used

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# index route
@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


# route for accepting images
@app.route('/', methods=['POST'])
def upload_image():
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file_path = "./uploads/" + file.filename
        # file.save(file_path)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "___main__":
    # when launching a flask app to production environment make debug false
    # debug = true - so that when we change the file the server will restart itself
    app.run(port=3000,debug=true)