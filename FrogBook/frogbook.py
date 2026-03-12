import base64
import io

from PIL import Image

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from FrogBook.auth import login_required
from FrogBook.db import get_db

bp = Blueprint('frogbook', __name__)


@bp.route('/')
def index():
    db = get_db()
    frogs = db.execute(
        'SELECT *'
        ' FROM frog f JOIN user u ON f.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('frogbook/index.html', frogs=frogs)

@bp.route('/my_frogs')
@login_required
def my_frogs():
    db = get_db()
    frogs = db.execute(
        'SELECT *'
        ' FROM frog f JOIN user u ON f.user_id = u.id'
        ' WHERE f.user_id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('frogbook/user_frogs.html', frogs=frogs)

#allowed file
def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    allowed_extensions = ['png','jpg', 'jpeg']
    if request.method == 'POST':
        #set error to none
        error = None
        name = request.form['name']
        image = request.files['image']

        if not name:
            error = 'Name is required.'

        if not image or image.filename == '':
            error = 'Image is required.'
        elif not allowed_file(image.filename, allowed_extensions):
            error = 'Image extension is not allowed.'

        if error is not None:
            flash(error)
        else:
            img = Image.open(image)
            img.thumbnail((500,500))

            mime = image.mimetype
            buffer = io.BytesIO()
            img.save(buffer, format=img.format)
            image = buffer.getvalue()
            image = base64.b64encode(image)
            image = 'data:' + mime + ';base64,' + str(image)[2:-1]
            db = get_db()
            db.execute(
                'INSERT INTO frog (name, user_id, img) VALUES (?, ?, ?)',
                (name, g.user['id'], image)
            )
            db.commit()
            return redirect(url_for('frogbook.index'))

    return render_template('frogbook/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('frogbook.index'))

    return render_template('frogbook/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('frogbook.index'))
