from flask import Blueprint, request, jsonify
from app.utils.exceptions import AppError

employee_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

class EmployeeController:
    def __init__(self, employee_service):
        self.employee_service = employee_service
        
    def register_routes(self, bp):
        bp.route('', methods=['GET'])(self.get_all_employees)
        bp.route('/<string:employee_id>', methods=['GET'])(self.get_employee)
        bp.route('', methods=['POST'])(self.create_employee)
        bp.route('/<string:employee_id>', methods=['PUT'])(self.update_employee)
        bp.route('/<string:employee_id>/deactivate', methods=['POST'])(self.deactivate_employee)
        bp.route('/<string:employee_id>/active', methods=['POST'])(self.activate_employee)
    
    def get_all_employees(self):
        try:
            employees = self.employee_service.get_all_employees()
            return jsonify([employee.to_dict() for employee in employees]), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_employee(self, employee_id):
        try:
            employee = self.employee_service.get_employee_by_id(employee_id)
            return jsonify(employee.to_dict()), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def create_employee(self):
        try:
            employee_data = request.get_json()
            new_employee = self.employee_service.create_employee(employee_data)
            return jsonify(new_employee.to_dict()), 201
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def update_employee(self, employee_id):
        try:
            employee_data = request.get_json()
            updated_employee = self.employee_service.update_employee(employee_id, employee_data)
            return jsonify(updated_employee.to_dict()), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def deactivate_employee(self, employee_id):
        try:
            self.employee_service.deactivate_employee(employee_id)
            return jsonify({"message": "Employee deactivated successfully"}), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def activate_employee(self, employee_id):
        try:
            self.employee_service.activate_employee(employee_id)
            return jsonify({"message": "Employee activated successfully"}), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
