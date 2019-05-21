import codecs
import json
import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

websites = ['https://warsawfoodie.pl/category/dzielnica/#page=1']

driver = webdriver.PhantomJS(executable_path=r'C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe') # or add to your PATH
driver.set_window_size(1024, 768) # optional
driver.get(websites[0])

while True:
    button = driver.find_element_by_class_name('read_more')
    if button.get_property('disabled'):
        break
    else:
        button.click()
        time.sleep(8)

descriptions = driver.find_element_by_class_name('description').text
desc_xpath = driver.find_elements_by_xpath('//*[@class="description"]')

links = []
for description in desc_xpath:
    ahref = description.find_elements_by_tag_name('a')
    href = ahref[0].get_attribute("href")
    links.append(href)

restaurants = []
for link in links:
    driver.get(link)
    restaurant_name = driver.find_element_by_class_name('post-title').text
    restaurant_description = driver.find_elements_by_class_name('post-content')[0].text
    restaurant_adress = 'nan'
    restaurant_price = 'nan'
    try:  # there are three types of the website
        restaurant_adress = driver.find_elements_by_class_name('localization')[0].text
        restaurant_price = driver.find_element_by_xpath(("//span[contains(text(), 'zł')]")).text
    except IndexError:
        page_content = driver.find_elements_by_tag_name('p')
        for element in page_content:
            if "Średnie" in element.text:
                restaurant_price = element.text
            if "Adres:" in element.text:
                restaurant_adress = (element.text.split(':', 1)[1])
    except NoSuchElementException:
        pass

    restaurant = {
        'name': restaurant_name,
        'description': restaurant_description,
        'price': restaurant_price,
        'adress': restaurant_adress
    }
    restaurants.append(restaurant)
    print('appended restaurant to list')

with codecs.open('..\\outputs\\warsaw_foodie.txt', 'w', encoding='utf-8') as outfile:
    json.dump(restaurants, outfile, ensure_ascii=False)