import os

class Config:
    """Configuración base para la aplicación"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
    
class TestingConfig(Config):
    """Configuración para entorno de pruebas"""
    TESTING = True
    
# Configuración por defecto según entorno
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# Obtiene la configuración del entorno actual
Config = config_by_name[os.environ.get('FLASK_ENV', 'development')]
