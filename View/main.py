from tkinter import *
from version_overview import VersionOverview

"""
Hauptklasse, in der eine Instanz von Tk() erzeugt wird
und diese dann in der neu erstellten Instanz von 
VersionOverview übergeben wird
"""

root = Tk()
root.geometry("700x80")
version_overview = VersionOverview(root)
root.mainloop()