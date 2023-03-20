
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re

## first step is to go to the lat/long city website and compile all the info into a dataframe

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

"""
## test run of the format for this website
url = "https://www.latlong.net/category/cities-236-15-1.html"
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content,'html.parser')

results = soup.find_all('td')

for result in results:
    print(result.text)
    print('--------------')
"""

"""
## scrape all 12 pages
pages = range(12)

data = pd.DataFrame()

for page_num in pages:
    index = len(data)
    lat_long_url = "https://www.latlong.net/category/cities-236-15-{0}.html".format(page_num+1)
    response = requests.get(lat_long_url,headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')

    results = soup.find_all('td')
    count = 3
    for result in results:
        if count % 3 == 0:
            data.loc[index, 'City'] = result.text
        elif count % 3 != 0 and (count - 1) % 3 == 0:
            data.loc[index, 'Latitude'] = result.text
        elif count % 3 != 0 and (count + 1) % 3 == 0:
            data.loc[index, 'Longitude'] = result.text
            index += 1
        count += 1


    print(data)
## keep it!
data.to_csv('cities-lat-long.csv',index=False)
"""

## now to scrape a google search of the population of each city and keep that as a new column

"""
## bit of a test run here
google_url = "https://www.google.com/search?q={0}%2C+{1}%2C+USA+population".format('Dallas', 'TX')

response = requests.get(google_url, headers=headers)
soup = BeautifulSoup(response.content,'html.parser')

results = soup.find_all('div', {'aria-level': '3'})
for result in results:
    try:
        population = result.find('div', {'class': 'ayqGOc kno-fb-ctx KBXm4e'}).text
    except AttributeError:
        try:
            population = result.find('div', {'class': 'ayqGOc kno-fb-ctx kpd-lv kpd-le KBXm4e'}).text
        except AttributeError:
            continue
    if ',' in population:
        population = int(population.split(' ')[0].replace(',', ''))
    elif 'million' in population:
        population = int(population.replace('\xa0',' ').split(' ')[0].replace('.', '')) * 1000
    print(population)
"""
"""
cities_lat_long = pd.read_csv('cities-lat-long.csv')
## just a warning to anybody that runs this code on their own, since it's searching every single city
## this chunk of code takes quite a while to run...
## Well... turns out Google isn't a huge fan of me scraping things... So we'll
## switch over to scraping the population from the wikipedia page of each city
## (assuming it exists for each one)
for index in range(len(cities_lat_long)):
    location = cities_lat_long.loc[index, 'City'].replace(' ','').split(',')
    city = location[0]
    state = location[1]
    google_url = "https://www.google.com/search?q={0}%2C+{1}%2C+USA+population".format(city, state)

    response = requests.get(google_url, headers=headers)
    soup = BeautifulSoup(response.content,'html.parser')

    results = soup.find_all('div',{'aria-level':'3'})
    for result in results:
        print(result)
        try:
            population = result.find('div', {'class': 'ayqGOc kno-fb-ctx KBXm4e'}).text
        except AttributeError:
            try:
                population = result.find('div', {'class': 'ayqGOc kno-fb-ctx kpd-lv kpd-le KBXm4e'}).text
            except AttributeError:
                continue

        if ',' in population:
            population = int(population.split(' ')[0].replace(',', ''))
        elif 'million' in population:
            population = int(population.replace('\xa0',' ').split(' ')[0].replace('.', '')) * 1000
        cities_lat_long.loc[index, 'Population'] = population

        print(population)
    print('-----------------------', index, '-----------------------', '\n', cities_lat_long)
    print()

    ## sends it to a csv at every step because sometimes (hard to tell when) Google blocks the requests,
    ## so I'll probably have to do this over the course of multiple days
    cities_lat_long.to_csv('cities-lat-long-pop.csv',index=False)
"""

