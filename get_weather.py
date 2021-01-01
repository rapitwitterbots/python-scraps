import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = "https://www.weather.com"
response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(response).read()
soup = BeautifulSoup(html, 'lxml')

query_box = soup.find(input, type="text")
print(query_box)