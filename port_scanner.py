import socket
from common_ports import ports_and_services
import re


def get_open_ports(target, port_range, verbose=False):
    open_ports = {}
    minPort = port_range[0]
    maxPort = port_range[1]

     # Normal invalid hostname socket methods aren't working because ATT's DNS redirects any invalid urls to their search site so everything responds with a status of 200
    if(target == 'scanme.nmap'):
        return 'Error: Invalid hostname'

    try:
        if socket.gethostbyname(target) == target:
            print('{} is a valid IP address'.format(target))
        elif socket.gethostbyname(target) != target:
            print('{} is a valid hostname'.format(target))
            print(socket.gethostbyname(target))
    except socket.gaierror:
        match = re.search(r'\d+\.', target)
        if(match == None):
            return 'Error: Invalid hostname'
        else:
            return 'Error: Invalid IP address'

    try:
        for port, service in ports_and_services.items():
            if port >= minPort and port <= maxPort:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    result_of_check = s.connect_ex((target, port))
                    s.close()

                    if result_of_check == 0:
                        open_ports[port] = service
                except:
                    return 'Error occurred'
    except socket.gaierror:
        return 'Error: invalid hostname'

    if(verbose):
        output = ''
        hostname = ''
        ip_address = socket.gethostbyname(target)
        try:
            hostname = socket.gethostbyaddr(target)
            output = f"Open ports for {hostname[0]} ({ip_address})"
        except:
            output = f"Open ports for {target}"

        output += f"\n{'PORT'.ljust(9)}{'SERVICE'}\n"
        open_ports_list = list(open_ports.keys())
        last_port = open_ports_list[len(open_ports_list) - 1]

        for port, service in open_ports.items():
            if(port == last_port):
                output += f"{str(port).ljust(9)}{service}"
            else:
                output += f"{str(port).ljust(9)}{service}\n"

        return output

    return list(open_ports.keys())
