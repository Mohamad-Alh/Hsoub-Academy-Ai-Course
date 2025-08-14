from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from datetime import date
from tabulate import tabulate 
import json

today = date.today().strftime('%d/%m/%Y')


def get_forecast_data():
    
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "notifications": 2,
            "media_stream": 2,
        }
    }
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.get("https://world-weather.info/")
    
    driver.add_cookie({'name': 'celsius', 'value': '1'})
    driver.refresh()

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    resorts = soup.find("div", id="resorts")
        
    re_cities = r'">([\w\s]+)<\/a><span>'
    cities = re.findall(re_cities , str(resorts))
        
    re_temps = r'<span>(\+\d+|\-\d+)<span'
    temps = re.findall(re_temps,str(resorts))
    temps = [int(temp)for temp in temps]
        
    conditions_tags = resorts.find_all('span' , attrs={"class":'tooltip'}) # or class_='tooltip'
    conditions = [condition.get('title') for condition in conditions_tags]
    
    driver.quit()
    
    data = zip(cities,temps,conditions)
    return list(data)


def get_forecast_txt():
    data = get_forecast_data()
    if data:
        with open('output.txt', 'w') as f:
            f.write("Popular Cities Forecast\n")
            f.write(today + '\n')
            f.write('='*58 + '\n' )
            table  = tabulate(data,headers=["City" , "Temperature" , "Condition"] , tablefmt="pretty")
            f.write(table)
 

def get_forecast_json():
    data = get_forecast_data()
    if data:
        cities = [{'city': city , 'temp': temps , 'condition': condition} for city , temps  , condition in data]
        data_json = {'title': "Popular Cities Forecast", 'date': today , 'cities':cities}
        with open('output.json', 'w') as f:
            json.dump(data_json , f , ensure_ascii=False)


        

if __name__ == "__main__":
    get_forecast_txt()
    get_forecast_json()

