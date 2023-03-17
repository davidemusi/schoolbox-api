from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
from ..models.students import Student, StudentCourse
from ..models.grades import Grade
from ..models.grades import Score
from ..models.gpa import GPA, convert_student_grade_to_gpa, get_student_grade
from http import HTTPStatus
from ..utils import db
from flask_jwt_extended import jwt_required, get_jwt_identity

student_namespace = Namespace('students', description='Student related operations')

student_model = student_namespace.model('Student', {
    'id': fields.Integer(required=True, description='Student id'),
    'username': fields.String(required=True, description='Student username'),
    'email': fields.String(required=True, description='Student email'),
    'courses': fields.List(fields.Nested(student_namespace.model('Course', {
        'id': fields.Integer(required=True, description='Course id'),
        'name': fields.String(required=True, description='Course name'),
        'teacher': fields.String(required=True, description='Course teacher'),
    })))
})

@student_namespace.route('/students')
class StudentList(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Get all students'
    )
    @jwt_required()
    def get(self):
        """
            Get all students
        """
        students = Student.query.all()  
        return students, HTTPStatus.OK

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Register a new student'
    )
    @jwt_required()
    def post(self):
        """
            Register a new student
        """

        username = get_jwt_identity()


        current_student = Student.query.filter_by(username=username).first()

        data = student_namespace.payload

        new_student = Student(
            username = data['username'],
            email = data['email'],
        )

        new_student.student = current_student

        new_student.save()

        return new_student, HTTPStatus.CREATED
    

@student_namespace.route('/students/<int:student_id>')
class GetUpdateDelete(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Retrieve a student by id',
        params = {
            'student_id': 'An ID for a student'
        }
    )

    @jwt_required()
    def get(self, student_id):
        """
            Retrieve a student by id
        """
        student = Student.get_by_id(student_id)

        return student, HTTPStatus.OK

    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Update a student by id',
        params = {
            'student_id': 'An ID for a student'
        }
    )
    @jwt_required()
    def put(self, student_id):
        """
            Update a student by id
        """
        student_to_update = Student.get_by_id(student_id)

        data = student_namespace.payload

        student_to_update.username = data["username"]
        student_to_update.email = data["email"]

        db.session.commit()

        return student_to_update, HTTPStatus.OK

    @student_namespace.doc(
        description='Delete a student by id',
        params = {
            'student_id': 'An ID for a student'
        }
    )
    @jwt_required()
    def delete(self, student_id):
        """
            Delete a student by id
        """

        student_to_delete = Student.get_by_id(student_id)

        student_to_delete.delete()

        return {"message": "Deleted Successfully"}, HTTPStatus.OK

@student_namespace.route('/students/<int:student_id>/courses')
class GetStudentCourses(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Get all courses for a student',
        params = {
            'student_id': 'An ID for a student'
        }
    )
    @jwt_required()
    def get(self, student_id): 
        """
            Get all courses for a student
        """
        student = Student.get_by_id(student_id)

        courses = student.courses

        return courses, HTTPStatus.OK

#retrieve grades for a student in a course
@student_namespace.route('/students/<int:student_id>/courses/<int:course_id>/grades')
class GetStudentCourseGrades(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Get all grades for a student in a course',
        params = {
            'student_id': 'An ID for a student',
            'course_id': 'An ID for a course'
        }
    )
    @jwt_required()
    def get(self, student_id, course_id):
        """
            Get all grades for a student in a course
        """
        student = Student.get_by_id(student_id)
        course = Course.get_by_id(course_id)

        grades = Grade.query.filter_by(student_id=student, course_id=course).all()

        return grades, HTTPStatus.OK
    

#calculate the GPA for each student based on their grades in each course. Use the standard 4.0 scale for calculating GPA.

@student_namespace.route('/students/<int:student_id>/gpa')
class GetStudentGPA(Resource):
    #@student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Get the GPA for a student',
        params = {
            'student_id': 'An ID for a student'
        }
    )
    #@jwt_required()
    def get(self, student_id):
        """
        Calculate a student gpa score
        """     
        student = Student.get_by_id(student_id)
        # get all the course the students offer
        courses = StudentCourse.get_student_courses(student.id)
        total_weighted_gpa = 0
        total_credit_hours = 0
        for course in courses:
            # This check if student have a score for the course
            score_exist = Score.query.filter_by(student_id=student.id, course_id=course.id).first()
            if score_exist:
                grade = score_exist.grade
                # This calculates the gpa for the course
                gpa = convert_student_grade_to_gpa(grade)
                weighted_gpa = gpa * course.credit_hours
                total_weighted_gpa += weighted_gpa
                total_credit_hours += course.credit_hours
        if total_credit_hours == 0:
            return {
                'message':'GPA calculation completed.',
                'gpa': total_credit_hours
            }, HTTPStatus.OK
        else:
            gpa =  total_weighted_gpa / total_credit_hours
            return {
                'message':'GPA calculation completed',
                'gpa': round(gpa , 2 ) 
            }, HTTPStatus.OK
    


        


