import requests
from bs4 import BeautifulSoup


search = str(input('Do you want to search for a Single or Album ?, yes or no : ')).lower()
if search in "yes":
    search_string = input('Enter the Name of Single or Album : ')
    url1 = 'http://iplusfree.com/search/' + search_string +'/page/'
else:
    url1 = 'http://iplusfree.com/page/'

px = 1
page = int(input('No. of Pages to Scrape : '))
while px <= page:
    main_url = str(url1).lower() + str(px)
    r = requests.get(main_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for item in soup.findAll('a', {'class', 'xst'}):
        title = item.string.replace('[iTunes Plus AAC M4A] ', '').replace('[iTunes Plus AAC M4A + M4V]', ' ').replace('–', '-').replace("’", "'").replace('…', '...')
        href = item.get('href')
        # print(title + " - " + href)
        rx = requests.get(href, stream=True)
        soupx = BeautifulSoup(rx.content, 'html.parser')
        for itemx in soupx.findAll('div', {'class', 'comment-content'}):
            dlink_services = itemx.contents[1].text
            dlink = str(itemx.contents[1].contents[1]).replace("""<input class="idbox" onclick="this.disabled=true; this.value='Downloading...';window.open('""", ''
                          ).replace("[", "").replace("""','_blank');" type="button" value="Click here">""", ''
                            ).replace("""','_blank');" type="button" value="Click here"/>""", ''
                              ).replace('</input>', '').replace('<br/>', '').replace('<br>', '').replace('part.', 'Part'
                                ).replace('http://linkshrink.net/zV3J=', '').replace(']', '').replace('<p>', '').replace('</p>', '').replace('–', '-')
            print('\n' + title + " : \n" + dlink)
    px += 1