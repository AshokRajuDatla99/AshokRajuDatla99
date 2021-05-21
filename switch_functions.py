
def find_interfaces(handler):
    arp_stats = handler.send_command("sh ip arp", use_textfsm=True)

    address = []
    mac = []
    for dict in arp_stats:
        address.append(dict['address'])
        mac.append(dict['mac'])

    print(address)
    print(mac)

    mac_table = handler.send_command("sh mac address-table", use_textfsm=True)
    interfaces = []
    new_macs = []
    mapped_ips = []
    for each_mac_dict in mac_table:
        if each_mac_dict['destination_address'] in mac:
            mapped_ips.append(address[mac.index(each_mac_dict['destination_address'])])
            new_macs.append(each_mac_dict['destination_address'])
            interfaces.append(each_mac_dict['destination_port'])


    print("interfaces:", interfaces)
    print("mapped ips :", mapped_ips)
    print("mapped macs:", new_macs)

    return interfaces