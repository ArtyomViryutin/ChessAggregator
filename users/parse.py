import re

import requests
from bs4 import BeautifulSoup

frc_ratings_names = {
    'Классические': 'classic_frc_rating',
    'Быстрые': 'rapid_frc_rating',
    'Блиц': 'blitz_frc_rating',
    'std': 'classic_fide_rating',
    'rpd': 'rapid_fide_rating',
    'blz': 'blitz_fide_rating'
}


fide_ratings_names = {
    'std': 'classic_fide_rating',
    'rapid': 'rapid_fide_rating',
    'blitz': 'blitz_fide_rating'
}


def parse_frc(player, url):
    document = requests.get(url + str(player['frc_id']))
    soup = BeautifulSoup(document.content, 'lxml')
    header = soup.find(class_='page-header').h1.text
    groups = soup.find_all(class_='list-group')
    frc_ratings = groups[1]
    fide_ratings = groups[2] if len(groups) > 3 else None
    for li in frc_ratings.find_all('li'):
        player[frc_ratings_names[li.span.text[:len(li.span.text) - 1]]] = int(li.b.text)
    if fide_ratings is not None:
        player['fide_id'] = int(fide_ratings.a.text)
        name = re.findall(r'([a-zA-Z]+)', header)
        player['latin_name'] = name[0] + ' ' + name[1]
        for rating in fide_ratings.find_all('span'):
            s = rating.text.split(':')
            player[frc_ratings_names[s[0]]] = int(s[1])
    return player


def parse_fide(player, url):
    document = requests.get(url + str(player['fide_id']))
    soup = BeautifulSoup(document.content, 'lxml')
    title = soup.find('div', class_='profile-top-title').text
    name = title.split(', ')
    player['latin_name'] = name[0] + ' ' + name[1]
    ratings = soup.find_all('div', class_='profile-top-rating-data')
    for div in ratings:
        player[fide_ratings_names[div.span.text]] = int(div.span.next_sibling)
    return player


def parse(frc_id=None, fide_id=None):
    frc_url = 'https://ratings.ruchess.ru/people/'
    fide_url = 'https://ratings.fide.com/profile/'
    player = {
        'latin_name': None,
        'latin_surname': None,
        'frc_id': frc_id,
        'fide_id': fide_id,
        'classic_frc_rating': None,
        'rapid_frc_rating': None,
        'blitz_frc_rating': None,
        'classic_fide_rating': None,
        'rapid_fide_rating': None,
        'blitz_fide_rating': None
    }
    try:
        if player['frc_id']:
            player = parse_frc(player, frc_url)
        if player['fide_id'] and not player['classic_frc_rating']:
            player = parse_fide(player, fide_url)
    except Exception as err:
        print(err)
    return player