"""
## test code
city = 'Middletown'
state = 'New York'
if ' ' in state:
    state = state.replace(' ','_')

try:
    wiki_url = "https://en.wikipedia.org/wiki/{0},_{1}".format(city, state)
    print('processing {0} ...'.format(wiki_url))
    response = requests.get(wiki_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find('tbody')
    if results is not None:
        results_list = []
        for result in results:
            results_list.append(result.text)

        for index2 in range(len(results_list)):
            if 'Population' in results_list[index2]:
                population = results_list[index2 + 1]
                population = re.sub("[^\d\.]", '', population)
                print('Population =', population)

    else:
        print('Error, multiple locations with the name {0} in {1} found...'.format(city, state))
        results = soup.find_all('li')
        for result in results:
            if 'city' in result.text.lower():
                res = result.find_all('a',href=True)
                wiki_url = "https://en.wikipedia.org{0}".format(res[0]['href'])
                print('processing {0} ...'.format(wiki_url))
                response = requests.get(wiki_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                results = soup.find('tbody')
                if results is not None:
                    results_list = []
                    for result in results:
                        results_list.append(result.text)

                    for index2 in range(len(results_list)):
                        if 'Population' in results_list[index2]:
                            population = results_list[index2 + 1]
                            population = re.sub("[^\d\.]", '', population)
                            print('Population =', population)


except AttributeError:
    pass
"""


"""
## real thing
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


cities_lat_long = pd.read_csv('cities-lat-long.csv')
for index1 in range(len(cities_lat_long)):
    location = cities_lat_long.loc[index1, 'City'].split(',')
    city = location[0]
    if ' ' in city:
        city = city.replace(' ','_')
    state_abb = location[1].replace(' ','')
    if len(state_abb) == 2:
        state = states[state_abb.upper()]
        if ' ' in state:
            state = state.replace(' ','_')
    if len(state_abb) > 2:
        if ' ' in state_abb:
            state = state_abb.replace(' ', '_')
        else:
            state = state_abb

    try:
        wiki_url = "https://en.wikipedia.org/wiki/{0},_{1}".format(city, state)
        print('processing {0} ...'.format(wiki_url))
        response = requests.get(wiki_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        results = soup.find('tbody')
        if results is not None:
            results_list = []
            for result in results:
                results_list.append(result.text)

            for index2 in range(len(results_list)):
                if 'Population' in results_list[index2]:
                    population = results_list[index2 + 1]
                    population = re.sub("[^\d\.]", '', population)
                    print('Population =', population)
                elif 'Land' in results_list[index2]:
                    land_area = results_list[index2].split(' ')[0]
                    land_area = re.sub("[^\d\.]", '', land_area)
                    print('Land Area =', land_area)
                elif 'Water' in results_list[index2]:
                    water_area = results_list[index2].split(' ')[0]
                    water_area = re.sub("[^\d\.]", '', water_area)
                    print('Water Area =', water_area)

        else:
            print('Error, multiple locations with the name {0} in {1} found...'.format(city, state))
            results = soup.find_all('li')
            for result in results:
                if 'city' in result.text.lower():
                    res = result.find_all('a',href=True)
                    wiki_url = "https://en.wikipedia.org{0}".format(res[0]['href'])
                    print('processing {0} ...'.format(wiki_url))
                    response = requests.get(wiki_url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    results = soup.find('tbody')
                    if results is not None:
                        results_list = []
                        for result in results:
                            results_list.append(result.text)

                        for index2 in range(len(results_list)):
                            if 'Population' in results_list[index2]:
                                population = results_list[index2 + 1]
                                population = re.sub("[^\d\.]", '', population)
                                print('Population =', population)
                            elif 'Land' in results_list[index2]:
                                land_area = results_list[index2].split(' ')[0]
                                land_area = re.sub("[^\d\.]", '', land_area)
                                print('Land Area =', land_area)
                            elif 'Water' in results_list[index2]:
                                water_area = results_list[index2].split(' ')[0]
                                water_area = re.sub("[^\d\.]", '', water_area)
                                print('Water Area =', water_area)


        cities_lat_long.loc[index1, 'Population'] = population
        cities_lat_long.loc[index1, 'Land Area'] = land_area
        cities_lat_long.loc[index1, 'Water Area'] = water_area

    except AttributeError:
        pass

    print('-----------------------', index1, '-----------------------', '\n', cities_lat_long)
    print()

    cities_lat_long.to_csv('cities-info.csv',index=False)
"""
"""
## keep only cities with population greater than 50,000 (supposedly the metropolitan level,
## technically the city is also supposed to be classified as "urban," but I can worry about that
## in the next step)
cities_info = pd.read_csv('cities-info.csv')
big_cities = cities_info[cities_info['Population'] >= 50000].reset_index(drop=True)
big_cities.to_csv('big-cities-info.csv',index=False)
"""
## now I want to check if they're classified as "urban,"
## I'll do this in a similar manner as the population scraping, by
## going through the wiki pages and just checking if the word "urban"
## is mentioned in the side column

