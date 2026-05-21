from flask import request,jsonify, Blueprint, current_app,make_response
from models import db, User
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random



auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "All fields required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username taken"}), 400
    
    avatar = f"https://picsum.photos/id/{random.randint(1,1084)}/200/200"
    
    
    user = User(
        email=email,
        username=username,
        full_name=data.get("fullName"),
        password=generate_password_hash(password), 
        birthday=data.get("birthday"),
        avatar=avatar
    )

    db.session.add(user)
    db.session.commit()

    print("Data Received")

    return jsonify({
        "message": "Account created Successfully!! ",
        "user": {
            "username": user.username,
            "email": user.email,
            "fullName": user.full_name,
            "avatar": user.avatar
        }
    })


@auth.route("/signin", methods=["POST"])
def signin():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
     return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter((User.email == email) | (User.username == email)).first()

    if not user:
     return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, password):
     return jsonify({"error": "Wrong password"}), 400
    
    token = jwt.encode( 
       
       {
       "user_id": user.id,
       "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    },
    current_app.config["SECRET_KEY"],
    algorithm="HS256"
    )

    if isinstance(token, bytes):
     token = token.decode("utf-8")

    response = make_response(jsonify({"message": "Login Successful"}))
    response.set_cookie(
        "token", 
        token,
        httponly=True,
        samesite="None",     
        secure=True,        
        path="/",
        max_age=60*60*24  
    )

    
    return response

@auth.route("/profile", methods=["GET"])
def profile():
    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Not logged in"}), 401

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

        user = User.query.get(data["user_id"])

        return jsonify({
            "username": user.username,
            "email": user.email,
            "fullName": user.full_name,
            "avatar": user.avatar          

        })

    except:
        return jsonify({"error": "Invalid or expired token"}), 401


@auth.route('/logout', methods=["POST"])
def logout():

    response = make_response(
        jsonify({"message": "Logged Out Successfully"})
    )

    response.delete_cookie(
        "token",
        path="/",
        samesite="None",
        secure=True
    )

    return response
   
   
   
   


       


         







    