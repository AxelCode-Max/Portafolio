# app/utils/exceptions.py
class AppError(Exception):
    """Clase base para errores de aplicación"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ResourceNotFoundError(AppError):
    """Error cuando un recurso no se encuentra"""
    def __init__(self, resource_type, resource_id):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, 404)

class ValidationError(AppError):
    """Error de validación de datos"""
    def __init__(self, message):
        super().__init__(message, 400)
