'''
Demo to Several Time polling command of UHF reader
To run the code successfully, add the library file of uhf to pico W 
-> https://github.com/sbcshop/UHF_Reader_Pico_W_Software/blob/main/examples/lib/uhf.py
'''
#Import the uhf library along with some inbuilt libraries.
import time
from uhf import UHF

reader = None

SET_REGION_EU ='070001030B'  #for Setting EU Region

# Crear instancia del lector
uhf = UHF(
    port="/dev/ttyUSB0",   # cambia si usas otro puerto
    baudrate=115200,
    timeout=0.3
)

def hex_to_signed_decimal(hex_number, bit_width):
    # Convert the hexadecimal number to a decimal integer
    decimal_number = int(hex_number, 16)
    
    # Calculate the maximum value for a signed integer of the given bit width
    max_value = 2 ** (bit_width - 1)
    
    # If the decimal number is greater than or equal to max_value, it is negative in two's complement
    if decimal_number >= max_value:
        decimal_number -= 2 ** bit_width

    return decimal_number
    
uhf.multiple_read() # Calling Method to initialise the multiple read by sending related UHF command 
try:
    while 1:
        rev = uhf.read_mul()  # storing the data frame in the array rev
        if rev is not None:
            print('EPC = ',"".join(rev[8:20])) # Extracting the EPC value from 8th bit to 20th bit & print it
            print('RSSI(dBm) = ',rev[5])       # Extracting the RSSI value stored at 5th bit & print it.
            rssi_dec = hex_to_signed_decimal(rev[5], 8)
            print("RSSI(decimal) = ", rssi_dec)
            print('CRC = ',rev[20],rev[21])    # Extracting the CRC values stored at 20th & 21st bit & print the same
            print('PC = ',rev[6],rev[7])	   # Extracting the PC  stored at 6th & 7th 
            print("\n")
        time.sleep(0.000001 )
        
except KeyboardInterrupt:
    uhf.stop_read()
    time.sleep(1)
    print("stop")