"""
## test code
city = 'Dallas'
state = 'Texas'

try:
    wiki_url = "https://en.wikipedia.org/wiki/{0},_{1}".format(city, state)
    print('processing {0} ...'.format(wiki_url))
    response = requests.get(wiki_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    urban = False
    results = soup.find('tbody')
    if results is not None:
        results_list = []
        for result in results:
            results_list.append(result.text)
        
        for index2 in range(len(results_list)):
            if 'Urban' in results_list[index2]:
                urban = True

    else:
        print('Error, multiple locations with the name {0} in {1} found...'.format(city, state))
        results = soup.find_all('li')
        for result in results:
            if 'city' in result.text.lower():
                res = result.find_all('a',href=True)
                wiki_url = "https://en.wikipedia.org{0}".format(res[0]['href'])
                print('processing {0} ...'.format(wiki_url))
                response = requests.get(wiki_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                results = soup.find('tbody')
                if results is not None:
                    results_list = []
                    for result in results:
                        results_list.append(result.text)

                    for index2 in range(len(results_list)):
                        if 'Urban' in results_list[index2]:
                            urban = True
except AttributeError:
    pass
"""

"""
## real thing
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


big_cities = pd.read_csv('big-cities-info.csv')
for index1 in range(len(big_cities)):
    location = big_cities.loc[index1, 'City'].split(',')
    city = location[0]
    if ' ' in city:
        city = city.replace(' ','_')
    state_abb = location[1].replace(' ','')
    if len(state_abb) == 2:
        state = states[state_abb.upper()]
        if ' ' in state:
            state = state.replace(' ','_')
    if len(state_abb) > 2:
        if ' ' in state_abb:
            state = state_abb.replace(' ', '_')
        else:
            state = state_abb

    try:
        wiki_url = "https://en.wikipedia.org/wiki/{0},_{1}".format(city, state)
        print('processing {0} ...'.format(wiki_url))
        response = requests.get(wiki_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        urban = False
        results = soup.find('tbody')
        if results is not None:
            results_list = []
            for result in results:
                results_list.append(result.text)

            for index2 in range(len(results_list)):
                if 'Urban' in results_list[index2]:
                    urban = True

        else:
            print('Error, multiple locations with the name {0} in {1} found...'.format(city, state))
            results = soup.find_all('li')
            for result in results:
                if 'city' in result.text.lower():
                    res = result.find_all('a',href=True)
                    wiki_url = "https://en.wikipedia.org{0}".format(res[0]['href'])
                    print('processing {0} ...'.format(wiki_url))
                    response = requests.get(wiki_url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    results = soup.find('tbody')
                    if results is not None:
                        results_list = []
                        for result in results:
                            results_list.append(result.text)

                        for index2 in range(len(results_list)):
                            if 'Urban' in results_list[index2]:
                                urban = True
    except AttributeError:
        pass

    if not urban:
        print(city, state, 'not urban, dropping...')
        big_cities = big_cities.drop(index=index1)

    print('-----------------------', index1, '-----------------------', '\n', big_cities)
    print()

    big_cities.to_csv('big-urban-cities.csv',index=False)
"""

## honestly... probably not going to use that dataframe. It got rid of Torrance, CA which,
## although is technically not an urban city, I think has way too many people (over 100,000)
## to be considered a "non-metro" area, at least for the purposes of my analysis.
## Maybe I'll just call these "large" cities rather than metro areas, since that's
## a technical classification.

