from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Repositorio base abstracto que define operaciones comunes"""
    
    @abstractmethod
    def find_all(self):
        pass
    
    @abstractmethod
    def find_by_id(self, id):
        pass
    
    @abstractmethod
    def create(self, entity):
        pass
    
    @abstractmethod
    def update(self, id, entity):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass
