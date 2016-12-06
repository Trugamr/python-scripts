import requests
from bs4 import BeautifulSoup
import shutil
import os


# features to be added : selective torrent downloads
# https://yts.ag/browse-movies/0/all/animation/4/latest?page=2

if not os.path.exists("yts"):
    os.makedirs("yts")
os.chdir('yts')


def tor_downloader(tor_url, name):
    t = requests.get(tor_url, stream=True)
    if t.status_code == 200:
        with open(name, 'wb') as f:
            t.raw.decode_content = True
            shutil.copyfileobj(t.raw, f)

av_genres = ["All", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
             "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show", "History", "Horror", "Music", "Musical",
             "Mystery", "News", "Reality-TV", "Romance", "Sci-Fi", "Sport", "Talk-Show", "Thriller", "War", "Western"]
av_orders = ["Latest", "Oldest", "Seeds", "Peers", "Year", "Rating", "Likes", "Alphabetical", "Downloads"]


dec = input('Do you want a Search for a Specific Movie ?, yes or no : ')
if dec in "yes" or dec in "YES" or dec in "Yes":
    spec_title = input('Enter the Movie Title : ')
    genre_search = "all"
    min_rating = "1"
    order_search = "year"
    pg = 1
    pg_search = ""
elif dec in "no" or dec in "NO" or dec in "No":
    pg = int(input('Enter Pages to Scrape : '))
    if pg == 1:
        pg_search = ""
    elif pg == 0:
        print('srlsy dude -_- , 0 ?')
        pg_search = ""
    else:
        pg_search = "?page=" + str(pg)
    spec_title = "0"
    adv_search = input('Advanced Search ?, yes or no : ')
    if adv_search in "yes" or dec in "YES" or dec in "Yes":
        print("Available Genres : ")
        print(*av_genres, sep=", ")
        genre_search = input('Enter a Genre : ').lower()
        min_rating = input('Minimum Rating (1-10) : ')
        print("Available Orders : ")
        print(*av_orders, sep=", ")
        order_search = input('Order By : ')

    elif adv_search in "no" or dec in "NO" or dec in "No":
        genre_search = "all"
        min_rating = "1"
        order_search = "latest"
    else:
        genre_search = "all"
        min_rating = "1"
        order_search = "latest"
        print('I said yes or no !, argh... lets go normal then.')

atc = str(input('Enable Automatic Torrent Downloads ?, yes or no : ')).lower()

print('\n')
page = 1
while page <= pg:
    if page == 0 or page == 1:
        pg_search = ""
    else:
        pg_search = "?page=" + str(page)
    url = 'https://yts.ag/browse-movies/' + spec_title + '/all/' + \
          genre_search + '/' + min_rating + '/' + order_search + pg_search
    r = requests.get(url, stream=True)
    soup = BeautifulSoup(r.content, 'html.parser')
    for item in soup.findAll('div', {'class', 'browse-movie-wrap'}):
        source = item.findAll('a', {'class', 'browse-movie-title'})
        source2 = item.findAll('div', {'class', 'browse-movie-year'})
        source3 = item.findAll('h4', {'class', 'rating'})
        source4 = item.findAll('div', {'class', 'browse-movie-tags'})
        source5 = item.contents[1].contents[1].contents[1].contents[1].contents[5]
        source6 = item.contents[1].contents[1].contents[1].contents[1].contents[7]
        title = source[0].string.replace(':', ' -').replace('/', ' ')
        genre1 = source5.string
        genre2 = source6.string
        if genre2 in "View Details":
            genres = "(" + genre1 + ")"
        else:
            genres = "(" + genre1 + ", " + genre2 + ")"
        href = source[0].get('href')
        year = "(" + source2[0].string + ")"
        rating = "[" + source3[0].string.replace(' / 10', '') + "]"

        # quality : 3D, 720p, 1080p
        try:
            q_1 = source4[0].contents[1].text
        except IndexError:
            q_1 = ""
        try:
            q_2 = source4[0].contents[3].text
        except IndexError:
            q_2 = ""
        try:
            q_3 = source4[0].contents[5].text
        except IndexError:
            q_3 = ""

        # torrent downloads
        if atc in "yes":
            try:
                d_1 = source4[0].contents[1].get('href')
                file_name = title + " " + year + " " + rating + " " + q_1 + '.torrent'
                tor_downloader(d_1, file_name)
            except IndexError:
                d_1 = ""
            try:
                d_2 = source4[0].contents[3].get('href')
                file_name = title + " " + year + " " + rating + " " + q_2 + '.torrent'
                tor_downloader(d_2, file_name)
            except IndexError:
                d_2 = ""
            try:
                d_3 = source4[0].contents[5].get('href')
                file_name = title + " " + year + " " + rating + " " + q_3 + '.torrent'
                tor_downloader(d_3, file_name)
            except IndexError:
                d_3 = ""
        else:
            try:
                d_1 = source4[0].contents[1].get('href')
                file_name = title + " " + year + " " + rating + " " + q_1 + '.torrent'
            except IndexError:
                d_1 = ""
            try:
                d_2 = source4[0].contents[3].get('href')
                file_name = title + " " + year + " " + rating + " " + q_2 + '.torrent'
            except IndexError:
                d_2 = ""
            try:
                d_3 = source4[0].contents[5].get('href')
                file_name = title + " " + year + " " + rating + " " + q_3 + '.torrent'
            except IndexError:
                d_3 = ""

        if q_3 in "3D":
            fx = ""
        else:
            fx = "\n"
        # file_name = title + year + rating + q_1 + '.torrent'
        print(" " + title, year, rating, "-", href, "\n", genres, "\n", q_1, d_1, "\n", q_2, d_2, "\n", q_3, d_3, fx)
    # print("Scraped from " + url)
    page += 1
notice = input(' tru ^.^')
