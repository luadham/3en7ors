from _tkinter import *
from tkinter import *
from tkinter import font
from PortScanner import PortScanner as pscanner
from VulnerabilityScanner import VulnerabilityScanner as vscanner

main_color = "#414141"

# This is the root Window
root = Tk()
# create Label

open_tcp_ports = []
open_udp_ports = []
udp_services = []

open_tcp_vul_ports = []
open_tcp_vul_banners = []


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
def scan_victim():
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


target_label = Label(root, text="Target", bg=main_color, fg="white")
target_label.place(x=10, y=13)

# TODO: You Must Make Sure that user enter valid IP Address
target_input = Entry(root)
target_input.insert(0, '192.168.1.1')
target_input.place(x=80, y=13)

# TODO: You Must Check that user enter ports number in range between 1 to 2^16
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
