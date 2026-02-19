#uhf library file

import serial
import time
import binascii
import array
import threading

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

class UHF:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=0.3):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.running = False

    def single_read(self):
        data = self.send_command([STARTBYTE, SINGLE_READ, ENDBYTE])
        time.sleep(0.5)
        rec_data = self.ser.read(24)
        #print(rec_data)
        if rec_data is not None and len(rec_data)>22:
            if rec_data[0] != 0xaa or rec_data[23] != 0xdd or rec_data[1] != 0x02:
                return None        
            return ['{:02x}'.format(x) for x in rec_data]
        
    def read_mul(self):
        data = self.send_command([STARTBYTE, MULTIPLE_READ, ENDBYTE])
        time.sleep(0.5)
        rec_data = self.ser.read(24)
        if rec_data is not None and len(rec_data)>22:
            if rec_data[0] != 0xaa or rec_data[23] != 0xdd or rec_data[1] != 0x02:
                return None        
            return ['{:02x}'.format(x) for x in rec_data]
        
    def stop_read(self):
        data = self.send_command([STARTBYTE, STOP_READ, ENDBYTE])
        time.sleep(0.5)
        rec_data = self.ser.read(24)
        #print(rec_data)    
    
    #####################################################
    def calculate_checksum(self,data):
        checksum = 0
        for byte in data:
            checksum += byte
        checksum_1 = (checksum) % 256
        return checksum

    def calculation(self,Data):
        bin_data1 = binascii.unhexlify(Data)
        chk_1 = (hex(self.calculate_checksum(bin_data1)))
        #print("checksum",chk_1)
        if len(chk_1) == 5:
            return str(chk_1[3:])
            
        elif len(chk_1) == 4:
            return str(chk_1[2:])
        
        else:
            return '0'+ str(chk_1[3:])
    ######################################################

    def send_command(self, data):
        Data = ''.join(data)
        #print(Data)
        bin_data = binascii.unhexlify(Data)
        response = self.ser.write(bin_data)


    
    def Kill_card(self):
        fig = '6500040000FFFF'   
        dat = self.calculation(fig)
        dat1 = STARTBYTE+fig+dat+ENDBYTE
        #print("dat1 = ",dat1)
        data = self.send_command(dat1)
        time.sleep(0.2)
        rec_data = self.ser.read(24)
        s = []
        if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                print("kill card = ",a)
                
                #if "".join(a) == 'bb01ff0001090a7e':
                #     return 'No card is there'
                
                #else:
                #    return "".join(a)[40:70]
                
    ####################################################################
    def Set_select_pera(self,tag_uid):          
        #fig = '0C00130'+Memory_bank+'000000206000'+ tag_uid
        fig = '0C001300000000206000'+ tag_uid # seleccionar toda la tarjeta
        dat = self.calculation(fig)
        dat1 = STARTBYTE+fig+dat+ENDBYTE
        #print('card select = ',dat1)
        data = self.send_command(dat1)
        time.sleep(0.2)
        rec_data = self.ser.read(16)
        s = []
        if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                #print('select response = ',a)
                if "".join(a) == 'aa010c0001000edd':   
                     return 'Select sucessfull'
                else:
                    return 'invalid'
                
    
    def Read_tag_data(self,memory_bank):
        fig = '390009000000000'+memory_bank+'00000008'   # leer 8 palabras
        dat = self.calculation(fig) # calcular checksum
        dat1 = STARTBYTE+fig+dat+ENDBYTE # crear comando completo
        #print("dat1 = ",dat1)
        
        data = self.send_command(dat1)
        time.sleep(0.2)
        rec_data = self.ser.read(40)
        s = []
        if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                print(a)
                if "".join(a) == 'aa01ff0001090add': # no hay tarjeta
                     return 'No card is there'
                    
                elif "".join(a) != 'aa01ff0001090add': # exito
                    if memory_bank == '2': # TID bank 
                        return "".join(a)[40:72]
                        
                    elif memory_bank == '3': # USER bank
                        return "".join(a)[40:70]
                    
                    elif memory_bank == '1': # EPC bank
                        return "".join(a)[48:72]
                    


    def Write_tag_data(self,data_w,memory_bank):  
        fig = '490019000000000'+memory_bank+'00000008'+ data_w      
        dat = self.calculation(fig)
        dat1 = STARTBYTE+fig+dat+ENDBYTE
        #print('write = ',dat1)
        data = self.send_command(dat1)
        time.sleep(0.2)
        rec_data = self.ser.read(23)
        s = []
        if rec_data is not None:
                a = ['{:02x}'.format(x) for x in rec_data]
                print('write data = ',a)
                if "".join(a) == 'aa01ff00011011dd':  
                     return 'Write card failed,No tag response'
                    
                elif "".join(a) == 'aa01ff00011718dd':   
                     return 'Command error'#'Data length should me should be integer multiple words'
                    
                elif a[2] == '49':
                    return 'Card sucessfull write'

    ################################################################################


    def hardware_version(self):
        self.send_command([STARTBYTE,HARD_VERSION,ENDBYTE])
        time.sleep(0.5)
        d = self.ser.read(19)
        s = []
        if d is not  None: 
            def split_bytes_data(data, packet_size):
                # Split the bytes object into packets of the specified size
                packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
                return packets
            ds = split_bytes_data(d,6)
            for i in range(1,len(ds)):
                   s.append(str(ds[i],'latin-1'))
            return "".join(s)


    def multiple_read(self):
        data = self.send_command([STARTBYTE, MULTIPLE_READ, ENDBYTE])

    def stop_read(self):
        data = self.send_command([STARTBYTE, STOP_READ, ENDBYTE])
    
    def setRegion_EU(self):
        data = self.send_command([STARTBYTE, SET_REGION_EU, ENDBYTE])
        time.sleep(0.5)
        rec_data = self.ser.read(24)
        #print(rec_data)    
    
    def getTransmit_Power(self):
        data = self.send_command([STARTBYTE, GET_TRANSMIT_PWR, ENDBYTE])
        time.sleep(0.5)
        rec_data = self.ser.read(24)
        return rec_data
    