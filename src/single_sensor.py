import serial

from time import time

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import numpy as np

import threading

connection = serial.Serial("COM9", 9600)



fig = plt.figure()
fig.set_figwidth(50)
ax = fig.add_subplot(1, 1, 1)

wifi = {}

def recieve_serial(): 
    while True:
        tmp = str(connection.readline())[2:-5]
        r_border = str.find(tmp,'>')
        ssid = tmp[1:r_border]
        rssi = float(tmp[r_border+1:])

        #print(ssid)
        #print(rssi)

        if not (ssid in wifi):
            wifi[ssid] = {}
            wifi[ssid]["time"]=[]
            wifi[ssid]["strength"]=[]
        wifi[ssid]["time"].append(time())
        wifi[ssid]["strength"].append(rssi)


threading.Thread(daemon=True, target=recieve_serial).start()

def update(i):
    ax.clear()
    for w in wifi:

        xs = wifi[w]["time"]#[-10:]
        ys = wifi[w]["strength"]#[-10:]

        #ax.plot(wifi[w]["time"], wifi[w]["strength"])
        ax.plot(xs, ys, label=w)

    
    #ax.plot(xs, ys)

    # Format plot
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=3 )

    plt.xticks(visible= False) #rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title(len(wifi))
    plt.ylabel('MyLabel')

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
    

'''
while True:
    tmp = str(connection.readline())[2:-5]
    r_border = str.find(tmp,'>')
    type = tmp[1:r_border]
    value = tmp[r_border+1:]
    #print(type)
    #print(value)
    
    if type in test:
        pass
    else:
        test[type] = []

    test[type].append((time(), value))
'''