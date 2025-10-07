from datetime import datetime
from models.db import DataBaseExecute

class Venta:
    _table = "ventas"
    
    def __init__(self, id_cliente: int, id_producto: int, cantidad: int, fecha_venta: str | datetime, id: int | None = None):
        self.id = id
        self.id_cliente = id_cliente
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.fecha_venta = fecha_venta
        
    def __str__(self) -> str:
        return f"Venta(id={self.id}, Cliente={self.id_cliente}, Producto={self.id_producto}, Cantidad={self.cantidad} FechaVenta={self.fecha_venta})"

    def __repr__(self) -> str:
        return f"Venta(id={self.id!r}, id_cliente={self.id_cliente!r}, id_producto={self.id_producto!r}, cantidad={self.cantidad}, fecha_venta={self.fecha_venta!r})"

    @property
    def id_cliente(self) -> int:
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, value: int):
        if value <= 0:
            raise ValueError("El id_cliente debe ser un entero positivo")
        self._id_cliente = int(value)

    @property
    def id_producto(self) -> int:
        return self._id_producto

    @id_producto.setter
    def id_producto(self, value: int):
        if value <= 0:
            raise ValueError("El id_producto debe ser un entero positivo")
        self._id_producto = int(value)

    @property
    def fecha_venta(self) -> str:
        return self._fecha_venta

    @fecha_venta.setter
    def fecha_venta(self, value: str | datetime):
        if isinstance(value, datetime):
            self._fecha_venta = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                self._fecha_venta = value
            except ValueError:
                raise ValueError("La fecha_venta debe estar en formato 'YYYY-MM-DD HH:MM:SS'")
        else:
            raise TypeError("La fecha_venta debe ser str o datetime")

    def to_dict(self) -> dict:
        return {
            "id_cliente": self.id_cliente,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "fecha_venta": self.fecha_venta
        }

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
            
    @classmethod
    def lista_ventas(cls):
        db = DataBaseExecute()
        result = db.execute_query('''
            SELECT
            vent.id id,
            vent.id_cliente id_cliente,
            client.nombre nombre_cliente,
            vent.id_producto id_producto,
            prod.nombre nombre_producto,
            prod.precio precio_unitario,
            vent.cantidad cantidad,
            (prod.precio * vent.cantidad) as total
            FROM clase_martes.ventas vent
            INNER JOIN clase_martes.productos prod ON (vent.id_producto = prod.id)
            INNER JOIN clase_martes.clientes client ON (vent.id_cliente = client.id); 
                               ''')
        
        return result
