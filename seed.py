from app import create_app
from models import db, Student, Subject, SubjectStructure, RegisteredSubject, User
from werkzeug.security import generate_password_hash
from datetime import date

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # สร้าง students (10 คน)
    students = [
        Student(student_code='69000001', title='ด.ญ.', first_name='อรทัย', last_name='ใจดี', dob=date(2008,3,12), school='โรงเรียนสาธิต', email='orn@example.com', program_code='10000001'),
        Student(student_code='69000002', title='ด.ช.', first_name='กิตติ์', last_name='สุขใจ', dob=date(2007,11,5), school='โรงเรียนกรุงไทย', email='kitt@example.com', program_code='10000001'),
        Student(student_code='69000003', title='น.ส.', first_name='มินตรา', last_name='เปี่ยมสุข', dob=date(2008,2,20), school='โรงเรียนเมือง', email='min@example.com', program_code='10000002'),
        Student(student_code='69000004', title='ด.ช.', first_name='อนันต์', last_name='สุขสันต์', dob=date(2006,7,1), school='โรงเรียนแก้ว', email='anan@example.com', program_code='10000002'),
        Student(student_code='69000005', title='น.ส.', first_name='ช่อทิพย์', last_name='ทองดี', dob=date(2007,5,14), school='โรงเรียนสาธิต', email='chotip@example.com', program_code='10000001'),
        Student(student_code='69000006', title='ด.ช.', first_name='พงษ์', last_name='ศรีสุข', dob=date(2007,9,2), school='โรงเรียนกรุงไทย', email='pong@example.com', program_code='10000002'),
        Student(student_code='69000007', title='ด.ช.', first_name='วุฒิ', last_name='พงศ์', dob=date(2008,4,10), school='โรงเรียนเมือง', email='wut@example.com', program_code='10000001'),
        Student(student_code='69000008', title='น.ส.', first_name='ปรียา', last_name='วิไล', dob=date(2007,12,3), school='โรงเรียนแก้ว', email='priya@example.com', program_code='10000002'),
        Student(student_code='69000009', title='ด.ช.', first_name='ธนภัทร', last_name='มีสุข', dob=date(2006,10,22), school='โรงเรียนสาธิต', email='than@example.com', program_code='10000001'),
        Student(student_code='69000010', title='น.ส.', first_name='อารี', last_name='เกษม', dob=date(2008,1,30), school='โรงเรียนเมือง', email='aree@example.com', program_code='10000002'),
    ]
    db.session.add_all(students)
    db.session.commit()

    # สร้าง subjects >=10
    subjects = [
        Subject(subject_code='05501001', name='คณิตศาสตร์เบื้องต้น 1', credit=3, instructor='ผศ.สมชาย', prereq_code=None),
        Subject(subject_code='05501002', name='คณิตศาสตร์เบื้องต้น 2', credit=3, instructor='ผศ.สมชาย', prereq_code='05501001'),
        Subject(subject_code='05502001', name='ฟิสิกส์เบื้องต้น', credit=3, instructor='รศ.วิทยา', prereq_code=None),
        Subject(subject_code='90690001', name='ภาษาอังกฤษพื้นฐาน', credit=3, instructor='ดร.จินตนา', prereq_code=None),
        Subject(subject_code='90690002', name='การเขียนเชิงวิชาการ', credit=2, instructor='อ.สุดา', prereq_code=None),
        Subject(subject_code='05503001', name='โปรแกรมมิ่งพื้นฐาน', credit=3, instructor='อ.ปกรณ์', prereq_code=None),
        Subject(subject_code='05503002', name='โครงงานเล็ก', credit=2, instructor='อ.ปกรณ์', prereq_code='05503001'),
        Subject(subject_code='05504001', name='ชีววิทยาเบื้องต้น', credit=3, instructor='ผศ.บุษบา', prereq_code=None),
        Subject(subject_code='05505001', name='สังคมศึกษา', credit=2, instructor='อ.สมศรี', prereq_code=None),
        Subject(subject_code='05501003', name='คณิตศาสตร์เพิ่มเติม', credit=2, instructor='ผศ.สมชาย', prereq_code='05501001'),
    ]
    db.session.add_all(subjects)
    db.session.commit()

    # SubjectStructure: 2 หลักสูตร ครอบคลุมเทอม >=3 วิชาต่อเทอม
    ss = [
        SubjectStructure(program_code='10000001', program_name='หลักสูตรวิทยาศาสตรบัณฑิต', dept_name='คณะวิทยาศาสตร์', required_subject_code='05501001', term=1),
        SubjectStructure(program_code='10000001', program_name='หลักสูตรวิทยาศาสตรบัณฑิต', dept_name='คณะวิทยาศาสตร์', required_subject_code='05502001', term=1),
        SubjectStructure(program_code='10000001', program_name='หลักสูตรวิทยาศาสตรบัณฑิต', dept_name='คณะวิทยาศาสตร์', required_subject_code='90690001', term=1),
        SubjectStructure(program_code='10000001', program_name='หลักสูตรวิทยาศาสตรบัณฑิต', dept_name='คณะวิทยาศาสตร์', required_subject_code='05503001', term=2),
        SubjectStructure(program_code='10000001', program_name='หลักสูตรวิทยาศาสตรบัณฑิต', dept_name='คณะวิทยาศาสตร์', required_subject_code='90690002', term=2),
        SubjectStructure(program_code='10000002', program_name='หลักสูตรครุศาสตร์', dept_name='คณะครุศาสตร์', required_subject_code='05501001', term=1),
        SubjectStructure(program_code='10000002', program_name='หลักสูตรครุศาสตร์', dept_name='คณะครุศาสตร์', required_subject_code='05504001', term=1),
        SubjectStructure(program_code='10000002', program_name='หลักสูตรครุศาสตร์', dept_name='คณะครุศาสตร์', required_subject_code='90690001', term=2),
    ]
    db.session.add_all(ss)
    db.session.commit()

    # บางการลงทะเบียน (บางคนมีเกรด)
    r = [
        RegisteredSubject(student_id=students[0].id, subject_id=subjects[0].id, grade='A'),
        RegisteredSubject(student_id=students[0].id, subject_id=subjects[3].id, grade=None),
        RegisteredSubject(student_id=students[1].id, subject_id=subjects[0].id, grade='B+'),
        RegisteredSubject(student_id=students[2].id, subject_id=subjects[1].id, grade=None),
    ]
    db.session.add_all(r)
    db.session.commit()

    # admin user
    admin = User(username='admin', password_hash=generate_password_hash('adminpass'), is_admin=True)
    # create a user account linked to student 1 (student portal)
    u_student = User(username='stu1', password_hash=generate_password_hash('studentpass'), is_admin=False, linked_student_id=students[0].id)
    db.session.add_all([admin, u_student])
    db.session.commit()

    print("Seeding completed.")