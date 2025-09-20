from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Student

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['is_admin'] = bool(user.is_admin)
            session['student_id'] = user.linked_student_id
            flash("ยินดีต้อนรับ " + username)
            # redirect to admin start or student profile
            if user.is_admin:
                return redirect(url_for('admin.admin_students'))
            elif user.linked_student_id:
                return redirect(url_for('student.profile', student_id=user.linked_student_id))
            else:
                return redirect(url_for('auth.login'))
        else:
            flash("ชื่อผู้ใช้หรือรหัสผ่านผิด")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash("ออกจากระบบเรียบร้อย")
    return redirect(url_for('auth.login'))