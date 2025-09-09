import socket
import threading
from queue import Queue
import argparse
import ipaddress


port_queue = Queue()
ports_open = {}
lock = threading.Lock()
ip = ''


def scan_single():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((ip, port))
            with lock:
                if ip in ports_open:
                    ports_open[ip].append(port)
                else:
                    ports_open[ip] = [port]
        except (ConnectionRefusedError, TimeoutError):
            pass
        except Exception:
            pass
        finally:
            sock.close()
            port_queue.task_done()

def scan_subnet():
    pass

def main():
    global ip

    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ipaddress', help='can be a single ip or a subnet (8.8.8.8 or 36.0.0.0/8)', required=True)
    parser.add_argument('-p', '--port', help='the port range goes from 1 to whatver you type, default is 1024', default=1024)
    parser.add_argument('-t', '--threads', help='the worker amount, be careful not to overwhelm your pc use catiously!', default=100)
    output = parser.parse_args()

    if int(output.port) > 65535:
        raise Exception(f'port {output.port} is a invalid port range')

    try:
        if '/' in output.ipaddress:
            net = ipaddress.ip_network(output.ipaddress, strict=True)
            for i in net:
                for port in range(int(output.port)):
                    port_queue.put(port)
                threads_count = int(output.threads)
                ip = str(i)

                for _ in range(threads_count):
                    t = threading.Thread(target=scan_single)
                    t.daemon = True
                    t.start()
                port_queue.join()

            print(ports_open)

        else:
            ip = output.ipaddress
            for port in range(int(output.port)):
                    port_queue.put(port)

            threads_count = int(output.threads)

            for _ in range(threads_count):
                t = threading.Thread(target=scan_single)
                t.daemon = True
                t.start()
            port_queue.join()
            print(ports_open)

    except ValueError:
        print(f'{output.ipaddress} is an invalid subnet or ip')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(ports_open)
        print('\nExiting..')
