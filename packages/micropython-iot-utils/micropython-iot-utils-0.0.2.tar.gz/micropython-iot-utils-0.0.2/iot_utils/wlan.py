import network
import time


class WlanStation:

    def __init__(self, creds=None, essid=None, ipconfig=None):
        """
        Wifi Station class, with some high level functions.
        
        creds (dict): dictionary with {SSID:PASSWORD,...} sets
        essid (str): preferred SSID to connect to, can be None
        ipconfig (tuple): tuple (MyIPAddress, NetMask, Gateway, Nameserver), can be None
        
        """
        self.sta = network.WLAN(network.STA_IF)
        self.essid = essid
        self.bssid = None
        self.creds = creds
        self.ipconfig = ipconfig

    def enable(self):
        if not self.sta.active():
            self.sta.active(True)

    def disable(self):
        if self.sta.active():
            self.sta.active(False)

    def scan(self):
        # scan_keys: = "ssid", "bssid", "channel", "RSSI", "authmode", "hidden"
        self.enable()
        try:
            ssid_info = self.sta.scan()
            # sort ssids by RSSI decreasing         
            found_ssids = [(s[0].decode("utf-8"), s[1]) for s in sorted(ssid_info, key=lambda x: x[3], reverse=True)]
        except OSError:
            found_ssids = []
        return found_ssids

    def find_known_network(self):
        rv = (None, None, None)
        if self.essid:
            essids = [(self.essid, "")]
        else:
            essids = self.scan()
        
        for e, b in essids:
            if e in self.creds:
                rv = (e, ":".join(["%02x" % i for i in b]), self.creds.get(e))
                break
        return rv

    def disconnect(self):
        self.sta.disconnect()
        self.disable()

    def auto_connect(self):
        e, b, p = self.find_known_network()
        if e and p:
            self._connect(e, b, p)

    def status(self):
        return self.sta.isconnected()  

    def __str__(self):
        ip = self.sta.ifconfig()[0]
        is_conn = self.sta.isconnected()
        return "<STA: essid:%s bssid:%s ip:%s conn:%d>" % (self.essid, self.bssid, 
                                                           ip, is_conn)

    def _connect(self, essid, bssid, passwd):
        self.essid = essid
        self.bssid = bssid
        self.enable()
        if self.ipconfig:
            self.sta.ifconfig(self.ipconfig)
        self.sta.connect(essid, passwd)
        connect_tmo = 20
        while connect_tmo > 0 and self.sta.isconnected() == False:
            connect_tmo -= 1
            time.sleep_ms(500)
        rv = self.sta.isconnected()            
        return rv

    def get_active_config(self):
        if self.sta.isconnected():
            rv = {
                "ssid" : self.essid,
                "ipconfig" : self.sta.ifconfig(),
                }
        else:
            rv = None
        return rv 


def wifi_off():
    network.WLAN(network.STA_IF).active(False)  # WiFi station interface
    network.WLAN(network.AP_IF).active(False)  # access-point interface
    
if __name__ == "__main__":
    import machine
    try:
        import app_config as cfg
    except:
        print("module app_cfg not found")

        class Cfg(object):
            pass

        cfg = Cfg()

    t0 = time.time()
    
    ws = WlanStation(creds=getattr(cfg, "creds", None),
                     essid=getattr(cfg, "ssid", None),
                     ipconfig=getattr(cfg, "ipconfig", None))
    ws.disable()
    ws.auto_connect()
    t1 = time.time()
    print("duration: %.2fs\nstatus: %s" % (t1 - t0, ws.sta.status()))
    print(ws.scan())
    print("ipconfig:", ws.sta.ifconfig())
    print("dhcp_hostname:", ws.sta.config("dhcp_hostname"))
    print(ws)
    
