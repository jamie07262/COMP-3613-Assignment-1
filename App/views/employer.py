from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_employer,
    view_shortlist,
    accept_student,
    reject_student,
    get_jwt_identity,
    jwt_authenticate,
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

#creating employer
@employer_views.route('/employer', methods=['POST'])
def create_employer():
    data = request.json
    employer = create_employer(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        companyName=data['companyName']
    )
    if employer:
        return jsonify({"message": "Employer created successfully", "employer_id": employer.id}), 201
    return jsonify({"error": "Failed to create employer"}), 409

@employer_views.route('/<employer_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(employer_id):
    # Logic to retrieve shortlists for the employer
    table = view_shortlist(employer_id)
    if table:
        return table, 200
    return jsonify({"message": f"Shortlists for employer {employer_id} not found."}), 404

@employer_views.route('/internships/<internship_id>/accept/<student_id>', methods=['PUT'])
@jwt_required()
def accept_student_route(internship_id, student_id):
    employer_id = get_jwt_identity()
    result = accept_student(employer_id, internship_id, student_id)
    if result:
        return jsonify({"message": f"Student {student_id} accepted for internship {internship_id}."}), 200
    return jsonify({"error": "Failed to accept student."}), 400

@employer_views.route('/internships/<internship_id>/reject/<student_id>', methods=['PUT'])
@jwt_required()
def reject_student_route(internship_id, student_id):
    employer_id = get_jwt_identity()
    result = reject_student(employer_id, internship_id, student_id)
    if result:
        return jsonify({"message": f"Student {student_id} rejected for internship {internship_id}."}), 200
    return jsonify({"error": "Failed to reject student."}), 400