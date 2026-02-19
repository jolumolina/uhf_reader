import time
import logging
from uhf_mejorado import UHF

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =========================
# Configuración del lector
# =========================
reader = None

# Detectar puerto automáticamente en Windows
import platform
import os

# Flag: si True, leer TID automáticamente tras una lectura simple
AUTO_READ_TID = True

def find_serial_port():
    """Detecta automáticamente el puerto serial disponible"""
    if platform.system() == "Windows":
        # En Windows, intenta COM1 a COM10
        for i in range(1, 11):
            port = f"COM{i}"
            try:
                test_serial = __import__('serial').Serial(port, timeout=0.1)
                test_serial.close()
                logger.info(f"Puerto serial encontrado: {port}")
                return port
            except:
                pass
    else:
        # En Linux, intenta /dev/ttyUSB0 y /dev/ttyUSB1
        for port in ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyACM0"]:
            try:
                test_serial = __import__('serial').Serial(port, timeout=0.1)
                test_serial.close()
                logger.info(f"Puerto serial encontrado: {port}")
                return port
            except:
                pass
    logger.warning("No se encontró puerto serial automáticamente")
    return None

# Intentar auto-detección o usar puerto por defecto
serial_port = find_serial_port() or "/dev/ttyUSB0"

try:
    uhf = UHF(
        port=serial_port,
        baudrate=115200,
        timeout=0.3
    )
    uhf.setRegion_EU()  # Configurar región EU
except Exception as e:
    logger.error(f"Error al inicializar UHF: {e}")
    uhf = None

# =========================
# Funciones auxiliares
# =========================
def hex_to_signed_decimal(hex_number, bit_width):
    """Convierte hexadecimal a decimal con signo (complemento a dos)"""
    try:
        decimal_number = int(hex_number, 16) 
        max_value = 2 ** (bit_width - 1) 
        if decimal_number >= max_value:
            decimal_number -= 2 ** bit_width
        return decimal_number
    except (ValueError, TypeError) as e:
        logger.error(f"Error en conversión hex: {e}")
        return 0


def validate_epc(epc: str) -> str:
    """Valida y normaliza un EPC proporcionado por el usuario.

    Retorna la cadena EPC normalizada (sin 0x ni espacios, en mayúsculas)
    o None si no es válida.
    """
    if not epc:
        return None
    epc_clean = epc.replace('0x', '').replace(' ', '').upper()
    # Debe tener longitud par y al menos 2 caracteres
    if len(epc_clean) == 0 or len(epc_clean) % 2 != 0:
        return None
    try:
        int(epc_clean, 16)
        return epc_clean
    except ValueError:
        return None


def leer_tid_por_epc(epc_hex):
    """Selecciona la etiqueta por EPC y lee el banco TID.

    epc_hex: cadena hex sin separadores, por ejemplo '300833B2DDD9014000000000'
    Retorna: TID en hex o mensaje de error.
    """
    if uhf is None:
        return "UHF no inicializado"
    try:
        # Validar y normalizar EPC
        epc_clean = validate_epc(epc_hex)
        if epc_clean is None:
            return 'EPC inválido'
        sel = uhf.Set_select_pera(epc_clean)
        # Aceptar cualquier respuesta positiva (True, 'Select sucessfull', etc.)
        if not sel:
            return 'No se pudo seleccionar la etiqueta'
        tid = uhf.Read_tag_data('2')  # Banco TID
        return tid or 'No data'
    except Exception as e:
        return f"Error al leer TID: {e}"
# =========================
# Lectura simple
# =========================
def lectura_simple():
    """Realiza una lectura simple de una etiqueta RFID"""
    if uhf is None:
        logger.error("UHF no inicializado")
        return
        
    print("\n--- LECTURA SIMPLE ---")

    try:
        response = uhf.single_read()
        print("Respuesta cruda:", response)

        if response is not None:
            epc = response[8:20]
            rssi = response[5]
            crc = response[20:22]
            
            rssi_dec = hex_to_signed_decimal(rssi, 8)
            
            print("EPC =", "".join(epc))
            print("RSSI (hex) =", rssi)
            print("RSSI (dBm) =", rssi_dec)
            print("CRC =", "".join(crc))
            # Si está activada la lectura automática de TID, intentar leerlo
            if AUTO_READ_TID:
                try:
                    tid = leer_tid_por_epc("".join(epc))
                    print("TID:", tid)
                except Exception as e:
                    logger.error(f"Error leyendo TID automáticamente: {e}")
        else:
            print("No se detectó ninguna etiqueta")
    except Exception as e:
        logger.error(f"Error en lectura simple: {e}")

    time.sleep(1)


# =========================
# Lectura múltiple
# =========================
def lectura_multiple():
    """Realiza lectura múltiple de etiquetas RFID hasta presionar Ctrl+C"""
    if uhf is None:
        logger.error("UHF no inicializado")
        return
        
    print("\n--- LECTURA MÚLTIPLE (Ctrl+C para detener) ---")
    
    try:
        uhf.multiple_read() # Iniciar lectura múltiple

        while True:
            rev = uhf.read_mul() # storing the data frame in the array rev
            if rev is not None:
                epc = "".join(rev[8:20])
                rssi_hex = rev[5]
                rssi_dec = hex_to_signed_decimal(rssi_hex, 8)
                crc = rev[20:22]
                pc = rev[6:8]
                
                print(f"EPC: {epc}")
                print(f"RSSI (hex): {rssi_hex}")
                print(f"RSSI (dBm): {rssi_dec}")
                print(f"CRC: {''.join(crc)}")
                print(f"PC: {''.join(pc)}")
                print("-" * 40)

            time.sleep(0.05)  # Espera pequeña para evitar saturación

    except KeyboardInterrupt:
        stop_lectura()
    except Exception as e:
        logger.error(f"Error en lectura múltiple: {e}")
        stop_lectura()

# =========================
# Stop lectura
# =========================
def stop_lectura():
    """Detiene la lectura múltiple de forma ordenada"""
    if uhf is None:
        return
    try:
        uhf.stop_read()
        time.sleep(1)
        print("\nLectura detenida correctamente")
    except Exception as e:
        logger.error(f"Error al detener lectura: {e}")

# =========================
# Menú principal
# =========================
def menu():
    """Muestra el menú principal"""
    print("\n" + "="*35)
    print("   APLICACIÓN RFID UHF MEJORADA")
    print("="*35)
    print("1. Lectura simple")
    print("2. Lectura múltiple")
    print("3. Detener lectura")
    print("4. Salir")
    print("5. Leer TID por EPC")
    print("="*35)

# =========================
# Programa principal
# =========================
def main():
    """Función principal - loop del programa"""
    if uhf is None:
        logger.error("No se pudo inicializar el lector UHF. Abortando.")
        return
    
    while True:
        try:
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
            elif opcion == "5":
                epc_in = input("Introduce EPC (hex): ").strip()
                if epc_in:
                    result_tid = leer_tid_por_epc(epc_in)
                    print(f"TID: {result_tid}")

            else:
                print("❌ Opción no válida. Intente de nuevo.")
                
        except KeyboardInterrupt:
            print("\n\nInterrupción del usuario detectada.")
            break
        except Exception as e:
            logger.error(f"Error inesperado en main: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error fatal: {e}")
    finally:
        if uhf is not None:
            try:
                uhf.ser.close()
                logger.info("Puerto serial cerrado")
            except:
                pass
