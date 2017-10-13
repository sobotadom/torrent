from imdbpie import Imdb


def seasonBuilder(title):

def season_builder(title):

    #gets the information of the show in general
    #Also gets the seasons and episdoes in a dict to use in the other file


    #iniatilize imdb object
    imdb = Imdb()
    imdb = Imdb(anonymize=True)

    title_json = imdb.search_for_title(title)
    if title_json == []:
        print('No Results Found')
    else:

        #get imdb id to get more information
        title_id = title_json[0]['imdb_id']
        result = imdb.get_title_by_id(title_id)

        show_title = result.title
        year = result.year
        image_url = result.cover_url
        description = result.plot_outline

        temp = imdb.get_episodes(title_id)

        #build season dict to send back to main file
        seasons = {}
        episodes = {}
        season_counter = 1
        for e in temp:



            #new dict entry for the next season, the number season of the show is the entry key
            if e.season > season_counter:

                #the current season is done, time to start building the next episiode dict
                seasons[season_counter] = episodes

                episodes = {}
                season_counter += 1

            episodes[e.episode] = [e.title, e.release_date, e.imdb_id]







        return show_title, year, image_url, description, seasons


#Gives the plot and poster image about a specific episode based off imdb_id returned in season_builder

def episodeBuilder(episode_id):

def episode_builder(episode_id):


    imdb = Imdb()
    imdb = Imdb(anonymize=True)

    episode = imdb.get_title_by_id(episode_id)

    return episode.plot_outline, episode.title
