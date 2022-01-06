import numpy as np
import sys
import serial
import serial.tools.list_ports as coms
import time
from datetime import datetime as dt
from matplotlib import pyplot as plt
import glob
import matplotlib.dates as mdates
from datetime import datetime as dt
from matplotlib.ticker import ScalarFormatter
# This is a program for measuring temperature by using 10k ohm thermistor from Thorlab (TH10K)
# This script acquire data from channel 1 (T1 on LCD).
# Set up pyplot
plt.figure(1)
ax1 = plt.gca()
plt.gcf().autofmt_xdate()
fmt = mdates.DateFormatter('%d-%m %H:%M')
ax1.xaxis.set_major_formatter(fmt)
color = 'tab:blue'
ax1.set_ylabel('Temperature (C)', color=color)
print('---------------------------\n-- 10k Thermistor logger --\n---------------------------\n')
# Seach for COM port of Arduino
COM_search=[];
for pinfo in coms.comports():
    COM_search.append('AB0LA6XMA' in pinfo.hwid)
    if 'AB0LA6XMA' in pinfo.hwid:
        print('PORT: '+str(pinfo)+' is connected')
        ser = serial.Serial(pinfo.device, baudrate = 115200, timeout = 2)
if not any(COM_search):
    # Close the program if there are no targeted Arduino is connected to the computer
    print('\n-------------------------------\n-- USB Device Not Recognized --\n-------------------------------\n')
    time.sleep(5)
    sys.exit()
print()

t_cycle = int(input('Input measurement cycle time (s): '))
t_cycle=t_cycle-1;
print()
# Create text file and print header row
filename = 'thermistor_log_' + dt.now().strftime('%y%d%m_%H%M%S') + '.txt'
np.savetxt(filename, ['time stamp,temperature (C)'], newline='\n', fmt='%s')
# Flush serial buffer before beginning
ser.flushInput()
ser.flushOutput()
Time=[]
Temp=[]
while(1):
    # Query Arduino and receive Arduino ADC reading
    ser.write('?'.encode())
    # there's no need to decode or strip;
    x = ser.readline() # .decode("ansi")# .strip()
    if not len(x): continue
    # Calculate thermistor resistance from voltage measurement
    V = 5.0*float(x)/1024
    R25 = 1e4 # Resistance at room temperature of thermistor
    Rt = R25*V/(5 - V)
    # Get temperature from thermistor resistance (using Thorlabs data)
    if Rt >= 187 and Rt <= 681.6:
        a,b,c,d = 3.3536166E-03,2.5377200E-04,8.5433271E-07,-8.7912262E-08
    elif Rt > 681.6 and Rt <= 3599:
        a,b,c,d = 3.3530481E-03,2.5420230E-04,1.1431163E-06,-6.9383563E-08
    elif Rt > 3599 and Rt <= 32770:
        a,b,c,d = 3.3540170E-03,2.5617244E-04,2.1400943E-06,-7.2405219E-08
    elif Rt > 32770 and Rt <= 692600:
        a,b,c,d = 3.3570420E-03,2.5214848E-04,3.3743283E-06,-6.4957311E-08
    Tinv = a + b*np.log(Rt/R25) + c*np.log(Rt/R25)**2 + d*np.log(Rt/R25)**3
    T = 1/Tinv - 273.15
    # Print temperature reading and time to terminal window
    time_object = dt.now()
    temp_string = str(np.round(T,2)) + ' C, '
    print('Temperature logged: ' + temp_string + time_object.strftime('%X  %d %b %Y'))

    # Save reading and timestamp to text file
    save_data = [dt.timestamp(time_object),T]
    f = open(filename,'ab')
    np.savetxt(f,[save_data],newline='\r\n',fmt='%0.3f,%0.3f')
    f.close()

    # Plot graph (real time)
    Time.append(time_object)
    Temp.append(np.round(T,2))
    i_plot=0;
    while(1):
        plt.plot(Time, Temp,'r',label = 'Current Temperature (C)')
        temptext = ax1.text(0.75, 1.08, "Temp = " + str(np.round(Temp[-1],2)) + ' C',color='b',transform = ax1.transAxes)
        plt.draw()
        plt.pause(0.1)
        temptext.remove()
        i_plot=1;
        if i_plot>0:
            break
    # Pause for user specified time
    time.sleep(float(t_cycle))
