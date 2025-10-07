from datetime import datetime

from models.cliente import Cliente
from models.producto import Producto
from models.venta import Venta

def print_lis(list_object: list[any]):
    for i in range(len(list_object)):
        print(f"| \033[45m({i + 1}).\033[0m \033[32m{list_object[i]}\033[0m")

def listar_productos():
    productos = Producto.find_all()
    
    if(len(productos) == 0):
        print("|\033[33m No hay productos en este momento.\033[0m")
        return
    
    print_lis(productos)

def crear_producto():
    try:
        nombre = str(input("|\033[44m Ingrese nombre del Producto: \033[0m"))
        precio = int(input("|\033[44m Ingrese precio del Producto: \033[0m"))
        stock = int(input("|\033[44m Ingrese stock del Producto: \033[0m"))
    except ValueError:
        print("|\033[31m El Tipo de dato es invalido \033[0m")
        return

    producto = Producto(nombre, precio, stock)
    
    if Producto.exist(producto.nombre):
        print("|\033[31m Producto ya existe \033[0m")
        return
    
    producto.save()
    
    print(f"|\033[32m {producto.id} | Producto {producto.nombre} ha sido registrada exitosamente. \033[0m")

def crear_cliente():
    try:
        nombre = str(input("|\033[44m Ingrese nombre del Producto: \033[0m"))
        correo = str(input("|\033[44m Ingrese precio del Producto: \033[0m"))
    except ValueError:
        print("|\033[31m El Tipo de dato es invalido \033[0m")
        return

    cliente = Cliente(nombre, correo)
    
    if len(cliente.exist()) > 0:
        print("|\033[31m Cliente ya existe \033[0m")
        return
    
    cliente.save()
    
    print(f"|\033[32m {cliente.id} | Cliente {cliente.nombre} ha sido registrada exitosamente. \033[0m")

def vender_producto():
    productos = Producto.find_all()
    
    if(len(productos) == 0):
        print("|\033[33m No hay productos en este momento.\033[0m")
        return
    
    print_lis(productos)
    
    try:
        id_producto = int(input("|\033[44m Ingrese el ID del producto a comprar: \033[0m"))
        cantidad = int(input("|\033[44m Ingrese el cantidad del producto a comprar: \033[0m"))
    except ValueError:
        print("|\033[31m El Tipo de dato es invalido \033[0m")
        return
    
    producto = Producto.find(id_producto)
    
    if not producto:
        print(f"Producto no valido.")
        return
        
    if producto.stock == 0 or producto.stock < cantidad:
        print(f"Producto sin stock.")
        return
    
    producto.stock = (producto.stock - cantidad)
    
    try:
        nombre = str(input("|\033[44m Ingrese nombre del Cliente: \033[0m"))
        correo = str(input("|\033[44m Ingrese correo del Cliente: \033[0m"))
    except ValueError:
        print("|\033[31m El Tipo de dato es invalido \033[0m")
        return
    
    cliente = Cliente(nombre, correo)
    cliente.syc()
    cliente.save()
        
    venta = Venta(cliente.id, producto.id, cantidad, datetime.now())
    venta.save()
    producto.save()
    
    print(f"|\033[32m Venta {venta.id} Registrada \033[0m")
    
def ver_ventas():
    ventas = Venta.lista_ventas()
    
    for venta in ventas:
        print(
            f"| \033[45m({venta['id']}).\033[0m "
            f"\033[33mCliente:\033[0m \033[32m{venta['nombre_cliente']}\033[0m "
            f"\033[33mProducto:\033[0m \033[32m{venta['nombre_producto']}\033[0m "
            f"\033[33mValor:\033[0m \033[32m{venta['precio_unitario']}\033[0m "
            f"\033[33mCantidad:\033[0m \033[32m{venta['cantidad']}\033[0m "
            f"\033[33mTotal:\033[0m \033[32m{venta['total']}\033[0m"
        )
        
def total_ventas():
    return sum(venta['total'] for venta in Venta.lista_ventas())