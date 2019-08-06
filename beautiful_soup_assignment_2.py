from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

position = input('Enter the position: ')
position = int(position)
number_of_times = input('Enter number of times: ')

url = "http://py4e-data.dr-chuck.net/known_by_Hassanali.html"

for i in range(0, int(number_of_times)+1):
  html = urlopen(url, context=ctx).read()
  soup = BeautifulSoup(html, "html.parser")
  title_name = soup.title.string.split()[2]
  print(title_name)
  # Retrieve all of the anchor tags
  tags = soup('a')
  url = tags[position-1].get('href', None)