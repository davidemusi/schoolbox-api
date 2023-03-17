from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.students import Student
from ..utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


auth_namespace = Namespace('auth', description='name space for authentication')


signup_model = auth_namespace.model(
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description='A password')
    }
)

student_model = auth_namespace.model(
    'Student', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description='A password'),
        'is_active': fields.Boolean(description="This shows that Student is active or not"),
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description='A password')
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(student_model)
    def post(self):
        """
            Sign up a student
        """
        data = request.get_json()
        # data = {"username":"Caleb", "email": "caleb.gmail.com", "password":"password"}

        new_student = Student(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )
        
        new_student.save()

        return new_student, HTTPStatus.CREATED

        

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """
        data = request.get_json()

        # data = {"email": "caleb.gmail.com", "password":"password"}

        email = data.get('email')
        password = data.get('password')
        
        student = Student.query.filter_by(email=email).first()


        if (student is not None) and check_password_hash(student.password_hash, password):
            
            access_token = create_access_token(identity=student.username)
            refresh_token = create_refresh_token(identity=student.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED



@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus