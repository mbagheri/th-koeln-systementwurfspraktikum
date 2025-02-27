import Model.orm_controller as orm
import tkinter as tk
import serial
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext
from Controller.consol_test import Mmc
import json


class VersionControl(Toplevel):

    def __init__(self, version_name):
        """
        Initialisierungsmethode, die aufgerufen wird beim Erstellen
        einer VersionControl Instanz, um das Fenster zu rendern.
        :param version_name: Übergebener Versionsname, der zuvor in der
        Versionsübersicht ausgewählt wurde zum Öffnen
        """

        super().__init__()
        self.title("Version Control")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.current_version = version_name
        self.group_command_list = [] # Warteliste für die Gruppenbefehle

        # Upper Left Frame
        self.upper_left_frame = tk.Frame(self, bg='#ffffff', highlightbackground='black', highlightthickness=1)
        self.upper_left_frame.grid(row=0, column=0, sticky='nsew')

        # Version Name
        self.version_label = tk.Label(self.upper_left_frame, text="Version Name: " + version_name)
        self.version_label.grid(row=0, column=0)

        # Command Name
        self.cmd = StringVar()
        self.command_name_label = tk.Label(self.upper_left_frame, text="Command Name:")
        self.command_name_label.grid(row=1, column=0)

        self.command_name_entry = tk.Entry(self.upper_left_frame)
        self.command_name_entry.grid(row=1, column=1)

        # COM Port
        self.com_label = tk.Label(self.upper_left_frame, text="COM Port:")
        self.com_label.grid(row=1, column=2)

        self.com = StringVar()
        self.com.set(self.serial_ports())
        # self.com.set("COM5")
        self.com_entry = tk.Entry(self.upper_left_frame, textvariable=self.com)
        self.com_entry.grid(row=1, column=3)
        self.comPort = self.com_entry.get()

        # Number Participants
        self.participants_label = tk.Label(self.upper_left_frame, text="Number Participants")
        self.participants_label.grid(row=1, column=4)

        self.participants = IntVar()
        self.participants.set(0)
        self.participants_entry = tk.Entry(self.upper_left_frame, textvariable=self.participants)
        self.participants_entry.grid(row=1, column=5)

        # Master-Slave-Option
        self.radio_btn_value = BooleanVar()
        self.master_radio = Radiobutton(self.upper_left_frame, text="Master", variable=self.radio_btn_value, value=1,
                                        command=self.toggle_from_value)
        self.master_radio.grid(row=2, column=0)

        self.slave_radio = Radiobutton(self.upper_left_frame, text="Slave", variable=self.radio_btn_value, value=0,
                                       command=self.toggle_from_value)
        self.slave_radio.grid(row=2, column=1)
        self.radio_btn_value.set(True)

        # Header Bye Num 1
        self.byte1_label = tk.Label(self.upper_left_frame, text="Byte Num.")
        self.byte1_label.grid(row=3, column=1)

        # Header Name 1
        self.name1_label = tk.Label(self.upper_left_frame, text="Name")
        self.name1_label.grid(row=3, column=2)

        # Header Byte Num 2
        self.byte2_label = tk.Label(self.upper_left_frame, text="Byte Num.")
        self.byte2_label.grid(row=3, column=4)

        # Header Name 2
        self.name2_label = tk.Label(self.upper_left_frame, text="Name")
        self.name2_label.grid(row=3, column=5)

        # SOF
        self.sof_label = tk.Label(self.upper_left_frame, text="SOF:")
        self.sof_label.grid(row=4, column=0)

        self.sof_byte = IntVar()
        self.sof_byte.set(0)
        self.sof_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sof_byte)
        self.sof_byte_entry.grid(row=4, column=1)

        self.sof_name = StringVar()
        self.sof_name_entry = tk.Entry(self.upper_left_frame)
        self.sof_name_entry.grid(row=4, column=2)

        # To
        self.to_label = tk.Label(self.upper_left_frame, text="To:")
        self.to_label.grid(row=5, column=0)

        self.to_byte = IntVar()
        self.to_byte.set(0)
        self.to_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.to_byte)
        self.to_byte_entry.grid(row=5, column=1)

        self.to_name = StringVar()
        self.to_name_entry = tk.Entry(self.upper_left_frame)
        self.to_name_entry.grid(row=5, column=2)

        # From
        self.from_label = tk.Label(self.upper_left_frame, text="From:")
        self.from_label.grid(row=6, column=0)

        self.from_byte = IntVar()
        self.from_byte.set(1)
        self.from_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.from_byte)
        self.from_byte_entry.grid(row=6, column=1)

        self.from_name = StringVar()
        self.from_name_entry = tk.Entry(self.upper_left_frame)
        self.from_name_entry.grid(row=6, column=2)

        # Vers.
        self.vers_label = tk.Label(self.upper_left_frame, text="Vers.:")
        self.vers_label.grid(row=7, column=0)

        self.vers_byte = IntVar()
        self.vers_byte.set(1)
        self.vers_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.vers_byte)
        self.vers_byte_entry.grid(row=7, column=1)

        self.vers_name = StringVar()
        self.vers_name_entry = tk.Entry(self.upper_left_frame)
        self.vers_name_entry.grid(row=7, column=2)

        # Hops
        self.hops_label = tk.Label(self.upper_left_frame, text="Hops:")
        self.hops_label.grid(row=8, column=0)

        self.hops_byte = IntVar()
        self.hops_byte.set(0)
        self.hops_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.hops_byte)
        self.hops_byte_entry.grid(row=8, column=1)

        self.hops_name = StringVar()
        self.hops_name_entry = tk.Entry(self.upper_left_frame)
        self.hops_name_entry.grid(row=8, column=2)

        # ApNr
        self.apNr_label = tk.Label(self.upper_left_frame, text="ApNr:")
        self.apNr_label.grid(row=9, column=0)

        self.apNr_byte = IntVar()
        self.apNr_byte.set(0)
        self.apNr_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.apNr_byte)
        self.apNr_byte_entry.grid(row=9, column=1)

        self.apNr_name = StringVar()
        self.apNr_name_entry = tk.Entry(self.upper_left_frame)
        self.apNr_name_entry.grid(row=9, column=2)

        # CRC
        self.crc_label = tk.Label(self.upper_left_frame, text="CRC:")
        self.crc_label.grid(row=10, column=0)

        self.crc_byte = IntVar()
        self.crc_byte.set(0)
        self.crc_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.crc_byte)
        self.crc_byte_entry.grid(row=10, column=1)

        self.crc_name = StringVar()
        self.crc_name_entry = tk.Entry(self.upper_left_frame)
        self.crc_name_entry.grid(row=10, column=2)

        # EOF
        self.eof_label = tk.Label(self.upper_left_frame, text="EOF:")
        self.eof_label.grid(row=11, column=0)

        self.eof_byte = IntVar()
        self.eof_byte.set(0)
        self.eof_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.eof_byte)
        self.eof_byte_entry.grid(row=11, column=1)

        self.eof_name = StringVar()
        self.eof_name_entry = tk.Entry(self.upper_left_frame)
        self.eof_name_entry.grid(row=11, column=2)

        # L7_SDU_0
        self.sdu_0_label = tk.Label(self.upper_left_frame, text="L7_SDU [0]:")
        self.sdu_0_label.grid(row=4, column=3)

        self.sdu0_byte = IntVar()
        self.sdu0_byte.set(0)
        self.sdu_0_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu0_byte)
        self.sdu_0_byte_entry.grid(row=4, column=4)

        self.sdu0_name = StringVar()
        self.sdu_0_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_0_name_entry.grid(row=4, column=5)

        # L7_SDU_1
        self.sdu_1_label = tk.Label(self.upper_left_frame, text="L7_SDU [1]:")
        self.sdu_1_label.grid(row=5, column=3)

        self.sdu1_byte = IntVar()
        self.sdu1_byte.set(0)
        self.sdu_1_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu1_byte)
        self.sdu_1_byte_entry.grid(row=5, column=4)

        self.sdu1_name = StringVar()
        self.sdu_1_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_1_name_entry.grid(row=5, column=5)

        # L7_SDU_2
        self.sdu_2_label = tk.Label(self.upper_left_frame, text="L7_SDU [2]:")
        self.sdu_2_label.grid(row=6, column=3)

        self.sdu2_byte = IntVar()
        self.sdu2_byte.set(0)
        self.sdu_2_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu2_byte)
        self.sdu_2_byte_entry.grid(row=6, column=4)

        self.sdu2_name = StringVar()
        self.sdu_2_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_2_name_entry.grid(row=6, column=5)

        # L7_SDU_3
        self.sdu_3_label = tk.Label(self.upper_left_frame, text="L7_SDU [3]:")
        self.sdu_3_label.grid(row=7, column=3)

        self.sdu3_byte = IntVar()
        self.sdu3_byte.set(0)
        self.sdu_3_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu3_byte)
        self.sdu_3_byte_entry.grid(row=7, column=4)

        self.sdu3_name = StringVar()
        self.sdu_3_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_3_name_entry.grid(row=7, column=5)

        # L7_SDU_4
        self.sdu_4_label = tk.Label(self.upper_left_frame, text="L7_SDU [4]:")
        self.sdu_4_label.grid(row=8, column=3)

        self.sdu4_byte = IntVar()
        self.sdu4_byte.set(0)
        self.sdu_4_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu4_byte)
        self.sdu_4_byte_entry.grid(row=8, column=4)

        self.sdu4_name = StringVar()
        self.sdu_4_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_4_name_entry.grid(row=8, column=5)

        # L7_SDU_5
        self.sdu_5_label = tk.Label(self.upper_left_frame, text="L7_SDU [5]:")
        self.sdu_5_label.grid(row=9, column=3)

        self.sdu5_byte = IntVar()
        self.sdu5_byte.set(0)
        self.sdu_5_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu5_byte)
        self.sdu_5_byte_entry.grid(row=9, column=4)

        self.sdu5_name = StringVar()
        self.sdu_5_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_5_name_entry.grid(row=9, column=5)

        # L7_SDU_6
        self.sdu_6_label = tk.Label(self.upper_left_frame, text="L7_SDU [6]:")
        self.sdu_6_label.grid(row=10, column=3)

        self.sdu6_byte = IntVar()
        self.sdu6_byte.set(0)
        self.sdu_6_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu6_byte)
        self.sdu_6_byte_entry.grid(row=10, column=4)

        self.sdu6_name = StringVar()
        self.sdu_6_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_6_name_entry.grid(row=10, column=5)

        # L7_SDU_7
        self.sdu_7_label = tk.Label(self.upper_left_frame, text="L7_SDU [7]:")
        self.sdu_7_label.grid(row=11, column=3)

        self.sdu7_byte = IntVar()
        self.sdu7_byte.set(0)
        self.sdu_7_byte_entry = tk.Entry(self.upper_left_frame, textvariable=self.sdu7_byte)
        self.sdu_7_byte_entry.grid(row=11, column=4)

        self.sdu7_name = StringVar()
        self.sdu_7_name_entry = tk.Entry(self.upper_left_frame)
        self.sdu_7_name_entry.grid(row=11, column=5)

        self.delay_label = tk.Label(self.upper_left_frame, text="Delay [ms]:")
        self.delay_label.grid(row=12, column=0)

        self.delay = IntVar()
        self.delay.set(0)
        self.delay_entry = tk.Entry(self.upper_left_frame, textvariable=self.delay)
        self.delay_entry.grid(row=12, column=1)

        self.iteration_label = tk.Label(self.upper_left_frame, text="Iteration:")
        self.iteration_label.grid(row=13, column=0)

        self.iteration = IntVar()
        self.iteration.set(1)
        self.iteration_entry = tk.Entry(self.upper_left_frame, textvariable=self.iteration)
        self.iteration_entry.grid(row=13, column=1)

        # Add Button
        self.add_btn = tk.Button(self.upper_left_frame, text="Add", command=self.add_entry)
        self.add_btn.grid(row=14, column=1, columnspan=2, sticky="we")

        # Update Button
        self.update_btn = tk.Button(self.upper_left_frame, text="Update Command", command=self.update_command)
        self.update_btn.grid(row=14, column=4)

        # Upper Right Frame
        self.upper_right_frame = tk.Frame(self, bg='#ffffff', highlightbackground='black', highlightthickness=1)
        self.upper_right_frame.grid(row=0, column=1, sticky='nsew')

        self.version_label = tk.Label(self.upper_right_frame, text="Single Command Options: ")
        self.version_label.grid(row=0, column=0)

        # Label to inform the user about errors and more
        self.notification_label = tk.Label(self.upper_right_frame, text="", fg="red")
        self.notification_label.grid(row=0, column=1)

        self.cb_label = tk.Label(self.upper_right_frame, text="Choose Single Command:")
        self.cb_label.grid(row=1, column=0)

        self.cb = ttk.Combobox(self.upper_right_frame, value=orm.get_current_version_commands(self.current_version))
        self.cb.grid(row=1, column=1)

        self.load_cmd_btn = tk.Button(self.upper_right_frame, text="Load Command", command=self.load_cmd)
        self.load_cmd_btn.grid(row=1, column=2)

        self.start_btn = tk.Button(self.upper_right_frame, text="Execute Command", command=self.execute_dropdown_option)
        self.start_btn.grid(row=2, column=0)

        self.delete_btn = tk.Button(self.upper_right_frame, text="Delete Command", command=self.delete_dropdown_option)
        self.delete_btn.grid(row=2, column=1)

        self.add_to_group_btn = tk.Button(self.upper_right_frame, text="Add Wait List",
                                          command=self.add_command_to_group_command_list)
        self.add_to_group_btn.grid(row=2, column=2)

        # Section to add Favorites
        self.upper_right_fav_label = tk.Label(self.upper_right_frame, text="Favorite:")
        self.upper_right_fav_label.grid(row=2, column=3)

        self.fav_radio_value = IntVar()
        self.fav1_radio = Radiobutton(self.upper_right_frame, text="1", variable=self.fav_radio_value, value=1)
        self.fav1_radio.grid(row=2, column=4)

        self.fav2_radio = Radiobutton(self.upper_right_frame, text="2", variable=self.fav_radio_value, value=2)
        self.fav2_radio.grid(row=2, column=5)

        self.fav3_radio = Radiobutton(self.upper_right_frame, text="3", variable=self.fav_radio_value, value=3)
        self.fav3_radio.grid(row=2, column=6)

        self.fav4_radio = Radiobutton(self.upper_right_frame, text="4", variable=self.fav_radio_value, value=4)
        self.fav4_radio.grid(row=2, column=7)

        self.fav5_radio = Radiobutton(self.upper_right_frame, text="5", variable=self.fav_radio_value, value=5)
        self.fav5_radio.grid(row=2, column=8)

        self.fav6_radio = Radiobutton(self.upper_right_frame, text="6", variable=self.fav_radio_value, value=6)
        self.fav6_radio.grid(row=2, column=9)

        self.fav7_radio = Radiobutton(self.upper_right_frame, text="7", variable=self.fav_radio_value, value=7)
        self.fav7_radio.grid(row=2, column=10)

        self.fav8_radio = Radiobutton(self.upper_right_frame, text="8", variable=self.fav_radio_value, value=8)
        self.fav8_radio.grid(row=2, column=11)

        self.add_fav_btn = tk.Button(self.upper_right_frame, text="add to Favorites", command=self.add_favorite)
        self.add_fav_btn.grid(row=2, column=12)

        self.separator = ttk.Separator(self.upper_right_frame, orient='horizontal')
        self.separator.grid(row=3, column=0, columnspan=12, sticky='we', ipady=15)

        # Section for group commands
        self.group_info_label = tk.Label(self.upper_right_frame, text="Group Command Options")
        self.group_info_label.grid(row=4, column=0)

        self.existing_groups_combo_label = tk.Label(self.upper_right_frame, text="Choose existing group:")
        self.existing_groups_combo_label.grid(row=5, column=0)

        self.existing_groups_combobox = ttk.Combobox(self.upper_right_frame, value=self.load_all_groups())
        self.existing_groups_combobox.grid(row=5, column=1)

        self.load_groups_btn = tk.Button(self.upper_right_frame, text="Load Group", command=self.load_group)
        self.load_groups_btn.grid(row=6, column=0)

        self.execute_group_btn = tk.Button(self.upper_right_frame, text="Execute Group", command=self.execute_group)
        self.execute_group_btn.grid(row=6, column=1)

        self.delete_groups_btn = tk.Button(self.upper_right_frame, text="Delete Group", command=self.delete_group)
        self.delete_groups_btn.grid(row=6, column=2)

        self.group_name_label = tk.Label(self.upper_right_frame, text="Group Name:")
        self.group_name_label.grid(row=7, column=0)

        self.group_name = StringVar()
        self.group_name_entry = tk.Entry(self.upper_right_frame)
        self.group_name_entry.grid(row=7, column=1)

        self.create_group_btn = tk.Button(self.upper_right_frame, text="Create Group", command=self.add_group_entry)
        self.create_group_btn.grid(row=7, column=2)

        self.add_command_label = tk.Label(self.upper_right_frame, text="Commands to add:")
        self.add_command_label.grid(row=8, column=0)

        self.adding_combobox = ttk.Combobox(self.upper_right_frame)
        self.adding_combobox.grid(row=8, column=1)

        self.update_group_btn = tk.Button(self.upper_right_frame, text="Update Group", command=self.update_group)
        self.update_group_btn.grid(row=8, column=2)

        self.group_command_label = tk.Label(self.upper_right_frame, text="Group Commands:")
        self.group_command_label.grid(row=9, column=0)

        self.loaded_group_combobox = ttk.Combobox(self.upper_right_frame)
        self.loaded_group_combobox.grid(row=9, column=1)

        self.delete_command_from_group_btn = tk.Button(self.upper_right_frame, text="Delete Command from Group",
                                                       command=self.delete_command_from_group)
        self.delete_command_from_group_btn.grid(row=9, column=2)

        # Bottom Left Frame
        self.bottom_left_frame = tk.Frame(self, bg='#ffffff', highlightbackground='black', highlightthickness=1)
        self.bottom_left_frame.grid(row=1, column=0, sticky='nsew')

        # Row 1 Favourite Buttons
        self.fav_label = tk.Label(self.bottom_left_frame, text="Favourite Execution Options: ")
        self.fav_label.grid(row=0, column=0)

        self.exec_btn = tk.Button(self.bottom_left_frame, text="Execute", command=self.execute_favorite)
        self.exec_btn.grid(row=0, column=1)

        self.del_btn = tk.Button(self.bottom_left_frame, text="Delete", command=self.delete_favorite)
        self.del_btn.grid(row=0, column=2)

        self.bl_fav_radio_value = IntVar()

        self.bl_fav1_radio = Radiobutton(self.bottom_left_frame, text="Favorite 1", variable=self.bl_fav_radio_value,
                                         value=1)
        self.bl_fav1_radio.grid(row=1, column=0)
        self.choosen_fav1_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav1_label.grid(row=1, column=1)

        self.bl_fav2_radio = Radiobutton(self.bottom_left_frame, text="Favorite 2", variable=self.bl_fav_radio_value,
                                         value=2)
        self.bl_fav2_radio.grid(row=2, column=0)
        self.choosen_fav2_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav2_label.grid(row=2, column=1)

        self.bl_fav3_radio = Radiobutton(self.bottom_left_frame, text="Favorite 3", variable=self.bl_fav_radio_value,
                                         value=3)
        self.bl_fav3_radio.grid(row=3, column=0)
        self.choosen_fav3_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav3_label.grid(row=3, column=1)

        self.bl_fav4_radio = Radiobutton(self.bottom_left_frame, text="Favorite 4", variable=self.bl_fav_radio_value,
                                         value=4)
        self.bl_fav4_radio.grid(row=4, column=0)
        self.choosen_fav4_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav4_label.grid(row=4, column=1)

        self.bl_fav5_radio = Radiobutton(self.bottom_left_frame, text="Favorite 5", variable=self.bl_fav_radio_value,
                                         value=5)
        self.bl_fav5_radio.grid(row=5, column=0)
        self.choosen_fav5_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav5_label.grid(row=5, column=1)

        self.bl_fav6_radio = Radiobutton(self.bottom_left_frame, text="Favorite 6", variable=self.bl_fav_radio_value,
                                         value=6)
        self.bl_fav6_radio.grid(row=6, column=0)
        self.choosen_fav6_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav6_label.grid(row=6, column=1)

        self.bl_fav7_radio = Radiobutton(self.bottom_left_frame, text="Favorite 7", variable=self.bl_fav_radio_value,
                                         value=7)
        self.bl_fav7_radio.grid(row=7, column=0)
        self.choosen_fav7_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav7_label.grid(row=7, column=1)

        self.bl_fav8_radio = Radiobutton(self.bottom_left_frame, text="Favorite 8", variable=self.bl_fav_radio_value,
                                         value=8)
        self.bl_fav8_radio.grid(row=8, column=0)
        self.choosen_fav8_label = tk.Label(self.bottom_left_frame, text="No Favorite")
        self.choosen_fav8_label.grid(row=8, column=1)

        # Bottom Right Frame
        self.bottom_right_frame = tk.Frame(self, bg='#ffffff', highlightbackground='black', highlightthickness=1)
        self.bottom_right_frame.grid(row=1, column=1, sticky='nsew')

        self.live_text = scrolledtext.ScrolledText(self.bottom_right_frame, width=75, height=15)
        self.live_text.config(highlightbackground='black', highlightthickness=2)
        self.live_text.pack()

        self.load_favorites()

    def execute_favorite(self):
        """
        Methode zum Ausführen eines Favorits. Es wird überprüft welcher
        Favorit ausgesucht wurde, woraufhin der entsprechende Befehl geladen
        und ausgeführt wird. Im Anschluss werden auch die übermittelten Daten
        im Fenster angezeigt
        """
        radio_value = self.bl_fav_radio_value.get()
        choosen_command = None
        if radio_value == 1:
            choosen_command = self.choosen_fav1_label.cget("text")
        elif radio_value == 2:
            choosen_command = self.choosen_fav2_label.cget("text")
        elif radio_value == 3:
            choosen_command = self.choosen_fav3_label.cget("text")
        elif radio_value == 4:
            choosen_command = self.choosen_fav4_label.cget("text")
        elif radio_value == 5:
            choosen_command = self.choosen_fav5_label.cget("text")
        elif radio_value == 6:
            choosen_command = self.choosen_fav6_label.cget("text")
        elif radio_value == 7:
            choosen_command = self.choosen_fav7_label.cget("text")
        elif radio_value == 8:
            choosen_command = self.choosen_fav8_label.cget("text")

        if len(orm.load_cmd(choosen_command, self.current_version)) == 0:
            if choosen_command == "No Favorite":
                self.notification_label.config(text="No Favorite to execute")
            else:
                self.notification_label.config(text="Command doesn't exist anymore")
        else:
            if choosen_command:
                loaded_cmd = self.return_loaded_command_as_list(choosen_command)
                ausgabe = Mmc(
                    self.serial_ports(),
                    loaded_cmd[5],
                    loaded_cmd[7],
                    loaded_cmd[9],
                    loaded_cmd[11],
                    loaded_cmd[13],
                    loaded_cmd[19],
                    loaded_cmd[21],
                    loaded_cmd[23],
                    loaded_cmd[25],
                    loaded_cmd[27],
                    loaded_cmd[29],
                    loaded_cmd[31],
                    loaded_cmd[33],
                    loaded_cmd[37],
                    loaded_cmd[35],
                    loaded_cmd[36],
                )
                ausgabe.findSlave()
                ausgabe.mmcExecute()
                self.live_text.insert('end', "---------NEW EXECUTION-------\n", 'warning')
                self.live_text.tag_config('warning', background="yellow", foreground="red")
                for messages in ausgabe.print_messages:
                    for message in messages[1]:
                        self.live_text.insert(tk.END, message)
                    self.live_text.insert(tk.END, "\n")
                self.live_text.insert('end', "---------EXECUTION END-------\n", 'warning')
                self.live_text.yview_pickplace("end")
                self.update()

    def execute_group(self):
        """
        Methode zum Ausführen einer Gruppe. Es wird ermittelt, welche Gruppe
        in der Combobox ausgewählt wurde. Diese Gruppe wird mit der Liste der
        dazugehörigen Befehle geladen. Durch die Liste der Befehle wird iteriert und
        alle notwendigen Informationen werden entweder zwischengespeichert (Zum ermitteln
        der Iterationsrunden einzelner Befehle) oder direkt verwertet zum Ausführen der Befehle
        """

        self.live_text.delete("1.0", "end")
        max_iteration = 0
        command_iteration_values = []
        all_commands = orm.load_group_commands(self.existing_groups_combobox.get())
        for command in all_commands:
            loaded_cmd = orm.load_cmd(command, self.current_version)
            if len(loaded_cmd) == 0:
                self.notification_label.config(text=f"Command {command} doesn't exist anymore")
            else:
                command_iteration_values.append(loaded_cmd[36])
                if loaded_cmd[36] > max_iteration:
                    max_iteration = loaded_cmd[36]
        iteration_counter = max_iteration
        while iteration_counter > 0:
            for command in all_commands:
                index = all_commands.index(command)
                if command_iteration_values[index] > 0:
                    loaded_cmd = self.return_loaded_command_as_list(command)
                    ausgabe = Mmc(
                        self.serial_ports(),
                        loaded_cmd[5],
                        loaded_cmd[7],
                        loaded_cmd[9],
                        loaded_cmd[11],
                        loaded_cmd[13],
                        loaded_cmd[19],
                        loaded_cmd[21],
                        loaded_cmd[23],
                        loaded_cmd[25],
                        loaded_cmd[27],
                        loaded_cmd[29],
                        loaded_cmd[31],
                        loaded_cmd[33],
                        loaded_cmd[37],
                        loaded_cmd[35],
                        loaded_cmd[36],
                    )
                    try:
                        if print_count() == 1:
                            ausgabe.findSlave()
                            ausgabe.mmcExecute()
                        else:
                            ausgabe.mmcExecute()

                        self.live_text.insert('end', f"---------NEW EXECUTION FOR {loaded_cmd[0]}-------\n", 'warning')
                        self.live_text.tag_config('warning', background="yellow", foreground="red")
                        for messages in ausgabe.print_messages:
                            for message in messages[1]:
                                self.live_text.insert(tk.END, message)
                            self.live_text.insert(tk.END, "\n")
                        self.live_text.insert('end', "---------EXECUTION END-------\n", 'warning')
                        self.live_text.yview_pickplace("end")
                        self.update()
                    except:
                        self.notification_label.config(text=f"Didnt' work for: {loaded_cmd[0]}")
                command_iteration_values[index] -= 1
            iteration_counter -= 1

    def return_loaded_command_as_list(self, input_cmd):
        loaded_values = []
        command = orm.load_cmd(input_cmd, self.current_version)
        for value in command:
            loaded_values.append(value)
        return loaded_values

    def add_command_to_group_command_list(self):
        """
        Methode, um einen Befehl zur Warteliste für die Gruppenbefehle hinzuzufügen
        :return:
        """
        self.notification_label.config(text="")
        if self.cb.get() and self.cb.get != "":
            if self.cb.get() not in self.group_command_list:
                self.group_command_list.append(self.cb.get())
                self.adding_combobox.config(value=self.group_command_list)
                self.notification_label.config(text=f"Added {self.cb.get()} to Wait List")
            else:
                self.notification_label.config(text="Command already in list")
        else:
            self.notification_label.config(text="Choose a command first")

    def add_group_entry(self):
        """
        Methode mit der ein defininierter Gruppenbefehl gespeichert wird
        """
        list_as_json = json.dumps(self.group_command_list)
        if orm.add_group_commands(self.group_name_entry.get(), self.current_version, list_as_json):
            self.existing_groups_combobox.config(values=self.load_all_groups())
            self.group_command_list.clear()
            self.adding_combobox.config(values=self.group_command_list)
            self.notification_label.config(text="Group Added")
        else:
            if orm.load_group(self.group_name_entry.get()):
                print(orm.load_group(self.group_name_entry.get()))
                self.notification_label.config(text="Group already exists")
            else:
                self.notification_label.config(text="Group not added")

    def load_all_groups(self):
        """
        Methode, die alle Gruppenbefehle aus der Datenbank lädt
        :return: Liste aller Gruppenbefehle
        """
        group_names = []
        result = orm.load_all_groups(self.current_version)
        for group in result:
            group_names.append(group[0])
        return group_names

    def load_all_group_commands(self):
        """
        Methode, die alle Gruppebefehle lädt und in der entsprechenden Combobox anzeigt
        """
        result = orm.load_group_commands(self.existing_groups_combobox.get())
        self.loaded_group_combobox.config(values=result)

    def delete_command_from_group(self):
        """
        Methode, die einen ausgewählten Gruppenbefehl löscht
        """
        self.notification_label.config(text="")
        if self.existing_groups_combobox.get():
            command_list = orm.load_group_commands(self.existing_groups_combobox.get())
            choosen_command = self.loaded_group_combobox.get()
            if choosen_command:
                command_list.remove(choosen_command)
                orm.update_group_command_list(self.existing_groups_combobox.get(), json.dumps(command_list))
                self.loaded_group_combobox.config(values=self.load_all_group_commands())
                self.loaded_group_combobox.set('')
                self.notification_label.config(text="Command removed from group")
            else:
                self.notification_label.config(text="Choose command to remove from group")
        else:
            self.notification_label.config(text="Choose group first")

    def update_group(self):
        """
        Methode die einen ausgewählten und geladenen Gruppenbefehl updatet.
        Hier werden Gruppenname und Befehlsliste geupdatet, sofern es eine Änderung gibt
        """
        current_name = self.existing_groups_combobox.get()
        new_name = self.group_name_entry.get()
        if current_name != "" and new_name != "":
            current_group_commands = orm.load_group_commands(self.existing_groups_combobox.get())
            for command in self.group_command_list:
                if command not in current_group_commands:
                    current_group_commands.append(command)
            if orm.update_group(current_name, new_name, json.dumps(current_group_commands)):
                self.existing_groups_combobox.config(values=self.load_all_groups())
                self.group_command_list.clear()
                self.adding_combobox.config(values=self.group_command_list)
                self.notification_label.config(text="Group Updated")
            else:
                self.notification_label.config(text="Couldn't Update Group")

    def load_group(self):
        """
        Methode, die einen ausgewählten Gruppenbefehl lädt
        """
        if self.existing_groups_combobox.get():
            result = orm.load_group(self.existing_groups_combobox.get())
            self.group_name.set(result[0])
            self.group_name_entry.config(textvariable=self.group_name)
            commands = json.loads(result[1])
            self.loaded_group_combobox.config(values=commands)
            self.group_command_list.clear()
            self.adding_combobox.config(values=self.group_command_list)
            self.adding_combobox.set('')
            self.notification_label.config(text="Group loaded")
        else:
            self.notification_label.config(text="Can't Load Group")

    def delete_group(self):
        """
        Methode, die einen ausgewäglten Gruppenbefehl löscht
        """
        if self.existing_groups_combobox.get():
            if orm.delete_group(self.existing_groups_combobox.get()):
                self.existing_groups_combobox.config(values=self.load_all_groups())
                self.existing_groups_combobox.set('')
                self.notification_label.config(text="Deleted Group")
            else:
                self.notification_label.config(text="Can't Delete")
        else:
            self.notification_label.config(text="Choose Group to Delete")

    def serial_ports(self):
        """
        Methode, mit der der COM Port automatisch ermittelt wird
        :return: Liste aller gefundenen COM Ports
        """
        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result[0]

    def toggle_from_value(self):
        """
        Methode, die bei Auswahl des Master Radio Buttons, den From Wert auf 1 ändert
        und bei der Auswahl von Slave auf 0
        """
        if self.radio_btn_value.get():
            self.from_byte.set(1)
            self.from_byte_entry.config(textvariable=self.from_byte)
        elif not self.radio_btn_value.get():
            self.from_byte.set(0)
            self.from_byte_entry.config(textvariable=self.from_byte)

    def check_from_to_fields(self):
        """
        Überprüft, dass Master nur den Wert 1 annehmen kann und ein Slave nur die Werte 0 und 2-99
        :return: Gibt False zurück, wenn Bedingungen nicht erfüllt sind, andernfalls True
        """
        value_validation = int(self.from_byte_entry.get())
        if self.radio_btn_value.get() and value_validation != 1:
            self.notification_label.config(text="Master must have From Value 1")
            return False
        elif not self.radio_btn_value.get() and value_validation == 1 or value_validation < 0 or value_validation > 99:
            self.notification_label.config(text="Slava Value can't be 1, smaller than 0, and higher than 99")
            return False
        else:
            return True

    def load_favorites(self):
        """
        Methode, die alle Favoritenbefehle aus der Datenbank lädt und anzeigt
        """
        result = orm.load_favorites(self.current_version)
        self.choosen_fav1_label.config(text=result[0])
        self.choosen_fav2_label.config(text=result[1])
        self.choosen_fav3_label.config(text=result[2])
        self.choosen_fav4_label.config(text=result[3])
        self.choosen_fav5_label.config(text=result[4])
        self.choosen_fav6_label.config(text=result[5])
        self.choosen_fav7_label.config(text=result[6])
        self.choosen_fav8_label.config(text=result[7])

    def delete_favorite(self):
        """
        Methode, die einen ausgewählten Favoriten aus der Liste
        der Favoriten entfernt
        """
        self.notification_label.config(text="")
        radio_value = self.bl_fav_radio_value.get()
        choosen_favorite = "Favorite" + str(radio_value)
        choosen_favorite_command = ""

        if radio_value == 1:
            choosen_favorite_command = self.choosen_fav1_label.cget("text")
        elif radio_value == 2:
            choosen_favorite_command = self.choosen_fav2_label.cget("text")
        elif radio_value == 3:
            choosen_favorite_command = self.choosen_fav3_label.cget("text")
        elif radio_value == 4:
            choosen_favorite_command = self.choosen_fav4_label.cget("text")
        elif radio_value == 5:
            choosen_favorite_command = self.choosen_fav5_label.cget("text")
        elif radio_value == 6:
            choosen_favorite_command = self.choosen_fav6_label.cget("text")
        elif radio_value == 7:
            choosen_favorite_command = self.choosen_fav7_label.cget("text")
        elif radio_value == 8:
            choosen_favorite_command = self.choosen_fav8_label.cget("text")

        try:
            if choosen_favorite_command == "No Favorite":
                self.notification_label.config(text="No Favorite to delete here")
            else:
                orm.delete_favorite(choosen_favorite_command, choosen_favorite)
                self.load_favorites()
                self.notification_label.config(text=f"Favorite {radio_value} deleted")
        except:
            if radio_value == 0:
                self.notification_label.config(text="Choose Favorite to delete")

    def add_entry(self):
        """
        Methode, die anhand der ausgefüllten Felder einen Befehl erstellt
        und in der Datenbank abspeichert
        """
        if len(orm.load_cmd(self.command_name_entry.get(), self.current_version)) > 0:
            self.notification_label.config(text="Command already exists")
        else:
            self.notification_label.config(text="")
            version = orm.get_current_version(self.current_version)
            new_command = orm.Command(
                cname=self.command_name_entry.get(),
                master=self.radio_btn_value.get(),
                sof_byte=self.sof_byte_entry.get(),
                to_byte=self.to_byte_entry.get(),
                from_byte=self.from_byte_entry.get(),
                vers_byte=self.vers_byte_entry.get(),
                hops_byte=self.hops_byte_entry.get(),
                apNr_byte=self.apNr_byte_entry.get(),
                crc_byte=self.crc_byte_entry.get(),
                eof_byte=self.eof_byte_entry.get(),
                l7sdu0_byte=self.sdu_0_byte_entry.get(),
                l7sdu1_byte=self.sdu_1_byte_entry.get(),
                l7sdu2_byte=self.sdu_2_byte_entry.get(),
                l7sdu3_byte=self.sdu_3_byte_entry.get(),
                l7sdu4_byte=self.sdu_4_byte_entry.get(),
                l7sdu5_byte=self.sdu_5_byte_entry.get(),
                l7sdu6_byte=self.sdu_6_byte_entry.get(),
                l7sdu7_byte=self.sdu_7_byte_entry.get(),
                delay=self.delay_entry.get(),
                iteration=self.iteration_entry.get(),
                participants=self.participants_entry.get(),

                sof_name=self.sof_name_entry.get(),
                to_name=self.to_name_entry.get(),
                from_name=self.to_name_entry.get(),
                vers_name=self.vers_name_entry.get(),
                hops_name=self.hops_name_entry.get(),
                apNr_name=self.apNr_name_entry.get(),
                crc_name=self.crc_name_entry.get(),
                eof_name=self.eof_name_entry.get(),
                l7sdu0_name=self.sdu_0_name_entry.get(),
                l7sdu1_name=self.sdu_1_name_entry.get(),
                l7sdu2_name=self.sdu_2_name_entry.get(),
                l7sdu3_name=self.sdu_3_name_entry.get(),
                l7sdu4_name=self.sdu_4_name_entry.get(),
                l7sdu5_name=self.sdu_5_name_entry.get(),
                l7sdu6_name=self.sdu_6_name_entry.get(),
                l7sdu7_name=self.sdu_7_name_entry.get(),
            )

            if (
                    (self.command_name_entry.get() != "") and
                    (self.sof_byte_entry.get() != "") and
                    (self.to_byte_entry.get() != "") and
                    (self.from_byte_entry.get() != "") and
                    (self.vers_byte_entry.get() != "") and
                    (self.hops_byte_entry.get() != "") and
                    (self.apNr_byte_entry.get() != "") and
                    (self.crc_byte_entry.get() != "") and
                    (self.eof_byte_entry.get() != "") and
                    (self.sdu_0_byte_entry.get() != "") and
                    (self.sdu_1_byte_entry.get() != "") and
                    (self.sdu_2_byte_entry.get() != "") and
                    (self.sdu_3_byte_entry.get() != "") and
                    (self.sdu_4_byte_entry.get() != "") and
                    (self.sdu_5_byte_entry.get() != "") and
                    (self.sdu_6_byte_entry.get() != "") and
                    (self.sdu_7_byte_entry.get() != "") and
                    (self.delay_entry.get() != "") and
                    (self.iteration_entry.get() != "") and
                    (self.com_entry.get() != "") and
                    (self.participants_entry.get() != "")
            ):
                try:
                    version.commands.append(new_command)
                    orm.session_commit()
                    self.cb.config(values=orm.get_current_version_commands(self.current_version))
                    self.notification_label.config(text="Command added")
                except:
                    orm.session_rollback()
                    if orm.cmd_exists(self.version_label.cget("text")):
                        self.notification_label.config(text="Command already exists")
            else:
                self.notification_label.config(text="Fill all the necessary fields")

    def execute_dropdown_option(self):
        """
        Methode, bei der ein ausgewählter Befehl ausgeführt wird
        """
        self.notification_label.config(text="")

        if not self.check_from_to_fields():
            pass
        elif self.check_from_to_fields():
            ausgabe = Mmc(
                self.serial_ports(),
                int(self.to_byte_entry.get()),
                int(self.from_byte_entry.get()),
                int(self.vers_byte_entry.get()),
                int(self.hops_byte_entry.get()),
                int(self.apNr_byte_entry.get()),
                int(self.sdu_0_byte_entry.get()),
                int(self.sdu_1_byte_entry.get()),
                int(self.sdu_2_byte_entry.get()),
                int(self.sdu_3_byte_entry.get()),
                int(self.sdu_4_byte_entry.get()),
                int(self.sdu_5_byte_entry.get()),
                int(self.sdu_6_byte_entry.get()),
                int(self.sdu_7_byte_entry.get()),
                int(self.participants_entry.get()),
                int(self.delay_entry.get()),
                int(self.iteration_entry.get()),
            )
            ausgabe.findSlave()
            ausgabe.mmcExecute()
            self.live_text.insert('end', "---------NEW EXECUTION-------\n", 'warning')
            self.live_text.tag_config('warning', background="yellow", foreground="red")
            for messages in ausgabe.print_messages:
                for message in messages[1]:
                    self.live_text.insert(tk.END, message)
                self.live_text.insert(tk.END, "\n")
            self.live_text.insert('end', "---------EXECUTION END-------\n", 'warning')
            self.live_text.yview_pickplace("end")
            self.update()

    def delete_dropdown_option(self):
        """
        Methode, bei der ein ausgewählter Befehl aus der Liste bestehender Befehle
        gelöscht wird
        """
        if self.cb.get():
            chosen_cmd = self.cb.get()
            orm.delete_cmd(chosen_cmd)
            self.cb.config(values=orm.get_current_version_commands(self.current_version))
            self.cb.set('')
            self.notification_label.config(text="Command deleted from list")
        else:
            self.notification_label.config(text="Choose command to delete")

    def add_favorite(self):
        """
        Methode, mit der ein Befehl zu den Favoriten hinzugefügt wird
        """
        self.notification_label.config(text="")
        try:
            orm.add_favorite(self.cb.get(), self.current_version, self.fav_radio_value.get())
            self.notification_label.config(text="Command added to Favorites")
            if self.fav_radio_value.get() == 1:
                self.choosen_fav1_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 2:
                self.choosen_fav2_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 3:
                self.choosen_fav3_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 4:
                self.choosen_fav4_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 5:
                self.choosen_fav5_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 6:
                self.choosen_fav6_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 7:
                self.choosen_fav7_label.config(text=self.cb.get())
            elif self.fav_radio_value.get() == 8:
                self.choosen_fav8_label.config(text=self.cb.get())
            self.load_favorites()
        except:
            self.notification_label.config(text="Choose Favorite to add")

    def update_command(self):
        """
        Methode, mit der ein geladener Befehl geupdated wird
        """
        orm.update_cmd(
            self.cb.get(),
            self.command_name_entry.get(),
            self.radio_btn_value.get(),
            self.sof_byte_entry.get(),
            self.sof_name_entry.get(),
            self.to_byte_entry.get(),
            self.to_name_entry.get(),
            self.from_byte_entry.get(),
            self.from_name_entry.get(),
            self.vers_byte_entry.get(),
            self.vers_name_entry.get(),
            self.hops_byte_entry.get(),
            self.hops_name_entry.get(),
            self.apNr_byte_entry.get(),
            self.apNr_name_entry.get(),
            self.crc_byte_entry.get(),
            self.crc_name_entry.get(),
            self.eof_byte_entry.get(),
            self.eof_name_entry.get(),
            self.sdu_0_byte_entry.get(),
            self.sdu_0_name_entry.get(),
            self.sdu_1_byte_entry.get(),
            self.sdu_1_name_entry.get(),
            self.sdu_2_byte_entry.get(),
            self.sdu_2_name_entry.get(),
            self.sdu_3_byte_entry.get(),
            self.sdu_3_name_entry.get(),
            self.sdu_4_byte_entry.get(),
            self.sdu_4_name_entry.get(),
            self.sdu_5_byte_entry.get(),
            self.sdu_5_name_entry.get(),
            self.sdu_6_byte_entry.get(),
            self.sdu_6_name_entry.get(),
            self.sdu_7_byte_entry.get(),
            self.sdu_7_name_entry.get(),
            self.delay_entry.get(),
            self.iteration_entry.get(),
            self.participants_entry.get()
        )
        self.cb.config(values=orm.get_current_version_commands(self.current_version))
        self.notification_label.config(text="Command Updated")
        self.cb.set(self.command_name_entry.get())

    def load_cmd(self):
        """
        Methode mit der ein ausgewählter Befehl geladen wird und
        dessen Werte in den Eingabefeldern geladen wird
        """
        chosen_cmd = self.cb.get()
        result = orm.load_cmd(chosen_cmd, self.current_version)

        # Load Command Name
        self.cmd.set(result[0])
        self.command_name_entry.config(textvariable=self.cmd)

        # Load Radio Value
        self.radio_btn_value.set(result[2])

        # Load SOF Byte
        self.sof_byte.set(result[3])
        self.sof_byte_entry.config(textvariable=self.sof_byte)

        # Load SOF Name
        # Falls Probleme auftauchen wieder result[xyz] == None
        if result[4] is None:
            self.sof_name.set("")
        else:
            self.sof_name.set(result[4])
        self.sof_name_entry.config(textvariable=self.sof_name)

        # Load To Byte
        self.to_byte.set(result[5])
        self.to_byte_entry.config(textvariable=self.to_byte)

        # Load To Name
        if result[6] is None:
            self.to_name.set("")
        else:
            self.to_name.set(result[6])
        self.to_name_entry.config(textvariable=self.to_name)

        # Load From Byte
        self.from_byte.set(result[7])
        self.from_byte_entry.config(textvariable=self.from_byte)

        # Load From Name
        if result[8] is None:
            self.from_name.set("")
        else:
            self.from_name.set(result[8])
        self.from_name_entry.config(textvariable=self.from_name)

        # Load Vers Byte
        self.vers_byte.set(result[9])
        self.vers_byte_entry.config(textvariable=self.vers_byte)

        # Load Vers Name
        if result[10] is None:
            self.vers_name.set("")
        else:
            self.vers_name.set(result[10])
        self.vers_name_entry.config(textvariable=self.vers_name)

        # Load Hops Byte
        self.hops_byte.set(result[11])
        self.hops_byte_entry.config(textvariable=self.hops_byte)

        # Load Hops Name
        if result[11] is None:
            self.hops_name.set("")
        else:
            self.hops_name.set(result[12])
        self.hops_name_entry.config(textvariable=self.hops_name)

        # Load apNr Byte
        self.apNr_byte.set(result[13])
        self.apNr_byte_entry.config(textvariable=self.apNr_byte)

        # Load apNr Name
        if result[14] is None:
            self.apNr_name.set("")
        else:
            self.apNr_name.set(result[14])
        self.apNr_name_entry.config(textvariable=self.apNr_name)

        # Load Crc Byte
        self.crc_byte.set(result[15])
        self.crc_byte_entry.config(textvariable=self.crc_byte)

        # Load Crc Name
        if result[16] is None:
            self.crc_name.set("")
        else:
            self.crc_name.set(result[16])
        self.crc_name_entry.config(textvariable=self.crc_name)

        # Load Eof Byte
        self.eof_byte.set(result[17])
        self.eof_byte_entry.config(textvariable=self.eof_byte)

        # Load Eof Name
        if result[18] is None:
            self.eof_name.set("")
        else:
            self.eof_name.set(result[18])
        self.eof_name_entry.config(textvariable=self.eof_name)

        # Load L7sdu0 Byte
        self.sdu0_byte.set(result[19])
        self.sdu_0_byte_entry.config(textvariable=self.sdu0_byte)

        # Load L7sdu0 Name
        if result[20] is None:
            self.sdu0_name.set("")
        else:
            self.sdu0_name.set(result[20])
        self.sdu_0_name_entry.config(textvariable=self.sdu0_name)

        # Load L7sdu1 Byte
        self.sdu1_byte.set(result[21])
        self.sdu_1_byte_entry.config(textvariable=self.sdu1_byte)

        # Load L7sdu1 Name
        if result[22] is None:
            self.sdu1_name.set("")
        else:
            self.sdu1_name.set(result[22])
        self.sdu_1_name_entry.config(textvariable=self.sdu1_name)

        # Load L7sdu2 Byte
        self.sdu2_byte.set(result[23])
        self.sdu_2_byte_entry.config(textvariable=self.sdu2_byte)

        # Load L7sdu2 Name
        if result[24] is None:
            self.sdu2_name.set("")
        else:
            self.sdu2_name.set(result[24])
        self.sdu_2_name_entry.config(textvariable=self.sdu2_name)

        # Load L7sdu3 Byte
        self.sdu3_byte.set(result[25])
        self.sdu_3_byte_entry.config(textvariable=self.sdu3_byte)

        # Load L7sdu3 Name
        if result[26] is None:
            self.sdu3_name.set("")
        else:
            self.sdu3_name.set(result[26])
        self.sdu_3_name_entry.config(textvariable=self.sdu3_name)

        # Load L7sdu4 Byte
        self.sdu4_byte.set(result[27])
        self.sdu_4_byte_entry.config(textvariable=self.sdu4_byte)

        # Load L7sdu4 Name
        if result[28] is None:
            self.sdu4_name.set("")
        else:
            self.sdu4_name.set(result[28])
        self.sdu_4_name_entry.config(textvariable=self.sdu4_name)

        # Load L7sdu5 Byte
        self.sdu5_byte.set(result[29])
        self.sdu_5_byte_entry.config(textvariable=self.sdu5_byte)

        # Load L7sdu5 Name
        if result[30] is None:
            self.sdu5_name.set("")
        else:
            self.sdu5_name.set(result[30])
        self.sdu_5_name_entry.config(textvariable=self.sdu5_name)

        # Load L7sdu6 Byte
        self.sdu6_byte.set(result[31])
        self.sdu_6_byte_entry.config(textvariable=self.sdu6_byte)

        # Load L7sdu6 Name
        if result[32] is None:
            self.sdu6_name.set("")
        else:
            self.sdu6_name.set(result[32])
        self.sdu_6_name_entry.config(textvariable=self.sdu6_name)

        # Load L7sdu7 Byte
        self.sdu7_byte.set(result[33])
        self.sdu_7_byte_entry.config(textvariable=self.sdu7_byte)

        # Load L7sdu7 Name
        if result[34] is None:
            self.sdu7_name.set("")
        else:
            self.sdu7_name.set(result[34])
        self.sdu_7_name_entry.config(textvariable=self.sdu7_name)

        # Load Delay
        self.delay.set(result[35])
        self.delay_entry.config(textvariable=self.delay)

        # Load Iteration
        self.iteration.set(result[36])
        self.iteration_entry.config(textvariable=self.iteration)

        # Load Number Participants
        self.participants.set(result[37])
        self.participants_entry.config(textvariable=self.participants)

        # Gleich Load Number Paricipants result[37] und nicht mehr result[38]


def print_count():
    """
    Diese Methode dient dazu den Aufruf einer Funktion zu zählen.
    :return: print_count.counter
    """
    print_count.counter += 1
    return print_count.counter


print_count.counter = 0
