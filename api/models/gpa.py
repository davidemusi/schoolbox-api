from ..utils import db

class GPA(db.Model):
    __tablename__ = 'gpa'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    grade_id = db.Column(db.Integer(), db.ForeignKey('grades.id'))
    student = db.relationship('Student', backref=db.backref('student_gpa', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('course_gpa', lazy='dynamic'))
    student_grade = db.relationship('Grade', backref=db.backref('grade_gpa', lazy='dynamic'))

    def __init__(self, student_id, course_id, grade_id):
        self.student_id = student_id
        self.course_id = course_id
        self.grade_id = grade_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'GPA: {self.id}'
    

def get_student_grade(score):
    """Converts the score to a letter grade."""
    if score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'
    
def convert_student_grade_to_gpa(grade):
    """Converts the letter grade to a gpa."""
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.0
    elif grade == 'C':
        return 2.0
    elif grade == 'D':
        return 1.0
    else:
        return 0.0
