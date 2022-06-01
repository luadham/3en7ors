from _tkinter import *
from cProfile import label
from tkinter import *
from tkinter import font
import tkinter
from tkinter import messagebox
from turtle import bgcolor, color
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

# 1
open_tcp_ports = []  # first

# 2
####
open_udp_ports = []  # kol port udp osado el service bet3to
udp_services = []
####

# 3
# red
open_tcp_vul_ports = []  # kol port wel banner bet3to
open_tcp_vul_banners = []
# red

new_back = customtkinter.CTkLabel(root)
new_back.place(x=0, y=0, relwidth=1, relheight=1)

# Text Area
text_area = st.ScrolledText(root,
                            width=50,
                            height=19, font=("Times New Roman", 15))
text_area.grid(column=0, pady=100, padx=110)

text_area.tag_config('x', foreground='red')
text_area.tag_config('y', foreground='gold')
text_area.tag_config('g', foreground='green')


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
# Print statement just for illustration YOU Should Delete it


def scan_victim():
    victim = target_input.get()
    number_of_ports = number_of_ports_input.get()
    global text_area
    print("I will scan")
    scan_button.configure(state=tkinter.DISABLED)
    if (scan_victim_ports(victim=victim, number_of_ports=number_of_ports) and scan_victim_vul(victim=victim, number_of_ports=number_of_ports)):
        
        text_area.insert(
            tk.INSERT, "==[ Open Vulnerability Ports ]==\n", 'black')
        text_area.insert(tk.INSERT, "Port\tBanner\n", 'black')
        idx = 0
        for port in open_tcp_vul_banners:
            text_area.insert(
                tk.INSERT, f"{open_tcp_vul_ports[idx]}\t{open_tcp_vul_banners[idx]}\n", 'x')
        text_area.insert(tk.INSERT, "==[ Open TCP Ports ]==\n", 'black')
        text_area.insert(tk.INSERT, "Port\tStatus\n", 'black')

        for port in open_tcp_ports:
            text_area.insert(tk.INSERT, f"{port}\tOpen\n", 'g')

        text_area.insert(tk.INSERT, "==[ Open UDP Ports ]==\n", 'black')
        text_area.insert(tk.INSERT, "Port\tService\n", 'black')

        idx = 0
        for port in open_udp_ports:
            text_area.insert(
                tk.INSERT, f"{open_udp_ports[idx]}\t{udp_services[idx]}\n", 'g')
            idx += 1

        text_area.configure(state='disabled')
        scan_button.configure(state=tkinter.NORMAL)
    if(int(number_of_ports) > int(number_of_ports) << 16 or int(number_of_ports) <= 1):
        print("a")
        messagebox.showerror("Error", "Enter a valid port number")
    else:
        global text_area
        
        print("I will scan")
        scan_button.configure(state=tkinter.DISABLED)
        if (scan_victim_ports(victim=victim, number_of_ports=number_of_ports) and scan_victim_vul(victim=victim, number_of_ports=number_of_ports)):
            text_area.insert(
                tk.INSERT, "==[ Open Vulnerability Ports ]==\n", 'black')
            text_area.insert(tk.INSERT, "Port\tBanner\n", 'black')
            idx = 0
            if(len(open_tcp_vul_ports) == 0):
                text_area.insert(tk.INSERT, "There is nothing opened\n",'g')
            for port in open_tcp_vul_banners:
                text_area.insert(
                    tk.INSERT, f"{open_tcp_vul_ports[idx]}\t{open_tcp_vul_banners[idx]}\n", 'x')
            text_area.insert(tk.INSERT, "==[ Open TCP Ports ]==\n", 'black')
            text_area.insert(tk.INSERT, "Port\tStatus\n", 'black')
            if(len(open_tcp_ports) == 0):
                text_area.insert(tk.INSERT, "There is nothing opened\n",'g')


            for port in open_tcp_ports:
                text_area.insert(tk.INSERT, f"{port}\tOpen\n", 'g')

            text_area.insert(tk.INSERT, "==[ Open UDP Ports ]==\n", 'black')
            text_area.insert(tk.INSERT, "Port\tService\n", 'black')

            idx = 0
            if(len(open_udp_ports) == 0):
                text_area.insert(tk.INSERT, "There is nothing opened\n",'g')
            for port in open_udp_ports:
                text_area.insert(
                    tk.INSERT, f"{open_udp_ports[idx]}\t{udp_services[idx]}\n", 'g')
                idx += 1

            text_area.configure(state='disabled')
            scan_button.configure(state=tkinter.NORMAL)
        else:
            assert "Check Victim IP of Number of Ports"


def run_diff_thread():
    t = threading.Thread(target=scan_victim)
    t.start()


target_label = customtkinter.CTkLabel(
    root, text="Target", fg="yellow",  text_font=("", 15))
target_label.place(x=10, y=13)


target_input = customtkinter.CTkEntry(
    root, text_color="white")
target_input.insert(0, '192.168.1.1')
target_input.place(x=120, y=13)

number_of_ports_input = customtkinter.CTkEntry(
    root, text_color="white")
number_of_ports_input.insert(0, '# of Ports')
number_of_ports_input.place(x=250, y=13)
labelTab = Label(root, bg="white", text="3een 7ors Output")
labelTab.place(x=111, y=75)

scan_button = customtkinter.CTkButton(
    root, text="Scan Port", command=run_diff_thread, text_color="white")
scan_button.place(x=385, y=13)


root['bg'] = main_color
# Title of Window
root.title("3en7ors")
# Size of Window
root.geometry("690x550")
root.iconbitmap('res/eye.ico')
root.resizable(False, False)
# INIT Window

root.mainloop()
