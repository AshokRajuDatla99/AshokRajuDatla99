import re

def ping_stats(handler,neighbour):

    print("\n Neighbour: %s" %neighbour)

    ping_info = handler.send_command('ping '+ neighbour + ' re 100')
    rtt_match = re.findall('(\d+[/]\d+[/]\d+)', ping_info)
    rtt_stats = rtt_match[0].split('/')  #min/avg/max in the list rtt stats
    print("\nrtt min:%s,avg:%s,max:%s"%(rtt_stats[0],rtt_stats[1],rtt_stats[2]))

    ping_success_rate = [int(i) for i in ping_info.split() if i.isdigit()]
    ping_success_rate = ping_success_rate[1]
    print("Ping success rate: %s" %ping_success_rate)

def fetch_bgp_interface(handler,neighbour):

    print("\n Neighbour: %s" %neighbour)

    fetch_info = handler.send_command('sh ip cef '+neighbour,use_textfsm=True)
    p,interface = fetch_info.split('Ethernet')
    interface = 'Gi'+interface
    return interface

def flap_check(handler):
    data = handler.send_command('sh log | i DUAL-5', use_textfsm=True)

    if(len(data)<3):
        print("No flapping")

    else:
        flaps = int(len(data) / 2)
        start_data = data[0]
        start_time = start_data['time']
        end_data = data[len(data) - 1]
        end_time = end_data['time']

        start_time = start_time.split('.')
        start_time = start_time[0]
        end_time = end_time.split('.')
        end_time = end_time[0]
        print("flaps: %s" % flaps)
        print("start time: %s" % start_time)
        print("end time: %s" % end_time)

        start_time = [int(i) for i in start_time.split(':') if i.isdigit()]
        end_time = [int(i) for i in end_time.split(':') if i.isdigit()]
        difference = []
        for i in range(len(start_time)):
            difference.append(end_time[i] - start_time[i])
        print("Flap time- hours:%s,minutes:%s,seconds:%s" %(difference[0],difference[1],difference[2]))



