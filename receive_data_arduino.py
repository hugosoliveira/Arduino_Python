
"""
    _    _
   | |  | |
   | |__| |_   _  __ _  ___
   |  __  | | | |/ _` |/ _ \
   | |  | | |_| | (_| | (_) |
   |_|__|_|\__,_|\__, |\___/
    / __ \| (_)   __/ | (_)
   | |  | | |___ |___/__ _ _ __ __ _
   | |  | | | \ \ / / _ \ | '__/ _` |
   | |__| | | |\ V /  __/ | | | (_| |
    \____/|_|_| \_/ \___|_|_|  \__,_|
Created by Hugo Oliveira

06-06-2022
"""

import encodings
from time import perf_counter
import numpy as np
import pyqtgraph as pg
import serial
import time
import csv
import os

# Information about the voltage divider
r_refer = 1_000_000
voltage_arduino = 5


# Definition of the name of the file
sponge = 'Melamine'
solution = 'DW-20ml_Soap-2g'
material = 'CB_0.2g'
name_file = sponge + '__' + solution + '__' + material + '.csv'

# Definition of the time in the data acquisiton
def current_milli_time():
    return round(time.time() * 1000)

initial_time = current_milli_time()

# Definition of the communication with the Arduino board
ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()
ser.close()
ser.open()

# Definition of plotting
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Auxetic Structure - Vizualization and acquisition of Data')
pg.setConfigOptions(antialias=True)
p4 = win.addPlot()
p4.setClipToView(True)
curve4 = p4.plot(pen=(200,200,200))
p4.setLabel('left', "Resistance", units='Ohms')
p4.setLabel('bottom', "Time", units='ms')

# Definition of arrays for the plotting
data_x = np.empty(100)
data_y = np.empty(100)
ptr4 = 0

def read_arduino():
    points_arduino = int(ser.readline().decode())

    if points_arduino:
        voltage = points_arduino * (voltage_arduino / 1023);
        r_sensor = (voltage_arduino - voltage) * r_refer / voltage;
    else:
        r_sensor = -1
    return r_sensor

# Check if there is already a file with the same name
if not os.path.exists(name_file):

    # Opening of the file 
    with open(name_file,'w') as file_writing:
        writer=csv.writer(file_writing, delimiter=',',lineterminator='\n',)
        writer.writerow(['Time (s)', 'Resistance (Ohms)'])

        # Update the plot
        def update2():
            global ptr4, data_x, data_y

            intermediate_data = read_arduino()

            # Feature to avoid reading problems coming from arduino
            if intermediate_data != -1:

                data_x[ptr4] = current_milli_time() - initial_time
                data_y[ptr4] = float(intermediate_data)

                writer.writerow([str(data_x[ptr4]/1000), str(data_y[ptr4])])

                ptr4 += 1
                print(ptr4)
                if ptr4 >= data_x.shape[0]:
                    tmp_x = data_x
                    tmp_y = data_y
                    data_x = np.empty(data_x.shape[0] * 2)
                    data_y = np.empty(data_y.shape[0] * 2)
                    data_x[:tmp_x.shape[0]] = tmp_x
                    data_y[:tmp_y.shape[0]] = tmp_y
                curve4.setData(data_x[:ptr4], data_y[:ptr4])

        # update plot
        def update():
            update2()

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)

        if __name__ == '__main__':
            pg.exec()
else:
    print(f'ATTENTION: File {name_file} already exists')