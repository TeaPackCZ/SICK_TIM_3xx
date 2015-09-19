#import sys
#import socket
import time
#from threading import Thread,Event,Lock
import usb.core
import usb.uti

#import mytplotlib.pyplot as plt
#import numpy as np

class TIM3xx:
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x19a2, idProduct=0x5001)
        self.dev.set_configuration()
        for i in range(10):
            try:
                self.dev.set_configuration()
                print "Connection succesfull"
                break
            except:
                print "Conect error " +str(i)
                time.sleep(0.1)

    def __del__(self):
        del self.dev

    def send_cmd(self, cmd):
        for i in range(10):
            try:
                self.dev.write(2|usb.ENDPOINT_OUT,"\x02"+cmd+"\x03\0",0)
                arr = self.dev.read(1|usb.ENDPOINT_IN,65535,timeout=100)
                return "".join([chr(x) for x in arr[1:-1]])
            except:
                #print "Laser error " + str(i)
                time.sleep(0.001)

    def internal_scan(self):
        data = self.send_cmd('sRN LMDscandata').split()
        if len(data) == 580:
            dist = [int(x,16) for x in data[26:271+26]]
            remission = [int(x,16) for x in data[304:-5]]
            run_time = int(data[9],16);
        else:
            print "Corrupted data, data_len = " + str(len(data))
        return run_time, dist, remission

laser = TIM3xx()
datas = []
for i in range(40):
    [running, distance, remission] = laser.internal_scan()
    datas.append(distance)
    time.sleep(0.05)
del laser

#x = [-135:1:135]
#for i in range(40):
#    plt.figure;
#    plt.plot(x,datas[i])
#    plt.show()



