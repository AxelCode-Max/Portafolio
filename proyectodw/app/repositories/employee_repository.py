from app.repositories.base_repository import BaseRepository
from app.models.employee import Employee
from datetime import datetime

class EmployeeRepository(BaseRepository):
    def __init__(self, db):
        self.collection = db.employees
    
    def find_all(self, filter_dict=None):
        filter_dict = filter_dict or {}
        employees = list(self.collection.find(filter_dict))
        return [Employee.from_dict(employee) for employee in employees]
    
    def find_by_id(self, id):
        employee = self.collection.find_one({"employee_id": id})
        return Employee.from_dict(employee) if employee else None
    
    def find_by_employee_id(self, employee_id):
        employee = self.collection.find_one({"employee_id": employee_id})
        return Employee.from_dict(employee) if employee else None
        
    def create(self, employee):
        employee_dict = employee.to_dict()
        employee_dict["_id"] = employee_dict.pop("id")
        result = self.collection.insert_one(employee_dict)
        return self.find_by_id(result.inserted_id)
    
    def update(self, id, employee_data):
        employee_data["updated_at"] = datetime.utcnow()
        self.collection.update_one({"employee_id": id}, {"$set": employee_data})
        return self.find_by_id(id)
    
    def delete(self, id):
        return self.collection.delete_one({"employee_id": id})
    
    def deactivate(self, id):
        return self.update(id, {"status": "inactive"})
    
    def activate(self, id):
        return self.update(id, {"status": "active"})
