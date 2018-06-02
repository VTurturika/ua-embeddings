import wikipedia
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup
import argparse


def get_sources():
    top_page = wikipedia.page('Wikipedia:Multiyear_ranking_of_most_viewed_pages')
    pages = top_page.links
    with open('data/sources_list', 'w') as file:
        file.writelines('\n'.join(pages))
        print('Wrote sources list to data/sources_list')


def read_sources():
    with open('data/sources_list', 'r') as file:
        return file.read().split('\n')


def get_ukrainian_title(page_title):
    wikipedia.set_lang('en')
    try:
        wiki_page = wikipedia.page(page_title)
    except wikipedia.WikipediaException:
        print('{0} article not found'.format(page_title))
        return ''
    url = 'https://en.wikipedia.org/wiki/' + wiki_page.title.replace(' ', '_')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    link = soup.select_one('li.interwiki-uk a')
    if link is None:
        return ''
    href = link['href']
    ua_title = href[ href.rfind('wiki/') + 5: ]
    return unquote(ua_title).replace('_', ' ')


def save_article(title):
    if len(title) == 0:
        return
    wikipedia.set_lang('uk')
    try:
        page = wikipedia.page(title)
    except wikipedia.WikipediaException:
        print('{0} article not found'.format(title))
        return
    with open('text/wiki/' + title.replace('/', ' '), 'w') as file:
        file.write(page.content)
        print('{0} - saved\n'.format(title))


parser = argparse.ArgumentParser()
parser.add_argument('action', metavar='action', type=str, help='sources | articles')
args = parser.parse_args()

if args.action == 'sources':
    get_sources()
elif args.action == 'articles':
    articles = read_sources()
    for en_title in articles:
        ua_title = get_ukrainian_title(en_title)
        print('En: {0}, Ua: {1}'.format(en_title, ua_title))
        save_article(ua_title)
else:
    print('usage: python wiki_parser.py sources|articles')