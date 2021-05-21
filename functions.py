from router_functions import *
import re

commands = {1: "sh ip protocol summary",
            2: "sh ip eigrp nei",
            3: "sh version",
            4: "sh clock",
            5: "sh proc mem | ex 0.00",
            6: "show proc cpu",
            7: "sh ip bgp sum"}

def device_stats(handler):

    device_info = handler.send_command(commands[3])
    version_info = device_info.splitlines()
    version_info = version_info[0]
    r,device_info = device_info.split('uptime is')
    up_time,r = device_info.split("System returned to ROM by reload")
    up_time  = [int(i) for i in up_time.split() if i.isdigit()] #up_time list of hours and minutes

    x,reload_reason = r.split("Last reload reason:")
    reload_reason,x = reload_reason.split('reason')

    print("VERSION INFO: %s" %version_info)
    print("UP_TIME: %s" % up_time)
    print("RELOAD REASON: %s" % reload_reason)

    # show clock

def proc_info(handler,ip):

    proc_mem = handler.send_command(commands[5],use_textfsm=True)
    proc_mem = proc_mem.splitlines()
    proc_pool = proc_mem[0]
    proc_pool = [int(i) for i in proc_pool.split() if i.isdigit()]
    proc_used = round((proc_pool[1] * 100 / proc_pool[0]), 3)
    proc_free = round((proc_pool[2] * 100 / proc_pool[0]), 3)

    io_pool = proc_mem[1]
    io_pool = [int(i) for i in io_pool.split() if i.isdigit()]
    io_used = round(io_pool[1]*100 / io_pool[0], 3)
    io_free = round(int(io_pool[2]*100 / io_pool[0]), 3)

    print("proc_used: %s" %proc_used)
    print("proc_free: %s" %proc_free)
    print("io_used: %s" %io_used)
    print("io_free: %s" %io_free)

    cpu_info = handler.send_command(commands[6],use_textfsm=True)
    cpu_info = cpu_info[0]
    cpu_5_sec = cpu_info['cpu_5_sec']
    cpu_1_min = cpu_info['cpu_1_min']
    cpu_5_min = cpu_info['cpu_5_min']
    print("%s %s %s" %(cpu_5_sec,cpu_1_min,cpu_5_min))

def protocol_summary(handler,ip):

    protocol_summary = handler.send_command(commands[1])

    if 'eigrp' in protocol_summary:
        print("\n I'm in EIGRP")
        eigrp_nei = handler.send_command(commands[2],use_textfsm=True)
        eigrp_neighbours = []
        eigrp_interfaces = []

        flap_check(handler)

        # for dict in eigrp_nei:
        #     eigrp_neighbours.append(dict['address'])
        #     eigrp_interfaces.append(dict['interface'])
        #
        # for i in range(len(eigrp_neighbours)):
        #     ping_stats(handler,eigrp_neighbours[i])
        #     check_interface(handler,eigrp_interfaces[i])

    # if 'bgp' in protocol_summary:
    #     print("\n I'm in BGP")
    #     bgp_nei = handler.send_command(commands[7],use_textfsm=True)
    #     bgp_neigbours = []
    #     uptimes =[]
    #     prefixes = []
    #
    #     for dict in bgp_nei:
    #         bgp_neigbours.append(dict['bgp_neigh'])
    #         uptimes.append(dict['up_down'])
    #         prefixes.append(dict['state_pfxrcd'])
    #
    #     print("BGP neighbours:",bgp_neigbours)
    #     print("BGP uptimes:",uptimes)
    #     print("BGP prefixes:",prefixes)
    #
    #     for nei in bgp_neigbours:
    #         each_interface = fetch_bgp_interface(handler,nei)
    #         check_interface(handler,each_interface)


def check_interface(handler,interface):

    print("Running on this interface: %s" %interface)
    int_stats = handler.send_command('sh int '+ interface,use_textfsm=True)
    int_stats = int_stats[0]
    crc = int_stats['crc']
    input_errors = int_stats['input_errors']
    bandwidth = int_stats['bandwidth']

    print("crc: %s,input_errors: %s, bandwidth: %s"%(crc,input_errors,bandwidth))

    load_stats = handler.send_command('sh int ' + interface)
    load_stats = re.findall('(\d+[/]\d+)', load_stats)
    num,den = load_stats[2].split('/')
    reliability = round(float(num)*100/float(den),2)
    num,den = load_stats[3].split('/')
    tx_load = round(float(num)*100/float(den),2)
    num,den = load_stats[4].split('/')
    rx_load = round(float(num)*100/float(den),2)

    print("reliability:%s,tx_load:%s,rx_load:%s" %(reliability,tx_load,rx_load))




