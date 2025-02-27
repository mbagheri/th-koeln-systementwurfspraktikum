from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, JSON
from sqlalchemy.orm import relationship
import sqlite3
import json


engine = create_engine('sqlite:///../Database/orm.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

con = sqlite3.connect('../Database/orm.db')
cur = con.cursor()


class Version(Base):
    """
    Tabellenklasse, mit der die Versions Tabelle erstellt wird
    """
    __tablename__ = 'Version'
    vname = Column(String(300), nullable=False, primary_key=True)
    commands = relationship('Command', cascade="all, delete", passive_deletes=True)


class Command(Base):
    """
    Tabellenklasse, mit der die Befehlsklasse erstellt wird
    """
    __tablename__ = 'Command'
    id = Column(Integer, autoincrement=True, primary_key=True)
    cname = Column(String(300), nullable=False)
    vname = Column(String(300), ForeignKey('Version.vname', ondelete="CASCADE"))
    master = Column(Boolean, nullable=False)
    sof_byte = Column(Integer, nullable=False)
    sof_name = Column(String(300))
    to_byte = Column(Integer, nullable=False)
    to_name = Column(String(300))
    from_byte = Column(Integer, nullable=False)
    from_name = Column(String(300))
    vers_byte = Column(Integer, nullable=False)
    vers_name = Column(String(300))
    hops_byte = Column(Integer, nullable=False)
    hops_name = Column(String(300))
    apNr_byte = Column(Integer, nullable=False)
    apNr_name = Column(String(300))
    crc_byte = Column(Integer, nullable=False)
    crc_name = Column(String(300))
    eof_byte = Column(Integer, nullable=False)
    eof_name = Column(String(300))
    l7sdu0_byte = Column(Integer, nullable=False)
    l7sdu0_name = Column(String(300))
    l7sdu1_byte = Column(Integer, nullable=False)
    l7sdu1_name = Column(String(300))
    l7sdu2_byte = Column(Integer, nullable=False)
    l7sdu2_name = Column(String(300))
    l7sdu3_byte = Column(Integer, nullable=False)
    l7sdu3_name = Column(String(300))
    l7sdu4_byte = Column(Integer, nullable=False)
    l7sdu4_name = Column(String(300))
    l7sdu5_byte = Column(Integer, nullable=False)
    l7sdu5_name = Column(String(300))
    l7sdu6_byte = Column(Integer, nullable=False)
    l7sdu6_name = Column(String(300))
    l7sdu7_byte = Column(Integer, nullable=False)
    l7sdu7_name = Column(String(300))
    delay = Column(Integer, nullable=False)
    iteration = Column(Integer, nullable=False)
    #com_port = Column(String(300), nullable=False)
    participants = Column(Integer, nullable=False)


class GroupCommand(Base):
    """
    Tabellenklasse, mit der die Tabelle der Gruppenbefehle erstellt wird
    """
    __tablename__ = 'GroupCommand'
    gname = Column(String(300), nullable=False, primary_key=True)
    vname = Column(String(300), nullable=False)
    commands = Column(JSON)


class Favorite1(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 1
    """
    __tablename__ = 'Favorite1'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite2(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 2
    """
    __tablename__ = 'Favorite2'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite3(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 3
    """
    __tablename__ = 'Favorite3'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite4(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 4
    """
    __tablename__ = 'Favorite4'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite5(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 5
    """
    __tablename__ = 'Favorite5'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite6(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 5
    """
    __tablename__ = 'Favorite6'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite7(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 6
    """
    __tablename__ = 'Favorite7'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


class Favorite8(Base):
    """
    Tabellenklasse zur Erstellung der Tabelle für Favorit 7
    """
    __tablename__ = 'Favorite8'
    vname = Column(String(300), nullable=False, primary_key=True)
    cname = Column(String(300), nullable=False)


def create_db():
    """
    Methode, die anhand der zuvor erstellten Tabellenklassen,
    die Datenbank erstellt und die Tabellen erzeugt
    :return:
    """
    Base.metadata.create_all(engine)


def add_version(version):
    """
    Methode, mit der eine Version in der DB gespeichert wird
    :param version: Zu speichernde Version
    :return: True, falls erfolgreich, andernfalls Fals
    """
    try:
        session.add(version)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def delete_version(version):
    """
    Methode, mit der eine Version aus der DB gelöscht wird
    :param version: Zu löschende Version
    :return: True, falls erfolgreich, andernfalls False
    """
    try:
        delete_all_group_commands(version)
        delete_all_favorites(version)
        delete_commands(version)
        query_result = session.query(Version).get(version)
        session.delete(query_result)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def get_all_versions():
    """
    Methode, die alle Versionen aus der DB lädt
    :return: Liste aller Versionen
    """
    entries = []
    for version in session.query(Version).all():
        entries.append(version.vname)
    return entries


def get_current_version(version):
    """
    Methode, die die aktuelle Version aus der DB lädt
    :param version:
    :return: geladene Version
    """
    query_result = session.query(Version).get(version)
    return query_result


def add_command(version, command):
    """
    Methode, die einen Befehl zur DB hinzufügt
    :param version: Versionsname
    :param command: Befehlsname
    :return: True, falls erfolgreich, andernfalls False
    """
    try:
        current_version = get_current_version(version)
        new_command = Command(cname=command)
        current_version.commands(new_command)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def session_commit():
    """
    Methode, um eine DB Session zu commiten
    """
    session.commit()


def session_rollback():
    """
    Methode, um eine DB Session zurück zu rollen
    """
    session.rollback()


def delete_commands(version):
    """
    Methode, um alle Befehle einer Version aus der DB zu löschen
    :param version: Version
    """
    commands = session.query(Command).filter(Command.vname == version)
    for command in commands:
        session.delete(command)
    session.commit()


def get_current_version_commands(version):
    """
    Methode, um alle Befehle der ausgewählten Version aus der DB zu laden
    :param version: Version
    :return:
    """
    entries = []
    commands = session.query(Command).filter(Command.vname == version)
    for command in commands:
        entries.append(command.cname)
    return entries


def delete_cmd(command):
    """
    Methode, um einen Befehl aus der DB zu löschen
    :param command: Befehl
    :return:
    """
    cur.execute(f"""DELETE FROM Command WHERE Command.cname = '{command}'""")
    con.commit()


def load_cmd(command, version):
    """
    Methode, mit der ein ausgewählter Befehl aus der DB geladen wird
    :param command: Befehl
    :param version: Version
    :return: Liste der Attributwerte, des geladenen Befehls oder leere Liste, falls Befehl nicht gefunden
    """

    try:
        query = cur.execute(
            f"""SELECT cname, vname, master, 
                sof_byte, sof_name, 
                to_byte, to_name, 
                from_byte, from_name, 
                vers_byte, vers_name, 
                hops_byte, hops_name, 
                apNr_byte, apNr_name, 
                crc_byte, crc_name, 
                eof_byte, eof_name, 
                l7sdu0_byte, l7sdu0_name, 
                l7sdu1_byte, l7sdu1_name, 
                l7sdu2_byte, l7sdu2_name, 
                l7sdu3_byte, l7sdu3_name, 
                l7sdu4_byte, l7sdu4_name, 
                l7sdu5_byte, l7sdu5_name, 
                l7sdu6_byte, l7sdu6_name, 
                l7sdu7_byte, l7sdu7_name,
                delay, 
                iteration,  
                participants 
                FROM Command WHERE cname = '{command}' AND vname = '{version}'""").fetchall()

        result = query[0]
        return result
    except:
        return []


def load_cmds(version):
    """
    Methode, zum Laden von Befehlen aus der DB
    :param version:
    """
    cur.execute(f"""SELECT Command.cname FROM Command WHERE Command.vname = '{version}'""")
    con.commit()


def cmd_exists(version):
    """
    Methode, zum Überprüfen, dass ein Befehl in der DB existiert
    :param version: Version
    :return: True bei Erfolg, andernfalls False
    """
    try:
        cur.execute(f"""SELECT Command.cname FROM Command WHERE Command.vname = '{version}'""")
        con.commit()
        return True
    except:
        session.rollback()
        return False


def update_cmd(
        chosen_cmd,
        cname,
        master,
        sof_byte,
        sof_name,
        to_byte,
        to_name,
        from_byte,
        from_name,
        vers_byte,
        vers_name,
        hops_byte,
        hops_name,
        apNr_byte,
        apNr_name,
        crc_byte,
        crc_name,
        eof_byte,
        eof_name,
        sdu0_byte,
        sdu0_name,
        sdu1_byte,
        sdu1_name,
        sdu2_byte,
        sdu2_name,
        sdu3_byte,
        sdu3_name,
        sdu4_byte,
        sdu4_name,
        sdu5_byte,
        sdu5_name,
        sdu6_byte,
        sdu6_name,
        sdu7_byte,
        sdu7_name,
        delay,
        iteration,
        participants
):
    """
    Methode, mit der die Daten eines angepassten Befehls in der DB gespeichert werden
    :param chosen_cmd: aktueller Befehlsname
    :param cname: neuer Befehlsname
    :param master: Master/Slave Wert
    :param sof_byte: Wird verwendet um die Hardware Schnittstelle anzusteuern.
    :param sof_name: Nutzinformation Beschreibung
    :param to_byte: Wird verwendet um die einen ausgewählten Slave anzusteuern.
    :param to_name: Nutzinformation Beschreibung
    :param from_byte: Wird verwendet um dem PC eine ID zu geben in der Kommunikation
    :param from_name: Nutzinformation Beschreibung
    :param vers_byte: Version des Eingebetteten Systems.
    :param vers_name: Nutzinformation Beschreibung
    :param hops_byte: Anzahl der Durchläufe
    :param hops_name: Nutzinformation Beschreibung
    :param apNr_byte: Die Application Nummer wird für die zu verwendende Funktion gebraucht.
    :param apNr_name: Nutzinformation Beschreibung
    :param crc_byte: crcCalc dient als Prüfinstanz um fehlerhafte oder unsichere Datenübertragungen abzufangen
    :param crc_name: Nutzinformation Beschreibung
    :param eof_byte: Wird zur out of Frame beobachtung genutzt.
    :param eof_name: Nutzinformation Beschreibung
    :param sdu0_byte: Nutzinformation
    :param sdu0_name: Nutzinformation Beschreibung
    :param sdu1_byte: Nutzinformation
    :param sdu1_name: Nutzinformation Beschreibung
    :param sdu2_byte: Nutzinformation
    :param sdu2_name: Nutzinformation Beschreibung
    :param sdu3_byte: Nutzinformation
    :param sdu3_name: Nutzinformation Beschreibung
    :param sdu4_byte: Nutzinformation
    :param sdu4_name: Nutzinformation Beschreibung
    :param sdu5_byte: Nutzinformation
    :param sdu5_name: Nutzinformation Beschreibung
    :param sdu6_byte: Nutzinformation
    :param sdu6_name: Nutzinformation Beschreibung
    :param sdu7_byte: Nutzinformation
    :param sdu7_name: Nutzinformation Beschreibung
    :param delay: Verzögerungswert
    :param iteration: Iterationswert
    :param participants: Anzahl Teilnehmer
    :return: con.commit lädt die Daten in die Datenbank
    """

    con.execute(
        f"""UPDATE Command
        SET cname='{cname}',
        master={master},
        sof_byte='{sof_byte}',
        sof_name='{sof_name}',
        to_byte='{to_byte}',
        to_name='{to_name}',
        from_byte='{from_byte}',
        from_name='{from_name}',
        vers_byte='{vers_byte}',
        vers_name='{vers_name}',
        hops_byte='{hops_byte}',
        hops_name='{hops_name}',
        apNr_byte='{apNr_byte}',
        apNr_name='{apNr_name}',
        crc_byte='{crc_byte}',
        crc_name='{crc_name}',
        eof_byte='{eof_byte}',
        eof_name='{eof_name}',
        l7sdu0_byte='{sdu0_byte}',
        l7sdu0_name='{sdu0_name}',
        l7sdu1_byte='{sdu1_byte}',
        l7sdu1_name='{sdu1_name}',
        l7sdu2_byte='{sdu2_byte}',
        l7sdu2_name='{sdu2_name}',
        l7sdu3_byte='{sdu3_byte}',
        l7sdu3_name='{sdu3_name}',
        l7sdu4_byte='{sdu4_byte}',
        l7sdu4_name='{sdu4_name}',
        l7sdu5_byte='{sdu5_byte}',
        l7sdu5_name='{sdu5_name}',
        l7sdu6_byte='{sdu6_byte}',
        l7sdu6_name='{sdu6_name}',
        l7sdu7_byte='{sdu7_byte}',
        l7sdu7_name='{sdu7_name}',
        delay='{delay}',
        iteration='{iteration}',
        participants='{participants}'
        WHERE Command.cname = '{chosen_cmd}'""")

    con.commit()


def add_group_commands(gname, vname, json):
    """
    Methode, mit der ein Gruppenbefehl in der DB gespeichert wird
    :param gname: Gruppenbefehlsname
    :param vname: Versionsname
    :param json: Json mit Befehlsliste
    :return: True bei Erfolg, andernfalls False
    """
    try:
        con.execute(f"""INSERT INTO GroupCommand (gname, vname, commands) VALUES('{gname}', '{vname}', '{json}')""")
        con.commit()
        return True
    except:
        session.rollback()
        return False


def delete_group(gname):
    """
    Methode, mit der eine ausgewählte Gruppe aus der DB gelöscht wird
    :param gname: Gruppenbefehlsname
    :return: True bei Erfolg, andernfall False
    """
    try:
        con.execute(f"""DELETE FROM GroupCommand WHERE gname = '{gname}'""")
        con.commit()
        return True
    except:
        session.rollback()
        return False


def load_group(gname):
    """
    Methode, mit der ein Gruppenbefehl geladen wird aus der DB
    :param gname: Gruppenbefehlsname
    :return: geladener Gruppenbefehl
    """
    query = con.execute(f"""SELECT gname, commands FROM GroupCommand WHERE gname = '{gname}'""").fetchone()
    return query


def load_all_groups(vname):
    """
    Methode, um alle Gruppenbefehle aus der DB zu laden
    :param vname: Versionsname
    :return: Liste aller Gruppenbefehle
    """
    query = con.execute(f"""SELECT gname, commands FROM GroupCommand WHERE vname = '{vname}'""").fetchall()
    return query


def load_all_group_commands(gname):
    """
    Methode, um alle Befehle eines Gruppenbefehls zu laden
    :param gname: Gruppenbefehlsname
    :return: Json mit Befehlsliste
    """
    query = con.execute(f"""SELECT commands FROM GroupCommand WHERE gname = '{gname}'""").fetchone()
    return json.loads(query[0])


def load_group_commands(gname):
    query = con.execute(f"""SELECT commands FROM GroupCommand WHERE gname = '{gname}'""").fetchone()
    return json.loads(query[0])


def update_group(old_gname, new_gname, json):
    '''Methode, um einen Gruppenbefehl zu updaten in der DB'''
    try:
        con.execute(f"""UPDATE GroupCommand SET gname='{new_gname}', commands='{json}' WHERE gname='{old_gname}'""")
        con.commit()
        return True
    except:
        session.rollback()
        return False


def update_group_command_list(gname, json):
    """
    Methode, die die Befehle in einer Gruppe updated
    :param gname: Gruppenbefehlsname
    :param json: Json mit Befehlsliste
    :return: True, falls erfolgreich, andernfalls False
    """
    try:
        con.execute(f"""UPDATE GroupCommand SET commands='{json}' WHERE gname='{gname}'""")
        con.commit()
        return True
    except:
        session.rollback()
        return False


def add_favorite(command, version, favorite):
    """
    Methode, die einen Befehl in die passende Favoriten Tabelle speichert
    :param command: Befehl
    :param version: Version
    :param favorite: Favorit
    """
    con.execute(f"""INSERT INTO Favorite{favorite} (vname, cname) VALUES('{version}', '{command}')""")
    con.commit()


def delete_favorite(command, favorite):
    """
    Methode, die einen Befehl aus der passenden Favoriten Tabelle löscht
    :param command: Befehl
    :param favorite: Favorit
    :return:
    """
    cur.execute(f"""DELETE FROM {favorite} WHERE {favorite}.cname = '{command}'""")
    con.commit()


def delete_all_group_commands(vname):
    """
    Methode, die alle Gruppenbefehle einer Version löscht
    :param vname: Versionsname
    """
    cur.execute(f"""DELETE FROM GroupCommand WHERE vname = '{vname}' """)
    con.commit()


def delete_all_favorites(version):
    """
    Methode, die alle Favoriten einer Version aus der DB löscht
    :param version: Version
    :return:
    """
    cur.execute(f"""DELETE FROM Favorite1 WHERE Favorite1.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite2 WHERE Favorite2.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite3 WHERE Favorite3.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite4 WHERE Favorite4.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite5 WHERE Favorite5.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite6 WHERE Favorite6.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite7 WHERE Favorite7.vname = '{version}'""")
    cur.execute(f"""DELETE FROM Favorite8 WHERE Favorite8.vname = '{version}'""")
    con.commit()


def load_favorites(version):
    """
    Methode, die alle Favoriten aus den enstprechenden Favoriten Tabellen lädt und in einer List zurück gibt
    :param version: Die Version, zu der die Favoriten geladen werden
    :return: Liste der geladenen Favoriten
    """
    try:
        fav1 = con.execute(f"SELECT cname FROM Favorite1 WHERE Favorite1.vname = '{version}'").fetchone()[0]
    except:
        fav1 = "No Favorite"

    try:
        fav2 = con.execute(f"SELECT cname FROM Favorite2 WHERE Favorite2.vname = '{version}'").fetchone()[0]
    except:
        fav2 = "No Favorite"

    try:
        fav3 = con.execute(f"SELECT cname FROM Favorite3 WHERE Favorite3.vname = '{version}'").fetchone()[0]
    except:
        fav3 = "No Favorite"

    try:
        fav4 = con.execute(f"SELECT cname FROM Favorite4 WHERE Favorite4.vname = '{version}'").fetchone()[0]
    except:
        fav4 = "No Favorite"

    try:
        fav5 = con.execute(f"SELECT cname FROM Favorite5 WHERE Favorite5.vname = '{version}'").fetchone()[0]
    except:
        fav5 = "No Favorite"

    try:
        fav6 = con.execute(f"SELECT cname FROM Favorite6 WHERE Favorite6.vname = '{version}'").fetchone()[0]
    except:
        fav6 = "No Favorite"

    try:
        fav7 = con.execute(f"SELECT cname FROM Favorite7 WHERE Favorite7.vname = '{version}'").fetchone()[0]
    except:
        fav7 = "No Favorite"

    try:
        fav8 = con.execute(f"SELECT cname FROM Favorite8 WHERE Favorite8.vname = '{version}'").fetchone()[0]
    except:
        fav8 = "No Favorite"

    return fav1, fav2, fav3, fav4, fav5, fav6, fav7, fav8
