import json
from selenium import webdriver
from itertools import chain

website = 'https://pl.tripadvisor.com/Restaurants-g274856-Warsaw_Mazovia_Province_Central_Poland.html#EATERY_OVERVIEW_BOX'

driver = webdriver.PhantomJS(executable_path=r'C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe') # or add to your PATH
driver.set_window_size(1024, 768) # optional
driver.get(website)
xpath = '//h3/a'
links = []


for i in range(2):
    link_list = driver.find_elements_by_class_name('property_title')
    link_list = [x.get_attribute('href') for x in link_list if x.get_attribute('href') is not None]
    links.append(link_list)
    new_website = driver.find_element_by_css_selector("a[class = 'nav next rndBtn ui_button primary taLnk']").get_attribute('href')
    print(new_website)

links = list(chain.from_iterable(links))
restaurants = []

for link in links:
    driver.get(link)
    restaurant_rate = driver.find_element_by_class_name('restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl').text
    restaurant_price = driver.find_element_by_class_name('restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h').text
    restaurant_tags = driver.find_element_by_class_name('restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h').text
    restaurant_name = driver.find_element_by_tag_name('h1').text
    restaurant_adress = driver.find_element_by_class_name('restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei').text
    restaurant = {
        'name': restaurant_name,
        'price': restaurant_price,
        'tags': restaurant_tags,
        'rate': restaurant_rate,
        'adress': restaurant_adress
    }
    restaurants.append(restaurant)


with open('..\\outputs\\trip_advisor.txt', 'w', encoding='utf-8') as outfile:
    json.dump(restaurants, outfile, ensure_ascii=False)
