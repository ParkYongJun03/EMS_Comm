import Adafruit_DHT as dht
import time
sensor = dht.DHT11
PIN = 2 # GPIO.BCM

try:
    while True:
        (h, t) = dht.read_retry(sensor, PIN) # humid, temper
        if h is not None and t is not None :
            print(f'Temp > {t:.1f} c / Humidity > {h:.1f}')
        else :
            print('Sensor Error!')

        time.sleep(1.0) # 1 second delay
except KeyboardInterrupt:
    print('End of Program')