## Next step is to obtain a dataset of the latitude and longitude for all the reservations in the
## dataset we'll be using.
"""
aian_data = pd.read_csv('earnings-income-by-race.csv')
reservations = aian_data['Native Lands']


## test code
reservation = reservations[0].replace(' ','+').replace(',','%2C')
try:
    ## for the record, only using bing because google blocked me with all my requests
    bing_url = "https://www.bing.com/search?q=latitude+and+longitude+of+{0}".format(reservation)
    print('processing {0} ...'.format(bing_url))
    response = requests.get(bing_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('li',{'class':'b_ans b_top b_topborder'})
    print(results)
    for result in results:
        lat_long = result.find('div',{'class':'b_focusTextMedium'}).text
        print(lat_long)
        lat_long = re.findall(r"\d+[.NW]", lat_long)
        print(lat_long)

        latitude = lat_long[0] + re.sub("[^\d\.]", '', lat_long[1])
        longitude = lat_long[2] + re.sub("[^\d\.]", '', lat_long[3])
        print('Lat:',latitude,'\nLong:',longitude)
except AttributeError:
    print('Error retrieving data')
    pass
"""
"""
## real thing
for index in range(len(reservations)):
    reservation = reservations[index].replace(' ', '+').replace(',', '%2C')
    error = True
    while error:
        try:
            ## for the record, only using bing because google blocked me with all my requests
            bing_url = "https://www.bing.com/search?q=latitude+and+longitude+of+{0}".format(reservation)
            print('processing {0} ...'.format(bing_url))
            response = requests.get(bing_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            results = soup.find_all('li', {'class': 'b_ans b_top b_topborder'})
            print(results)
            for result in results:
                lat_long = result.find('div', {'class': 'b_focusTextMedium'}).text
                print(lat_long)
                lat_long = re.findall(r"\d+[.NW]", lat_long)
                print(lat_long)
                if len(lat_long) == 4:
                    latitude = lat_long[0] + re.sub("[^\d\.]", '', lat_long[1])
                    longitude = lat_long[2] + re.sub("[^\d\.]", '', lat_long[3])
                    print('Success!\nLat:', latitude, '\nLong:', longitude,'\n\n')

                    aian_data.loc[index, 'Latitude'] = latitude
                    aian_data.loc[index, 'Longitude'] = longitude
                    error = False
        except AttributeError:
            print('Error retrieving data')
            pass

    aian_data.to_csv('earnings-income-by-race-plus-lat-long.csv',index=False)
"""

"""
## here's some code I found to try and get random proxies for the
## google search request to (assuming it works) mask my IP address
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from IPython.display import clear_output

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

# Here I provide some proxies for not getting caught while scraping
ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]
proxies_req = Request('https://www.sslproxies.org/')
proxies_req.add_header('User-Agent', ua.random)
proxies_doc = urlopen(proxies_req).read().decode('utf8')

soup = BeautifulSoup(proxies_doc, 'html.parser')
proxies_table = soup.find(id='list')
# Save proxies in the array
for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

# Choose a random proxy
proxy_index = random_proxy()
proxy = proxies[proxy_index]

for n in range(1, 20):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

# Every 10 requests, generate a new proxy
if n % 10 == 0:
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

# Make the call
try:
  my_ip = urlopen(req).read().decode('utf8')
  print('#' + str(n) + ': ' + my_ip)
  clear_output(wait = True)
except: # If error, delete this proxy and find another one
  del proxies[proxy_index]
  print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
#print(len(proxies))
#print(proxies)


## test code

reservation = reservations[0].replace(' ','+').replace(',','%2C')

user_agent = random.choice(user_agent_list)
new_headers = {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
proxy = random.choice(proxies)

url = "https://www.google.com/search?q=latitude+and+longitude+of+{0}".format(reservation)
print('processing {0} ...'.format(url))

session = requests.session()
response = requests.get(url, headers=headers, proxies=proxy)
#print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
#print(soup)
results = soup.find_all('div', {'class': 'kp-header'})
num = 1
for result in results:
    lat_long = result.find('div',{'class':'Z0LcW t2b5Cf'})
    if lat_long is not None:
        lat_long = lat_long.text

        west = False
        if 'w' in lat_long.lower():
            west = True

        south = False
        if 's' in lat_long.lower():
            south = True

        lat_long = re.findall(r"\d+[.°]", lat_long)
        #print(lat_long)

        longitude = float(lat_long[2] + lat_long[3][:-1])
        if west:
            longitude = -1 * longitude
        print('Longitude:',longitude)

        latitude = float(lat_long[0] + lat_long[1][:-1])
        if south:
            latitude = -1 * latitude
        print('Latitude:',latitude)
"""

