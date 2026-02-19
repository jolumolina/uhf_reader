import time
from uhf import UHF

# =========================
# Configuración del lector
# =========================
reader = None

uhf = UHF(
    port="/dev/ttyUSB0",
    baudrate=115200,
    timeout=0.3
)

SET_REGION_EU ='070001030B'  # configurar región EU

reading_multiple = False

# =========================
# Funciones auxiliares
# =========================
def hex_to_signed_decimal(hex_number, bit_width): 
    # Convierte hex a decimal con signo
    decimal_number = int(hex_number, 16) 
    # Calculate the maximum value for a signed integer of the given bit width
    max_value = 2 ** (bit_width - 1) 
    # # If the decimal number is greater than or equal to max_value, it is negative in two's complement
    if decimal_number >= max_value:
        decimal_number -= 2 ** bit_width
    
    return decimal_number
'''
def leer_tid_por_epc(epc):
    """sudo 
    Selecciona la etiqueta por EPC y lee la memoria TID
    """
    try:
        sel = uhf.Set_select_pera(epc)
        if sel != "Select sucessfull":
            return "No se pudo seleccionar"

        tid = uhf.Read_tag_data('2')  # Banco TID
        return tid if tid else "TID vacío"

    except Exception as e:
        return f"Error TID"
'''
# =========================
# Lectura simple
# =========================
def lectura_simple():
    print("\n--- LECTURA SIMPLE ---")

    response = uhf.single_read()
    print("Respuesta cruda:", response)

    if response is not None:
        epc = response[8:20]
        rssi = response[5]
        crc = response[20:22]
        '''
        rssi_dec = hex_to_signed_decimal(rssi_hex)
        tid = leer_tid_por_epc(epc)
        '''
        print("EPC =", "".join(epc))
        print("RSSI (dBm) =", rssi)
        print("CRC =", "".join(crc))
    else:
        print("No se detectó ninguna etiqueta")

    time.sleep(1)


# =========================
# Lectura múltiple
# =========================
def lectura_multiple():
    #global reading_multiple
    print("\n--- LECTURA MÚLTIPLE (Ctrl+C para detener) ---")
    
    #reading_multiple = True
    uhf.multiple_read() # Iniciar lectura múltiple

    try:
        while 1:
            rev = uhf.read_mul() # storing the data frame in the array rev
            if rev is not None:
                print("EPC =", "".join(rev[8:20])) # Extracting the EPC value from 8th bit to 20th bit & print it
                print("RSSI(hex) =", rev[5])       # Extracting the RSSI value stored at 5th bit & print it.
                rssi_dec = hex_to_signed_decimal(rev[5], 8)
                print("RSSI(decimal) =", rssi_dec)
                print("CRC =", rev[20], rev[21]) # Extracting the CRC values stored at 20th & 21st bit & print the same
                print("PC =", rev[6], rev[7]) # Extracting the PC  stored at 6th & 7th
                print("\n")

            time.sleep(0.000001)

    except KeyboardInterrupt:
        stop_lectura()

# =========================
# Stop lectura
# =========================
def stop_lectura():
    #global reading_multiple
    #reading_multiple = False
    uhf.stop_read()
    time.sleep(1)
    print("\nLectura detenida")

# =========================
# Menú principal
# =========================
def menu():
    print("\n==============================")
    print("   APLICACIÓN RFID UHF")
    print("==============================")
    print("1. Lectura simple")
    print("2. Lectura múltiple")
    print("3. Stop lectura")
    print("4. Salir")
    print("==============================")

# =========================
# Programa principal
# =========================
def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            lectura_simple()

        elif opcion == "2":
            lectura_multiple()

        elif opcion == "3":
            stop_lectura()

        elif opcion == "4":
            stop_lectura()
            print("Saliendo de la aplicación...")
            break

        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
