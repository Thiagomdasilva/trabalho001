from datetime import datetime
from typing import Optional
from bson import ObjectId

class Car:
    def __init__(
        self,
        marca: str,
        modelo: str,
        ano: int,
        cor: str,
        preco: float,
        quilometragem: int,
        combustivel: str,
        cambio: str,
        portas: int,
        placa: str,
        vendido: bool = False,
        data_cadastro: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.preco = preco
        self.quilometragem = quilometragem
        self.combustivel = combustivel
        self.cambio = cambio
        self.portas = portas
        self.placa = placa.upper()
        self.vendido = vendido
        self.data_cadastro = data_cadastro or datetime.now()
    
    def to_dict(self):
        car_dict = {
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "cor": self.cor,
            "preco": self.preco,
            "quilometragem": self.quilometragem,
            "combustivel": self.combustivel,
            "cambio": self.cambio,
            "portas": self.portas,
            "placa": self.placa,
            "vendido": self.vendido,
            "data_cadastro": self.data_cadastro
        }
        
        if self._id:
            car_dict["_id"] = self._id
            
        return car_dict
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get('_id'),
            marca=data['marca'],
            modelo=data['modelo'],
            ano=data['ano'],
            cor=data['cor'],
            preco=data['preco'],
            quilometragem=data['quilometragem'],
            combustivel=data['combustivel'],
            cambio=data['cambio'],
            portas=data['portas'],
            placa=data['placa'],
            vendido=data.get('vendido', False),
            data_cadastro=data.get('data_cadastro')
        )
    
    def __str__(self):
        status = "VENDIDO" if self.vendido else "DISPONÍVEL"
        return (f"{self.marca} {self.modelo} {self.ano} - {self.cor}\n"
                f"Preço: R$ {self.preco:,.2f} | KM: {self.quilometragem}\n"
                f"Combustível: {self.combustivel} | Câmbio: {self.cambio}\n"
                f"Placa: {self.placa} | Status: {status}")