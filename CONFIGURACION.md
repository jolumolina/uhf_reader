# Configuración del Lector UHF RFID

## Parámetros del Puerto Serial

### Windows
- Puerto típico: **COM3** o **COM4**
- Para encontrar el puerto:
  1. Conecta el lector USB
  2. Abre "Administrador de dispositivos"
  3. Busca "Puertos (COM y LPT)"
  4. Localiza el puerto asignado

### Linux (Raspberry Pi)
- Puerto típico: **/dev/ttyUSB0**
- Para encontrar:
  ```bash
  ls /dev/tty*
  ```

## Parámetros Serial

```python
Baudrate: 115200  # Velocidad fija
Timeout: 0.3      # Timeout en segundos
```

## Regiones Soportadas

- **EU (Europa)**: `070001030B` ← Configurado por defecto
- Consulta el manual del dispositivo para otras regiones

## Pruebas Recomendadas

### 1. Prueba de Conectividad
```bash
python UHF_singleRead_test.py
```

### 2. Lectura Múltiple
```bash
python UHF_multipleRead_test.py
```

### 3. Aplicación Principal
```bash
python main.py
```

## Solución de Problemas

### Error: "Puerto no encontrado"
- Verifica que el dispositivo está conectado
- Comprueba que tienes los drivers USB instalados
- Usa `find_serial_port()` para debug automático

### Error: "SerialException"
- El puerto está en uso por otro programa
- Cierra otras aplicaciones que usen el puerto
- Reinicia el dispositivo

### Sin lectura de etiquetas
- Verifica que la región EU está configurada
- Acerca la etiqueta más al lector
- Revisa los logs para mensajes de error

## Formato de Datos

### EPC (Electronic Product Code)
- Posición en respuesta: bytes 8-20
- Longitud: 12 caracteres hex
- Identificador único de la etiqueta

### RSSI (Received Signal Strength Indicator)
- Posición: byte 5
- Valor en hex
- Rango típico: -30 a -90 dBm

### PC (Protocol Control)
- Posición: bytes 6-7
- Información de control del protocolo

### CRC (Cyclic Redundancy Check)
- Posición: bytes 20-21
- Verificación de integridad
