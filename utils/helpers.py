import os

def validar_input_string(prompt):
    while True:
        dato = input("").strip()
        if dato:
            return dato
        print("Ingrese un texto valido.")

def validar_input_int(prompt):
    while True:
        try:
            dato = int(input(""))
            if dato >= 0:
                return dato
            print("Ingrese un numero mayor o igual a 0.")
        except ValueError:
            print("Ingrese un numero valido.")
            
def validar_input_float(prompt):
    while True:
        try:
            dato = float(input(""))
            if dato >= 0:
                return dato
            print("Ingrese un numero mayor o igual a 0.")
        except ValueError:
            print("Ingrese un numero valido.")