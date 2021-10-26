#from Collectors import CrushCollector, EsnCollector, StayHappeningCollector, meetupAPI
from accessibility_places import accessibilityAPI
#from twitter import twitterAPI
from open_data import opendataAPI
#cc = CrushCollector()
#esn = EsnCollector()
#sh = StayHappeningCollector()
if __name__ == "__main__":

    try:
        #print('DO NOT RUN')
        # CRUSH, ESN, STAY HAPPENING
        #cc.write_events()
        #esn.visit_event_and_write()
        #sh.write_events()
        
        # Twitter
        #visit_trentino = twitterAPI()
        #visit_trentino.parsing_tweets()

        # Meetup
        #meetup = meetupAPI(url="https://api.meetup.com/corsicampanetibetane/events/281042154?")
        #meetup.parsing_events()

        # Opendata Rovereto
        #op = opendataAPI()
        #op.get_events(url="https://www2.comune.rovereto.tn.it/servizionline/extra/json_sito/event/", city = "rovereto")
        #op.save_file()

        # Opendata Trento
        #op.get_events(url="https://www.comune.trento.it/api/opendata/v2/content/search?classes=event", city = "trento")
        #op.save_file()

        # Accessibility
        # acc = accessibilityAPI()
        # acc.save_acc_file(path="Trento_2021-10-26_09-56-54.csv", city = "trento")
        # acc.parse_acc_file()

        acc_rov = accessibilityAPI()
        acc_rov.save_acc_file(path="Rovereto_2021-10-23_11-58-52.csv", city="rovereto")
        acc_rov.parse_acc_file()

    except:
        print('Error in page building encountered, please check if the link is correct')


print('Scraping has ended. No more links to visit')
