import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers ={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    'Accept-language' 'en-US, en;q=0.5'
}

search_query = 'Mobile' .replace(' ', '+')
base_url = 'https://www.amazon.com.au/s?k={0}' .format(search_query)

items = []
for i in range (1, 6):
    print('Processing {0} ...' .format(base_url + '&page={0}' .format(i)))
    response = requests.get(base_url + '&page = {0}'.format(i), headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
    
    for result in results:
        product_name = result.h2.text
        
        try:
            rating = result.find('i', {'class': 'a-icon' }).text
            rating_count  = result.find('span', {'class': 'a-size-base'}).text
        except AttributeError:
            continue
        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price =(price1 + price2)

            product_url = 'https://www.amazon.com.au' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])

        except AttributeError:
            continue
        
    sleep(1.5)

df = pd.DataFrame(items, columns=['products', 'rating', 'rating count', 'price', 'product url'])
df.to_csv('{0}.csv'.format(search_query), index=False)
