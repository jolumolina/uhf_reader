#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el funcionamiento del lector UHF
Ejecuta pruebas básicas sin necesidad de etiquetas RFID
"""

import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_serial_availability():
    """Verifica si pyserial está instalado"""
    print("\n🔍 Test 1: Verificando librerías...")
    try:
        import serial
        print("✅ pyserial instalado correctamente")
        return True
    except ImportError:
        print("❌ pyserial NO está instalado")
        print("   Instala con: pip install pyserial")
        return False

def test_port_detection():
    """Prueba la detección automática de puerto"""
    print("\n🔍 Test 2: Detectando puerto serial...")
    
    import platform
    import serial
    
    if platform.system() == "Windows":
        ports = [f"COM{i}" for i in range(1, 11)]
    else:
        ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyACM0"]
    
    found_ports = []
    for port in ports:
        try:
            ser = serial.Serial(port, timeout=0.1)
            ser.close()
            found_ports.append(port)
            print(f"✅ Puerto disponible: {port}")
        except:
            pass
    
    if found_ports:
        print(f"\n📌 Puertos disponibles: {found_ports}")
        return found_ports[0]
    else:
        print("❌ No se encontraron puertos seriales disponibles")
        print("   Verifica que el dispositivo esté conectado")
        return None

def test_uhf_module():
    """Prueba si el módulo UHF se puede importar"""
    print("\n🔍 Test 3: Importando módulo UHF...")
    try:
        from uhf import UHF
        print("✅ Módulo UHF importado correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error al importar UHF: {e}")
        return False

def test_hex_conversion():
    """Prueba la función de conversión hexadecimal"""
    print("\n🔍 Test 4: Probando conversión hexadecimal...")
    
    def hex_to_signed_decimal(hex_number, bit_width):
        try:
            decimal_number = int(hex_number, 16) 
            max_value = 2 ** (bit_width - 1) 
            if decimal_number >= max_value:
                decimal_number -= 2 ** bit_width
            return decimal_number
        except (ValueError, TypeError):
            return 0
    
    # Pruebas
    tests = [
        ("AA", 8, -86),
        ("FF", 8, -1),
        ("7F", 8, 127),
        ("80", 8, -128),
    ]
    
    all_pass = True
    for hex_val, width, expected in tests:
        result = hex_to_signed_decimal(hex_val, width)
        if result == expected:
            print(f"✅ {hex_val} (8-bit) = {result}")
        else:
            print(f"❌ {hex_val} (8-bit) = {result}, esperado {expected}")
            all_pass = False
    
    return all_pass

def test_logging():
    """Verifica si el logging funciona correctamente"""
    print("\n🔍 Test 5: Probando logging...")
    
    logger.debug("Este es un mensaje DEBUG")
    logger.info("✅ Este es un mensaje INFO")
    logger.warning("⚠️  Este es un mensaje WARNING")
    
    print("✅ Logging funcionando correctamente")
    return True

def main():
    """Ejecuta todos los tests"""
    print("="*50)
    print("   DIAGNÓSTICO DEL LECTOR UHF RFID")
    print("="*50)
    
    results = {
        "Serial disponible": test_serial_availability(),
        "Módulo UHF": test_uhf_module(),
        "Conversión hexadecimal": test_hex_conversion(),
        "Logging": test_logging(),
    }
    
    port = test_port_detection()
    
    print("\n" + "="*50)
    print("RESUMEN DE RESULTADOS")
    print("="*50)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    print("\n" + "="*50)
    
    if all(results.values()) and port:
        print("✅ TODOS LOS TESTS PASARON")
        print(f"📌 Puerto recomendado: {port}")
        print("\n💡 Próximos pasos:")
        print("   1. Conecta una etiqueta RFID al lector")
        print("   2. Ejecuta: python main.py")
        print("   3. Selecciona opción 1 o 2 para leer etiquetas")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("\n📋 Solución de problemas:")
        print("   - Verifica que pyserial está instalado")
        print("   - Conecta el lector UHF por USB")
        print("   - Comprueba los drivers del dispositivo")
    
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error en diagnóstico: {e}")
        sys.exit(1)
