from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            # Se não for admin, redireciona para uma página de erro ou página inicial
            return redirect(url_for('home'))  # Ou redirecionar para outra página
        return f(*args, **kwargs)
    return decorated_function

