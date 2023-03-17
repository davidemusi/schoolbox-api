from ..utils import db
from enum import Enum
from datetime import datetime


class courseStatus(Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    DELETED = 'Deleted'

class Course(db.Model):
    __tablename__='courses'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    teacher = db.Column(db.String(), nullable=False)
    course_status = db.Column(db.Enum(courseStatus), default=courseStatus.ACTIVE)
    credit_hours = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    enrollee = db.Column(db.Integer(), db.ForeignKey('students.id'))
    grades = db.relationship('Grade', backref='id_of_course', lazy=True)
    gpa = db.relationship('GPA', backref='id_of_course', lazy=True)


    def __repr__(self):
        return f"<Course {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(model, id):
        return model.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
