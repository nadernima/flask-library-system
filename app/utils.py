from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles and not (current_user.is_admin() and "admin" in roles):
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator
