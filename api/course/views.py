from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
from ..models.students import Student
from http import HTTPStatus
from ..utils import db
from flask_jwt_extended import jwt_required, get_jwt_identity

course_namespace = Namespace('courses', description='name space for courses')
#student_namespace = Namespace('students', description='name space for students')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description='An ID'),
        'name': fields.String(description='Name of course', required=True, example='Maths'),
        'teacher': fields.String(description='Teacher of course', required=True, example='Mr. David'),
        #'students': fields.List(fields.String, description='Students in course', required=True, example='Caleb'),
        'course_status': fields.String(description='The Status of our Course', required=True,
            enum = ['ACTIVE','INACTIVE','DELETED']),
         'credit_hours': fields.Integer(description='Credit hours of course', required=True, example='3'),
    }
)

course_status_model = course_namespace.model(
    'CourseStatus', {
        'order_status': fields.String(required=True, description='Course Status',
             enum = ['ACTIVE','INACTIVE','DELETED'])
    }
)

# student_model = student_namespace.model(
#     'Student', {
#         'id': fields.Integer(description='An ID'),
#         'username': fields.String(description='Name of student', required=True),
#         'email': fields.String(description='Email of student', required=True),
#     }
# )

@course_namespace.route('/courses')
class CourseGetCreate(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get all courses'
    )
    @jwt_required()
    def get(self):
        """
            Get all courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Register a new course'
    )
    @jwt_required()
    def post(self):
        """
            Register a new course
        """

        username = get_jwt_identity()


        current_student = Student.query.filter_by(username=username).first()

        data = course_namespace.payload

        new_course = Course(
            name = data['name'],
            teacher = data['teacher'],
            credit_hours = data['credit_hours'],
        )

        new_course.student = current_student

        new_course.save()

        return new_course, HTTPStatus.CREATED


@course_namespace.route('/course/<int:course_id>')
class GetUpdateDelete(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Retrieve a course by id',
        params = {
            'course_id': 'An ID for a course'
        }
    )
    @jwt_required()
    def get(self, course_id):
        """
            Retrieve an course by id
        """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Update a course by id',
        params = {
            'course_id': 'An ID for an course'
        }
    )
    @jwt_required()
    def put(self, course_id):
        """
            Update a course by id
        """
        course_to_update = Course.get_by_id(course_id)

        data = course_namespace.payload

        course_to_update.name = data["name"]
        course_to_update.teacher = data["teacher"]


        db.session.commit()

        return course_to_update, HTTPStatus.OK
    

@course_namespace.route('/course/<int:course_id>/students')
class CourseStudent(Resource):
    
        @course_namespace.marshal_with(course_model)
        @course_namespace.doc(
            description='Get all students for a course',
            params = {
                'course_id': 'An ID for a course'
            }
        )
        @jwt_required()
        def get(self, course_id):
            """
                Get all students for a course
            """
            course = Course.get_by_id(course_id)
    
            students = course.students
    
            return students, HTTPStatus.OK
        


    


    











    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



