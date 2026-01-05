from datetime import datetime
from bson import ObjectId

class Attendance:
    def __init__(self, employee_id, check_in_time=None, check_out_time=None, id=None):
        self.id = id or str(ObjectId())
        self.employee_id = employee_id
        self.check_in_time = check_in_time or datetime.utcnow()
        self.check_out_time = check_out_time
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "check_in_time": self.check_in_time,
            "check_out_time": self.check_out_time,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        attendance = cls(
            employee_id=data.get("employee_id"),
            check_in_time=data.get("check_in_time"),
            check_out_time=data.get("check_out_time"),
            id=data.get("id")
        )
        
        attendance.created_at = data.get("created_at", datetime.utcnow())
        attendance.updated_at = data.get("updated_at", datetime.utcnow())
        
        return attendance
