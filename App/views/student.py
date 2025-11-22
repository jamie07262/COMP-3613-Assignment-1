from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import ( create_student, view_my_shortlists)
from App.controllers.auth import jwt_authenticate

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student', methods=['POST'])
def create_student():
    data = request.json
    student = create_student(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        skills=data['skills']
    )
    if student:
        return jsonify({"message": "Student created successfully", "student_id": student.id}), 201
    else:
        return jsonify({"error": f"Username {data['username']} already taken."}), 409


@student_views.route('/<student_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(student_id):
    table = view_my_shortlists(student_id)
    if table:
        return table, 200
    return jsonify({"error": "No shortlists found."}), 404