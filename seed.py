from app import app
from models import db, User, Post
import json
import random

with app.app_context():

    
    with open("json/post.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    posts = data["posts"]

    for item in posts:

        
        existing_user = User.query.filter_by(
            username=item["username"]
        ).first()

       
        if not existing_user:

            new_user = User(

                username=item["username"],

                full_name=item["displayName"],

                display_name=item["displayName"],

                avatar=item["avatar"],

                is_verified=item["isVerified"],

                email=f'{item["username"]}@gmail.com',

                password="12345678",

                birthday="2000-01-01"
            )

            db.session.add(new_user)
            db.session.commit()

            existing_user = new_user

        
        new_post = Post(

            image_url=item["postImage"],

            caption=item["caption"],

            likes=random.randint(10, 500),

            comments=random.randint(1, 80),

            user_id=existing_user.id
        )

        db.session.add(new_post)

    db.session.commit()

    print("✅ Database seeded successfully")