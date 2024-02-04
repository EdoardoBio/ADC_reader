'This simple script is meant to be used for plant resistance measurement using the ADS1115 ADC'
"The required circuit is a simple 100k Ohm resistor in series with two electrodes inserted in the plant"
"I suggest the use of 0.4V as the voltage imposed between circuit's edges"

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

Plant='plant'
Vin=0.3 
Distance='5cm'
desiredSamples=200

try:
    file = open(f"PlantResistanceAnalysis_{Plant}_{Vin}V_{Distance}.txt", "r")
except FileNotFoundError:
    file = open(f"PlantResistanceAnalysis_{Plant}_{Vin}V_{Distance}.txt", "w")
    file.write('Plant Resistance in MOhm,Flowing current uA,Reading range %\n')
file.close()


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c, gain=16)#[0.6666666666666666, 1, 2, 4, 8, 16]
# Create differential input between channel 0 and 1
chan = AnalogIn(ads, ADS.P0, ADS.P1)
#print("{:>5}\t{:>5}".format('raw', 'v'))

#R=V/I  3.3-R*I-Vmeasured=0  =>   R*Vmeasured/100k = 3.3-Vmeasured    =>   R = (Vin-Vmeasured)*100k/Vmeasured
#Vmeasured = R*I = 100k*I   =>   I = Vmeasured/100k
#plant_resistance = (Vin-chan.voltage)*100000/chan.voltage

reliableMeasurements=0
while reliableMeasurements<desiredSamples:
    #print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    Vmeasured=chan.voltage
    raw_value=chan.value
    if Vmeasured>0:
      
        file = open(f"PlantResistanceAnalysis_{Plant}_{Vin}V_{Distance}.txt", "a")
        file.write(f"{(Vin-Vmeasured)*100000/Vmeasured/1000000},{Vmeasured}\n")
        file.close()
        print('Plant Resistance in MOhm		Flowing current uA')
        print(f'{(Vin-Vmeasured)*100000/Vmeasured/1000000}\t\t{Vmeasured}\t\t{(raw_value+2**15)/2**16*100}')    
        #time.sleep(0.5)
        reliableMeasurements+=1
