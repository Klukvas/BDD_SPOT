import re
with open('/Users/andrey.p/Desktop/BDD_SPOT/email_templates/Success_Login.txt') as f:
    a = f.read()

# print(a)
# wiFee = re.search(r'Withdrawal Fee: (0|[1-9]|\.)* .{2,4}', a).group(0)

ip = re.search(r'IP address: ([0-9]|\.)*', a).group(0)

time = re.search(r'Time: ([0-9]|\-)*\s([0-9]|:)*\sUTC', a).group(0)
print(ip)
print(time)
