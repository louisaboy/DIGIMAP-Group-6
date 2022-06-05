# render_template - return an html page
#  url_for - used to link the css file to the html file
from flask import Flask, render_template, url_for, request

# import the dataset here
# SAMPLE: from sklearn.datasets import load_iris

# import the model to be used

app = Flask(__name__)

# index route
@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


# route for accepting images
@app.route("/", methods=["POST"])
def colorize():
    imagefile = request.files['imagefile']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)
    return render_template("index.html")

if __name__ == "___main__":
    # when launching a flask app to production environment make debug false
    # debug = true - so that when we change the file the server will restart itself
    app.run(port = 3000, debug = True)