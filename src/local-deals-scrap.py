from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
api = Api(app)
CORS(app)


''' Edit the place ID with the area code '''
PLACE_ID = "63"

''' Maximum number of pages to scrape '''
MAX_PAGE_TO_SCRAPE = 2

''' ID of the dropdown used to select the neighbourhood '''
NEIGHBOURHOODS_DROPDOWN_ID = 'advanced-search-content'

class AreaCodes(Resource):
        
    def get(self):
        ''' Grab the neighbourhood codes '''
        url = 'https://dubai.dubizzle.com/classified/electronics/home-audio-turntables/amplifiers/?price__gte=&price__lte=&keywords=&is_basic_search_widget=1&is_search=1'

        soup = buildRequest(url)
        neighbourhoods = {}
        sorted_neighbourhoods = {}
        try:
            dropdown = soup.find(id=NEIGHBOURHOODS_DROPDOWN_ID)

            for neighbourhood in dropdown.find_all('option'):
                neighbourhoods.update({"".join(neighbourhood.contents): neighbourhood['value']})
            # We sort the areas alphabetically
            for key, value in sorted(neighbourhoods.items(), key = lambda x: x[0]):
                sorted_neighbourhoods.update({key: value})

            return sorted_neighbourhoods
        except Exception as e:
            print("Failed to retrieve the area codes: " + str(e))
            return ""
        

class LocalDeals(Resource):
    def get(self,code):
        ''' Now that the area code has been selected, we navigate to the corresponding page '''
        url = "https://dubai.dubizzle.com/classified/search/?places__id__in="+str(code)+"%2C&is_search=1"
        soup = buildRequest(url)

        try:
            
            ''' Extract the last page number 
            last_page = soup.find(id="last_page")['href']
            last_page_index_start = last_page.find("page=") + len("page=")
            last_page_index_end = last_page.find("&")
            how_many_pages = last_page[last_page_index_start:last_page_index_end]
            how_many_pages = int(how_many_pages)'''
            ''' We now know how many pages of items are online for this area '''
            ''' We then load all pages, and grab the items '''
            items = {}

            for page in range(1,MAX_PAGE_TO_SCRAPE + 1):
                url = "https://dubai.dubizzle.com/classified/search/?page=" + str(page) + "&places__id__in="+str(code)+"%2C&is_search=1"
                soup = buildRequest(url)
                print("Starting grabbing items on page " + str(page))
                for item in soup.find_all("div", {"class": "list-item-wrapper"}):
                    ''' Extract the ID '''
                    id = item.find("div",{"class":"listing-item"})['data-id']
                    
                    ''' Extract the title of the item '''
                    title = item.find("a", {"class":"lpv-link-item"}).contents
                    title = ' '.join(title)
                    title = title.strip()
                    
                    ''' Extract the category '''
                    category = item.find("p", {"class":"breadcrumbs"}).contents
                    category = ' '.join(category)
                    category = category.strip()
                    
                    ''' Extract the posting date '''
                    posted_date = item.find("p",{"class":"date"})
                    posted_date = ' '.join(posted_date)
                    posted_date = posted_date.strip()
                    
                    ''' Extract the thumbnail '''
                    thumbnail = item.find("div",{"class":"thumb"})
                    if thumbnail:
                        href = thumbnail.find("a")['href']
                        thumbnail = thumbnail.a.div['style']
                        find_url = thumbnail.find("url(") + len("url(")
                        thumbnail = thumbnail[find_url:-2]
                    else:
                        href = False
                    
                    ''' Extract the price '''
                    price = item.find("span",{"class":"selling-price__amount"}).contents[0]
                    price = ' '.join(price.split())
                    
                    ''' Extract the features '''    
                    features = {}
                    for features_ad in item.find_all("ul",{"class":"features"}):
                        for li in features_ad.find_all("li"):
                            key = li.contents[0][:-2]
                            value = ' '.join(li.contents[1].contents)
                            features[key] = value
                    
                    
                    ''' We save all the results in a dictionary '''
                    items[id] = {
                        "title": title,
                        "category": category,
                        "posted_date": posted_date,
                        "thumbnail": thumbnail,
                        "url": href,
                        "price": price,
                        "features": features        
                    }
                
            return items
        except Exception as e:
            print("Failed to retrieve the local deals: " + str(e))
            return ""
        
       
api.add_resource(AreaCodes,"/areacodes/")
api.add_resource(LocalDeals,"/localdeals/<int:code>")

def buildRequest(url):
    ''' Port used by Tor '''
    torport = 9050

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    proxies = {
        'http': "socks5h://localhost:{}".format(torport),
        'https': "socks5h://localhost:{}".format(torport)
    }

    r = requests.get(url,proxies=proxies,headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    return(soup)


if __name__ == "__main__":
    # Only for development environment! Do not leave the below in production!!
    app.run(debug=True)
