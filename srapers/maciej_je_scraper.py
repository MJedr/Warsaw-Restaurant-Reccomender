import json
import re
from bs4 import BeautifulSoup
import requests
import urllib
import urllib.request

websites = ['https://maciej.je/kategorie/na-miescie/warszawa/']

def make_soup(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)
    return soup


def get_restaurant_info(url):
    soup_restuarant = make_soup(url)
    restaurant_title = soup_restuarant.find('h2', {'class': "entry-title"}).text
    tags = soup_restuarant.find_all('article', {'class': re.compile("post-single.")}, id=re.compile('post.'))
    grade_words = soup_restuarant.find('div', {'class': "grade-verdict"})
    grade_numeric = len(soup_restuarant.find_all('i', {'class': "fa fa-star"}))
    grade_users = len(soup_restuarant.find_all('i', {'class': "fa fa-star mr-star-full"}))
    paragraphs = soup_restuarant.find_all('p')
    adress_pattern = re.compile("Lokalizacja.")
    paragraphs_text = [p.getText() for p in paragraphs]
    adress = list(filter(adress_pattern.match, paragraphs_text))
    adress_cleaned = [re.split(":|\|", x, 2)[1] for x in adress]
    for tag in tags:
        restaurant_tags = tag.get('class')
        regex = re.compile(r'tag-.')
        filtered_restaurant_tags = list(filter(regex.match, restaurant_tags))
        cleaned_restaurant_tags = [re.split('tag-', x, 1)[1] for x in filtered_restaurant_tags]
    restaurant = {
        'name': restaurant_title,
        # 'grade_words': grade_words,
        'grade_numetic': grade_numeric,
        'grade_users': grade_users,
        'tags': cleaned_restaurant_tags,
        'adress': adress_cleaned
    }
    return (restaurant)


def get_page(soup):
    restaurants_info = []
    links_restaurants = soup.find_all('a', {'class': "read-more-link"}, href=True)
    for link in links_restaurants:
        print(link['href'])
        info = get_restaurant_info(link['href'])
        restaurants_info.append(info)
    return restaurants_info

restaurants_info = {}
restaurants_info['restaurant'] = []
for website in websites:
    soup = make_soup(website)
    link_next_page = soup.find_all('a', {'class': 'page larger'})[0]['href']
    try:
        while True:
            restaurants_from_page = get_page(soup)
            restaurants_info['restaurant'].append(restaurants_from_page)
            soup = make_soup(link_next_page)
            link_next_page = soup.find_all('a', {'class': 'page larger'})[0]['href']
    except IndexError:
        break

with open('maciejje_rest.txt', 'w', encoding='utf-8') as outfile:
    json.dump(restaurants_info, outfile)