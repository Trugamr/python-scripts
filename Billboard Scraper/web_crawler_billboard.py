import requests
from bs4 import BeautifulSoup


# clearing old data and writing html
billboard_txt = open("Billboard Hot 100.htm", 'w')
billboard_txt.write('<style>body{font-family: "Didact Gothic", sans-serif;font-size: 18.5px;letter-spacing: 0.07em}\
    hr{border:1px solid #d1d1d1;}a{text-decoration:none;transition:ease all 0.20s;}a:hover{color:#ff3838;}</style>\
    <link href="https://fonts.googleapis.com/css?family=Didact+Gothic" rel="stylesheet">')
billboard_txt.close()


r = requests.get('http://www.billboard.com/charts/hot-100')
soup = BeautifulSoup(r.content, 'html.parser')
for item in soup.findAll('div', {'class': 'chart-row__main-display'}):
    rank = str(item.contents[1].contents[1].text) + ". "
    last_week = str(item.contents[1].contents[3].text)
    artist = " - " + str(item.contents[5].contents[1].contents[3].text).replace('\n', '')\
        .replace('                                ', '').replace('                            ', '')
    song = str(item.contents[5].contents[1].contents[1].text)
    try:
        spot_link = item.contents[7].find('a', {'class': 'chart-row__link--spotify'}).get('data-href')[:-23]
        vev_link = item.contents[7].find('a', {'class': 'chart-row__link--video'}).get('data-href')[:-83]
        # vev_short = to hold short url
        # spot_short = to hold short url
    except:
        try:
            spot_link = item.contents[7].find('a', {'class': 'chart-row__link--spotify'}).get('data-href')[:-23]
        except:
            spot_link = "N/A"
        try:
            vev_link = item.contents[7].find('a', {'class': 'chart-row__link--video'}).get('data-href')[:-83]
        except:
            vev_link = "N/A"

    print(rank + song + artist + "\n" + "Spotify - " + spot_link + " | " + "Vevo - " + vev_link + "\n")
    billboard_txt = open("Billboard Hot 100.htm", 'a')

    if vev_link is "N/A" and spot_link is not "N/A":
        billboard_txt.write(rank + song + artist + " - " + "<a href='" + spot_link + "'target='_blank'>Spotify</a>"\
                           + " : " + "<a href='#'>N/A</a>" + "<br><hr>")
    elif vev_link is not "N/A" and spot_link is "N/A":
        billboard_txt.write(rank + song + artist + " - " + "<a href='#'>N/A</a>"\
                           + " : " + "<a href='" + vev_link + "'target='_blank'>Vevo</a>" + "<br><hr>")
    elif vev_link and spot_link is 'N/A':
        billboard_txt.write(rank + song + artist + " - " + "<a href='#'>N/A</a>" + " : "\
                            + "<a href='#'>N/A</a>" + "<br><hr>")
    elif vev_link and spot_link is not "N/A":
        billboard_txt.write(rank + song + artist + " - " + "<a href='" + spot_link + "'target='_blank'>Spotify</a>"\
                            + " : " + "<a href='" + vev_link + "'target='_blank'>Vevo</a>" + "<br><hr>")

    #billboard_txt.write(rank + song + artist + " - " + "<a href='"+ spot_link + "'target='_blank'>Spotify</a>" + " : "\
    #                  + "<a href='" + vev_link + "''target='_blank'>Vevo</a>" + "<br><hr>")
    # billboard_txt.write(rank + song + artist + "\n" +
    # "Spotify - " + spot_link + " | " + "Vevo - " + vev_link + "\n\n")
    billboard_txt.close()

print("Scraping Complete.\nInformation written to 'Billboard Hot 100.htm' file.")
end = input('Press Enter Key to Exit.')
