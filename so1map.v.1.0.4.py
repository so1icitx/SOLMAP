from queue import Queue
import threading, datetime, time, json, csv, argparse, ipaddress, socket, re, sys
from colorama import Fore

ip = ''
port_queue = Queue()
open_ports = {}
results = []

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

def scan_sub():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((ip, port))
            if not quiet:
                print(f'{ip}\t{port}\t{Fore.GREEN}open{Fore.WHITE}')
            if file_format == 'json-clean':
                data = {
                    'ip':ip,
                    'port':port,
                    'status':'open'
                    }
                write_file(data)

            elif file_format == 'json':
                data = {
                    'ip':ip,
                    'port':port,
                    'status':'open'
                    }
                results.append(data)
            elif file_format == 'csv':
                data = [ip, port, 'open']
                write_file(data)

            elif file_format == 'txt':
                data = f'{ip}\t{port}\topen\n'
                write_file(data)
            else:
                pass

        except (ConnectionRefusedError, TimeoutError):
            pass

        except Exception:
            pass

        finally:
            sock.close()
            port_queue.task_done()

def write_file(data):
    if file_format == 'json-clean':
        with open(output_file, 'a') as file:
            json.dump(data, file, indent=2)
            file.write('\n')
    elif file_format == 'json':
        with open(output_file, 'a') as file:
            file.write(json.dumps(data))
    elif file_format == 'csv':
        with open(output_file, 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)
    else:
        with open(output_file, 'a') as file:
            file.write(data)

def main():
    global ip
    global quiet
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ipaddress', help='can be a single ip or a subnet (8.8.8.8 or 36.0.0.0/8).', required=True)
    parser.add_argument('-p', '--port', help='the port range goes from 1 to whatver you type, default is 1024.', default=1024)
    parser.add_argument('-t', '--threads', help='the worker amount, be careful not to overwhelm your pc use catiously, default is 100', default=100)
    parser.add_argument('-f', '--file_type', choices=['csv', 'json', 'json-clean', 'txt'], help='output results to various file formats.', default='no')
    parser.add_argument('-o', '--output', help='filename & location (scan.txt or ~/Documents/scan.csv)')
    parser.add_argument('--quiet', help='supresses terminal output', action='store_true')
    args = parser.parse_args()
    quiet = args.quiet


    if ((args.output and not args.file_type) or (args.file_type and not args.output) and not args.quiet) and not args.file_type == 'no':
        print('Arguments -o/--ouput and -f/--file_type must be used together!')
        sys.exit()
    elif args.output and args.file_type:
        global output_file
        global file_format
        file_format = args.file_type
        output_file = args.output
    else:
        file_format = args.file_type
        pass

    if args.file_type == 'csv':
        write_file(['IP', 'PORT', 'STATUS'])

    elif args.file_type == 'txt':
        write_file(f'Starting so1map (https://so1icitx.cfd) at {datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")} beaconing {args.ipaddress}\nIP\t\tPORT\tSTATE\n')
    if not args.quiet:
        print(f'Starting so1map (https://so1icitx.cfd) at {datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")} beaconing {args.ipaddress}\n')
    start = time.time()

    if '/' in args.ipaddress:
        try:
            if not args.quiet:
                print(f'IP\t\tPORT\tSTATE')
            net = ipaddress.ip_network(args.ipaddress)
            for ip in net:
                ip = str(ip)
                for port in range(int(args.port)):
                    port_queue.put(port)

                thread_count = int(args.threads)

                for _ in range(thread_count):
                    t = threading.Thread(target=scan_sub)
                    t.daemon = True
                    t.start()

                port_queue.join()

            end = time.time()
            if file_format == 'json':
                write_file(results)
            elif file_format == 'txt':
                write_file(f'scanned in {end - start:.2f} seconds')
            print()
            if not args.quiet:
                print(f'scanned in {end - start:.2f} seconds')
        except ValueError:
            print(f'error invalid ip {args.ipaddress}')



    else:
        pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        valid_ip = re.findall(pattern, args.ipaddress)
        if not valid_ip:
            print(f'error invalid ip {args.ipaddress}')
            sys.exit()

        ip = args.ipaddress

        for port in range(int(args.port)):
            port_queue.put(port)

        thread_count = int(args.threads)

        for _ in range(thread_count):
            t = threading.Thread(target=scan)
            t.daemon = True
            t.start()

        port_queue.join()
        if not args.quiet:
            print(f'PORT\tSTATE')
        for ip in open_ports:
            for port in open_ports[ip]:
                if not args.quiet:
                    print(f'{port}\t{Fore.GREEN}open{Fore.WHITE}')
        end = time.time()
        print()
        if not args.quiet:
            print(f'scanned in {end - start:.2f} seconds')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        if file_format == 'json':
                write_file(results)


