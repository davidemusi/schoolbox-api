import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.students import Student
from ..models.courses import Course
from ..models.grades import Grade


class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app = None
        self.appctx.pop()
        self.client = None

    # Function to test the retrieval of all courses
    def test_get_all_courses(self):
        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/course/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == []

    # Function to test the creation of a course
    def test_register_course(self):
        data = {
            "name": "Ada",
            "teacher": "Lovelace",
            "credit_hours": 4
        }

        token = create_access_token(identity='testuser')

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post('/course/courses', json=data, headers=headers)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        assert course_id == 1

        assert len(courses) == 1

        assert courses[0].name == "Ada"

        assert courses[0].teacher == "Lovelace"




