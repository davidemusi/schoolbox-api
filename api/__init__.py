from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .course.views import course_namespace
from .student.views import student_namespace
from .config.config import config_dict
from .utils import db
from .models.students import Student
from .models.courses import Course
from .models.grades import Grade
from .models.gpa import GPA
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['prod']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your Bearer Token'
        }
    }

    api = Api(app, 
              title='Student Management API',
              description='A simple student management API', 
              authorizations=authorizations,
              security='Bearer Auth'  
            )

    api.add_namespace(student_namespace, path='/student')
    api.add_namespace(course_namespace, path='/course')
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def handle_not_found(error):
        return {'message': 'Not found'}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        return {'message': 'Method not allowed'}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Student': Student,
             'Course': Course,
                'Grade': Grade,
                'GPA': GPA
        }

    return app   

# Path: api\__init__.py


