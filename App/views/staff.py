from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_student,
    create_staff,
    create_employer,
    get_all_users,
    get_all_users_json,
    jwt_authenticate,
    is_staff,
    is_student,
    is_employer,
    get_user
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

#creating staff
@staff_views.route('/staff', methods=['POST'])
def create_staff():
    data = request.json
    staff = create_staff(
        username=data['username'],
        password=data['password'],
        email=data['email']
    )
    if staff:
        return jsonify({"message": "Staff created successfully", "staff_id": staff.id}), 201
    return jsonify({"error": "Failed to create staff"}), 409