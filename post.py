from flask import Blueprint, jsonify, request, current_app
from models import db, Post, User
import json
import os
import jwt
import humanize
from datetime import datetime
import random
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo
from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


post_bp = Blueprint("post", __name__)

@post_bp.route("/posts", methods=["GET"])
def get_posts():

    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    posts = Post.query.filter(
    Post.user_id.isnot(None)
).order_by(
    Post.created_at.desc()
).all()

    return jsonify({
        "posts": [
            {
                "id": post.id,

                "username": post.user.username,

                "displayName": post.user.display_name,

                "avatar": post.user.avatar,

                "isVerified": post.user.is_verified,

                "postImage": post.image_url,

                "caption": post.caption,

                "likes": random.randint(100, 900),

                "comments": random.randint(10, 500),

                "timeAgo": humanize.naturaltime(datetime.utcnow() - post.created_at)
            }

            for post in posts
        ]
    })


@post_bp.route("/suggestions", methods=["GET"])
def get_suggestion():

    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    with open("json/suggestion.json", "r", encoding="utf-8") as file:
        suggestions = json.load(file)

    return jsonify(suggestions)

@post_bp.route("/upload", methods=["POST"])
def upload_image():

    token = request.cookies.get("token")

    if not token:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    image = request.files.get("image")

    caption = request.form.get("caption")

    if not image:
        return jsonify({
            "error": "No image uploaded"
        }), 400

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/jpg"
    ]

    if image.content_type not in allowed_types:

        return jsonify({
            "error": "Invalid image type"
        }), 400

    try:

        decoded = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

        user_id = decoded["user_id"]

        upload_result = cloudinary.uploader.upload(
            image,
            folder="instagram_posts"
        )

        image_url = upload_result["secure_url"]

        public_id = upload_result["public_id"]

        new_post = Post(
            image_url=image_url,
            public_id=public_id,
            caption=caption,
            user_id=user_id,
            likes=random.randint(100, 900),
            comments=random.randint(10, 500)
        )

        db.session.add(new_post)

        db.session.commit()

        return jsonify({
            "message": "Post uploaded successfully",
            "image_url": image_url
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500