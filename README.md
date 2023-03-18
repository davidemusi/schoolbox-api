# SchoolBox API
SchoolBox API is a RESTful API for managing school-related information. It provides endpoints for managing schools, students, teachers, classes, and more. This API is built using Python Flask, and SQLAlchemy.

# Getting Started

To get started with SchoolBox API, follow these steps:

1. Clone the repository: https://github.com/davidemusi/schoolbox-api
2. Install dependencies: pip install -r requirements.txt
3. Create a .env file based on the .env.example file and set your environment variables
4. Start the server: python app.py
5. The server should now be running on http://localhost:5000. You can test the API using a tool like Postman or insomnia. Better stil you can checkout the live API hosted at https://skulbox.herokuapp.com

# API Endpoints

SchoolBox API provides the following endpoints:

- GET /schools - Get a list of all schools
- GET /schools/:id - Get a specific school by ID
- POST /schools - Create a new school
- PUT /schools/:id - Update an existing school by ID
- DELETE /schools/:id - Delete a school by ID
- GET /students - Get a list of all students
- GET /students/:id - Get a specific student by ID
- POST /students - Create a new student
- PUT /students/:id - Update an existing student by ID
- DELETE /students/:id - Delete a student by ID
- GET /teachers - Get a list of all teachers
- GET /teachers/:id - Get a specific teacher by ID
- POST /teachers - Create a new teacher
- PUT /teachers/:id - Update an existing teacher by ID
- DELETE /teachers/:id - Delete a teacher by ID
- GET /classes - Get a list of all classes
- GET /classes/:id - Get a specific class by ID
- POST /classes - Create a new class
- PUT /classes/:id - Update an existing class by ID
- DELETE /classes/:id - Delete a class by ID

# Authentication
SchoolBox API uses JSON Web Tokens (JWT) for authentication. To access protected endpoints, you must include a valid JWT in the Authorization header of your requests. To obtain a JWT, send a POST request to the /auth/login endpoint with your credentials.

# Error Handling

SchoolBox API handles errors by returning an error object with a status code and message property. If there is an error with the request, the status code will be in the 4xx range. If there is an error on the server, the status code will be in the 5xx range.

# Contributing

Contributions to SchoolBox API are welcome. To contribute, follow these steps:

1. Fork the repository
2. Create a new branch: git checkout -b my-feature-branch
3. Make your changes and commit them: git commit -m "Add new feature"
4. Push to the branch: git push origin my-feature-branch
5. Create a pull request

# License
- SchoolBox API is licensed under the MIT License. See LICENSE for more information.
- ALTSCHOOL AFRICA SEMESTER PROJECT
