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






