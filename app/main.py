import shutil
from flask import Flask, render_template, request, redirect 
import os
from shutil import ExecError, rmtree
from flask.json import jsonify
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms.fields import SelectField
#import Zipfile

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
UPLOAD_EXTENSIONS = [".zip"]
UPLOADS = os.path.join(os.getcwd(),"..","uploads")

def is_vaild_file(filename):
    return(filename and
           "." in filename and 
           ("." + filename.split(".")[-1]) in UPLOAD_EXTENSIONS
           )

# try:
#     rmtree(UPLOADS)
# finally:
#     os.mkdir(UPLOADS)

app.config["UPLOAD_PATH"] = UPLOADS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload/", methods=["POST","GET"])
def upload_file():
    if request.method == "POST":
        try:
            user_file = request.files["file"]
            username = "aa"#request.args.get("username")
            
            assert is_vaild_file(user_file.filename)

            if not os.path.exists(os.path.join(UPLOADS,username)):
                os.mkdir(os.path.join(UPLOADS,username))

            if os.path.exists(os.path.join(UPLOADS,username,user_file.filename)):
                os.remove(os.path.join(UPLOADS,username,user_file.filename))

            with open(os.path.join(UPLOADS,username,secure_filename(user_file.filename)), "+wb") as f:
                user_file.save(f)
            return render_template("success.html")

        except Exception as e:
            print(e)
            return render_template("error_occurred.html"), 400

    else:
        return render_template("upload.html"), 200

class Form(FlaskForm):
    files = SelectField("File",choices=[(0, "----------------No File Selected----------------")])

@app.route("/results/", methods=["GET", "POST"])
def results():
    form = Form()
    form.files.choices = []

    if request.method == "POST":
        return f"<h1>{form.username.value}/{form.files.name}</h1>"

    return render_template("results.html",form=form)


@app.route("/user_files/<user>")
def get_files(user):
    defualt_files = [{"id" : 0, "name" : "----------------No File Selected----------------"}]
    if not os.path.exists(os.path.join(UPLOADS,user)): print(5); return jsonify({"files": defualt_files})
    return jsonify({
        "files" : defualt_files + [{"id" : i+1, "name" : f}for i, f in enumerate(os.listdir(os.path.join(UPLOADS,user)))]
        })




@app.route("/error_occurred/", methods=["GET"])
def display_error():
    return render_template("error_occurred.html")