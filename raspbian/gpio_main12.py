# import Adafruit_DHT as dht
# sudo apt install libgpiod2
import adafruit_dht as dht
import time
import board

SENSOR = dht.DHT11(board.D2)

while True:
    try:
        t= SENSOR.temperature
        h= SENSOR.humidity
        print(f'TEMP > {t:.1f}`C / HUMID > {h:.1f}%')
    except RuntimeError as e:
        print(f'ERROR > {e.args[0]}')
        time.sleep(1.0)
    except Exception as e:
        SENSOR.exit()
        raise e
    time.sleep(2.0)
