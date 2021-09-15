import requests

URL = "https://bitinfocharts.com/bitcoin/address/1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ"
page = requests.get(URL)

print(page.text)