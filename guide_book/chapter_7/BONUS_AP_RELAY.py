import board, digitalio
import wifi, socketpool
from adafruit_httpserver import Server, Request, Response, POST

def setup_wifi_ap():
    ap_ssid = "EDUPICO_AP"
    ap_password = "12345678"
    wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
    pool = socketpool.SocketPool(wifi.radio)
    return pool

def setup_relay():
    relay = digitalio.DigitalInOut(board.GP22)
    relay.direction = digitalio.Direction.OUTPUT
    return relay

def light_on(relay):
    print("Light ON")
    relay.value = True

def light_off(relay):
    print("Light OFF")
    relay.value = False

def webpage():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="refresh" content="5">
    <title>USB Relay Control</title>
    </head>
    <body>
    <p>USB Relay Light Control</p>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="Light On"
    value="light_on" type="submit">Light On</button></a>
    <button class="button" name="Light Off"
    value="light_off" type="submit">Light Off</button></a>
    </form>
    </body>
    </html>
    """
    return html

def setup_server(pool, relay):
    server = Server(pool, "/static")

    @server.route("/")
    def base(request: Request):
        return Response(request, f"{webpage()}", content_type='text/html')

    @server.route("/", POST)
    def buttonpress(request: Request):
        if request.method == POST:
            raw_text = request.raw_request.decode("utf8")
            if "light_on" in raw_text:
                light_on(relay)
            if "light_off" in raw_text:
                light_off(relay)
            return Response(request, f"{webpage()}", content_type='text/html')

    print("Starting server...")
    server.start(str(wifi.radio.ipv4_address_ap))
    print("Listening on http://%s" % wifi.radio.ipv4_address_ap)
    return server

pool = setup_wifi_ap()
relay = setup_relay()
server = setup_server(pool, relay)
while True:
    server.poll()
