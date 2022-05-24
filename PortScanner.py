import socket
from threading import Semaphore, Thread


# Port Scanning class 
class PortScanner:

    # this list will contain the open tcp ports for victim 
    _open_tcp_ports = []
    _banners = []

    # this list will contain the open udp ports for victim
    __open_udp_ports = []
    __udp_service = []
    __ping_MESSAGE = 'ping'

    # We will use semaphore to make sure that only one Thread can append to our List
    _tcp_semaphore = [Semaphore(1), Semaphore(1), Semaphore(1)] 
    _udp_semaphore = Semaphore(1)

    def __init__(self, victim, number_of_ports):
        self.victim = victim
        self.number_of_ports = number_of_ports


    # We will Classify The open Ports to 3 Category
    # Open
        # Open Port may have request (banner) message that Contain some info about The server
        # So if it have a message we will store this message to our banner list
    # Closed 
    # Filtered

    # This function will scan Tcp Port
    # @parameter Port 
    # @modify _open_ports, _banners 
    def __scan_tcp_port(self, port):
        sock = socket.socket() # The default of Socket object is TCP and IPV4
        try:
            sock.connect((self.victim, port))
            #self._tcp_semaphore[0].acquire() # This is block any thread to modify the list like sem_wait()
            self._open_tcp_ports.append(port) # if code reach to this line it means that the port is open
            #self._tcp_semaphore[0].release() # This release the resource
            print(f"[+] {port} Open")
            try:
                # Try To Get Banner if exist
                print(f"[+] Get Header fot {port}")
                banner = sock.recv(1024)
                # if There is a panner store it 
                #self._tcp_semaphore[1].acquire()
                self._banners.append(banner.decode().strip('\n').strip('\r')) 
                #self._tcp_semaphore[1].release()
            except:
                # If code reach to this line it means that there is not banner for this open port
                # so we will add dummy data
                #self._tcp_semaphore[2].acquire()
                self._banners.append(' ')
                #self._tcp_semaphore[2].release()
        except:
            # if code reach to this line to mean that port is closed or filtered
            pass


    # This Function open Thread for each Port and scan it
    # The default method is TCP Scanning
    # @return True if All ports scanned Successfully
    def scan(self, method="TCP"):
        _method = self.__scan_tcp_port
        if (method.upper() == "UDP"):
            _method = self.__scan_udp_port
        else:
            # If user send wrong parameter Must raise error
            assert "Method Must be TCP OR UDP"
    
        _threads = []
        cnt = 0
        try :
            for i in range(1, self.number_of_ports + 1):
                _threads.append(Thread(target=_method, args=(i,)))
                cnt += 1
        
            for i in range(cnt):
                _threads[i].start()

            for i in range(cnt):
                _threads[i].join()
            return True

        except:
            return False

    # @return open tcp ports
    def get_open_tcp_ports(self):
        return self._open_tcp_ports
    
    # @return banners for open ports
    def get_tcp_banners(self):
        return self._banners

    # This Function Scan For Open UDP Port
    # Mechanism
        # We send packet Ping Packet using UDP connection and add timeout
        # Then we wait a message from Victim if there is a message so this is not service 
        # but it an open port
        # If user didn't reply by message
        # We will try to get service name
    # @param Port Number 
    # @modify __open_udp_ports, __udp_service  
    def __scan_udp_port(self, port):
        sock = socket.socket(type=socket.SOCK_DGRAM)
        try:
            sock.sendto(self.__ping_MESSAGE.decode('utf_8'), (self.victim, port))
            
            data, addr = sock.recvfrom(1024)
        except:
            try:
                serv = socket.getservbyport(port, 'UDP')
                self._tcp_semaphore.acquire()
                self.__open_udp_ports.append(port)
                self.__udp_service.append(serv)
            except:
                pass
            self._tcp_semaphore.release()
        

    # @return open udp ports
    def get_open_udp_ports(self):
        return self.__open_udp_ports
    
    # @return service for open udp ports
    def get_udp_service(self):
        return self.__udp_service
        

