import psutil
from time import sleep


def get_cpu_info():
    get_cpu_temp()
    get_cpu_usage()
    get_process_cpu_util()

def get_cpu_temp():
    print("\n\n--- CPU INFO ---")
    if not hasattr(psutil, "sensors_temperatures"):
        print("system not supported")
    else:   
        temps = psutil.sensors_temperatures()
    
    if not temps:
        print("no temps read")
    else:
        for name, temp_measures in temps.items():
            if name == ("k10temp" or "coretemp"):

                temp = temp_measures[0]
                msg = f"\tCPU core temp: {temp.current} °C"

                if temp.high and temp.critical:
                    msg += f"--- high = {temp.high} °C, critical = {temp.critical} °C)"

                print(msg)

                break


def get_cpu_usage():
    if not hasattr(psutil, "cpu_percent"):
        print("system not supported")
    else:
        usage = psutil.cpu_percent()
        if not usage:
            print("no cpu usage read")
        else:
            for i in range(5):
                sleep(0.5)
                usage = psutil.cpu_percent()
                print(f"\tCPU utilization: {usage}%")

def get_process_cpu_util():
    highest_util = [None] * 5
    for i in range(25):
        for proc in psutil.process_iter(['name','cpu_percent']):
            if proc.info.get('cpu_percent') > 0:
                print(proc.info)
        print("-------------------")
        sleep(2)
        