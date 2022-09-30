from flask import (Blueprint, render_template)

from werkzeug.exceptions import abort
from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<string:username>')
def profile(username):
    user = get_user(username)
    return render_template('user/profile.html', user=user)


def get_user(username):
    user = get_db().execute(
        'SELECT id, username FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        abort(404, "User not found")

    return user
