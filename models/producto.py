from models.db import DataBaseExecute

class Producto:
    _table = "productos"
    
    def __init__(self, nombre: str, precio: float, stock:int, id: int | None = None):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id = id
        
    def __str__(self) -> str:
        return f"Producto(id={self.id}, nombre={self.nombre}, precio={self.precio:.2f}, stock={self.stock})"

    def __repr__(self) -> str:
        return f"Producto(id={self.id!r}, nombre={self.nombre!r}, precio={self.precio!r}, stock={self.stock!r})"
        
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip().title()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float):
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = round(float(value), 2)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int):
        if value < 0:
            raise ValueError("El stock no puede ser negativo")
        self._stock = int(value)

    def to_dict(self) -> dict:
        return {"nombre": self.nombre, "precio": self.precio, "stock": self.stock}
    
    @classmethod
    def find(cls, id: int):
        db = DataBaseExecute()
        row = db.find(cls._table, id)
        if not row:
            return None
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            precio=row["precio"],
            stock=row["stock"]
        )
    
    @classmethod
    def find_all(cls):
        db = DataBaseExecute()
        rows = db.find_all(cls._table)
        return [
            cls(
                nombre=row["nombre"],
                precio=float(row["precio"]),
                stock=row["stock"],
                id=row["id"]
            )
            for row in rows
        ]
    
    @classmethod
    def exist(cls, nombre: str) -> bool: 
        db = DataBaseExecute()
        rows = db.find_by(cls._table, "nombre", nombre)
        
        return rows > 0
        
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
    