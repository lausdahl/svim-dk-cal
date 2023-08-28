import urllib.request, json
from icalendar import Calendar, Event
import os
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup, NavigableString
import csv


def fetch_and_dump_ics(entry_filter=None):
    cal = Calendar()
    cal_jylland = Calendar()
    cal_odder = Calendar()

    with open('odder.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        odder_events = [str(row[0]).strip() for row in csv_reader]
        odder_events = [k for k in odder_events if len(k) > 0]

    url = "https://xn--svmmetider-1cb.dk/staevner/liste_ajax.php?_=1660577257550"
    print("Fetching data from %s" % url)
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        for d in data['data']:
            event_raw_date = d['meet_date_start']
            if (entry_filter == None and datetime.strptime(event_raw_date,
                                                           '%Y-%m-%d').year >= datetime.today().year) or (
                    entry_filter and entry_filter(datetime.strptime(event_raw_date, '%Y-%m-%d'))):
                url = str(d['meet_link']).replace('\\', '')
                url = url[url.index("'") + 1:-1]
                url = url[0:url.index("'")].replace('../', 'https://xn--svmmetider-1cb.dk/')
                pool_filter = d['filter_pool']
                pool = d['pool']

                name = str(d['meet_link'])[str(d['meet_link']).index('>') + 1:-1]
                name = name[0:name.index('<')]

                print('%s on %s link %s' % (name, event_raw_date, url))
                # driver = webdriver.Chrome(url)
                # content = driver.page_source
                event = Event()

                event_date_found = False
                event_date_end_found = False
                bassin = ''
                deltagere = ''
                tilmeld_frist = ''
                zip_code = None
                dk = False

                def to_en(s):
                    for a, b in {('January', 'januar')
                        , ('February', 'februar'), ('March', 'marts'),
                                 ('April', 'april'), ('May', 'maj'), ('June', 'juni'),
                                 ('July', 'juli'), ('August', 'august'), ('September', 'september'),
                                 ('October', 'oktober'),
                                 ('November', 'november'),
                                 ('December', 'december')}:
                        s = str(s).lower().replace(b, a)
                    return s

                soup = BeautifulSoup(requests.get(url).text,features="html.parser")
                for div in soup.findAll('div', attrs={'class': 'k-portlet__body'}):
                    for p in div.findAll('p'):
                        if 'Stævnestart:' in p.text:
                            texts = [l.text for l in p.children]
                            for idx, text in enumerate(texts):
                                if idx + 1 < len(texts):
                                    if 'Stævnestart:' in text:
                                        try:
                                            event.add('dtstart',
                                                      datetime.strptime(to_en(texts[idx + 1]), '%d. %B %Y').date())
                                            event_date_found = True
                                        except ValueError:
                                            pass
                                    if 'Stævneslut:' in text:
                                        try:
                                            event.add('dtend',
                                                      datetime.strptime(to_en(texts[idx + 1]), '%d. %B %Y').date())
                                            event_date_end_found = True
                                        except ValueError:
                                            pass
                                    if 'Bassin:' in text:
                                        bassin = texts[idx + 1]
                                    if 'Deltagere:' in text:
                                        deltagere = texts[idx + 1]
                                    if 'Deltagere:' in text:
                                        tilmeld_frist = texts[idx + 1]

                if not event_date_found:
                    event.add('dtstart', datetime.strptime(event_raw_date, '%Y-%m-%d').date())
                if not event_date_end_found:
                    event.add('dtend', datetime.strptime(event_raw_date, '%Y-%m-%d').date())

                for div in soup.findAll('div', attrs={'class': 'k-portlet k-portlet--mobile'}):
                    if True in ['Placering' in div_pos.text for div_pos in
                                div.findAll('h3', attrs={'class': 'k-portlet__head-title'})]:
                        position = ",".join([c2 for c2 in [c for c in div.find_next('div', attrs={
                            'class': 'k-portlet__body'}).children if c.name == 'p'][0].children if
                                             type(c2) == NavigableString])
                        event.add('location', position)
                        address = position.split(',')
                        if len(address) > 1 and len(address[1].split(' ')) > 1:
                            try:
                                zip_code = int(address[1].split(' ')[0])

                            except ValueError:
                                pass
                        dk = 'Danmark' in position
                # web=requests.get(url).text
                # print(web)
                # ET.fromstring(web)
                # with urllib.request.urlopen(
                #         url) as st_url:
                #     # print(st_url.read())
                #     # doc = parse(st_url.read().text)
                #     # ET.fromstring(requests.get(
                #     print(doc)
                #
                #     f=doc.xpath('//P[text()="A"]')

                event.add('summary', name.encode('utf-8'))

                # event.add('dtend', datetime.strptime(event_raw_date, '%Y-%m-%d'))
                # event.add('dtstamp', datetime.strptime(event_raw_date, '%Y-%m-%d'))
                event.add('description', '\n'.join([l for l in [bassin, deltagere, tilmeld_frist, url] if len(l) > 0]))
                cal.add_component(event)
                if zip_code and zip_code > 5000 and dk:
                    cal_jylland.add_component(event)

                if True in [k in url for k in odder_events]:
                    cal_odder.add_component(event)

        directory = str(Path(__file__).parent) + "/"
        print("ics file will be generated at ", directory)
        with open(os.path.join(directory, 'swimming_meet.ics'), 'wb') as f:
            f.write(cal.to_ical())
        with open(os.path.join(directory, 'swimming_meet_jylland.ics'), 'wb') as f:
            f.write(cal_jylland.to_ical())
        with open(os.path.join(directory, 'swimming_meet_odder.ics'), 'wb') as f:
            f.write(cal_odder.to_ical())
