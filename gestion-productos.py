"""
#############################################################
######  Preentrega para Talento Tech - Comisión 26209  ######
#############################################################

Testeado en Linux (Arch) y Windows 10 

NOTA: se qué pedía que no tuviese centavos, pero opcionalmente 
si se pueden ingresar, tanto con "." como con ",".       
"""

#############################################################
#############################################################
##                                                         ##
##  Programa en Python para gestión de productos con JSON  ##
##                                                         ##
#############################################################
#############################################################

import os
import json

ARCHIVO = "productos.json"

def normalizar_texto(texto):
    sustituciones = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "ü": "u", "Ü": "U",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U",
        "ñ": "n", "Ñ": "N",
    }
    for original, comun in sustituciones.items():
        texto = texto.replace(original, comun)
    return texto.strip().lower()

def normalizar_precio(precio):
    if precio.count(".") > 1 or precio.count(",") > 1:
       return "ERROR"
    precio = precio.strip().replace(",", "")
    precio = precio.strip().replace(".", "")
    # print("PRECIO NORMALIZADO >>>> ", precio) # Para debugueo
    if not precio.isdecimal():
       return "ERROR"
    return precio 

def imprime_menu (tipo=""):
    print("\n░▒▒▓▓▓████ SISTEMA DE GESTIÓN DE PRODUCTOS ████▓▓▓▒▒░")
    print("")
    print("1. Agregar")
    print("2. Mostrar")
    print("3. Buscar")
    print("4. Eliminar")
    print("5. Salir")
    print("")
    if tipo != "":
       print(">", tipo)
       print("")
       
def pausa(opcion=""):
    if opcion != "":
        input("")
    else:    
        input("\nPresioná ENTER para continuar...")
    
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_productos():
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, ValueError):
        limpiar_pantalla()
        print("⚠️  JSON incorrecto, se inicia sin lista.")
        pausa()
        return []

def guardar_productos(lista):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, ensure_ascii=False, indent=4)

productos = cargar_productos()

Salir = False

while not Salir:
    limpiar_pantalla()
    imprime_menu()
    opcion = input("> ").strip()

    match opcion:

        ### OPCIÓN 1: Agrega producto ###
        case "1":
             print("\n░▒▓█ Agregar producto █▓▒░")
             print("")
             nombre = input("Ingresá el nombre del producto: ").strip()
             if nombre == "":
                print("❌ ¡El nombre ingresado es incorrecto!")
                pausa()
                continue

             categoria = input("Ingrese la categoría del producto: ").strip()
             if categoria == "":
                print("❌ ¡La categoría ingresada es incorrecta!")
                pausa()
                continue

             precio_texto = input("Ingresá el precio (sin centavos): ").strip()
             precio_normalizado = normalizar_precio(precio_texto)
             if precio_normalizado == "ERROR":
                print("❌ ¡El precio ingresado es incorrecto!")
                pausa()
                continue
            
             precio_texto = precio_texto.strip().replace(",", ".")
             precio = float(precio_texto)
             productos.append([nombre, categoria, precio])
             guardar_productos(productos)
             print(f"✔️  Producto '{nombre}' agregado.")
             pausa()

        ### OPCIÓN 2: Muestra productos ###
        case "2":
             print("\n░▒▓█ Listar productos █▓▒░")
             if len(productos) == 0:
                print("")
                print("❌ No hay productos registrados.")
                pausa()
             else:
                 print("\nProductos registrados:")
                 print("")
                 for i in range(len(productos)):
                     print(f"   {i + 1}. Nombre: {productos[i][0]} | Categoría: {productos[i][1]} | Precio: ${productos[i][2]}")
                 pausa()
                 
        ### OPCIÓN 3: Busca producto ###
        case "3":
             sigue_preguntando = True
             while (sigue_preguntando):
                   limpiar_pantalla()
                   imprime_menu("3")
                   print("░▒▓█ Búsqueda de productos █▓▒░")
                   print("")
                   busqueda = normalizar_texto(input("Ingrese el nombre a buscar: "))
                   if busqueda == "":
                      print("❌ ¡La búsqueda no puede estar vacía!")
                      pausa()
                   else:
                       sigue_preguntando = False
                      

             encontrados = False
             for i in range(len(productos)):
                 if busqueda in normalizar_texto(productos[i][0]):
                     print(f"{i + 1}. Nombre: {productos[i][0]} | Categoría: {productos[i][1]} | Precio: ${productos[i][2]}")
                     encontrados = True
           
             if not encontrados:
                print("❌ ¡No se encontraron resultados!")
          
             pausa()
            
        ### OPCIÓN 4: Elimina producto ###
        case "4":
             sigue_preguntando = True
             while (sigue_preguntando):
                   limpiar_pantalla()
                   imprime_menu("4")
                   print("\n░▒▓█ Eliminar producto █▓▒░")
                   print("")
                   if len(productos) == 0:
                      print("❌ No hay productos para eliminar.")
                      pausa()
                      sigue_preguntando = False
                      continue

                   print("Productos disponibles:\n")
                   for i in range(len(productos)):
                       print(f"   {i + 1}. {productos[i][0]}")
                   opcion_salida = len(productos) + 1
                   print(f"   {opcion_salida}. Salir")
                   print("")
             
                   posicion_texto = input("Ingresá el número del producto para eliminar: ").strip()
                   posicion = 0 
                   if not posicion_texto.isdigit():
                      print("❌ ¡Opcion errónea, debe ser un número entero dentro del rango!")
                      posicion = -1 
                      pausa()
                   else:
                      posicion = int(posicion_texto)
                      if (posicion < 1 or posicion > opcion_salida):
                         print("❌ ¡Opcion fuera de rango!")
                         pausa()
                      else:
                          if posicion == opcion_salida:
                             sigue_preguntando = False
                             continue
                          eliminado = productos.pop(posicion - 1)
                          guardar_productos(productos)
                          print(f"✔️  Producto '{eliminado[0]}' eliminado.")
                          pausa()
                          sigue_preguntando = False

        ### OPCIÓN 5: Salir ###
        case "5":
             print("")
             print("¡Saliste del sistema! 🏃🚪")
             Salir = True 
             continue

        ### OPCIÓN INCORRECTA ###
        case _:
             print("❌ Opción errónea")
             pausa("No muestra texto de input")
