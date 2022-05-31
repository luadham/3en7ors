from _tkinter import *
from tkinter import *
from tkinter import font
from PortScanner import PortScanner as pscanner
from VulnerabilityScanner import VulnerabilityScanner as vscanner

main_color = "#414141"

# This is the root Window
root = Tk()
# create Label
# Add label to screen

open_tcp_ports = []
tcp_banners = []
vul_ports = []
vul_banners = []
open_udp_ports = []
udp_service = []

def scan_victim():
    pass



target_label = Label(root, text="Target", bg=main_color, fg="white")
target_label.place(x=10, y=13)

target_input = Entry(root)
target_input.insert(0, '192.168.1.1')
target_input.place(x=80, y=13)

number_of_ports_input = Entry(root)
number_of_ports_input.insert(0, '# of Ports')
number_of_ports_input.place(x=250, y=13)

scan_button = Button(root, text="Scan Port", command=scan_victim)
scan_button.place(x=400, y=10)

vul_text_area = Text(root)
vul_text_area.place(x=20, y=60)

root['bg'] = main_color
# Title of Window
root.title("3en7ors")
# Size of Window
root.geometry("690x500")
# INIT Window
root.mainloop()
