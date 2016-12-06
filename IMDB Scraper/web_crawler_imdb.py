import requests
from bs4 import BeautifulSoup

# Creating/Overwriting the File
file_save = open("IMDB.txt", "w")
file_save.write("")
file_save.close()
# Getting Genre Info from User
av_genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family",\
             "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport",\
             "Thriller", "War", "Western"]
print("Available Genres : ")
print(*av_genres, sep="\n")
genre = input('\nEnter Genre to Scrape :  ')
if genre in av_genres or genre in str(av_genres).lower():
    genre = genre
else:
    genre = "comedy"
    print("Entered Genre is not Valid, Using Default Genre (Comedy)")

# Getting Sorting Info from User
av_sorts = ["Popularity (moviemeter)", "Alphabetical (alpha)", "Rating (user_rating)", "Votes (num_votes)",\
            "Box Office (boxoffice_gross_us)", "Runtime (runtime)", "Year (year)", "Release Date (release_date)"]
print("\nAvailable Sorting Methods : ")
print(*av_sorts, sep="\n")
in_sort = str(input("\nEnter Sorting Method : "))

if in_sort in "Popularity" or in_sort in "popularity" or in_sort in "moviemeter":
    sort_method = "moviemeter"
elif in_sort in "Alphabetical" or in_sort in "alphabetical" or in_sort in "alpha":
    sort_method = "alpha"
elif in_sort in "Rating" or in_sort in "user_rating":
    sort_method = "user_rating"
elif in_sort in "Votes" or in_sort in "num_votes":
    sort_method = "num_votes"
elif in_sort in "Box Office" or in_sort in "boxoffice_gross_us" or in_sort in "box_office":
    sort_method = "boxoffice_gross_us"
elif in_sort in "Runtime" or in_sort in "runtime":
    sort_method = "runtime"
elif in_sort in "Year" or in_sort in "year":
    sort_method = "year"
elif in_sort in "Release Date" or in_sort in "release_date":
    sort_method = "release"
else:
    sort_method = "moviemeter"
    print('Entered Sorting Method is not Valid, Using default Sorting Method.')

av_sort_orders = ["Ascending (asc)", "Descending (desc)"]
print("\nAvailable Sorting Orders : ")
print(*av_sort_orders, sep="\n")
in_sort_order = input("\nEnter Sorting Order : ")
if in_sort_order in "Ascending" or in_sort_order in "asc":
    sort_order = "asc"
elif in_sort_order in "Descending" or in_sort_order in "desc":
    sort_order = "desc"
else:
    print("Entered Sorting Order is not Valid, Using default Sorting Order.")
    sort_order ="asc"

# rating checks
# pos_ratings = str(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
# feature or all films
all_or_ft = input("\nScrape for Only Feature Films ?, yes or no : ")
if all_or_ft in "yes" or all_or_ft in "YES":
    url = 'http://www.imdb.com/search/title?genres=' + genre + '&title_type=feature&sort='+ sort_method + ',' +\
          sort_order + '&page='
else:
    url = 'http://www.imdb.com/search/title?genres=' + genre + '&sort=' + sort_method + ',' +\
          sort_order + '&page='

page = 1
pages = input('Pages to Scrape: ')
while page <= int(pages):
    r = requests.get(url + str(page))
    soup = BeautifulSoup(r.content, 'html.parser')
    for item in soup.findAll('div', {'class', 'lister-item-content'}):
        number = str(item.contents[1].contents[1].string)
        title = str(item.contents[1].contents[3].string)
        year = str(item.contents[1].contents[5].string)
        url_link = str("http://www.imdb.com/" + item.contents[1].contents[3].get('href')).replace("//title", "/title")
        try:
            rating = str(item.contents[5].contents[1].contents[3].contents).replace("'", "")
        except:
            rating = "[N/A]"

        print(number + " " + title + " " + rating + " " + year + " - " + str(url_link)[:-16])
        file_save = open("IMDB.txt", "a")
        file_save.write(number + " com" + title + " " + rating + " " + year + " - " + str(url_link)[:-16] + "\n")
        file_save.close()
    page += 1

print("Copied to IMDB.txt ;)")
print("Successfully Scraped Info from IMDB" + " ( " + url + " ) ")

input('Press Enter Key to Exit :)')