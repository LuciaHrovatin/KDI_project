
from scraping import Scraping, parser, path_crush, path_esn
import urllib.request

class CrushCollector():
    def __init__(self):

        self.categories =  ['danza-teatro', 'musica', 'cinema','didattica','incontri','mostre','iniziative-bambini']
        self.classe = ["colonna-1-5007-testoeviint","colonna-1-5007-testoevi"]
        self.path = path_crush
        self.start = "https://www.crushsite.it/it/{}{}"

    def collect(self) : 
        """Creates links to each subcategory containing lists of events"""
        links = []
        for c in self.categories : 
            category_main = self.start.format(c,'/')
            links.append(category_main)
        return links

    def visit_sub_event(self):
        """ Visits each subcategory link's event """
        links = self.collect()
        to_scrape = set()
        
        for l in links : 
           
            source =urllib.request.urlopen(l).read()
            main_categories = Scraping(source,l, parser)
            events = set(main_categories.select_link())
            for e in events :
               
                link = "https://www.crushsite.it{}"
                v = link.format(e)
                if (e is not None and not e.startswith('https:') ) :
                    if ('void' not in e and '#' not in e and '@' not in e) :
                        to_scrape.add(v)
                    
        to_scrape = list(to_scrape)
        return to_scrape
    
    def write_events(self) :
        lista = self.visit_sub_event() 

        for link in lista:
            try :
                source = urllib.request.urlopen(link).read()
                scrape = Scraping(source, link, parser)
                title = link.split('/')
                title = ''.join(title[-3:])
                scrape.write_to_csv(title,self.classe, path_crush)
                print("Scraping {} and writing it to file".format(link))
            except :
                print("Not able to access {}".format(link))
            
            
        


class EsnCollector() :
    def __init__(self) : 
        self.classe = ['title-container','node node-event node-promoted view-mode-full clearfix']
        self.path = path_esn
        self.start = "https://trento.esn.it/?q=events"
        self.source =  urllib.request.urlopen(self.start).read()
        self.categories = [l for l in Scraping(self.source, self.start, parser).select_link()]
        self.past = []

    def collect(self, iterator):
        """Creates links to each subcategory containing events"""
        events = []
        start = "https://trento.esn.it{}"

        for c in iterator:
            category_main = start.format(c)
            events.append(category_main)
        return events

    def visit_event_and_write(self):
        """ #Visits each subcategory link's event """
        events = self.collect(self.categories)#

        for e in events:
            if ('page' in e):
                self.past.append(e)

            else:
                source = urllib.request.urlopen(e).read()
                try:
                    scrape = Scraping(source,e, parser)
                    print("Scraping {} and writing it to file".format(e))
                    title = e.split('/')
                    title = title[-1]
                    scrape.write_to_csv(title,self.classe, path_esn)     
                except:
                    print('Issue with {} encountered'.format(e))
        self.past_events()

    def past_events(self):
        for p in self.past:
            source = urllib.request.urlopen(p).read()
            past_scraping = Scraping(source, p, parser)
            past_events = past_scraping.select_link()
            past = self.collect(past_events)  # Link intero
            for e in past:
                source = urllib.request.urlopen(e).read()
                try:
                    scrape = Scraping(source,e, parser)
                    print("Scraping {} and writing it to file".format(e))
                    title = e.split('/')
                    title = title[-1]
                    scrape.write_to_csv(title,self.classe, path_esn)
                except:
                    print('Issue with {} encountered'.format(e))

    
