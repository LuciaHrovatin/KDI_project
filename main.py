from Collectors import CrushCollector, EsnCollector
#from twitter import twitterAPI
#from meetup_data import meetupAPI
cc = CrushCollector()
esn = EsnCollector()
if __name__ == "__main__":

    try:
        print('DO NOT RUN')
        #cc.write_events()
        #esn.visit_event_and_write()

        # Twitter
        #visit_trentino = twitterAPI()
        #visit_trentino.parsing_tweets()

        # Meetup
        #meetup = meetupAPI(url="https://api.meetup.com/corsicampanetibetane/events/281042154?")
        #meetup.parsing_events()

    except:
        print('Error in page building encountered, please check if the link is correct')


print('Scraping has ended. No more links to visit')
