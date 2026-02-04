import subprocess
import json 

#function for returning interfaces and their respective IP addresses

def get_ip_addr():

    ip_return = subprocess.run(["ip","-j","addr"], text=True, capture_output=True)
    ip_json = json.loads(ip_return.stdout)

    return iter_JSON(ip_json)


#Function for iterating over json input from ip -j addr call as well as grabbing DNS servers per int

def iter_JSON(json_file):
    
    dns_per_int = get_DNS()

    interfaces_output = {}

    for interface in json_file:

        interface_name = f"Interface {interface.get("ifindex")}"
        interface_info = f"\n\tName: {interface.get("ifname")}"

        ipv4_list = get_IPs(interface.get("addr_info"),proto=4)
        ipv6_list = get_IPs(interface.get("addr_info"),proto=6)
        

        if ipv4_list:
            interface_info += f"\n\tIPV4:"
            for ip in ipv4_list:
                interface_info += f"\n\t\t{ip}"

        if ipv6_list:
            interface_info += f"\n\tIPV6:"
            for ip in ipv6_list:
                interface_info += f"\n\t\t{ip}"

        link_name = "Link " + str(interface.get("ifindex")) + f" ({interface.get("ifname")})"  

        if link_name in dns_per_int:
            interface_info += f"\n\tDNS:"
            wordlist = dns_per_int[link_name].split()
            interface_info += f"\n\t\t{wordlist[-1]}"

        ip_info = {interface_name: interface_info} 

        interfaces_output.update(ip_info)
    
    return interfaces_output

#function to get the ips from command line output
  
def get_IPs(addr_info, proto = 4):
    ip_addrs = []

    for ip in addr_info:
        if proto == 4 and ip.get("family") == "inet":
            # this is an IPV4 addr, which we are trying to get
            address = ip.get("local")
            prefix = ip.get("prefixlen")
            dynamic = ip.get("dynamic")

            if prefix:
                ip_addrs.append(address + f"/{prefix} --- " + "dynamic" if dynamic else address + f"/{prefix}")
            else:
                ip_addrs.append(ip.get("local"))
        if proto == 6 and ip.get("family") == "inet6":
            # this is an IPV6 addr, which we are trying to get
            address = ip.get("local")
            prefix = ip.get("prefixlen")
            if prefix:
                ip_addrs.append(address + f"/{prefix}")
            else:
                ip_addrs.append(ip.get("local"))
        
    return ip_addrs


#function to get dns info from command line output

def get_DNS():
    dns_info = subprocess.run(["resolvectl", "status"], text=True, capture_output=True)
    dns_info_out = dns_info.stdout
    interface = "Default"
    dns_int = {}

    for line in dns_info_out.splitlines():
        if "Current DNS Server" in line:
            dns_int[interface] = line
        elif line.startswith(("Link","Global")):
            interface = line

    return dns_int