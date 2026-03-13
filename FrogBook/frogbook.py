import base64
import io
import math
import random

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
    return render_template('frogbook/index.html')

@bp.route('/top_frogs')
def top_frogs():
    db = get_db()
    frogs = db.execute(
        'SELECT *'
        ' FROM frog f JOIN user u ON f.user_id = u.id'
        ' ORDER BY elo DESC'
    ).fetchmany(size=12)
    return render_template('frogbook/top_frogs.html', frogs=frogs)

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

#get frog by id
def get_frog(id, check_author=True):
    db = get_db()
    #get frog with id
    frog = db.execute(
        'SELECT * from frog WHERE id = ?', (id,)
    ).fetchone()

    #no frog was found
    if frog is None:
        abort(404, f"Frog id {id} doesn't exist.")

    return frog

# Function to calculate the Probability
def probability(rating1, rating2):
    # Calculate and return the expected score
    return 1.0 / (1 + math.pow(10, (rating1 - rating2) / 400.0))

#battle route
@bp.route('/battle', methods=('GET', 'POST'))
@login_required
def battle():
    # get db
    db = get_db()

    if request.method == 'POST':

        print(request.form['winner'])

        winner_id = request.form['winner']
        loser_id = request.form['loser']

        frog1 = request.form['frog1']
        frog2 = request.form['frog2']

        print(winner_id, loser_id)

        winner = get_frog(winner_id)
        loser = get_frog(loser_id)
        get_frog(frog1)
        get_frog(frog2)


        #elo calculation
        winner_elo = winner['elo']
        loser_elo = loser['elo']

        #constant for elo calculation
        K = 30

        winner_elo += int(K * (1 - probability(loser_elo, winner_elo)))
        loser_elo += int(K * (0 - probability(winner_elo, loser_elo)))

        #update winner
        db.execute(
            'UPDATE frog SET elo = ?, wins = ?, battles = ? WHERE id = ?',
            (winner_elo, winner['wins'] + 1, winner['battles'] + 1, winner_id)
        )
        db.commit()

        #update loser
        db.execute(
            'UPDATE frog SET elo = ?, battles = ? WHERE id = ?',
            (loser_elo, loser['battles'] + 1, loser_id)
        )
        db.commit()

        #update user
        db.execute(
            'UPDATE user SET battles = ? WHERE id = ?',
            (g.user['battles'] + 1,g.user['id'])
        )
        db.commit()

        #add battle to the history
        db.execute(
            'INSERT INTO battles (user_id, frog1_id, frog2_id, winner_id) VALUES (?, ?, ?, ?)',
            (g.user['id'], frog1, frog2, winner_id)
        )
        db.commit()

        return redirect(url_for('frogbook.battle'))

    #choose two frog for battle


    #get all frogs not made by the user
    frogs = db.execute(
        'SELECT * FROM frog WHERE user_id != ?', (g.user['id'],)
    ).fetchall()

    #set frog1 and 2
    frog1 = frog2 = None
    #select 2 frogs
    if frogs:
        frog1 = random.choice(frogs)
        frogs.remove(frog1)
    if frogs:
        frog2 = random.choice(frogs)

    return render_template('frogbook/battle.html', frog1=frog1, frog2=frog2)



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


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    frog = get_frog(id)

    #check if loged in user is the creator of the frog
    if(frog['user_id'] != g.user['id']):
        abort(403)
    db = get_db()
    db.execute('DELETE FROM frog WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('frogbook.my_frogs'))


#user history
@bp.route('/history')
@login_required
def user_history():
    db = get_db()
    battles = db.execute(
        'SELECT * FROM battles WHERE user_id = ? ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()

    history = []
    for battle in battles:
        frog1 = get_frog(battle['frog1_id'])
        frog2 = get_frog(battle['frog2_id'])
        history.append({
            'battle': battle,
            'frog1': frog1,
            'frog2': frog2
        })

    return render_template('frogbook/user_history.html', history=history)

#frog history
@bp.route('/<int:id>/history')
@login_required
def frog_history(id):
    db = get_db()

    frog = get_frog(id)

    battles = db.execute(
        'SELECT * from battles where frog1_id = ? OR frog2_id = ? ORDER BY created DESC',
        (id,id)
    ).fetchall()

    history = []
    for battle in battles:
        frog1 = get_frog(battle['frog1_id'])
        frog2 = get_frog(battle['frog2_id'])

        #gets the evil frog
        evil_frog = get_frog(frog2['id'] if frog['id'] == frog1['id'] else frog1['id'])

        history.append({
            'battle': battle,
            'evil_frog': evil_frog
        })

    return render_template('frogbook/frog_history.html', history=history, frog=frog)