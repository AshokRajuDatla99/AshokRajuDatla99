from netmiko import ConnectHandler
from ssh import check_ssh
from functions import *
from switch_functions import *

src = '192.168.1.50'
dst = '172.16.1.6'

commands = {1: "sh ip protocol summary",
            2: "sh ip eigrp nei",
            3: "sh version",
            4: "sh clock",
            5: "sh proc mem | ex 0.00",
            6: "show proc cpu"}

def log_tree(ip):

    net_connect = check_ssh(ip)

    if net_connect == None:
        print("Sorry you have an issue at this ip: %s\n"%ip)

    else:
        host_name = net_connect.find_prompt()
        print("\n %s" %host_name)

        if 'Router' in host_name:

            print("\nI'm in router")
            # device_stats(net_connect)
            # proc_info(net_connect,ip)
            protocol_summary(net_connect,ip)

        if 'Switch' in host_name:

            print("\nI'm in switch")
            # device_stats(net_connect)
            # interfaces = find_interfaces(net_connect)
            # for i in interfaces:
            #     print("\n INTERFACE ",i)
                # check_interface(net_connect,i)

        net_connect.disconnect()


def path(src,dst):

    addr = [src]
    hop = ['0']

    ios = {
            'device_type': 'cisco_ios',
            'ip': src,
            'username': 'dev',
            'password': 'datla',
            'global_delay_factor': 2
    }

    net_connect = ConnectHandler(**ios)
    command = 'trace '
    command += dst

    route_dict = net_connect.send_command(command, use_textfsm=True)
    # print(route_dict)
    for hop_dict in route_dict:
        addr.append(hop_dict['address'])
        hop.append(hop_dict['hop_num'])

    if dst not in addr:
        hop.append(str(len(hop)))
        addr.append(dst)

    route_info = dict(zip(hop, addr))
    return route_info

def Main():

    print("In the main function")
    route_table = path(src,dst)

    print(route_table)

    for ip in route_table.values():
        log_tree(ip)


if __name__ == '__main__':
    Main()