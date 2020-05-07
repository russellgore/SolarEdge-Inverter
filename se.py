import time
import urllib
from pyModbusTCP.client import ModbusClient
import win_inet_pton 

#How often to pull the data from the inverter (in seconds)
pollTime = 10

#IP/Port of solarEdge inverter 
seIp = '192.168.5.226'
sePort = 1502
c = ModbusClient(host=seIp,port=sePort, auto_open=True, auto_close=True)

def get(reg,length):
    return(c.read_holding_registers(reg,length))
while True:
	#Get the power generation data from the inverter
    generateData = get(40083,2)
    if generateData[1] == 0:
        genPower = generateData[0]/1000.0
    else:
        genPower = generateData[0]/10000.0

    #How much power we are exporting to the grid
    export = int(get(40206,1)[0])

    if export > 20000:
        export = export - 65535.0

    #How much power we are currently consuming at home
    consume = genPower - (export/1000.0)
    
    #get unix time stamp
    currentTime = int(time.time()) 
    print "%i,Generate: %f, Consume: %f, Export: %f" %(currentTime,genPower,consume,export / 1000.0)
    time.sleep(pollTime)
