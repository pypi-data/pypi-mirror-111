import machine
import utime

class HCSR04:
    def __init__(self, trig, echo):
        self.TrigPin = machine.Pin(trig, machine.Pin.OUT)
        self.EchoPin = machine.Pin(echo, machine.Pin.IN)

    def read(self):
        self.TrigPin.off()
        utime.sleep_us(2)
        self.TrigPin.on()
        utime.sleep(10)
        self.TrigPin.off()
        try:
            pulse_time = machine.time_pulse_us(self.EchoPin, 1, 500*30*2)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')

if __name__ == "__main__":
    TRIG = 12 # D6
    ECHO = 13 # D7
    hc = HCSR04(TRIG, ECHO)
    while 1:
        print(hc.read())
        utime.sleep(1)
