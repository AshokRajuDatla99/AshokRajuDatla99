from ssh import check_ssh
import re

ip = '172.16.1.225'

handler = check_ssh(ip)
data = handler.send_command('sh log | i DUAL-5',use_textfsm=True)
# print(data)

flaps = int(len(data)/2)
start_data = data[0]
start_time = start_data['time']
end_data = data[len(data)-1]
end_time = end_data['time']

start_time = start_time.split('.')
start_time = start_time[0]
end_time = end_time.split('.')
end_time = end_time[0]
print("flaps: %s" %flaps)
print("start time: %s" %start_time)
print("end time: %s" %end_time)


start_time = [int(i) for i in start_time.split(':') if i.isdigit()]
end_time = [int(i) for i in end_time.split(':') if i.isdigit()]
difference =[]
for i in range(len(start_time)):
    difference.append(end_time[i]-start_time[i])
print(difference)


