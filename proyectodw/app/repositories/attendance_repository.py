from datetime import datetime
from bson.objectid import ObjectId

class AttendanceRepository:
    def __init__(self, db):
        self.collection = db.attendance

    def find_by_employee_and_date(self, employee_id, date):
        # Convertir datetime.date a rango de datetime.datetime (inicio y fin del día)
        start_of_day = datetime.combine(date, datetime.min.time())  # 00:00:00
        end_of_day = datetime.combine(date, datetime.max.time())    # 23:59:59.999999

        # Buscar registros dentro del rango del día
        return self.collection.find_one({
            "employee_id": employee_id,
            "check_in_time": {"$gte": start_of_day, "$lte": end_of_day}
        })

    def find_by_employee_id(self, employee_id):
        return list(self.collection.find({"employee_id": employee_id}))

    def find_by_date(self, date):
        # Convertir datetime.date a rango de datetime.datetime
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())

        return list(self.collection.find({
            "check_in_time": {"$gte": start_of_day, "$lte": end_of_day}
        }))

    def create(self, attendance):
        attendance_dict = attendance.to_dict()
        if "id" in attendance_dict:
            del attendance_dict["id"]
        return self.collection.insert_one(attendance_dict)

    def update(self, id, attendance_data):
        try:
            object_id = ObjectId(id)  # Convertir el ID a ObjectId
            self.collection.update_one({"_id": object_id}, {"$set": attendance_data})  # Buscar por _id
            return self.find_by_id(id)
        except Exception as e:
            print(f"Error en update: {e}")
            raise

    def find_by_id(self, id):
        try:
            object_id = ObjectId(id)  # Convertir el ID a ObjectId
            return self.collection.find_one({"_id": object_id})  # Buscar por _id
        except Exception as e:
            print(f"Error en find_by_id: {e}")
            raise

