from repo.Zipfile import Zipfile
import os

from hashlib import md5
from flask import Flask, request, redirect, jsonify, json
from flask_restplus import Api, fields, Resource, model
import werkzeug
import jwt

app = Flask(__name__)
api = Api(app, title="BNB API",
          version="unknown",
          doc='/api/doc/',
          base_url='/')

secret = "secret"

app.config['SECRET_KEY'] = 'secret'
USER_DB = os.path.join("repo", "DB", "users.json")
UPLOAD_EXTENSIONS = [".zip"]
UPLOADS = os.path.join(os.getcwd(), "../..", "uploads")


def create_jwt(username, password):
    return jwt.encode(payload={"username": username, "password": password}, key=secret, algorithm="HS256").decode('utf-8')


def check_jwt(token):
    try:
        jwt_dic = jwt.decode(token, key=secret)
        username = jwt_dic["username"]
        password = jwt_dic["password"]

    except Exception:
        return False

    with open(USER_DB, "r") as db:
        users = json.load(db)["users"]
        if username not in users or users[username] != md5(password.encode("utf-8")).hexdigest():
            return False

    return True


def is_vaild_file(filename):
    return(filename and
           "." in filename and
           ("." + filename.split(".")[-1]) in UPLOAD_EXTENSIONS
           )


file_data = api.model("file data",
                      {
                          "username":
                          fields.String(
                              description="The folder name associated with this user",
                              Required=True
                          ),
                          "filename":
                          fields.String(
                              description="The files name",
                              Required=True
                          ),
                      })

user_data = api.model("user data",
                      {
                          "username":
                          fields.String(
                              description="The user's name",
                              Required=True
                          ),
                          "password":
                          fields.String(
                              description="The user's password",
                              Required=True
                          )
                      })

authed_user_data = api.model("authed user data",
                             {
                                 "username":
                                 fields.String(
                                     description="The folder name associated with this user",
                                     Required=True
                                 )
                             })

@api.route('/token/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class Token(Resource):
    def get(self):
        if not check_jwt(request.headers.get("Auth")):
            return None, 401
        return [], 200
@api.route('/file_upload/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class upload(Resource):
    @api.expect(file_data)
    def post(self):
        print(request.json)
        if not check_jwt(request.headers.get("Auth")):
            return None, 401

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

        if not is_vaild_file(filename):
            return None, 401

        filepath = os.path.join(userpath, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

        with open(filepath, "+wb") as f:
            rfile.save(f)

        return ["Saved successfully"], 200


@api.route('/file_get_report')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
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
            return None, 404

        filepath = os.path.join(userpath, filename)
        if not os.path.exists(filepath):
            return None, 404

        if not is_vaild_file(filename):
            return None, 401

        zf = Zipfile.Zipfile(filepath)

        return jsonify(zf.to_json()), 200


@api.route('/user_file_list/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class FileList(Resource):
    @api.expect(authed_user_data)
    def get(self):
        print(request)
        if not check_jwt(request.headers.get("Auth")):
            return None, 401
        user = werkzeug.secure_filename(request.args.get("username"))

        defualt_files = [
            {"id": 0, "name": "----------------No File Selected----------------"}]
        if not os.path.exists(os.path.join(UPLOADS, user)):
            print(5)
            return jsonify({"files": defualt_files})
        return jsonify({
            "files": defualt_files + [{"id": i+1, "name": f}for i, f in enumerate(os.listdir(os.path.join(UPLOADS, user)))]
        })


@api.route('/login/')
class Login(Resource):
    @api.expect(user_data)
    def post(self):
        print(request.json)
        data = request.get_json()
        username = werkzeug.secure_filename(data.get("username"))
        password = data.get("password")

        with open(USER_DB, "r") as db:
            users = json.load(db)["users"]
            if username not in users:
                return "USER DOES NOT EXIST", 404
            if users[username] != md5(password.encode("utf-8")).hexdigest():
                return "WRONG PASSWORD", 401
        return [{"Auth": create_jwt(username, password)}], 200


@api.route("/signup/")
class SignUp(Resource):
    @api.expect(user_data)
    def post(self):
        data = request.get_json()
        username = werkzeug.secure_filename(data.get("username"))
        password = data.get("password")
        with open(USER_DB, "r") as db:
            users = json.load(db)["users"]
            if username in users:
                return "USER ALREADY EXISTS", 401
            users[username] = md5(password.encode("utf-8")).hexdigest()
            json.load(db)["users"]

        os.mkdir(os.path.join(UPLOADS, username))

        return [{"Auth" : create_jwt(username, password)}], 200
