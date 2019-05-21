import codecs
import json
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium import webdriver

website = 'https://www.tasteaway.pl/category/polska/warszawa-gdzie-zjesc/'

driver = webdriver.PhantomJS(executable_path=r'C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe') # or add to your PATH
driver.set_window_size(1024, 768) # optional
driver.get(website)
xpath = '//h3/a'
links = []

try:
    while True:
        link = driver.find_element_by_class_name('ajax-load-more')
        print(link.get_attribute('href'))
        driver.get(link.get_attribute('href'))
        restaurants = driver.find_elements_by_xpath(xpath)
        for restaurant in restaurants:
            links.append(restaurant.get_attribute('href'))
except NoSuchElementException:
    print('all pages loaded')


restaurants = []
for link in links:
    driver.get(link)
    tag_frame = driver.find_elements_by_class_name('post-tags')
    tags = [a.text for a in tag_frame][0].replace('Tags:', '').split(',')
    tags = [tag.strip().lower() for tag in tags]
    post_content = driver.find_element_by_class_name('post-content')
    p = post_content.find_elements_by_tag_name('p')
    post_text = []
    for nb, pp in enumerate(p):
        if 'PRAKTYCZNE' in pp.text:
            paragraphs_number = nb
            print(paragraphs_number)
            break # other way?
        else:
            paragraphs_number = 1
    post_text = [pp.text for pp in p[0:paragraphs_number]]
    restaurant_name = p[paragraphs_number+1].text
    try:
        restaurant_adress = p[paragraphs_number+2].text
    except IndexError:
        restaurant_adress = driver.find_element_by_class_name('_2iem').text
    if restaurant_name != '':
        restaurant = {
            'name': restaurant_name,
            'adress': restaurant_adress,
            'text': post_text,
            'tags': tags
        }
        restaurants.append(restaurant)
    else:
        pass

with codecs.open('..\\outputs\\taste_away.txt', 'w', encoding='utf-8') as outfile:
    json.dump(restaurants, outfile, ensure_ascii=False)
