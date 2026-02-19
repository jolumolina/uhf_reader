#!/usr/bin/env python3
"""
GUÍA RÁPIDA - Lector UHF RFID Mejorado

Este archivo contiene los pasos para empezar rápidamente.
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║        GUÍA RÁPIDA - LECTOR UHF RFID MEJORADO                 ║
╚════════════════════════════════════════════════════════════════╝

📋 PASOS RÁPIDOS PARA EMPEZAR:

1️⃣  VERIFICAR INSTALACIÓN
   python diagnostico.py
   
   ✅ Debería mostrar:
   - ✅ pyserial instalado
   - ✅ Puerto disponible detectado
   - ✅ Módulo UHF importable
   - ✅ Conversiones funcionando
   - ✅ Logging activo

2️⃣  CONECTAR HARDWARE
   - Conecta el lector UHF por USB
   - Espera a que se reconozca en el sistema

3️⃣  EJECUTAR APLICACIÓN
   python main.py
   
   📺 Verás un menú:
   ==============================
      APLICACIÓN RFID UHF MEJORADA
   ==============================
   1. Lectura simple
   2. Lectura múltiple
   3. Detener lectura
   4. Salir

4️⃣  LEER ETIQUETAS
   
   Opción 1 - Lectura Simple:
   - Acerca UNA etiqueta al lector
   - Verás: EPC, RSSI, CRC
   - Se lee 1 vez y detiene
   
   Opción 2 - Lectura Múltiple:
   - Lee continuamente
   - Presiona Ctrl+C para detener
   - Muestra: EPC, RSSI, CRC, PC

╔════════════════════════════════════════════════════════════════╗
║                      EJEMPLO DE SALIDA                         ║
╚════════════════════════════════════════════════════════════════╝

--- LECTURA MÚLTIPLE ---
EPC: 012345678901ABCDEF00
RSSI (hex): A2
RSSI (dBm): -94
CRC: 1234
PC: 3000
----------------------------------------
EPC: 987654321FEDCBA0F00
RSSI (hex): 95
RSSI (dBm): -107
CRC: 5678
PC: 3000
----------------------------------------

╔════════════════════════════════════════════════════════════════╗
║                  ARCHIVOS IMPORTANTES                          ║
╚════════════════════════════════════════════════════════════════╝

main.py                 → Aplicación principal
uhf.py                  → Librería UHF mejorada
diagnostico.py          → Verificación del sistema

RESUMEN_FINAL.md        → 📊 Resumen ejecutivo de mejoras
MEJORAS_REALIZADAS.md   → 📋 Detalle técnico de cambios
CONFIGURACION.md        → ⚙️  Guía de configuración
CHECKLIST.md            → ✅ Verificación de cambios

╔════════════════════════════════════════════════════════════════╗
║              SOLUCIÓN DE PROBLEMAS RÁPIDA                      ║
╚════════════════════════════════════════════════════════════════╝

❌ Problema: "Puerto no encontrado"
✅ Solución: 
   1. Conecta el lector USB
   2. Ejecuta: python diagnostico.py
   3. Nota el puerto detectado

❌ Problema: "SerialException"
✅ Solución:
   1. Desconecta el lector
   2. Espera 3 segundos
   3. Reconecta
   4. Intenta de nuevo

❌ Problema: "No se leen etiquetas"
✅ Solución:
   1. Acerca la etiqueta más (<10cm)
   2. Verifica que es etiqueta UHF
   3. Revisa los logs para errores

❌ Problema: "pyserial no encontrado"
✅ Solución:
   pip install pyserial

╔════════════════════════════════════════════════════════════════╗
║                    DATOS IMPORTANTES                           ║
╚════════════════════════════════════════════════════════════════╝

EPC (Electronic Product Code)
  → Identificador único de la etiqueta
  → 12 caracteres hexadecimales
  → Ejemplo: 012345678901

RSSI (Received Signal Strength Indicator)
  → Fortaleza de la señal
  → Rango típico: -30 a -90 dBm
  → Valor más negativo = señal más débil

PC (Protocol Control)
  → Información de control del protocolo
  → Típicamente: 3000

CRC (Cyclic Redundancy Check)
  → Verificación de integridad de datos
  → Detecta errores en transmisión

╔════════════════════════════════════════════════════════════════╗
║                  MEJORAS IMPLEMENTADAS                         ║
╚════════════════════════════════════════════════════════════════╝

✅ Auto-detección de puerto serial
✅ Soporte Windows + Linux
✅ Manejo robusto de excepciones
✅ Logging completo
✅ Detección automática de región EU
✅ Interfaz de usuario mejorada
✅ Validación de datos completa
✅ Cierre seguro del puerto

╔════════════════════════════════════════════════════════════════╗
║                    PRÓXIMOS PASOS                              ║
╚════════════════════════════════════════════════════════════════╝

1. Lee la documentación completa:
   - RESUMEN_FINAL.md (visión general)
   - MEJORAS_REALIZADAS.md (detalles técnicos)

2. Ejecuta el diagnóstico:
   python diagnostico.py

3. Prueba la aplicación:
   python main.py

4. Sugerencias para mejorar:
   - Agregar base de datos de etiquetas
   - Crear interfaz gráfica
   - Exportar datos a CSV/JSON

╔════════════════════════════════════════════════════════════════╗
║              ¿PREGUNTAS O PROBLEMAS?                           ║
╚════════════════════════════════════════════════════════════════╝

1. Revisa los logs (mensajes con timestamp)
2. Ejecuta: python diagnostico.py
3. Consulta CONFIGURACION.md
4. Revisa RESUMEN_FINAL.md

═══════════════════════════════════════════════════════════════

                    🎉 ¡LISTO PARA USAR! 🎉

═══════════════════════════════════════════════════════════════
""")
