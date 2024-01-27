from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

def confirmation_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            return redirect(url_for('account_unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function