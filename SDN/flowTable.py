import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

class flowTable(object):
    # Lightweight flow model object for template rendering.
    openflowID = ""
    openflowSPort = ""
    packet="断开"
    def __init__(self):
        openflowID = ""
        openflowSPort = ""
        packet=""
        pass

    def get_openflowID(self):
        return self.openflowID
