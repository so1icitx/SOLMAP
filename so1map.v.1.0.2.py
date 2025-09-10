import threading
import socket
import argparse
from queue import Queue
import ipaddress
import datetime
import time

open_ports = {}
port_queue = Queue()
ip = ''

def scan():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((ip, port))
            if ip in open_ports:
                open_ports[ip].append(port)
            else:
                open_ports[ip] = [port]

        except (ConnectionRefusedError, TimeoutError):
            pass
        except Exception:
            pass

        finally:
            sock.close()
            port_queue.task_done()


def main():
    global ip
    print(f'Starting so1map 1.01 (https://so1icitx.cfd/) at {datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")}')
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ipaddress')
    parser.add_argument('-p', '--port')
    parser.add_argument('-t', '--threads')
    args = parser.parse_args()
    try:
        if '/' in args.ipaddress:
            start = time.time()
            net = ipaddress.ip_network(args.ipaddress, strict=True)
            print('\nIP\t\tPORT\tSTATE')
            for i in net:
                port_queue = Queue()
                ip = str(i)
                for port in range(int(args.port)):
                    port_queue.put(port)

                thread_count = int(args.threads)


                for _ in range(thread_count):
                    t = threading.Thread(target=scan)
                    t.daemon = True
                    t.start()

                port_queue.join()
                if not ip in open_ports:
                    pass
                else:
                    for i in open_ports[ip]:
                        print(f'{ip}\t{i}\t{"open"}')

            end = time.time()
            print(f'\nScanned in {(end - start):.2f} seconds')

        else:
            ip = args.ipaddress
            for port in range(int(args.port)):
                port_queue.put(port)

            thread_count = int(args.threads)

            for _ in range(thread_count):
                t = threading.Thread(target=scan)
                t.daemon = True
                t.start()

            port_queue.join()
            end = time.time()
            print('\nPORT\tSTATE')
            if open_ports != {}:
                for i in open_ports[ip]:
                    print(f'{i}/tcp\topen')


            print(f'\nScanned in {(end - start):.2f} seconds')


    except ValueError:
        print(f'invalid ip {args.ipaddress}')



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        # print(open_ports)

