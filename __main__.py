from machine import Pin, I2C, Timer
#from utime import sleep
import ssd1306
import select
import sys
import time

# USER VARIABLES
oledScreenHeight = 64 #typically 32 OR 64
displayLines = 2 #no. of lines to display at once
screenChangeTime = 5 #time in seconds

#Setup Display
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128,oledScreenHeight,i2c)

display.text('Starting Up', 0,0)
display.show()

#Setup reading from serial
poll_obj = select.poll()
# Register sys.stdin (standard input) for monitoring read events with priority 1
poll_obj.register(sys.stdin,1)

#stores the data from the connected machine
data_in = ['']
currentDataIndex = 0
isActive = False


def updateDisplay():
    display.fill(0)
        
    for lineIndex in range(displayLines):
        line = ''
        if (len(data_in) > currentDataIndex + lineIndex):
            line = data_in[currentDataIndex + lineIndex]
        
        display.text(line, 0, lineIndex * 16)
    display.show()
    
    
def showNextScreen(timer):
    #check if screen needs to change
    if len(data_in) <= displayLines or not isActive:
        return
    
    #print('Displaying Next Screen')
    global currentDataIndex
    currentDataIndex += displayLines
    
    if currentDataIndex >= len(data_in):
        currentDataIndex = 0
    

def mainLoop():
    global isActive
    while True:
        dataLength = 0
        # Check if there is any data available on sys.stdin without blocking
        if poll_obj.poll(0):  # poll(0) checks immediately without waiting (non-blocking)
            isActive = True
            for line in sys.stdin:
                line = line.strip()  # Remove leading/trailing whitespace
                if line:  # Process only non-empty lines
                    # Replace or append line in data array
                    if len(data_in) > dataLength:
                        data_in[dataLength] = line
                    else:
                        data_in.append(line)
                    dataLength += 1  # Increment data length counter
                else:
                    break

            if len(data_in) > 2:
                print(data_in)
        
        if (len(data_in) > 0 and isActive):
            updateDisplay()
        
        # Small delay to avoid high CPU usage in the loop
        time.sleep(1)

if __name__ == '__main__':
    timer = Timer(period=screenChangeTime * 1000, mode=Timer.PERIODIC, callback=showNextScreen)
    mainLoop()