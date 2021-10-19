from Collectors import CrushCollector, EsnCollector
from twitter import twitterAPI

if __name__ == "__main__":
        try:
            cc = CrushCollector()
            cc.visit_event_and_write()


            #esn = EsnCollector()
            #esn.visit_event_and_write()

            # Twitter
            #visit_trentino = twitterAPI()
            #visit_trentino.parsing_tweets()

        except:
                print('Error in page building encountered, please check if the link is correct')


print('Scraping has ended. No more links to visit')
