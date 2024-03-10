import socket
import threading
import subprocess
import sys
from datetime import datetime
from queue import Queue

# Ask for input
remoteServer = input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

# Common ports and their typical use
common_ports = {
    21: 'FTP - File Transfer Protocol',
    22: 'SSH - Secure Shell',
    23: 'Telnet - Unencrypted text communications',
    25: 'SMTP - Simple Mail Transfer Protocol',
    53: 'DNS - Domain Name System',
    80: 'HTTP - HyperText Transfer Protocol',
    110: 'POP3 - Post Office Protocol',
    443: 'HTTPS - HTTP Secure',
    3306: 'MySQL - Database Server',
}

# Thread lock for synchronized output
print_lock = threading.Lock()

# Function to scan ports
def portscan(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = sock.connect_ex((remoteServerIP, port))
        if con == 0:
            with print_lock:
                service = common_ports.get(port, "Unknown service")
                print(f"Port {port}: Open ({service})")
                if port in common_ports:
                    print(f"-> This port is commonly used for {common_ports[port]}.")
                    if port in [21, 23, 25, 80]:
                        print("-> Consider securing or closing this port if not in use, as it can pose security risks.")
                else:
                    print("-> This is not a common port. Ensure that it's open for a valid reason.")
        con.close()
    except:
        pass

# Thread worker function
def threader():
    while True:
        worker = port_queue.get()
        portscan(worker)
        port_queue.task_done()

# Queue for worker threads
port_queue = Queue()

# Number of threads to create - can be adjusted based on your requirement
thread_count = 100

# Start threads and add to the queue
for x in range(thread_count):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# Start time
start = datetime.now()

# Scanning ports in range
for worker in range(1, 1025):
    port_queue.put(worker)

# Wait for the queue to be empty
port_queue.join()

# Calculate and print total scan time
end = datetime.now()
total = end - start
print('Scanning Completed in:', total)
