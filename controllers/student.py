from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from helpers import login_required
from models import db, Student, Subject, RegisteredSubject, SubjectStructure

bp = Blueprint('student', __name__, url_prefix='/student')

def has_passed_prereq(student, subject):
    if not subject.prereq_code:
        return True
    prereq = Subject.query.filter_by(subject_code=subject.prereq_code).first()
    if not prereq:
        return True
    rec = RegisteredSubject.query.filter_by(student_id=student.id, subject_id=prereq.id).first()
    if not rec or rec.grade is None:
        return False
    return rec.grade != 'F'  # ถือว่าผ่านถ้าไม่ F

@bp.route('/<int:student_id>')
@login_required
def profile(student_id):
    # นักเรียนต้องดูของตัวเอง หรือ admin จะดูได้ (admin check เป็นที่-level route)
    if session.get('student_id') != student_id and not session.get('is_admin'):
        flash("ไม่สามารถดูข้อมูลนักเรียนคนอื่นได้")
        return redirect(url_for('auth.login'))
    student = Student.query.get_or_404(student_id)
    return render_template('student_profile.html', student=student)

@bp.route('/<int:student_id>/register', methods=['GET','POST'])
@login_required
def register_view(student_id):
    if session.get('student_id') != student_id and not session.get('is_admin'):
        flash("ไม่สามารถจัดการข้อมูลนักเรียนคนอื่นได้")
        return redirect(url_for('auth.login'))
    student = Student.query.get_or_404(student_id)
    # หา subject ในหลักสูตรปี1 ที่ยังไม่ได้ลง
    required_codes = [s.required_subject_code for s in SubjectStructure.query.filter_by(program_code=student.program_code).all()]
    subjects = Subject.query.filter(Subject.subject_code.in_(required_codes)).all()
    # filter out already registered
    registered_subject_ids = {r.subject_id for r in student.registrations}
    available = [s for s in subjects if s.id not in registered_subject_ids]
    if request.method == 'POST':
        subj_id = int(request.form['subject_id'])
        subj = Subject.query.get_or_404(subj_id)
        # business rule: age >= 15
        if student.age() < 15:
            flash("นักเรียนต้องมีอายุอย่างน้อย 15 ปี")
            return redirect(url_for('student.profile', student_id=student.id))
        # prereq
        if not has_passed_prereq(student, subj):
            flash(f"ไม่ผ่านเงื่อนไขวิชาบังคับก่อน: {subj.prereq_code}")
            return redirect(url_for('student.register_view', student_id=student.id))
        # create registration
        new = RegisteredSubject(student_id=student.id, subject_id=subj.id)
        db.session.add(new)
        db.session.commit()
        flash("ลงทะเบียนสำเร็จ")
        return redirect(url_for('student.profile', student_id=student.id))
    # ตัด subjects ตาม term หรืออื่นๆ ได้ตามต้องการ
    return render_template('register_subjects.html', student=student, subjects=available)