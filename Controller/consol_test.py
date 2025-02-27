import Controller.communication
from time import sleep


class Slave:
    """
    Dieser Abschnitt sollte ausgelagert werden auf die entsprechenden Slaves und Projekte
    """
    def __init__(self, port, to, from_, vers, hops, apNr, l7_0, l7_1, l7_2, l7_3, l7_4, l7_5, l7_6, l7_7):
        """
        Initialisierung der benötigten Komponenten.
        :param port: Wird verwendet um die Hardware Schnittstelle anzusteuern.
        :param to: Wird verwendet um die einen ausgewählten Slave anzusteuern.
        :param from_: Wird verwendet um dem PC eine ID zu geben in der Kommunikation
        :param vers: Version des Eingebetteten Systems.
        :param hops: Anzahl der Durchläufe
        :param apNr: Die Application Nummer wird für die zu verwendende Funktion gebraucht.
        :param l7_0: Nutzinformation
        :param l7_1: Nutzinformation
        :param l7_2: Nutzinformation
        :param l7_3: Nutzinformation
        :param l7_4: Nutzinformation
        :param l7_5: Nutzinformation
        :param l7_6: Nutzinformation
        :param l7_7: Nutzinformation
        """
        self.ring = port
        self.to = to
        self.from_ = from_
        self.vers = vers
        self.hops = hops
        self.apNr = apNr
        self.l7_0 = l7_0
        self.l7_1 = l7_1
        self.l7_2 = l7_2
        self.l7_3 = l7_3
        self.l7_4 = l7_4
        self.l7_5 = l7_5
        self.l7_6 = l7_6
        self.l7_7 = l7_7
        self.message = None

    def goBeep(self):
        """
        Hier werden die in der GUI eingegebenen Daten an sendByte übergeben zum Senden.
        :return: message wird für die Konsole und die live Daten in der GUI benötigt.
        """
        self.message = self.ring.sendBytes([self.to, self.from_, self.vers, self.hops, self.apNr, self.l7_0, self.l7_1,
                                            self.l7_2, self.l7_3, self.l7_4, self.l7_5, self.l7_6, self.l7_7])
        return self.message


class Mmc:
    """
    Dieser Abschnitt bildet das Marble/Mobility Machine Control Protocol (MMCP)
    """

    def __init__(self, port, to, from_, vers, hops, apNr, l7_0, l7_1, l7_2, l7_3, l7_4, l7_5, l7_6, l7_7, anzahlSlaves,
                 delay, interation):
        """
        Initialisierung der benötigten Komponenten.
        :param port: Wird verwendet um die Hardware Schnittstelle anzusteuern.
        :param to: Wird verwendet um die einen ausgewählten Slave anzusteuern.
        :param from_: Wird verwendet um dem PC eine ID zu geben in der Kommunikation
        :param vers: Version des Eingebetteten Systems.
        :param hops: Anzahl der Durchläufe
        :param apNr: Die Application Nummer wird für die zu verwendende Funktion gebraucht.
        :param l7_0: Nutzinformation
        :param l7_1: Nutzinformation
        :param l7_2: Nutzinformation
        :param l7_3: Nutzinformation
        :param l7_4: Nutzinformation
        :param l7_5: Nutzinformation
        :param l7_6: Nutzinformation
        :param l7_7: Nutzinformation
        :param anzahlSlaves: Übergibt die Anzahl der abzufragenden Slaves
        :param delay: Enthält die Zeit, um welche eine Nachricht verzögert wird
        :param interation: Wird für die wiederholung einer Nachricht benötigt
        """
        self.port = port
        self.to = to
        self.from_ = from_
        self.vers = vers
        self.hops = hops
        self.apNr = apNr
        self.l7_0 = l7_0
        self.l7_1 = l7_1
        self.l7_2 = l7_2
        self.l7_3 = l7_3
        self.l7_4 = l7_4
        self.l7_5 = l7_5
        self.l7_6 = l7_6
        self.l7_7 = l7_7
        self.anzahlSlaves = anzahlSlaves
        self.delay = delay
        self.interation = interation
        self.ring = Controller.communication.Communication(port)  # relevant für die GUI
        self.bords = []
        self.print_messages = []
        self.message = None

        self.bords.append(Slave(self.ring, self.to, self.from_, self.vers, self.hops, self.apNr, self.l7_0,
                                        self.l7_1, self.l7_2, self.l7_3, self.l7_4, self.l7_5, self.l7_6, self.l7_7))

    def findSlave(self):
        """
        Hiermit werden die Anzufragenden Slaves gesucht.
        :return: print_messages wird für die Konsole und die live Daten in der GUI benötigt.
        """
        for to in range(1, self.anzahlSlaves+1):
            self.message = self.ring.sendBytes([to, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
            self.print_messages.append(self.message)

    def mmcExecute(self):
        """
        Hier werden Nachrichten an Slaves übermittelt und mit einem entsprechenden Delay versehen.
        :return: print_messages wird für die Konsole und die live Daten in der GUI benötigt.
        """
        sleep(self.delay * 0.001) #delay time in mili seconds
        for x in range(len(self.bords)):
            self.print_messages.append(self.bords[x].goBeep())
