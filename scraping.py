from urllib import request
from bs4 import BeautifulSoup
import csv

def scraping():
    url = "https://kakaku.com/pet/list/CategoryCD=5510/MakerCD=0/"

    #get html
    html = request.urlopen(url)

    #set BueatifulSoup
    soup = BeautifulSoup(html, "html.parser")
    breeds = list(soup.find_all("p", class_="name"))
    breeds = [breed.find('a') for breed in breeds]
    breeds = [breed for breed in breeds if breed is not None]
    breeds = [breed.string for breed in breeds]
    
    with open('C:/Users/Owner/study/dog/dog_breeds.csv', 'w', encoding='utf-8') as f:
        for breed in breeds:
            f.write(breed + '\n')
        print('書き込み完了')




if __name__ == "__main__":
    scraping()


