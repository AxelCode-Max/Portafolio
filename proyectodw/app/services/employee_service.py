from app.models.employee import Employee
from app.utils.exceptions import ResourceNotFoundError, ValidationError
from datetime import datetime

class EmployeeService:
    def __init__(self, employee_repository):
        self.employee_repository = employee_repository
    
    def get_all_employees(self):
        return self.employee_repository.find_all()
    
    def get_active_employees(self):
        return self.employee_repository.find_all({"status": "active"})
    
    def get_employee_by_id(self, employee_id):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError("Employee", employee_id)
        return employee
    
    def create_employee(self, employee_data):
        # Validar datos del empleado
        self._validate_employee_data(employee_data)
        
        # Verificar si ya existe un empleado con el mismo ID
        existing_employee = self.employee_repository.find_by_employee_id(
            employee_data.get('employee_id')
        )
        if existing_employee:
            raise ValidationError(f"Employee with ID {employee_data.get('employee_id')} already exists")
        
        employee = Employee(
            name=employee_data.get("name"),
            employee_id=employee_data.get("employee_id"),
            department=employee_data.get("department"),
            pay=employee_data.get("pay"),
        )
        
        return self.employee_repository.create(employee)
    
    def update_employee(self, id, employee_data):
        employee = self.get_employee_by_id(id)
        
        # Actualizar solo los campos proporcionados
        for key, value in employee_data.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        
        employee.updated_at = datetime.utcnow()
        return self.employee_repository.update(id, employee.to_dict())
    
    def deactivate_employee(self, id):
        employee = self.get_employee_by_id(id)
        return self.employee_repository.deactivate(id)
    
    def activate_employee(self, id):
        employee = self.get_employee_by_id(id)
        return self.employee_repository.activate(id)
    
    def _validate_employee_data(self, data):
        required_fields = ['name', 'employee_id', 'department']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"Field '{field}' is required")
