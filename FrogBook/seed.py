import base64
import io
import os
import click

from PIL import Image
from faker import Faker

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from FrogBook.auth import login_required
from FrogBook.db import get_db


@click.command()
def seed_database():
    fake = Faker()
    #create fake user
    db = get_db()

    db.execute(
        'DELETE from user'
    )
    db.commit()

    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        ('ADMIN', generate_password_hash('root'))
    )
    db.commit()

    path = os.path.join(os.path.dirname(__file__), '..', 'downloaded_frogs')

    #get all images
    for img in os.listdir(path):
        if(img.endswith('.jpg')):
            image = Image.open(os.path.join(path, img))
            image.thumbnail((500,500))
            mime = 'image/jpeg'
            buffer = io.BytesIO()
            image.save(buffer, format=image.format)
            image = buffer.getvalue()
            image = base64.b64encode(image)
            image = 'data:' + mime + ';base64,' + str(image)[2:-1]
            db.execute(
                'INSERT INTO frog (name, user_id, img, elo) VALUES (?, ?, ?, ?)',
                (fake.first_name(), 1, image, 1000)
            )
            db.commit()

    click.secho('Seeded the database!', fg='green')