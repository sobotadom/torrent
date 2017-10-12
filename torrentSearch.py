'''
Finds torrents on piratebay from a VIP user(green crossbones) and
returns the torrent info in a dictionary
The dict returned has the form {torrent#: [ name, time, size, uploader, magnet_link]}
'''
from bs4 import BeautifulSoup
from PyQt4 import QtGui
import requests

def torrentSearch(show_name, season_episode):
    url = 'https://thepiratebay.org/search/' + show_name + ' ' + season_episode

    webpage = requests.get(url)
    html = webpage.text


    body_soup = BeautifulSoup(html, 'html.parser')
    links = body_soup.find_all('tr')



    torrents = {}
    name = ''
    magnet_link = ''
    torrent_index = 0


    for link in links:

        link_soup = BeautifulSoup(str(link), 'html.parser')

        #Get torrent name
        title = link_soup.find_all('div',{'class':'detName'})
        for t in title:

            trusted = link_soup.find_all('img',{'title':'VIP'})
            if trusted != []:

                name = t.text.strip()


                #information
                tagline = link_soup.find_all('font',{'class': 'detDesc'})
                for i in tagline:
                    info = i.text

                temp = info.split(',')
                time = temp[0]
                size = temp[1]
                user = temp[2]


                #magnet link
                magnets = link_soup.find_all('a',{'title':'Download this torrent using magnet'})
                for m in magnets:
                    magnet_link = str(m['href'])
                    #print(magnet_link)


                if all(x in name.lower() for x in [season_episode.lower(), show_name.lower()]):

                    torrents.update({torrent_index : [name,time,size,user,magnet_link] })
                    torrent_index += 1



    return torrents
