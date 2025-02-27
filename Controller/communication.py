import sys
import serial
import time


class Communication:
    """
    Diese Klasse wird verwendet um mit dem STM32 Board mittels des MMCP
    Protokolls kommunizieren zu können.
    """

    def __init__(self, port):
        """
        Initialisierung der benötigten Komponenten.
        :param port: Wird verwendet um die Hardware Schnittstelle anzusteuern.
        """
        try:
            self.ser = serial.Serial(port, 115200, timeout=1)
            if not self.ser.isOpen():
                self.ser.open()
        except Exception:
            sys.exit(0)
        self.states = ["idle", "calibrate_active", "calibrate_done", "cnt_active", "cnt_done", "receivemarbles_active",
                       "receivemarbles_done", "sendmarbles_active", "sendmarbles_done", " forwardmarbles_active",
                       "play_prepare",
                       "play_active", "play_done", "sfx_prepare", "sfx_active", "sfx_done"]
        self.polynomial = 7
        self.crc = [0] * 256
        self.noAnswer = 0
        topbit = 128
        self.message = bytearray(13)
        for dividend in range(256):
            remainder = dividend
            for bit in range(8, 0, -1):
                if remainder & topbit:
                    remainder = ((remainder << 1) & 255) ^ self.polynomial
                else:
                    remainder = ((remainder << 1) & 255)
            self.crc[dividend] = remainder

        self.crcTable = bytearray(self.crc)

    def crcCalc(self, message, nBytes):
        """
        crcCalc dient als Prüfinstanz um fehlerhafte oder unsichere Datenübertragungen abzufangen und zu verwerfen.
        :param message: Enthält den Datensatz der zu sendenden Nachricht.
        :param nBytes: Überprüft ob das CRC genau 8 Byte als Prüfsumme hat.
        :return: reminder, welcher dem überprüften Datensatz entspricht.
        """
        remainder = 0x00
        for byte in range(nBytes):
            data = message[byte] ^ remainder
            remainder = self.crcTable[data] ^ ((remainder << 8) & 255)
        return remainder

    def sendBytes(self, data):
        """
        sendBytes wird verwendet um Daten über einen Seriellen Port zu versenden.
        :param data: enthält die Nutzdaten und vermittlungsschicht welche versendet werden sollen.
        :return: der beantworteten Nachricht.
        """
        if not self.ser.isOpen():
            self.ser.open()
        rList2 = [0, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                  data[11], data[12], self.crcCalc(bytearray(data), 13), 0]
        message2 = bytearray(rList2)
        # seconds passed since epoch
        seconds = 1642208201.3774784
        res = time.ctime(seconds)
        output = \
            ("  Send message   = " + str(res) + " \nSO,TO,FR,VE,HO,Ap,L0,L1,L2,L3,L4,L5,L6,L7, CRC,EOF\n" + str(rList2))
        self.ser.write(message2)
        answer = self.ser.read(16)
        if len(answer) == 0:
            output = output + "\nno answer "
            self.noAnswer = 1
        else:
            self.noAnswer = 0
            output = output + "\n["
            for x in range(15):
                output = output + str(int(answer[x])) + ", "
            output = output + str(int(answer[15])) + "]\n  Answer receive = " + str(res) + "\n"

            for x in range(1, 14):
                self.message[x - 1] = answer[x]
        self.ser.close()
        return self.message, output

    def receivedBytes(self):
        """
        receivedBytes wird verwendet um Daten über einen Seriellen Port zu empfangen.
        :return: der empfangenen Nachricht.
        """
        global message, answer, success
        success = 1
        TimeoutCounter = 0
        flag = True
        while flag and TimeoutCounter < 5:
            answer = self.ser.read(16)
            TimeoutCounter = TimeoutCounter + 1
            if len(answer) == 16 or self == False:
                flag = False
                TimeoutCounter = 0
        if len(answer) < 16:
            stret = "\n  No answer - "
            if self == 0:
                stret = stret + "correct\n"
            else:
                stret = stret + "incorrect\n"
                success = 0
        elif self == 0:
            stret = "\n  An answer came, although none was expected\n"
            stret = stret + "  Received answer:\n  ["
            for x in range(15):
                stret = stret + str(int(answer[x])) + ", "
            stret = stret + str(int(answer[15])) + "]\n"
            success = 0
        else:
            message = answer
            stret = "  Received answer:\n  ["
            for x in range(15):
                stret = stret + str(int(answer[x])) + ", "
            stret = stret + str(int(answer[15])) + "]\n"
        return stret