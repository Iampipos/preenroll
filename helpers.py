from functools import wraps
from flask import session, redirect, url_for, flash
from models import User

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("กรุณาเข้าสู่ระบบก่อน")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            flash("ต้องเป็นผู้ดูแลระบบ (admin) เท่านั้น")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper