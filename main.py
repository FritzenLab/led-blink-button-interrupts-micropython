from machine import Pin, Timer
import time
#import gc
#gc.collect()


button = Pin(14,Pin.IN,Pin.PULL_UP) #Pi Pico 2
#button = Pin(26,Pin.IN,Pin.PULL_UP) #Xiao RP2350
led= machine.Pin(15, machine.Pin.OUT) #Pi Pico 2
ledonboard= machine.Pin(25, machine.Pin.OUT) #Pi Pico 2
#led= machine.Pin(27, machine.Pin.OUT) #Xiao RP2350

shouldblink= 0
ledblink= 0
buttontime= time.ticks_ms()
flowcontroltime= time.ticks_ms()

def myFunction(button):
    global shouldblink
    global buttontime
    
    if time.ticks_diff(time.ticks_ms(), buttontime) > 500: # this IF will be true every 5	00 ms
        buttontime= time.ticks_ms() #update with the "current" time
        
        print("Interrupt has occured")
        
        if shouldblink == 0: # alternate between blinking and not blinking, for every button press
            shouldblink = 1
        else:
            shouldblink = 0
            
def led_interrupt(timer):
    
    global ledblink
    global shouldblink
    
    if shouldblink == 1:
        led.value(not led.value())
    else:
        led.value(0)
        
if __name__ == "__main__":
    
    tim= Timer(-1)
    tim.init(mode=Timer.PERIODIC, period=200, callback=led_interrupt)
    button.irq(trigger=Pin.IRQ_RISING, handler=myFunction)
    
    while True: # Put anything here, it will not interfere or be interfered by the interrupts code
    
        ledonboard.value(1)
        time.sleep_ms(200)
        ledonboard.value(0)
        time.sleep_ms(200)
               