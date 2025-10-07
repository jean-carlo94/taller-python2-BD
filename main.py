from models import crud
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    print("| *****************************\033[33m Menu:\033[0m ****************************** |")
    print("|                                                                    |")
    print("| \033[42m(1)\033[0m.\033[33m Ver Inventario\033[0m                                                |")
    print("|                                                                    |")
    print("| \033[42m(2)\033[0m.\033[33m Añadir Productos\033[0m                                              |")
    print("|                                                                    |")
    print("| \033[42m(3)\033[0m.\033[33m Vender Productos\033[0m                                              |")
    print("|                                                                    |")
    print("| \033[42m(4)\033[0m.\033[33m Crear Cliente\033[0m                                                 |")
    print("|                                                                    |")
    print("| \033[42m(5)\033[0m.\033[33m Ver Ventas\033[0m                                                    |")
    print("|                                                                    |")
    # print("| \033[42m(6)\033[0m.\033[33m Buscar mascotas\033[0m                                               |")
    # print("|                                                                    |")
    print("| \033[42m(0)\033[0m.\033[33m Salir\033[0m                                                         |")
    print("|                                                                    |")
    print(f"|                                            Total Ventas: \033[32m${crud.total_ventas()}\033[0m |")
    print("|********************************************************************|")
    
def actions():
    menu()
    opt = input("|                                    \033[44m Seleccione una opción:\033[0m")
    print("|********************************************************************|")
    
    if opt == "1":
        print("|                                                                    |")
        print("|\033[42m Crear Productos:\033[0m                                               |")
        print("|                                                                    |")
        
        crud.listar_productos()
        
        print("|                                                                    |")
        print("|                                                                    |")
        
        input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
        clear()
        actions()
        
    elif opt == "2":
        print("|                                                                    |")
        print("|\033[42m Crear Productos:\033[0m                                               |")
        print("|                                                                    |")
        
        crud.crear_producto()
        
        print("|                                                                    |")
        print("|                                                                    |")
        
        input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
        clear()
        actions()
        
    elif opt == "3":
        print("|                                                                    |")
        print("|\033[42m Adoptar Mascota:\033[0m                                                   |")
        print("|                                                                    |")
        
        crud.vender_producto()
        
        print("|                                                                    |")
        print("|                                                                    |")
        
        input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
        clear()
        actions()
        
    elif opt == "4":
        print("|                                                                    |")
        print("|                                                                    |")
        print("|\033[42m Listado de mascotas disponibles:\033[0m                                   |")
        
        crud.crear_cliente()
        
        print("|                                                                    |")
        print("|                                                                    |")
        
        input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
        clear()
        actions()
        
    elif opt == "5":
        print("|                                                                    |")
        print("|\033[42m Listado de mascotas adoptadas:\033[0m                                     |")
        print("|                                                                    |")
        
        crud.ver_ventas()
        
        print("|                                                                    |")
        print("|                                                                    |")
        
        input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
        clear()
        actions()
        
    # elif opt == "6":
    #     print("|                                                                    |")
    #     print("|\033[42m Buscar Mascotas:\033[0m                                    |")
    #     print("|                                                                    |")
        
    #     helpers.buscar_mascota_por_nombre()
        
    #     print("|                                                                    |")
    #     print("|                                                                    |")
        
    #     input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
    #     clear()
    #     actions()
        
    elif opt == "0":
        print("|                                                                    |")
        print("|\033[32m Gracias por visitar el programa de adopción de mascotas.\033[0m           |")
        print("|********************************************************************|")
    else:
        print("|                                                                    |")
        print("|\033[31m Opción no válida. Por favor, intente de nuevo.\033[0m                     |")
        print("|                                                                    |")
        
        input("|\033[46m Presiona ENTER para ver el siguiente...  \033[0m                          |")  
        clear()
        actions()
    

def main():
    print("| ***************** Programa de adopción de mascotas *************** |")
    
    actions()
    
program = main()