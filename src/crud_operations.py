from .database import mongodb_connection
from .models import Car
from bson import ObjectId
from typing import List, Optional
from pymongo import ReturnDocument

class CarCRUD:
    def __init__(self):
        self.db = mongodb_connection.get_database()
        self.collection = self.db['cars']
    
    def create_car(self, car: Car) -> str:
        """Cria um novo carro no banco de dados"""
        result = self.collection.insert_one(car.to_dict())
        return str(result.inserted_id)
    
    def read_car_by_id(self, car_id: str) -> Optional[Car]:
        """Busca um carro pelo ID"""
        try:
            car_data = self.collection.find_one({"_id": ObjectId(car_id)})
            if car_data:
                return Car.from_dict(car_data)
            return None
        except:
            return None
    
    def read_all_cars(self) -> List[Car]:
        """Retorna todos os carros"""
        cars = []
        for car_data in self.collection.find():
            cars.append(Car.from_dict(car_data))
        return cars
    
    def update_car(self, car_id: str, update_data: dict) -> Optional[Car]:
        """Atualiza um carro existente"""
        try:
            result = self.collection.find_one_and_update(
                {"_id": ObjectId(car_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )
            if result:
                return Car.from_dict(result)
            return None
        except:
            return None
    
    def delete_car(self, car_id: str) -> bool:
        """Remove um carro do banco de dados"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(car_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do estoque"""
        total = self.collection.count_documents({})
        available = self.collection.count_documents({"vendido": False})
        sold = self.collection.count_documents({"vendido": True})
        
        return {
            "total_cars": total,
            "available_cars": available,
            "sold_cars": sold
        }