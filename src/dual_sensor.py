from time import time

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import numpy as np

import threading,serial, math

from scipy.signal import argrelextrema


wifi = {}
lock = threading.Lock()

con_1 = serial.Serial("COM5", 9600)
def read_con_1():
    while True:
        tmp = str(con_1.readline())[2:-5]
        r_border = str.find(tmp,'>')
        ssid = tmp[1:r_border]
        rssi = float(tmp[r_border+1:])
        with lock:
            if not (ssid in wifi):
                wifi[ssid] = {}
                wifi[ssid]['con1'] = {}
                wifi[ssid]['con1']['time'] = []
                wifi[ssid]['con1']['rssi'] = []
                wifi[ssid]['con2'] = {}
                wifi[ssid]['con2']['time'] = []
                wifi[ssid]['con2']['rssi'] = []
            #t = math.ceil(time() / 10.0) * 10
            t = math.floor(time())
            #wifi[ssid]['con1']['time'].append(time())
            wifi[ssid]['con1']['time'].append(t)
            wifi[ssid]['con1']['rssi'].append(rssi)


con_2 = serial.Serial("COM7", 9600)
def read_con_2():
    while True:
        tmp = str(con_2.readline())[2:-5]
        r_border = str.find(tmp,'>')
        ssid = tmp[1:r_border]
        rssi = float(tmp[r_border+1:])
        #print(rssi)
        with lock:
            if not (ssid in wifi):
                wifi[ssid] = {}
                wifi[ssid]['con1'] = {}
                wifi[ssid]['con1']['time'] = []
                wifi[ssid]['con1']['rssi'] = []
                wifi[ssid]['con2'] = {}
                wifi[ssid]['con2']['time'] = []
                wifi[ssid]['con2']['rssi'] = [] 
            #t = math.ceil(time() / 10.0) * 10
            t = math.floor(time())
            #wifi[ssid]['con2']['time'].append(time())
            wifi[ssid]['con2']['time'].append(t)    
            wifi[ssid]['con2']['rssi'].append(rssi)



threading.Thread(target=read_con_1, daemon=True).start()
threading.Thread(target=read_con_2, daemon=True).start()

fig = plt.figure()
fig.set_figwidth(50)
ax = fig.add_subplot(1, 1, 1)

count = 0
show_dif = False

def on_press(event):
    global count, show_dif
    if event.key == "down":
        if count > 0 : count -= 1
    elif event.key == "up":
        if count < len(wifi) - 1: count += 1
    elif event.key == 'x':
        show_dif = not show_dif
    #print(count)

fig.canvas.mpl_connect('key_press_event', on_press)

def update(i):
    global count
    ax.clear()
    if len(list(wifi)) == 0 : return
    #if not ("A54 von Hans" in wifi) : return
    #print(count)
    key = list(wifi)[count]
    #key = "A54 von Hans"

    #ax.plot(wifi[key]['con1']['time'], wifi[key]['con1']['rssi'], label="con1")
    #ax.plot(wifi[key]['con2']['time'], wifi[key]['con2']['rssi'], label="con2")

    #xs = np.asanyarray(wifi[key]['con1']['time'])
    ys_1 = np.asanyarray(wifi[key]['con1']['rssi'])
    max_1 = np.asanyarray(argrelextrema(ys_1, np.greater))[0]
    
    x1 = [wifi[key]['con1']['time'][x] for x in max_1]
    y1 = [wifi[key]['con1']['rssi'][y] for y in max_1]

    ax.plot(x1, y1, label="m_con_1")
    
    ys_2 = np.asanyarray(wifi[key]['con2']['rssi'])
    max_2 = np.asanyarray(argrelextrema(ys_2, np.greater))[0]
    
    x2 = [wifi[key]['con2']['time'][x] for x in max_2]
    y2 = [wifi[key]['con2']['rssi'][y] for y in max_2]
    
    ax.plot(x2, y2, label="m_con_2")
    if show_dif:
        tmp = []
        for i,val in enumerate(y1): 
            try:
                tmp.append(y1[i]-y2[i])
            except: pass
        try:
            ax.plot(x1[:len(tmp)], tmp, label="dif")
        except: pass

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=3 )

    plt.xticks(visible= False) #rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title(str(count+1) + "/" + str(len(wifi)))
    plt.ylabel(key)

ani = animation.FuncAnimation(fig, update) #, interval=10)
plt.show()