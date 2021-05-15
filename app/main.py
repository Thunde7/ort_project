from logging import error
from typing import final
from flask import Flask, render_template, request
import os
from shutil import ExecError, rmtree
from werkzeug.utils import redirect, secure_filename

import Zipfile

app = Flask(__name__)


UPLOAD_EXTENSIONS = [".zip"]
UPLOADS = os.path.join(os.getcwd(),"..","uploads")

def is_vaild_file(filename):
    return(filename and
           "." in filename and 
           ("." + filename.split(".")[-1]) in UPLOAD_EXTENSIONS
           )

try:
    rmtree(UPLOADS)
finally:
    os.mkdir(UPLOADS)

app.config["UPLOAD_PATH"] = UPLOADS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload/", methods=["POST","GET"])
def upload_file():
    if request.method == "POST":
        print(555555555)
        try:
            user_file = request.files["file"]
            username = request.args.get("username")
            
            assert is_vaild_file(user_file)

            user_file.save(os.path.join(UPLOADS,username,secure_filename(user_file.filename)))
            redirect("/results/")

        except Exception:
            return render_template("error_occurred.html"), 400

    else:
        return render_template("upload.html"), 200

@app.route("/results/", methods=["GET"])
def get_results():
    username = request.args.get("username")

    file_list = get_file_list()

    display_file_list(file_list)

    chosen = get_chosen_file()

    zf = Zipfile.Zipfile(chosen)






@app.route("/error_occurred/", methods=["GET"])
def display_error():
    render_template("error_occurred.html")