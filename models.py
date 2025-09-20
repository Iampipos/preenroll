from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    linked_student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=True)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(8), unique=True, nullable=False)  # 8 digits starts 69...
    title = db.Column(db.String(20))
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    school = db.Column(db.String(200))
    email = db.Column(db.String(200))
    program_code = db.Column(db.String(8))
    registrations = db.relationship("RegisteredSubject", back_populates="student")

    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(8), unique=True, nullable=False)  # per spec patterns
    name = db.Column(db.String(200), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(200))
    prereq_code = db.Column(db.String(8), nullable=True)  # subject_code of prereq
    registrations = db.relationship("RegisteredSubject", back_populates="subject")

class SubjectStructure(db.Model):
    __tablename__ = "subject_structures"
    id = db.Column(db.Integer, primary_key=True)
    program_code = db.Column(db.String(8), nullable=False)  # ไม่ขึ้นต้นด้วย 0 ตามโจทย์
    program_name = db.Column(db.String(200), nullable=False)
    dept_name = db.Column(db.String(200))
    required_subject_code = db.Column(db.String(8), nullable=False)
    term = db.Column(db.Integer, nullable=False)  # 1 or 2

class RegisteredSubject(db.Model):
    __tablename__ = "registered_subjects"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    grade = db.Column(db.String(3), nullable=True)  # A,B+,B,...
    student = db.relationship("Student", back_populates="registrations")
    subject = db.relationship("Subject", back_populates="registrations")