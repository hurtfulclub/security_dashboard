import subprocess
import json 

def get_ip_addr():

    '''function for returning interfaces and their respective IP addresses'''

    print("\n\n--- NETWORK INFO ---")
    ip_return = subprocess.run(["ip","-j","addr"], text=True, capture_output=True)
    ip_json = json.loads(ip_return.stdout)

    iter_JSON(ip_json)

def iter_JSON(json_file):
    
    '''Function for iterating over json input from ip -j addr call as well as grabbing DNS servers per int'''

    dns_per_int = get_DNS()

    for interface in json_file:

        print(f"\n\nInterface {interface.get("ifindex")}:")
        print("-" * 20)
        print("\tName:" + "\n" + "\t" * 2 + interface.get("ifname"))

        ipv4_list = get_IPs(interface.get("addr_info"),proto=4)
        ipv6_list = get_IPs(interface.get("addr_info"),proto=6)
        

        if ipv4_list:
            print(f"\n\tIPV4:")
            for ip in ipv4_list:
                print("\t" * 2 + ip)
        
        if ipv6_list:
            print(f"\n\tIPV6:")
            for ip in ipv6_list:
                print("\t" * 2 + ip)
        
        link_name = "Link " + str(interface.get("ifindex")) + f" ({interface.get("ifname")})"

        if link_name in dns_per_int:
            print(f"\n\tDNS:")
            wordlist = dns_per_int[link_name].split()
            print("\t" * 2 + wordlist[-1])
    
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