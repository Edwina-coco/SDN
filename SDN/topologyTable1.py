import pycurl
from io import BytesIO
from bs4 import BeautifulSoup


class topologyTable(object):
    openflowID = ""
    openflowSPort = ""
    openflowDPort = ""
    DDeviceID = ""
    DDeviceIP = "无"
    BytesMatch = 0
    d00 = ""
    d01 = 0
    d02 = 0
    d03 = 0
    d04 = 0
    d05 = 0
    d06 = 0
    d07 = 0
    d08 = 0
    d09 = 0
    d10 = 0
    d11 = 0
    d12 = 0
    d13 = 0
    d14 = 0
    d15 = 0
    d16 = 0
    d17 = 0
    d18 = 0
    d19 = 0
    d20 = 0

    def __init__(self):
        openflowID = ""
        openflowSPort = ""
        openflowDPort = ""
        DDeviceID = ""
        DDeviceIP = "无"
        BytesMatch = 0
        d00 = ""
        d01 = 0
        d02 = 0
        d03 = 0
        d04 = 0
        d05 = 0
        d06 = 0
        d07 = 0
        d08 = 0
        d09 = 0
        d10 = 0
        d11 = 0
        d12 = 0
        d13 = 0
        d14 = 0
        d15 = 0
        d16 = 0
        d17 = 0
        d18 = 0
        d19 = 0
        d20 = 0
        pass

    def get_openflowID(self):
        return self.openflowID