import ip_addr as ip
import tui

def main():
    #ip.get_ip_addr()
    #ip.get_DNS()
    tui.runTUI(ip.get_ip_addr())

if __name__ == "__main__":
    main()