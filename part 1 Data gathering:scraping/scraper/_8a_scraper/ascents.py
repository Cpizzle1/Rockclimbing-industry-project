import json
from bs4 import BeautifulSoup

try:
    from utils import login
except:
    from _8a_scraper.utils import login

def get_ascents(name, category):
    driver = login()
    name = name.lower().replace(' ', '+')
    url = f'https://www.8a.nu/api/search?query={name}&pageSize=100'
    driver.get(url)
    pre = driver.find_element_by_tag_name('pre').text
    items = json.loads(pre)['items']
    _category = 1 if category=='bouldering' else 0
    if items != None:
        possibilities = [i for i in items if 'zlaggableName' in i and
                i['category']==_category]
        # print(possibilities)
        # print(len(possibilities))
        if possibilities == []:
            return []

        else:  
            ascent = max(possibilities, key=lambda x: x['totalAscents'])
            
            base_url = 'https://www.8a.nu/api/crags/{}/{}/{}/sectors/{}/routes/{}/ascents?pageIndex={}&sortfield='
            page_index = 0
            ascents = []
            while True:
                url = base_url.format(category, ascent['countrySlug'], ascent['cragSlug'], ascent['sectorSlug'], ascent['zlaggableSlug'], page_index)
                driver.get(url)
                pre = driver.find_element_by_tag_name('pre').text
                data = json.loads(pre)
                if 'items' in data:
                    # dct1 = data['items']
                    # dct1['Country'] = ascent['countrySlug']
                    # dct1['Crag'] = ascent['cragSlug']
                    # dct1['Sector'] = ascent['sectorSlug']
                    # dct1['Name'] = 
                    
                    # print(data)




                    ascents+=data['items']
                if 'pagination' in data and data['pagination']['hasNext']:
                    page_index+=1
                else:
    
                    break
    else:
        return [] 
    # 
    driver.quit()
    print(f'{name} route is done!')
    return ascents  
