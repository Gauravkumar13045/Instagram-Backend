from flask import Blueprint, jsonify, request
from models import db, Post, User
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo
from dotenv import load_dotenv
load_dotenv()


post_bp = Blueprint("post", __name__)

@post_bp.route("/posts", methods=["GET"])
def get_posts():

    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    with open("json/post.json", "r", encoding="utf-8") as file:
        posts = json.load(file)

    return jsonify(posts)


@post_bp.route("/suggestions", methods=["GET"])
def get_suggestion():

    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    with open("json/suggestion.json", "r", encoding="utf-8") as file:
        suggestions = json.load(file)

    return jsonify(suggestions)


@post_bp.route("/upload", methods=["GET"])
def upload_image():

    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Unauthorized"}), 401
    
    
    





