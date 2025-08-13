from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re


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

def get_forecast_data():
    
    driver.add_cookie({'name': 'celsius', 'value': '1','domain': 'world-weather.info'})
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


print(get_forecast_data())


    