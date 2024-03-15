"""
Description: Class to parse HTML/XHTML and print an IP address from dyndns.org
Author: Jonathan Spurling
Section Number: ADEV-3005 (251409)
Date Created: March 11, 2024

Updates:
"""

from html.parser import HTMLParser
import urllib.request
from urllib.error import URLError

class MyIPParser(HTMLParser):
    """ Class that parses HTML/XHTML and prints an IP address from dyndns.org"""
    def __init__(self,*, convert_charrefs: bool = ...) -> None:
        """ Initializes the MyHTMLParser class"""
        super().__init__(convert_charrefs=convert_charrefs)
        self.body = False
        self.ip = ''

    def handle_starttag(self, tag, attrs):
        """ Finds the body start tag """
        if tag == 'body':
            self.body = True

    def handle_endtag(self, tag):
        """ Finds the body end tag """
        if tag == 'body':
            self.body = False

    def handle_data(self, data):
        """ Extracts the IP address from the body tag returned from dyndns.org """
        if self.body is True:
            try:
                self.ip = data[data.index(':') + 1:len(data)].strip()
            except ValueError:
                print("Error: Unable to extract IP address.")

ip_parser = MyIPParser()

try:
    with urllib.request.urlopen('http://checkip.dyndns.org/') as response:
        # html = str(response.read())
        html = response.read().decode('utf-8')
    ip_parser.feed(html)
    print(ip_parser.ip)
except URLError as e:
    print(f"Error: Unable to connect to the server. {e}")
