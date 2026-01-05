from flask import Flask, jsonify
from pymongo import MongoClient
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.attendance_repository import AttendanceRepository
from app.services.employee_service import EmployeeService
from app.services.attendance_service import AttendanceService
from app.controllers.employee_controller import EmployeeController, employee_bp
from app.controllers.attendance_controller import AttendanceController, attendance_bp
from app.utils.exceptions import AppError
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()
def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuración
    app.config.from_object('app.config.Config')
    
    db_password = os.getenv('MONGO_PASSWORD')
    
    # Construir URI de conexión a MongoDB Atlas
    mongo_uri = f"mongodb+srv://honoka:{db_password}@flaskapi.rvw7w.mongodb.net/"
    
    # Conectar a MongoDB Atlas
    try:
        mongo_client = MongoClient(mongo_uri)
        # Verificar conexión
        mongo_client.admin.command('ping')
        app.logger.info("Conexión a MongoDB Atlas establecida correctamente")
        
        # Seleccionar base de datos
        db = mongo_client.attendance_management
        
        # Inicializar repositorios
        employee_repository = EmployeeRepository(db)
        attendance_repository = AttendanceRepository(db)
        
        # Inicializar servicios
        employee_service = EmployeeService(employee_repository)
        attendance_service = AttendanceService(attendance_repository, employee_repository)
        
        # Inicializar controladores
        employee_controller = EmployeeController(employee_service)
        attendance_controller = AttendanceController(attendance_service)
        
        # Registrar rutas
        employee_controller.register_routes(employee_bp)
        attendance_controller.register_routes(attendance_bp)
        
        # Registrar blueprints
        app.register_blueprint(employee_bp)
        app.register_blueprint(attendance_bp)
        
        # Configurar CORS para permitir solicitudes desde el frontend
        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
            return response
            
        # Manejador global de errores
        @app.errorhandler(AppError)
        def handle_app_error(error):
            response = {
                'error': error.message,
                'status_code': error.status_code
            }
            return jsonify(response), error.status_code
        
        return app
        
    except Exception as e:
        app.logger.error(f"Error conectando a MongoDB Atlas: {str(e)}")
        raise
