from flask import Flask,request,jsonify
from flask_cors import CORS
from models import db
from config import Config
from routes.auth import auth
from post import post_bp



app = Flask(__name__)

app.config.from_object(Config)

CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://kz9sppkz-5173.inc1.devtunnels.ms"],
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"],
    expose_headers=["Set-Cookie"]
)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(post_bp)



@app.route("/")
def home():
    return "Backend is running 🚀"



if __name__ == "__main__":
    app.run(debug=True)































# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins="*")   

# @app.route("/login", methods=["POST"])
# def login():
#     try:
#         data = request.get_json()
#         username = data.get("username")
#         password = data.get("password")

#         if username == "Admin123" and password == "qwerty123":
#             return jsonify({"status": "success"}), 200
#         else:
#             return jsonify({"status": "fail", "message": "Invalid credentials"}), 401
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route("/")
# def home():
#     return "Flask Backend is Running Successfully!"

# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0", port=5000)