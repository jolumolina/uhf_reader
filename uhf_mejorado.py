#uhf library file - VERSIÓN MEJORADA

import serial
import time
import binascii
import array
import threading
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

'''
standard commands for UHF operations, refer command manual for more details
https://github.com/sbcshop/UHF_Reader_Pico_W_Software/blob/main/documents/UHF%20Commands%20Manual.pdf
So, you can add more commands for other operation
'''

STARTBYTE     ='AA00' # combine Header + Type
ENDBYTE       ='DD'

'''2.1 Get the reader module information'''
HARD_VERSION  ='0300010004'

''' 2.2 Single polling command '''
SINGLE_READ   ='22000022'

''' 2.3 Several times polling command '''
MULTIPLE_READ ='27000322271083'

STOP_READ     ='28000028'

'''section: 2.12 Set Working Place'''
SET_REGION_EU = '070001030B' #for Setting EU Region

'''Section: 2.16 Get transmitting power '''
GET_TRANSMIT_PWR = 'B70000B7'
1
class UHF:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=0.3):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            self.running = False
            logger.info(f"Puerto serial {port} abierto exitosamente")
        except serial.SerialException as e:
            logger.error(f"Error al abrir puerto serial: {e}")
            raise

    def single_read(self):
        """Lee una sola etiqueta RFID"""
        try:
            data = self.send_command([STARTBYTE, SINGLE_READ, ENDBYTE])
            time.sleep(0.5)
            rec_data = self.ser.read(24)
            
            if rec_data is not None and len(rec_data) > 22:
                if rec_data[0] != 0xaa or rec_data[23] != 0xdd or rec_data[1] != 0x02:
                    logger.warning("Respuesta de lectura inválida")
                    return None        
                return ['{:02x}'.format(x) for x in rec_data]
            return None
        except Exception as e:
            logger.error(f"Error en lectura simple: {e}")
            return None
        
    def read_mul(self):
        """Lee múltiples etiquetas RFID"""
        try:
            rec_data = self.ser.read(24)
            if rec_data is not None and len(rec_data) > 22:
                if rec_data[0] != 0xaa or rec_data[23] != 0xdd or rec_data[1] != 0x02:
                    return None        
                return ['{:02x}'.format(x) for x in rec_data]
            return None
        except Exception as e:
            logger.error(f"Error en lectura múltiple: {e}")
            return None
        
    def stop_read(self):
        """Detiene la lectura múltiple"""
        try:
            data = self.send_command([STARTBYTE, STOP_READ, ENDBYTE])
            time.sleep(0.5)
            rec_data = self.ser.read(24)
            logger.info("Lectura detenida")
        except Exception as e:
            logger.error(f"Error al detener lectura: {e}")    
    
    #####################################################
    def calculate_checksum(self, data):
        """Calcula el checksum de los datos"""
        checksum = 0
        for byte in data:
            checksum += byte
        return checksum % 256

    def calculation(self, Data):
        """Calcula y retorna el checksum en formato hexadecimal"""
        try:
            bin_data1 = binascii.unhexlify(Data)
            chk_1 = self.calculate_checksum(bin_data1)
            return '{:02x}'.format(chk_1)
        except Exception as e:
            logger.error(f"Error al calcular checksum: {e}")
            return '00'
    ######################################################

    def send_command(self, data):
        """Envía comando al dispositivo UHF"""
        try:
            Data = ''.join(data)
            bin_data = binascii.unhexlify(Data)
            response = self.ser.write(bin_data)
            return response
        except Exception as e:
            logger.error(f"Error al enviar comando: {e}")
            return None


    
    def Kill_card(self):
        """Desactiva una etiqueta RFID (comando de sacrificio)"""
        try:
            fig = '6500040000FFFF'   
            dat = self.calculation(fig)
            dat1 = STARTBYTE+fig+dat+ENDBYTE
            data = self.send_command(dat1)
            time.sleep(0.2)
            rec_data = self.ser.read(24)
            if rec_data is not None:
                    a = ['{:02x}'.format(x) for x in rec_data]
                    logger.info(f"Kill card response: {a}")
        except Exception as e:
            logger.error(f"Error en Kill_card: {e}")
                
    ####################################################################
    def Set_select_pera(self, tag_uid):
        """Selecciona una etiqueta por su UID"""          
        try:
            fig = '0C001300000000206000'+ tag_uid
            dat = self.calculation(fig)
            dat1 = STARTBYTE+fig+dat+ENDBYTE
            data = self.send_command(dat1)
            time.sleep(0.2)
            rec_data = self.ser.read(16)
            if rec_data is not None:
                    a = ['{:02x}'.format(x) for x in rec_data]
                    if "".join(a) == 'aa010c0001000edd':   
                         return 'Select sucessfull'
                    else:
                        logger.warning(f"Select failed: {''.join(a)}")
                        return 'invalid'
        except Exception as e:
            logger.error(f"Error en Set_select_pera: {e}")
            return 'error'
                
    
    def Read_tag_data(self, memory_bank):
        """Lee datos de memoria de la etiqueta (banco 1: EPC, 2: TID, 3: USER)"""
        try:
            fig = '390009000000000'+memory_bank+'00000002'   # leer 2 palabras
            dat = self.calculation(fig)
            dat1 = STARTBYTE+fig+dat+ENDBYTE
            
            data = self.send_command(dat1)
            time.sleep(0.2)
            rec_data = self.ser.read(40)
            if rec_data is not None:
                    a = ['{:02x}'.format(x) for x in rec_data]
                    if "".join(a) == 'aa01ff0001090add':
                         logger.warning("No card detected")
                         return 'No card is there'
                    else:
                        if memory_bank == '2': # TID bank 
                            return "".join(a)[40:72]   # TID data    
                        elif memory_bank == '3': # USER bank
                            return "".join(a)[40:70]  # USER data
                        elif memory_bank == '1': # EPC bank
                            return "".join(a)[48:72]
        except Exception as e:
            logger.error(f"Error en Read_tag_data: {e}")
            return 'error'
                    


    def Write_tag_data(self, data_w, memory_bank):
        """Escribe datos en la memoria de la etiqueta"""
        try:
            fig = '490019000000000'+memory_bank+'00000008'+ data_w      
            dat = self.calculation(fig)
            dat1 = STARTBYTE+fig+dat+ENDBYTE
            data = self.send_command(dat1)
            time.sleep(0.2)
            rec_data = self.ser.read(23)
            if rec_data is not None:
                    a = ['{:02x}'.format(x) for x in rec_data]
                    logger.info(f"Write response: {a}")
                    if "".join(a) == 'aa01ff00011011dd':  
                         return 'Write card failed,No tag response'
                    elif "".join(a) == 'aa01ff00011718dd':   
                         return 'Command error'
                    elif a[2] == '49':
                        return 'Card sucessfull write'
        except Exception as e:
            logger.error(f"Error en Write_tag_data: {e}")
            return 'error'

    ################################################################################

    def hardware_version(self):
        """Obtiene la versión del hardware"""
        try:
            self.send_command([STARTBYTE, HARD_VERSION, ENDBYTE])
            time.sleep(0.5)
            d = self.ser.read(19)
            if d is not None: 
                def split_bytes_data(data, packet_size):
                    packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
                    return packets
                ds = split_bytes_data(d, 6)
                s = []
                for i in range(1, len(ds)):
                       s.append(str(ds[i], 'latin-1'))
                return "".join(s)
        except Exception as e:
            logger.error(f"Error en hardware_version: {e}")
            return None

    def multiple_read(self):
        """Inicia lectura múltiple"""
        try:
            data = self.send_command([STARTBYTE, MULTIPLE_READ, ENDBYTE])
        except Exception as e:
            logger.error(f"Error en multiple_read: {e}")
    
    def setRegion_EU(self):
        """Configura la región a EU"""
        try:
            data = self.send_command([STARTBYTE, SET_REGION_EU, ENDBYTE])
            time.sleep(0.5)
            rec_data = self.ser.read(24)
            logger.info("Región EU configurada")
        except Exception as e:
            logger.error(f"Error en setRegion_EU: {e}")
    
    def getTransmit_Power(self):
        """Obtiene la potencia de transmisión"""
        try:
            data = self.send_command([STARTBYTE, GET_TRANSMIT_PWR, ENDBYTE])
            time.sleep(0.5)
            rec_data = self.ser.read(24)
            return rec_data
        except Exception as e:
            logger.error(f"Error en getTransmit_Power: {e}")
            return None
