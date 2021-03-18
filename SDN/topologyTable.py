import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

class topologyTable(object):
    openflowID = ""
    openflowSPort = ""
    openflowDPort = ""
    DDeviceID = ""
    DDeviceIP = "无"
    Dstat="断开"
    Lstat="普通"
    def __init__(self):
        openflowID = ""
        openflowSPort = ""
        openflowDPort = ""
        DDeviceID = ""
        DDeviceIP = "无"
        Dstat = "断开"
        Lstat = "普通"
        pass

    def get_openflowID(self):
        return self.openflowID