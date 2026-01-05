from datetime import datetime
from bson import ObjectId

class Employee:
    def __init__(self, name, employee_id, department, pay, status="active", id=None):
        self.id = id or str(ObjectId())
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.pay = pay
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "employee_id": self.employee_id,
            "department": self.department,
            "pay": self.pay,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        employee = cls(
            name=data.get("name"),
            employee_id=data.get("employee_id"),
            department=data.get("department"),
            pay=data.get("pay"),
            status=data.get("status", "active"),
            id=data.get("id")
        )
        employee.created_at = data.get("created_at", datetime.utcnow())
        employee.updated_at = data.get("updated_at", datetime.utcnow())
        return employee
