"""
Permite leer el codigo de barras de una cedula de identidad colombiana
desde un lector de códigos de barra físico (ejemplo: Netum L8BL)

Este debe estar configurado en modo serial (COM)

Notas: Estos lectores arrojan lecturas iguales en linux y mac pero en windows
se comportan distinto. Arrojan una lectura en donde truncan los bytes nulos.
Esto dificulta un poco la lectura de los datos.

Este script soporta tanto windows como linux y mac.

Por ejemplo para linux y mac el inicio de la lectura inicia así:
"0320065791NULNULNULNULNULNULNULNULNULNULNULNULNULNULPubDSK_1"

Pero para windows iniciaría así:
"0320065791NULNULNULPubDSK_1....."

Note que en windows solo se envían 3 nulos luego del código afis (20065791)
mientras que en linux y mac si se envían todos los nulos.
"""

import json
from threading import Thread
import serial.tools.list_ports
import serial



from src.barcode.colombian_pdf417_decoder import ColombianIdCardPdf417Decoder

# Debes cambiar esto por el puerto serial del lector de códigos de barra
# Ejemplo: 'COM3'
DEFAULT_SERIAL_PORT = 'COM3'
BAUD = 9600
COLOMBIAN_CEDULA_PDF417_FULL_LEN = 531
COLOMBIAN_CEDULA_PDF417_TRUNKED_LEN = 200

NULL_BYTE = bytes('\x00', 'ascii')

TRUNKED_FRAME_PUB_SDK_MARK_IDX = 13
# Esta marca se encuentra en el pdf417
# Normalmente está en el byte 24
# Pero si la lectura es truncada, está en el byte 13
PUB_SDK_MARK = bytes('PubDSK_', 'ascii')

#                           macOS       | Linux        |  Windows
SERIAL_PORT_NAMES = ['/dev/cu.usbmodem', '/dev/ttyACM', 'COM']


def find_serial_port() -> str:
    ports = serial.tools.list_ports.comports()
    latest_port_number = 0
    latest_port_number_name = ''
    for port in ports:
        print(port.device)
        for name in SERIAL_PORT_NAMES:
            if port.device.startswith('/dev/cu.usbmodem'):
                return port.device
            if not port.device.startswith(name):
                continue
            port_number_str: str = port.device[len(name):]
            port_number = int(port_number_str.lstrip('0'))
            if port_number >= latest_port_number:
                latest_port_number = port_number
                latest_port_number_name = port.device
    return latest_port_number_name


def barcode_serial():
    serial_port_path = find_serial_port()
    if not serial_port_path:
        print('No se encontró ningún puerto serial')
        print("se tomará el siguiente puerto por defecto: {}".format(DEFAULT_SERIAL_PORT))
        serial_port_path = DEFAULT_SERIAL_PORT
    print("Iniciando....")
    try:
        serial_port = serial.Serial(serial_port_path, BAUD)
        serial_port.flushInput()

        frame = bytearray()
        while True:
            # Se leen los primeros 200 bytes de la lectura
            # En estos primeros 200 bytes se encuentra toda la data que extraeremos
            c = serial_port.read(COLOMBIAN_CEDULA_PDF417_TRUNKED_LEN)
            print(c)
            c = "0361231117PubDSK_14883801002388110ROJANOMARQUEZLUISAFERNANDA0F20000424051180O+200023QS025501280128}my0141x0131l014850134!yDs01930135<^^aXVeL0136o01290137013901550141017220165g01470167Z0168fV0158015901580168{A0152N0143016001470160017001700134301400173]017401500182x0188s8~0194l01990139M|0174016301810137018801481lEjQ\[iW[a^]OqT}Wqtzd017402530142o0243022301820016AR01320235T[0253700027PU025501280128w01300145j01280162o0146s0154x016801450166o0171h0152015001270205o01440132^01410164f016401360198g0170`0198015002010137L0134015101540178W:0135+01270162SF^Wo0162^3^[Jel0129013301530171l01510167od01610176z0174o0164014701840142019201420201014701570164AzUvVTdvtiu_q01270142exu}01510133j01390160l0184VQ01400174001702550219U%02510150S02010127022100170151019601960006K>Z01310158~013100040248/0209~Y5022501450232-l0238L0001020302000194022001416N”01760008"
            frame.extend(c)
            
            pub_sdk_mark_idx = frame.find(PUB_SDK_MARK)
            if pub_sdk_mark_idx == -1:
                continue
            if frame[pub_sdk_mark_idx - 10:pub_sdk_mark_idx].count(NULL_BYTE) > 4:
                frame = frame[pub_sdk_mark_idx - 24:]
            else:
                frame = frame[pub_sdk_mark_idx - 13:]
            if len(frame) < 200:
                continue
            serial_port.flush()
            serial_port.flushInput()
            serial_port.flushOutput()
            decoder = ColombianIdCardPdf417Decoder(frame)
            frame = bytearray()
            data = decoder.decode()
            result = json.dumps(data, indent=2, default=lambda o: o.__dict__)
            print(result)

    except Exception as e:
        print(e)

def test_string():
    frame = bytearray()
    c = "0361231117PubDSK_14883801002388110ROJANOMARQUEZLUISAFERNANDA0F20000424051180O+200023QS025501280128}my0141x0131l014850134!yDs01930135<^^aXVeL0136o01290137013901550141017220165g01470167Z0168fV0158015901580168{A0152N0143016001470160017001700134301400173]017401500182x0188s8~0194l01990139M|0174016301810137018801481lEjQ\[iW[a^]OqT}Wqtzd017402530142o0243022301820016AR01320235T[0253700027PU025501280128w01300145j01280162o0146s0154x016801450166o0171h0152015001270205o01440132^01410164f016401360198g0170`0198015002010137L0134015101540178W:0135+01270162SF^Wo0162^3^[Jel0129013301530171l01510167od01610176z0174o0164014701840142019201420201014701570164AzUvVTdvtiu_q01270142exu}01510133j01390160l0184VQ01400174001702550219U%02510150S02010127022100170151019601960006K>Z01310158~013100040248/0209~Y5022501450232-l0238L0001020302000194022001416N”01760008"
    frame.extend(c)
    print(frmae)
    
    pub_sdk_mark_idx = frame.find(PUB_SDK_MARK)
    if pub_sdk_mark_idx == -1:
        print(1)
    if frame[pub_sdk_mark_idx - 10:pub_sdk_mark_idx].count(NULL_BYTE) > 4:
        frame = frame[pub_sdk_mark_idx - 24:]
    else:
        frame = frame[pub_sdk_mark_idx - 13:]
    if len(frame) < 200:
        print(2)
    decoder = ColombianIdCardPdf417Decoder(frame)
    frame = bytearray()
    data = decoder.decode()
    result = json.dumps(data, indent=2, default=lambda o: o.__dict__)
    print(result)


if __name__ == '__main__':
    test_string()
    # thread1 = Thread(target=barcode_serial)
    # thread1.start()
    # thread1.join()
