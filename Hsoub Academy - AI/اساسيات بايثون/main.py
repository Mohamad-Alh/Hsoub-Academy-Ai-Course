import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate 
from datetime import date
import json

today = date.today().strftime('%d/%m/%y')

def get_book_data():
    url = 'https://books.toscrape.com/index.html'
    my_user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
    headers = {'user-agent': my_user_agent}
    response = requests.get(url , headers=headers)
    
    if response.ok:
        soup = BeautifulSoup(response.content,'html.parser')
        resorts = soup.find('div' , class_="col-sm-8 col-md-9")
        
        re_rating = r'<p class="(\w+-\w+\s+[\w\s\-]+)">'
        rating = re.findall(re_rating , str(resorts))
        
        re_name = r'title="([\w\s\']+)'
        name = re.findall(re_name , str(resorts))
        
    
        re_price = r'<p class="price_color">(£[\d.\d]+)<\/p>'
        price = re.findall(re_price , str(resorts))
        
        data = zip(name,rating,price)
        return list(data)
    else:
        return False

data = get_book_data()


def get_data_txt():
    if data:
        with open('output.txt' , 'w', encoding='utf-8') as f:
            f.write('Books Data')
            f.write(f'\n{today}')
            f.write('='*100 + '\n')
            table = tabulate(data , headers=['Book', 'Rating', 'Price'] , tablefmt='fancy_grid')
            f.write(table)

def get_data_json():
    
    books = [{'book':book ,'rating': rating , 'price': price}for book , rating , price in data]
    data_json = {'title': "Books Information" , 'Date': today , 'Books': books}
    
    with open('output.json' , 'w', encoding='utf-8') as f:
        json.dump(data_json , f ,ensure_ascii=False)

 
if __name__ == "__main__":
    get_data_txt()
    get_data_json()


    




