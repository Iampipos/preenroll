from flask import Blueprint, render_template, request, redirect, url_for, flash
from helpers import login_required, admin_required
from models import db, Student, Subject, RegisteredSubject

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/students')
@admin_required
def admin_students():
    q = request.args.get('q','')
    school = request.args.get('school','')
    order = request.args.get('order','name')
    query = Student.query
    if q:
        q_like = f"%{q}%"
        query = query.filter((Student.first_name.ilike(q_like)) | (Student.last_name.ilike(q_like)) | (Student.student_code.ilike(q_like)))
    if school:
        query = query.filter_by(school=school)
    students = query.all()
    if order == 'age':
        students.sort(key=lambda s: s.age())
    else:
        students.sort(key=lambda s: s.first_name)
    return render_template('admin_students.html', students=students)

@bp.route('/grades/<int:subject_id>', methods=['GET','POST'])
@admin_required
def grade_entry(subject_id):
    subj = Subject.query.get_or_404(subject_id)
    regs = RegisteredSubject.query.filter_by(subject_id=subj.id).all()
    if request.method == 'POST':
        # for each registration set grade
        allowed = ['A','B+','B','C+','C','D+','D','F','']
        for reg in regs:
            g = request.form.get(f'grade_{reg.id}','').strip()
            if g == '':
                reg.grade = None
            elif g in allowed:
                reg.grade = g
            else:
                flash("ค่าหมายเกรดไม่ถูกต้อง")
                return redirect(url_for('admin.grade_entry', subject_id=subj.id))
        db.session.commit()
        flash("บันทึกเกรดเรียบร้อย")
        return redirect(url_for('admin.grade_entry', subject_id=subj.id))
    return render_template('grade_entry.html', subject=subj, regs=regs)