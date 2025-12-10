def validar_input_string(prompt):
    """
    Solicita al usuario una cadena de texto y valida que no esté vacía.

    Args:
        prompt (str): El mensaje que se muestra al usuario antes de pedir la entrada.

    Returns:
        str: La cadena de texto válida ingresada por el usuario.
    """
    while True:
        # Se muestra el mensaje (prompt) y se captura la entrada, eliminando espacios iniciales/finales.
        dato = input(prompt).strip()
        if dato:
            # Si la cadena no está vacía, se devuelve como válida.
            return dato
        # Si está vacía, se imprime un mensaje de error y el bucle se repite.
        print("Ingrese un texto valido.")

def validar_input_int(prompt):
    """
    Solicita al usuario un número entero (int) y valida que sea válido y no negativo.

    Args:
        prompt (str): El mensaje que se muestra al usuario.

    Returns:
        int: El número entero válido ingresado por el usuario.
    """
    while True:
        try:
            # Intenta convertir la entrada del usuario a un entero.
            dato = int(input(prompt))
            if dato >= 0:
                # Si es un entero válido y mayor o igual a 0, se devuelve.
                return dato
            # Si es negativo, se imprime un error específico.
            print("Ingrese un numero mayor o igual a 0.")
        except ValueError:
            # Si la conversión a int falla (ej. el usuario ingresa letras), se captura la excepción.
            print("Ingrese un numero valido.")
            
def validar_input_float(prompt):
    """
    Solicita al usuario un número decimal (float) y valida que sea válido y no negativo.

    Args:
        prompt (str): El mensaje que se muestra al usuario.

    Returns:
        float: El número decimal válido ingresado por el usuario.
    """
    while True:
        try:
            # Intenta convertir la entrada del usuario a un float.
            dato = float(input(prompt))
            if dato >= 0:
                # Si es un float válido y mayor o igual a 0, se devuelve.
                return dato
            # Si es negativo, se imprime un error específico.
            print("Ingrese un numero mayor o igual a 0.")
        except ValueError:
            # Si la conversión a float falla, se captura la excepción.
            print("Ingrese un numero valido.")