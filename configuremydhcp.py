import os # os library is required to handle file IO
import socket
import netifaces #get access to the list of the network interfaces available on the local machine
import re #to perform Regular Expression operations.
import sys #manage commandline arguments passes to the program

def splitIP( ipStr):

    l = re.split('(.*)\.(.*)\.(.*)\.(.*)', ipStr)
    return l[1:-1]
   
def ifacelist():
	iface = netifaces.interfaces()
	return iface

def startDHCP(dhcpIntf):
	os.system("dhcpd -cf /etc/dhcp/dhcpd.conf -pf /var/run/dhcpd.pid "+dhcpIntf)
	os.system('/etc/init.d/isc-dhcp-server start')

if __name__ == "__main__":
	#os.system("clear")
	if not os.path.isfile("/etc/init.d/isc-dhcp-server"):
		sys.exit('['+R+'-'+W+'] DHCP server not installed.\n Command to install: apt-get install isc-dhcp-server')
	flag = 0
	if os.geteuid():
		sys.exit('['+R+'-'+W+'] Please run as root')
	DN = open(os.devnull, 'w')
	iface = ifacelist()
	while flag == 0:
		try:
			default_lease_time = int(raw_input("Enter the Default Lease Time for DHCP (Ex. 600): "))
		except:
			print '['+R+'!'+W+'] Invalid input. Please provide a valid integer.'
			continue
				
		if type(default_lease_time) == int:
			default_lease_time = int(default_lease_time)
			flag = 1
			
	while flag == 1:
		try:
			max_lease_time = int(raw_input("Enter the Maximum Lease Time for DHCP (Ex. 7200): "))
		except:
			print '['+R+'!'+W+'] Invalid input. Please provide a valid integer.'
			continue
				
		if type(max_lease_time) == int:
			max_lease_time = int(max_lease_time)
			flag = 2
			
	while flag == 2:
		subnet = raw_input("Enter your Subnet Address (Ex. 192.168.2.0): ")
		try:
			spl_ip = splitIP(subnet)
			socket.inet_aton(subnet)
			if len(spl_ip) != 4:
				print '['+R+'!'+W+']Invalid Subnet Address entered.'
				continue
			elif int(spl_ip[3]) != 0:
				print '['+R+'!'+W+']Invalid Subnet Address entered.'
				continue
			flag = 3
		except socket.error:
			print '['+R+'!'+W+']Invalid Address entered.'
	
	while flag == 3:
		mask = raw_input("Enter your Subnet Mask (Ex. 255.255.255.0): ")
		try:
			socket.inet_aton(mask)
			if len(splitIP(mask)) != 4:
				print '['+R+'!'+W+']Invalid Mask entered.'
				continue
			flag = 4
		except socket.error:
			# Not legal
			print '['+R+'!'+W+']Invalid Mask entered.'
			
	while flag == 4:
		broadcast = raw_input("Enter your Broadcast Address (Ex. 192.168.2.255): ")
		try:
			socket.inet_aton(broadcast)
			spl_ip = splitIP(broadcast)
			#print str(len(spl_ip)) + "  " + str(spl_ip[3])
			if len(spl_ip) != 4:
				print '['+R+'!'+W+']Invalid Broadcast Address entered.'
				continue
			elif int(spl_ip[3]) != 255:
				print '['+R+'!'+W+']Invalid Broadcast Address entered.'
				continue
			flag = 5
		except socket.error:
			# Not legal
			print '['+R+'!'+W+']Invalid Broadcast Address entered.'
			
	while flag == 5:
		gateway = raw_input("Enter Address of Gateway / Router (Ex. 192.168.2.1): ")
		try:
			socket.inet_aton(gateway)
			spl_ip = splitIP(gateway)
			#print str(len(spl_ip)) + "  " + str(spl_ip[3])
			if len(spl_ip) != 4:
				print '['+R+'!'+W+']Invalid Address entered.'
				continue
			flag = 6
		except socket.error:
			# Not legal
			print '['+R+'!'+W+']Invalid Address entered.'
		
	
	while flag == 6:
		dns = raw_input("Enter Address of DNS server (Ex. 8.8.8.8): ")
		try:
			socket.inet_aton(dns)
			spl_ip = splitIP(dns)
			#print str(len(spl_ip)) + "  " + str(spl_ip[3])
			if len(splitIP(dns)) != 4:
				print '['+R+'!'+W+']Invalid Address entered.'
				continue
			flag = 7
		except socket.error:
			# Not legal
			print '['+R+'!'+W+']Invalid Address entered.'
			
	while flag == 7:
		startip = raw_input("Enter Start IP address to assign (Ex. 192.168.2.50): ")
		try:
			socket.inet_aton(startip)
			spl_ip = splitIP(startip)
			#print str(len(spl_ip)) + "  " + str(spl_ip[3])
			if len(splitIP(startip)) != 4:
				print '['+R+'!'+W+']Invalid Address entered.'
				continue
			flag = 8
		except socket.error:
			# Not legal
			print '['+R+'!'+W+']Invalid Address entered.'	
			
	while flag == 8:
		endip = raw_input("Enter End IP address to assign (Ex. 192.168.2.100): ")
		try:
			socket.inet_aton(subnet)
			spl_ip = splitIP(subnet)
			#print str(len(spl_ip)) + "  " + str(spl_ip[3])
			if len(splitIP(subnet)) != 4:
				print '['+R+'!'+W+']Invalid Address entered.'
				continue
			flag = 9
		except socket.error:
			# Not legal
			print '['+R+'!'+W+']Invalid Address entered.'
			
			
	intf_dhcp = []	
	flg2 = 0	
	while flag == 9:
		try:
			intf_count = int(raw_input("Enter number of Interfaces to run DHCP server (Ex. 1): "))
		except:
			print ('['+R+'!'+W+'] Invalid Number entered!!')
			continue
		print str(intf_count)
		for i in range(0,intf_count):
			flg2 = 0
			while flg2 == 0:
				intf_val = raw_input("Enter Interface "+str(i+1)+" (Ex. wlan0) :")
				if intf_val in iface:
					flg2 = 1
					intf_dhcp.append(intf_val)
				else:
					# If user enters an invalid interface name, then it lists all available interfaces.
					print('['+R+'!'+W+'] Invalid Interface entered!!')
					
			if i == (intf_count - 1):
				flag = 10
				
	#Writing Details into configuration File
			
	conf_file = open("/etc/dhcp/dhcpd.conf", "w")	
	conf_file.write("ddns-update-style interim;\n")
	conf_file.write("authoritative;\n")
	conf_file.write("default-lease-time "+str(default_lease_time)+";\n")
	conf_file.write("max-lease-time "+ str(max_lease_time) +";\n")
	conf_file.write("subnet "+str(subnet)+" netmask "+str(mask)+" {\n")
	conf_file.write("option subnet-mask "+str(mask)+";\n")
	conf_file.write("option broadcast-address "+str(broadcast)+";\n")
	conf_file.write("option routers "+str(gateway)+";\n")
	conf_file.write("option domain-name-servers "+str(dns)+";\n")
	conf_file.write("range "+str(startip)+" "+str(endip)+ ";\n")
	conf_file.write("}")
	conf_file.close()
	
	#Writing Details into interface File
	
	intf_file = open("/etc/default/isc-dhcp-server", "w")
	intf_file.write('INTERFACES="')
	for p in intf_dhcp:
		intf_file.write(str(p)+" ")
	intf_file.write('"')
	intf_file.close()
	startDHCP(str(intf_dhcp[0]))
	
