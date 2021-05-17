from module.Zipfile import Zipfile
import os

from flask import Flask, request, redirect, jsonify
from flask_restplus import Api, fields, Resource, model
import werkzeug

app = Flask(__name__)
api = Api(app, title="BNB API",
          version="unknown",
          doc='/api/doc/',
          base_url='/')

app.config['SECRET_KEY'] = 'secret'
UPLOAD_EXTENSIONS = [".zip"]
UPLOADS = os.path.join(os.getcwd(),"..","uploads")

def is_vaild_file(filename):
    return(filename and
           "." in filename and 
           ("." + filename.split(".")[-1]) in UPLOAD_EXTENSIONS
           )

file_data = api.model("file data",
                        {
                            "username":
                              fields.String(
                                description="the folder name associated with this user",
                                Required=True
                              ),
                              "filename":
                                fields.String(
                                  description="the files name",
                                  Required=True
                                )
                        })

user_data = api.model("user data",
                        {
                            "username":
                              fields.String(
                                description="the folder name associated with this user",
                                Required=True
                              ),
                        })

@api.route('/file_upload/')
class upload(Resource):
  @api.expect(file_data)
  def post(self): #might need to be post
    data = request.get_json()
    username = data.get("username")
    filename = data.get("filename")
    rfile = data.get("file")

    if username in None or filename is None:
      return None, 400

    username = werkzeug.secure_filename(username)
    filename = werkzeug.secure_filename(filename)

    userpath = os.path.join(UPLOADS, username)
    if not os.path.exists(userpath):
      os.mkdir(userpath)

    filepath = os.path.join(userpath, filename)
    if os.path.exists(filepath):
      os.remove(filepath)

    with open(filepath, "+wb") as f:
      rfile.save(f)

    return "Saved successfully", 200


@api.route('/file_get_report')
class report(Resource):
  @api.expect(file_data)
  def get(self):
    username = request.args.get("username")
    filename = request.args.get("filename")

    if username in None or filename is None:
      return None, 400

    username = werkzeug.secure_filename(username)
    filename = werkzeug.secure_filename(filename)

    userpath = os.path.join(UPLOADS, username)
    if not os.path.exists(userpath):
      return "USER NOT FOUND", 404

    filepath = os.path.join(userpath, filename)
    if not os.path.exists(filepath):
      return "FILE NOT FOUND", 404

    if not is_vaild_file(filename):
      return "BAD FILE NAME"

    zf = Zipfile.Zipfile(filepath)

    return jsonify(zf.to_json()), 200   


@api.route('/user_file_list/')
class FileList(Resource):
  @api.expect(user_data)
  def get(self):
    user = werkzeug.secure_filename(request.arg.get("username"))

    defualt_files = [{"id" : 0, "name" : "----------------No File Selected----------------"}]
    if not os.path.exists(os.path.join(UPLOADS,user)): print(5); return jsonify({"files": defualt_files})
    return jsonify({
        "files" : defualt_files + [{"id" : i+1, "name" : f}for i, f in enumerate(os.listdir(os.path.join(UPLOADS,user)))]
        })


