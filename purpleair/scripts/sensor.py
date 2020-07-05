# This script detects for the presence of either a BME680 sensor on the I2C bus or a Sense HAT
# The BME680 includes sensors for temperature, humidity, pressure and gas content
# The Sense HAT does not have a gas sensor, and so air quality is approximated using temperature and humidity only.

import sys
import time
import os
from purpleair_bt import PurpleAir
from http.server import HTTPServer, BaseHTTPRequestHandler

class balenaPurpleAir():
    readfrom = 'unset'

    def __init__(self):
        # First, check for enviro plus hat (since it also has BME on 0x76)
        try:
            self.s = PurpleAir()
        except IOError:
            print('PurpleAir not found')
        else:
            print('PurpleAir error, exiting')
            sys.exit()


        # Next, check to see if there is a BME680 on the I2C bus
        if self.readfrom == 'unset':
            try:
                self.bus.write_byte(0x76, 0)
            except IOError:
                print('BME680 not found on 0x76, trying 0x77')
            else:
                print('BME680 found on 0x76')
                self.sensor = BME680(self.readfrom)
                self.readfrom = 'bme680primary'
                

    def sample(self):
        return self.s.as_flat_dict()



class balenaPurpleHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        API_ROOT = 'https://www.purpleair.com/json'
        id = 22079
        response = requests.get(f'{API_ROOT}?show={id}')
        self.wfile.write(json.dumps(response[0]['results']).encode('UTF-8'))
        #measurements = balenasense.sample()
        #self.wfile.write(json.dumps(measurements[0]['fields']).encode('UTF-8'))

    def do_HEAD(self):
        self._set_headers()


# Start the server to answer requests for readings
balenapurpleair = balenaPurpleAir()

while True:
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, balenaPurpleHTTP)
    print('Purple HTTP server running')
    httpd.serve_forever()
