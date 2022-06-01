from _tkinter import *
from tkinter import *
from tkinter import font
from PortScanner import PortScanner as pscanner
from VulnerabilityScanner import VulnerabilityScanner as vscanner
import tkinter as tk
import tkinter.scrolledtext as st
import customtkinter
import threading
import time


main_color = "#414141"

# This is the root Window
root = customtkinter.CTk()
# create Label

open_tcp_ports = []  # first
open_udp_ports = []  # kol port udp osado el service bet3to
udp_services = []

open_tcp_vul_ports = []  # kol port wel banner bet3to
open_tcp_vul_banners = []

bg = PhotoImage(file="res/img.png")
new_back = customtkinter.CTkLabel(root, image=bg)
new_back.place(x=0, y=0, relwidth=1, relheight=1)

text_area = st.ScrolledText(root,
                            width=50,
                            height=19,
                            font=("Times New Roman",
                                  15))
text_area.grid(column=0, pady=80, padx=80)

text_area.insert(tk.INSERT,
                 """\
1st
                 """, 'x')


text_area.insert(tk.INSERT,
                 """\
                 2nd
                 
                 """, 'y')
text_area.tag_config('x', foreground='red')
text_area.tag_config('y', foreground='gold')


text_area.configure(state='disabled')
# This Function Take victim ip and number if ports that we want to scan
# and then fill open_tcp_ports, open_udp_ports, udp_services
# You Should Call it when user click to Scan Button


def scan_victim_ports(victim, number_of_ports):
    port_scanner = pscanner(victim=victim, number_of_ports=number_of_ports)

    global open_tcp_ports
    global open_udp_ports
    global udp_services

    if (port_scanner.scan(method='TCP') and port_scanner.scan('UDP')):
        open_tcp_ports = port_scanner.get_open_tcp_ports()
        open_udp_ports = port_scanner.get_open_udp_ports()
        udp_services = port_scanner.get_udp_service()
    else:
        return False
    return True


# This Function Take victim ip and number if ports that we want to scan for VULNERABILITY
# and then fill open_tcp_vul_ports, open_tcp_vul_banners
# You Should Call it when user click to Scan Button
def scan_victim_vul(victim, number_of_ports):
    global open_tcp_vul_ports
    global open_tcp_vul_banners
    vul_scanner = vscanner(victim_ip=victim, number_of_ports=number_of_ports)
    if (vul_scanner.vulnerability_scan()):
        open_tcp_vul_ports = vul_scanner.get_open_ports()
        open_tcp_vul_banners = vul_scanner.get_vulnerability()
    else:
        return False
    return True

# This is Function Will invoke when user click on scan button
# TODO: WE MUST CALL THIS FUNCTION IN ANOTHER THREAD
# Print statement just for illustration YOU Should Delete it


def scan_victim2():
    victim = target_input.get()
    number_of_ports = number_of_ports_input.get()
    if (scan_victim_ports(victim=victim, number_of_ports=number_of_ports) and scan_victim_vul(victim=victim, number_of_ports=number_of_ports)):
        print("==[ Open TCP Ports ]==")
        for i in open_tcp_ports:
            print(i)
        print("==[ Open UDP Ports ]==")
        cnt = 0
        for i in open_udp_ports:
            print(f'{i} -> {udp_services[cnt]}')
            cnt += 1

        print("==[ Vul Ports ]==")
        cnt = 0
        for i in open_tcp_vul_ports:
            print(f"{i} -> {open_tcp_vul_banners[cnt]}")
            cnt += 1

    else:
        assert "Check Victim IP of Number of Ports"


def runDiffThread():
    t = threading.Thread(target=scan_victim2)
    t.start()


target_label = customtkinter.CTkLabel(
    root, text="Target", bg=main_color, fg="white")
target_label.place(x=10, y=13)

# TODO: You Must Make Sure that user enter valid IP Address
target_input = customtkinter.CTkEntry(root)
target_input.insert(0, '192.168.1.1')
target_input.place(x=120, y=13)

# TODO: You Must Check that user enter ports number in range between 1 to 2^16
number_of_ports_input = customtkinter.CTkEntry(root)
number_of_ports_input.insert(0, '# of Ports')
number_of_ports_input.place(x=250, y=13)

scan_button = customtkinter.CTkButton(
    root, text="Scan Port", command=runDiffThread)
scan_button.place(x=400, y=10)

#vul_text_area = Text(root)
#vul_text_area.place(x=20, y=60)
# listbox = Listbox(root)
#
# listbox.insert(1,"Bread")
# listbox.insert(2, "Milk")
# listbox.insert(3, "Meat")
# listbox.insert(4, "Cheese")
# listbox.insert(5, "Vegetables")
#
# listbox.place(x=20, y=60)
#listbox.size(x=50, y=80)

#T = Text(root, height = 5, width = 52)

# Create label

#l.config(font =("Courier", 14))

# Fact = """A man can be arrested """
# #l.size(x=50, y=80)
# l.pack()


# tk.Label(root,
# text = "ScrolledText Widget Example",
#          font = ("Times New Roman", 15),
#          background = 'green',
#          foreground = "white").grid(column = 0,
#                                     row = 0)


root['bg'] = main_color
# Title of Window
root.title("3en7ors")
# Size of Window
root.geometry("690x500")
root.iconbitmap('res/eye.ico')
root.resizable(False, False)
# INIT Window
root.mainloop()
