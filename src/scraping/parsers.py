import requests
import codecs
from bs4 import BeautifulSoup as bs
from random import randint

__all__ = ('work', 'rabota')  # TODO что такое __all__ ???

accept = '*/*'
headers = [{
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Accept': accept,
}, {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': accept,
}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
    'Accept': accept,
}]


def work(url, city=None, language=None):
    jobs = []
    errors = []

    if not url:
        return jobs, errors

    domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers[randint(0, 2)])

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')

        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})

            for div in div_list:
                title_tag = div.find('h2')
                title = title_tag.text
                href = title_tag.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')

                if logo:
                    company = logo['alt']

                jobs.append({'title': title, 'url': domain + href, 'description': content,
                             'company': company, 'city_id': city, 'language_id': language})
        else:
            errors.append({'url': url, 'title': 'Main div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []

    if not url:
        return jobs, errors

    domain = 'https://www.radota.ua'

    resp = requests.get(url, headers=headers[randint(0, 2)])

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')
        main_table = soup.find('table', id='ctl00_content_ctl00_gridList')

        if main_table:
            tr_list = main_table.find_all('tr', attrs={'id': True})

            for tr in tr_list:
                title_tag = tr.find('p', attrs={'class': 'card-title'})
                href = title_tag.find('a')['href']
                title = title_tag.find('a')['title']
                content = tr.find('div', attrs={'class': 'card-description'}).text
                company = ''
                company_div = tr.find('a', attrs={'class': 'company-profile-name'})

                if company_div:
                    company = company_div.text

                jobs.append({'title': title, 'url': domain + href, 'description': content,
                             'company': company, 'city_id': city, 'language_id': language})
        else:
            errors.append({'url': url, 'title': 'Table does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


if __name__ == '__main__':  # TODO что такое __name__ ???
    url = 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python'
    jobs, errors = rabota(url)
    h = codecs.open('work.json', 'w', 'utf-8')  # 'w' work with file in write mode
    h.write(str(jobs))  # write to file
    h.close()



