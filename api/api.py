from re import I
from repo.Zipfile import Zipfile
import os

from hashlib import md5
from flask import Flask, request, redirect, jsonify, json
from flask_restplus import Api, fields, Resource, model
from flask_cors import CORS
import werkzeug
import base64
from datetime import date
import jwt

app = Flask(__name__)
api = Api(app, title="BNB API",
          version="1.0.0.26",
          doc='/api/doc/',
          base_url='/')
CORS(app)

secret = "secret"

app.config['SECRET_KEY'] = 'secret'
USER_DB = os.path.join("DB", "users.json")
UPLOAD_EXTENSIONS = [".zip"]
UPLOADS = os.path.join(os.getcwd(), "uploads")


def create_jwt(username, password):
    return jwt.encode(payload={"username": username, "password": password}, key=secret, algorithm="HS256").decode('utf-8')


def check_jwt(token, username):
    try:
        jwt_dic = jwt.decode(token, key=secret)
        jwt_username = jwt_dic["username"]
        password = jwt_dic["password"]

        if jwt_username != werkzeug.secure_filename(username):
            return False

    except Exception:
        return False

    with open(USER_DB, "r") as db:
        users = json.load(db)["users"]
        print(users[jwt_username])
        if jwt_username not in users or users[jwt_username]["password"] != md5(password.encode("utf-8")).hexdigest():
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
                          ),
                          "filename":
                          fields.String(
                              description="The files name",
                              Required=True
                          ),
                          "file":
                          fields.String(
                              description="The file encoded in base64",
                              Required=True
                          )
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

signup_data = api.model("sign up data",
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
                          ),
                         "firstname":
                          fields.String(
                              description="The user's first name",
                              Required=True
                          ),
                          "lastname":
                          fields.String(
                              description="The user's last name",
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
    @api.expect(authed_user_data)
    def get(self):
        if not check_jwt(request.headers.get("Auth"),request.args.get("username")):
            return None, 401
        return [], 200


@api.route('/file-upload/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class Upload(Resource):
    @api.expect(file_data)
    def post(self):
        #print(request.json["data"])
        data = request.get_json()["data"]

        if not check_jwt(request.headers.get("Auth"), data["username"]):
            return None, 401

        username = data.get("username")
        filename = data.get("filename")
        rfile = data.get("file")

        if None in {username, filename, rfile}:
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

        file_data = base64.b64decode(rfile)[27:]

        with open(USER_DB, "r") as db:
            data = json.loads(db.read())
        data["files"][username].append({"name": filename, "date": str(date.today())})

        with open(USER_DB,"w") as db:
            db.write(json.dumps(data, indent=2))

        with open(filepath, "wb") as f:
            f.write(file_data)

        return ["Saved successfully"], 200

@api.route('/latest-file/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class Latest(Resource):
    @api.expect(authed_user_data)
    def get(self):
        if not check_jwt(request.headers.get("Auth"),request.args.get("username")):
            return None, 401
        
        username = request.args.get("username")

        if username is None:
            return None, 400

        username =werkzeug.secure_filename(username)

        with open(USER_DB, "r") as db:
            files = json.load(db)["files"][username]
            print(files)
            latest = sorted(files,key=lambda f : f["date"], reverse=True)[0]

        print(latest)
        return [latest], 200

@api.route('/file-get-report/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class Report(Resource):
    @api.expect(file_data)
    def get(self):
        if not check_jwt(request.headers.get("Auth"),request.args.get("username")):
            return None, 401

        username = request.args.get("username")
        filename = request.args.get("filename")

        if username is None or filename is None:
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

        zf = Zipfile(filepath)

        return [(zf.to_dict())], 200


@api.route('/user-file-list/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class FileList(Resource):
    @api.expect(authed_user_data)
    def get(self):
        print(request)
        if not check_jwt(request.headers.get("Auth"), request.args.get("username")):
            return None, 401
        user = werkzeug.secure_filename(request.args.get("username"))

        if not os.path.exists(os.path.join(UPLOADS, user)):
            return jsonify({"files": []})
        return jsonify({
            "files": [{"id": i+1, "name": f} for i, f in enumerate(os.listdir(os.path.join(UPLOADS, user)))]
        })


@api.route('/file-data-list/')
@api.doc(params={'Auth': {'in': 'header', 'description': 'jwt token'}})
class FileDataList(Resource):
    @api.expect(authed_user_data)
    def get(self):
        print(request)
        if not check_jwt(request.headers.get("Auth"), request.args.get("username")):
            return None, 401
        user = werkzeug.secure_filename(request.args.get("username"))

        if not os.path.exists(os.path.join(UPLOADS, user)):
            return jsonify({"files": []})
        return jsonify({
            "files": [{"id": i+1, "name": f, "metadata": Zipfile(os.path.join(UPLOADS,user,f)).to_dict()} for i, f in enumerate(os.listdir(os.path.join(UPLOADS, user)))]
        })

@api.route('/login/')
class Login(Resource):
    @api.expect(user_data)
    def post(self):
        print(request.json)
        data = request.get_json()["data"]
        username = data.get("username")
        password = data.get("password")

        if username is None or password is None:
            return None, 401

        username = werkzeug.secure_filename(username)

        with open(USER_DB, "r") as db:
            users = json.load(db)["users"]
            if username not in users:
                return "USER DOES NOT EXIST", 404
            if users[username]["password"] != md5(password.encode("utf-8")).hexdigest():
                return "WRONG USERNAME OR PASSWORD", 401
        return [{"Auth": create_jwt(username, password)}], 200


@api.route("/signup/")
class Signup(Resource):
    @api.expect(signup_data)
    def post(self):
        print(request.json)
        data = request.get_json()['data']
        username = data.get("username")
        password = data.get("password")
        firstname = data.get("firstname")
        lastname = data.get("lastname")

        print(request)

        if None in {username, password, firstname, lastname}:
            return None, 403

        username = werkzeug.secure_filename(username)

        with open(USER_DB, "r") as db:
            data = json.loads(db.read())
        if username in data["users"]:
            return "USER ALREADY EXISTS", 401
        data["users"][username] = {"password" : md5(password.encode("utf-8")).hexdigest(),
                                   "firstname" : firstname, "lastname": lastname }
        data["files"][username] = []
        with open(USER_DB,"w") as db:
            db.write(json.dumps(data, indent=2))

        os.mkdir(os.path.join(UPLOADS, username))

        return [{"Auth" : create_jwt(username, password)}], 200
