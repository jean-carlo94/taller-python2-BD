import re
from models.db import DataBaseExecute

class Cliente:
    _table = "clientes"
    
    def __init__(self, nombre: str, correo: str, id: int | None = None):
        self.nombre = nombre
        self.correo = correo
        self.id = id
        
    def __str__(self) -> str:
        return f"Cliente:{self.id}, Nombre:{self.nombre}, Email:{self.correo}"

    def __repr__(self) -> str:
        return f"Cliente(id={self.id!r} nombre={self.nombre!r}, correo={self.correo!r})"

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip().title()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, value: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Correo inválido")
        self._correo = value.strip().lower()

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "correo": self.correo
        }
        
    @classmethod
    def find(cls, id: int):
        db = DataBaseExecute()
        row = db.find(cls._table, id)
        
        if not row:
            return None
        return cls(
                nombre=row["nombre"],
                correo=(row["correo"]),
                id=row["id"]
            )
        
    @classmethod
    def find_all(cls):
        db = DataBaseExecute()
        rows = db.find_all(cls._table)
        return [
            cls(
                nombre=row["nombre"],
                correo=(row["correo"]),
                id=row["id"]
            )
            for row in rows
        ]
    
    @classmethod
    def exist(cls, correo: str) -> bool:
        db = DataBaseExecute()
        rows = db.find_by(cls._table, "correo", correo)
        
        return rows > 0
    
    def syc(self):
        db = DataBaseExecute()
        rows = db.find_by(self._table, "correo", self.correo)
        
        if len(rows) > 0: 
            self.id = rows[0]["id"]

    def save(self):
        db = DataBaseExecute()
        
        if self.id is None:
            self.id = db.insert(self._table, self.to_dict())
        else:
            db.update(self._table, self.id, self.to_dict())
        return self.id
    
    def delete(self):
        db = DataBaseExecute()
        
        if self.id is not None:
            db.delete(self._table, self.id)
            self.id = None