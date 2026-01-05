from app.models.attendance import Attendance
from app.utils.exceptions import ResourceNotFoundError, ValidationError
from datetime import datetime
from bson.objectid import ObjectId

class AttendanceService:
    def __init__(self, attendance_repository, employee_repository):
        self.attendance_repository = attendance_repository
        self.employee_repository = employee_repository
    
    def register_check_in(self, employee_id):
        # Verificar que el empleado existe y está activo
        employee = self.employee_repository.find_by_employee_id(employee_id)
        if not employee:
            raise ResourceNotFoundError("Employee", employee_id)
        
        if employee.status != "active":
            raise ValidationError("Cannot register attendance for inactive employee")
        
        # Verificar si ya hizo check-in hoy
        today = datetime.utcnow().date()
        existing_attendance = self.attendance_repository.find_by_employee_and_date(
            employee_id, today
        )
        
        if existing_attendance and existing_attendance["check_in_time"]:
            raise ValidationError("Employee already checked in today")
        
        now = datetime.utcnow()
        
        if existing_attendance:
            existing_attendance["check_in_time"] = now
            existing_attendance["updated_at"] = now
            return self.attendance_repository.update(
                existing_attendance["_id"],
                existing_attendance
            )
        else:
            attendance = Attendance(
                employee_id=employee_id,
                check_in_time=now
            )
            return self.attendance_repository.create(attendance)
    
    def register_check_out(self, employee_id):
        # Verificar que el empleado existe
        employee = self.employee_repository.find_by_employee_id(employee_id)
        if not employee:
            raise ResourceNotFoundError("Employee", employee_id)

        # Verificar si hizo check-in hoy
        today = datetime.utcnow().date()
        existing_attendance = self.attendance_repository.find_by_employee_and_date(
            employee_id, today
        )

        if not existing_attendance or not existing_attendance["check_in_time"]:
            raise ValidationError("Employee has not checked in today")

        if existing_attendance["check_out_time"]:
            raise ValidationError("Employee already checked out today")

        now = datetime.utcnow()
        # No modificar el objeto existente, crear un nuevo objeto con solo el campo a actualizar
        update_data = {
            "check_out_time": now,
            "updated_at": now
        }

        # Llamar al método update del repositorio con el _id del registro de asistencia y los datos a actualizar
        self.attendance_repository.update(
            str(existing_attendance["_id"]), # Usar el _id del documento
            update_data
        )
        
        return self.attendance_repository.find_by_id(str(existing_attendance["_id"]))

    
    def get_attendance_by_employee(self, employee_id):
        # Verificar que el empleado existe
        employee = self.employee_repository.find_by_employee_id(employee_id)
        if not employee:
            raise ResourceNotFoundError("Employee", employee_id)
        attendances = self.attendance_repository.find_by_employee_id(employee_id)
        if not attendances:
            raise ResourceNotFoundError("Attendances for Employee", employee_id)
        return attendances
    
    def get_attendance_by_date(self, date):
        return self.attendance_repository.find_by_date(date)
