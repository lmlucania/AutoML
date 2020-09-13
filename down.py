from bs4 import BeautifulSoup
from urllib.error import HTTPError
import lxml
import requests
import urllib.request
import os
import time
def scraping():
    with open('C:/Users/Owner/study/dog/dog_breeds.csv', encoding='utf-8') as f:
        breeds = f.read().splitlines()
        for breed in breeds:
            dir_name = './data/{0}/'.format(breed)
            if os.path.exists(dir_name):
                continue
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            if breed == 'ボクサー':
                breed = 'ボクサー犬'
            if len(breed) >= 8:
                breed_alt = breed[:7] + '...'
            else:
                breed_alt = breed

                #300枚
            for num in range(15):
                headers = {'Uer-Agent': 'hoge'}
                URL = 'https://search.yahoo.co.jp/image/search?fr=sfp_ga1_as&p={0}&oq=&ei=UTF-8&b={1}'.format(breed, 1 + 20*num)
                resp = requests.get(URL,  headers=headers)
                time.sleep(2)
                soup = BeautifulSoup(resp.text, 'lxml')

                imgs = soup.find_all(alt='「{}」の画像検索結果'.format(breed_alt))

                for i in range(len(imgs)):

                    filepath = dir_name + '{0}-{1}.jpg'.format(num, i)
                    try:
                        urllib.request.urlretrieve(imgs[i]['src'], filepath)
                    except urllib.error.HTTPError:
                        pass


if __name__ == "__main__":
    scraping()
