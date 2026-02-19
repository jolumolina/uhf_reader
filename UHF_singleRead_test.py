'''
Demo code to test UHF for single poll command
To run the code successfully, add the library file of uhf to pico W 
-> https://github.com/sbcshop/UHF_Reader_Pico_W_Software/blob/main/examples/lib/uhf.py
'''
"""
Demo code to test UHF for single poll command
Compatible with uhf.py (class-based implementation)
"""

import time
from uhf import UHF   # importar la clase UHF

reader = None

# Crear instancia del lector
uhf = UHF(
    port="/dev/ttyUSB0",   # cambia si usas otro puerto
    baudrate=115200,
    timeout=0.3
)

SET_REGION_EU ='070001030B'  # configurar región EU

# Ejecutar lectura única
response = uhf.single_read()

print("Respuesta cruda:", response) # imprimir respuesta completa

if response is not None:
    # response es una lista de strings hex
    epc = response[8:20]
    rssi = response[5]
    crc = response[20:22]

    print("EPC =", "".join(epc))
    print("RSSI (dBm) =", rssi)
    print("CRC =", "".join(crc))
else:
    print("No se detectó ninguna etiqueta")

time.sleep(1)
