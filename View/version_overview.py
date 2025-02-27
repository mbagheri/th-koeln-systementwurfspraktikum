import Model.orm_controller as orm
from tkinter import *
from tkinter import ttk
from version_control import VersionControl


class VersionOverview:

    def __init__(self, master):
        """
        Initialisierungsmethode, die aufgerufen wird beim Erstellen
        einer VersionOverview Instanz.
        :param master: Ist eine Instanz von Tk(), in der die Elemente des Fenster gerendert werden
        """
        orm.create_db()

        self.master = master
        self.master.title("Version Overview")

        # Row 1 widgets
        self.version_list = ["Test-Project 1", "Test-Project 2", "Test-Project 3"]

        self.new_version_entry = Entry(master)
        self.new_version_entry.insert(END, "Version Name Here")
        self.new_version_entry.grid(row=0, column=0)

        self.add_project_button = Button(master, text="add new version", padx=5, pady=5, command=self.add_new_version)
        self.add_project_button.grid(row=0, column=1)

        self.notification_label = Label(master, text="", fg="red")
        self.notification_label.grid(row=0, column=2)

        # Row 2 widgets
        self.combobox_label = Label(master, text="Choose existing Version to open or to delete:")
        self.combobox_label.grid(row=1, column=0)

        self.combobox_option = StringVar()
        self.combobox_option.set("Choose a Version")
        self.combobox = ttk.Combobox(master, value=orm.get_all_versions())
        self.combobox.grid(row=1, column=1)

        self.combobox_version_open = Button(master, text="open version", padx=5, pady=5, command=self.open_version)
        self.combobox_version_open.grid(row=1, column=2)

        self.combobox_version_delete = Button(master, text="delete version", padx=5, pady=5, command=self.delete_version)
        self.combobox_version_delete.grid(row=1, column=3)

    def add_new_version(self):
        """
        Methode, um eine neue Version hinzuzufügen
        :return:
        """
        self.notification_label.config(text="")
        version_name = self.new_version_entry.get()
        if version_name and version_name != "Version Name Here":
                version = orm.Version(vname=version_name)
                if orm.add_version(version):
                    self.combobox.config(values=orm.get_all_versions())
                    self.notification_label.config(text="Version added successfully")
                else:
                    self.notification_label.config(text="Version already exists")
        else:
            self.notification_label.config(text="Write a version name")

    def open_version(self):
        """
        Methode, um eine ausgewählte Version zu öffnen
        :return:
        """
        self.notification_label.config(text="")
        chosen_version = self.combobox.get()
        if chosen_version:
            VersionControl(chosen_version)
        else:
            self.notification_label.config(text="Choose version to open")

    def delete_version(self):
        """
        Methode, um eine ausgewählte Version zu entfernen
        :return:
        """
        self.notification_label.config(text="")
        chosen_version = self.combobox.get()
        if chosen_version:
            if orm.delete_version(chosen_version):
                self.combobox.config(values=orm.get_all_versions())
                self.combobox.set('')
                self.notification_label.config(text="Version deleted successfully")
            else:
                self.notification_label.config(text="Version not available")
        else:
            self.notification_label.config(text="Choose version to delete")
