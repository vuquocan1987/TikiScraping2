import requests
from bs4 import BeautifulSoup
import time
def get_soup(url):
    time.sleep(1)
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, 'html.parser')
        return response
    except Exception as err:
        print('****************************************************************Error on request:' , err)