"""
## use the following two lines if starting from scratch
#aian_data = pd.read_csv('earnings-income-by-race.csv')
#reservations = aian_data['Native Lands']

## use the following 7 lines if adding on lat/long data from existing file
aian_data = pd.read_csv('earnings-income-by-race-plus-lat-long.csv')
aian_data_w_latlong = aian_data[~aian_data['Latitude'].isna()]
aian_data_wo_latlong = aian_data[aian_data['Latitude'].isna()]
print('----------DATA WITH LAT/LONG----------\n',aian_data_w_latlong)
print('----------DATA WITHOUT LAT/LONG----------\n',aian_data_wo_latlong)
aian_data = aian_data_wo_latlong
reservations = aian_data['Native Lands']


## real thing (fingers crossed!)


## IP address masking code ##
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from IPython.display import clear_output

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

# Here I provide some proxies for not getting caught while scraping
ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]
proxies_req = Request('https://www.sslproxies.org/')
proxies_req.add_header('User-Agent', ua.random)
proxies_doc = urlopen(proxies_req).read().decode('utf8')

soup = BeautifulSoup(proxies_doc, 'html.parser')
proxies_table = soup.find(id='list')
# Save proxies in the array
for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

# Choose a random proxy
proxy_index = random_proxy()
proxy = proxies[proxy_index]

for n in range(1, 20):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

# Every 10 requests, generate a new proxy
if n % 10 == 0:
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

# Make the call
try:
  my_ip = urlopen(req).read().decode('utf8')
  print('#' + str(n) + ': ' + my_ip)
  clear_output(wait = True)
except: # If error, delete this proxy and find another one
  del proxies[proxy_index]
  print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


## latitude/longitude scraping code ##
for index in aian_data.index:
    reservation = reservations[index]
    if 'Off-Reservation' in reservation or 'Trust Land' in reservation:
        reservation = reservation.split('and')[0][:-1] + ', ' + reservation[-2:]
    reservation = reservation.replace(' ','+').replace(',','%2C')


    url = "https://www.google.com/search?q=latitude+and+longitude+of+{0}".format(reservation)
    print('processing {0} ...'.format(url))

    blocked = True
    tries = 0
    while blocked or tries < 25:
        user_agent = random.choice(user_agent_list)
        new_headers = {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
        proxy = random.choice(proxies)

        session = requests.session()
        response = requests.get(url, headers=headers, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(str(soup))
        if 'captcha' not in str(soup).lower():
            print('Results found! Searching for data...')
            blocked = False
            break
        print('Proxy {0} failed, no results found. Trying again...'.format(proxy))
        if tries == 25:
            print('Too many attempts, exiting code.')
            raise StopIteration
        tries += 1

    results = soup.find_all('div', {'class': 'kp-header'})
    # print(results)
    num = 1
    for result in results:
        lat_long = result.find('div',{'class':'Z0LcW t2b5Cf'})
        if lat_long is not None:
            lat_long = lat_long.text

            west = False
            if 'w' in lat_long.lower():
                west = True

            south = False
            if 's' in lat_long.lower():
                south = True

            lat_long = re.findall(r"\d+[.°]", lat_long)

            try:
                longitude = float(lat_long[2] + lat_long[3][:-1])
                if west:
                    longitude = -1 * longitude
                print('Longitude:',longitude)

                latitude = float(lat_long[0] + lat_long[1][:-1])
                if south:
                    latitude = -1 * latitude
                print('Latitude:',latitude)

                full_aian_data = pd.read_csv('earnings-income-by-race-plus-lat-long.csv')
                full_aian_data.loc[index, 'Latitude'] = latitude
                full_aian_data.loc[index, 'Longitude'] = longitude
                full_aian_data.to_csv('earnings-income-by-race-plus-lat-long.csv', index=False)
                
                ## this line is if you're starting from scratch
                #aian_data.to_csv('earnings-income-by-race-plus-lat-long.csv',index=False)
            except:
                pass

    print('-------------------',index,'-------------------\n',aian_data)
"""
