import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

#creating list of urls and scrapping the 'archives' landing page of the Hatchet to fill list with URLs of each volume summary page.
URL = 'https://www.gwhatchet.com/archives/'
r = requests.get(URL)
soup = BeautifulSoup(r.text)

url_list = []

body_class = soup.select_one('div.primary-container') #select div with just the volume headings and links
for link in body_class.findAll('a')[0:5]: #limiting to the first few urls for the purposes of testing. remove this range if desired to scrap ALL links
    url_list.append(link.get('href'))

complete_url_list = []

for urls in url_list: ##this for loop will populate a new list with page numbers 1-7 for each url in the url list. probably a better way to do this, but it works for now
  count = 1
  while count < 8:
    complete_url_list.append(urls + 'page/' +str(count))
    count += 1

#creating dataframe to hold info
data = pd.DataFrame(columns=['headline', 'author', 'category', 'content', 'full_url'])

for link in range(len(complete_url_list)): ##loop through URLs to create soup for each url in complete_url_list
  result = requests.get(complete_url_list[link])
  html = result.content
  soup = BeautifulSoup(html)

  for post in soup.find_all('article', attrs ={'class' : 'post'}):  ##use each soup to extract headline, author, category, content, and url info
    try:
      headline = post.find('h2', attrs ={'class' : 'post-title'}).text
    except:
      print('No Headline found')
      pass

    try:
      author = post.find('span', attrs = {'class' : 'byline-author'}).text.strip('By ') #stripping By and whitespace #####this line will error out because some posts lack author
    except: 
      print('No Author found')
      pass

    try:
      category = post.find('div', attrs={'class' : 'category-badge'}).text.strip() 
    except:
      print('No Category found')
      pass

    try:
      content = post.find('div', attrs={'class' : 'post-content'}).text.strip()
    except:
      print('No Content found')
      pass

    try:
     full_url = post.find('h2').find('a').get('href')
    except:
      print('No full_url found')
      pass

    data = data.append({'headline': headline, 'author': author, 'category': category, 'content': content, 'full_url': full_url}, ignore_index=True) #add extracted info to dataframe

    sleep(1)

data.to_csv (r'hatchet_dataframe.csv', index = False, header = True)
