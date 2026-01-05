from flask import Blueprint, request, jsonify
from app.utils.exceptions import AppError

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

class AttendanceController:
    def __init__(self, attendance_service):
        self.attendance_service = attendance_service
        
    def register_routes(self, bp):
        bp.route('/check-in', methods=['POST'])(self.register_check_in)
        bp.route('/check-out', methods=['POST'])(self.register_check_out)
        bp.route('/employee/<string:employee_id>', methods=['GET'])(self.get_attendance_by_employee)
        bp.route('/date/<string:date>', methods=['GET'])(self.get_attendance_by_date)
    
    def register_check_in(self):
        try:
            data = request.get_json()
            employee_id = data.get('employee_id')
            
            if not employee_id:
                return jsonify({"error": "Employee ID is required"}), 400
                
            attendance = self.attendance_service.register_check_in(employee_id)
            return jsonify({"today's attendance": employee_id}), 201
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def register_check_out(self):
        try:
            data = request.get_json()
            employee_id = data.get('employee_id')
            
            if not employee_id:
                return jsonify({"error": "Employee ID is required"}), 400
                
            attendance = self.attendance_service.register_check_out(employee_id)
            return jsonify({"Exit to work": employee_id}), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def get_attendance_by_employee(self, employee_id):
        try:
            attendances = self.attendance_service.get_attendance_by_employee(employee_id)
            
            # Convertir documentos de MongoDB a diccionarios
            attendance_dicts = [
                {
                    "check_in_time": attendance["check_in_time"],
                    "check_out_time": attendance["check_out_time"],
                    # Agrega otros campos según sea necesario
                } for attendance in attendances
            ]
            
            return jsonify(attendance_dicts), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    
    def get_attendance_by_date(self, date):
        try:
            attendances = self.attendance_service.get_attendance_by_date(date)
            return jsonify([attendance.to_dict() for attendance in attendances]), 200
        except AppError as e:
            return jsonify({"error": str(e)}), e.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
