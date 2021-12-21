
from os import lseek
from scraping import Scraping, parser, path_crush, path_esn, path_stay
import urllib.request
import json
import requests
import csv
import bs4 as bs 
class CrushCollector():
    def __init__(self):

        self.categories =  ['danza-teatro', 'musica', 'cinema','didattica','incontri','mostre','iniziative-bambini']
        self.classe = ["colonna-1-5007-testoeviint","colonna-1-5007-testoevi"]
        self.path = path_stay
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
        self.categories = set([l for l in Scraping(self.source, self.start, parser).select_link() if 'events' in l][2:])
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
        events = self.collect(self.categories)

        for e in events:
            if ('events&page' in e):
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
                    print('Not able to access {}'.format(e))
        self.past_events()

    def past_events(self):
        older_events = []
        while len(self.past) > 0:
            popped = self.past.pop()
            source = urllib.request.urlopen(popped).read()
            past_scraping = Scraping(source, popped, parser)
            past_events = past_scraping.select_link()
            past = self.collect(past_events)  # Link intero
            older_events.extend(past)

        older_events = set(older_events)
        
        for e in older_events:
            if ('page' in e) :
                self.past.append(e)
            else :
                source = urllib.request.urlopen(e).read()
                try:
                    scrape = Scraping(source,e, parser)
                    print("Scraping {} and writing it to file".format(e))
                    title = e.split('/')
                    title = title[-1]
                    scrape.write_to_csv(title,self.classe, path_esn)
                except:
                    print('Issue with {} encountered'.format(e))
                    
        if (len(self.past) > 0) :
            self.past_events()
        

    
class StayHappeningCollector():
    def __init__(self):

        self.categories =  ['--entertainment', '--music', '--art','--workshops','--trips-adventures','--health-wellness',
        '--business','--theatre','--literary-art', '--exhibitions', '--parties','--trekking']
        self.classe = ["text-center","col-xl-8 col-lg-10 offset-xl-2 offset-lg-1", "mt-3"]
        self.path = path_stay
        self.start = "https://stayhappening.com/trento{}"

    def collect(self) : 
        """Creates links to each subcategory containing lists of events"""
        links = []
        for c in self.categories : 
            category_main = self.start.format(c,'/')
            links.append((c,category_main))
        return links

    def visit_sub_event(self):
        """ Visits each subcategory link's event """
        links = self.collect()
        to_scrape = set()
        
        for l in links : 
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url = l[1]
            source = urllib.request.urlopen(reg_url).read()
            #past_scraping = Scraping(source, popped, parser)
            #req = urllib.request.Request(url=reg_url, headers=headers) 
            #source = urllib.request.urlopen(req).read() 
           
            main_categories = Scraping(source,l[1], parser)
            events = set(main_categories.select_link())
            for e in events :
                
                
                if (e is not None ) :
                    if ('void' not in e and '#' not in e and '@' not in e) :
                        to_scrape.add((l[0],e))
                       
                    
        to_scrape = list(to_scrape)
        return to_scrape
    
    def write_events(self) :
        lista = self.visit_sub_event() 
       
        for link in lista:
            try : 
                headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
                reg_url = link[1]
                #req = urllib.request.Request(url=reg_url, headers=headers) 
                source = urllib.request.urlopen(reg_url).read() 
                scrape = Scraping(source, link[1], parser)

                title = link[1].split('/e/')
                title = link[0][2:]+'-'+''.join(title[-1]) 
                
                
                scrape.write_to_csv(title.replace('/',''),self.classe, path_stay)
                print("Scraping {} and writing it to file".format(link))
            except :
                print("Not able to access {}".format(link[1]))
           

class SubLanEvents() :
    def __init__(self) :
        self.link = "https://www.mymovies.it/cinema/trento/versione-originale/"
        self.classe = ["schedine-titolo","mm-line-height-130 schedine-lancio", "mm-medium", 
        'mm-btn stonda3 mm-btn-nocursor mm-padding-2 mm-letter-spacing btn-buy-no mm-margin-b4' ]
    
    def scrape_and_write(self) : 
        source = urllib.request.urlopen(self.link).read()
        scrape = Scraping(source,self.link, parser)
        print("Scraping {} and writing it to file".format(self.link))
        body = scrape.get_body(self.classe)

        with open('Original_language_movies_html.csv', 'w', encoding = 'utf-8') as f :
            writer = csv.writer(f)
            writer.writerow(body)
            f.close()

        
                    
                    
class meetupAPI:

    def __init__(self, url):
        self.url = url
        self.file_name = "meetup_data.json"

    def parsing_events(self):
        df = requests.get(self.url)
        data = df.json()

        with open(self.file_name,"w", encoding="utf-8") as f:
            final_str = json.dumps(data, indent=4,
                                   sort_keys=True,
                                   separators=(",", ": "),
                                   ensure_ascii=False)
            f.write(final_str)


class Reviewer() : 

    def __init__(self) :
        self.link = ["https://www.tripadvisor.it/ShowUserReviews-g187861-d600982-r509916737-Castello_del_Buonconsiglio_Monumenti_e_Collezioni_Provinciali-Trento_Province_of_.html",
        "https://www.tripadvisor.it/ShowUserReviews-g194889-d2054642-r140669078-Museo_di_Arte_Moderna_e_Contemporanea_di_Trento_e_Rovereto-Rovereto_Province_of_.html",
        "https://www.tripadvisor.it/Restaurant_Review-g187861-d1128166-Reviews-Antica_Birreria_Pedavena-Trento_Province_of_Trento_Trentino_Alto_Adige.html",
        "https://www.tripadvisor.com/Restaurant_Review-g187861-d10304321-Reviews-Bookique-Trento_Province_of_Trento_Trentino_Alto_Adige.html"
        ]
        self.classe = ["ui_column is-9"]

    def scrape_and_write(self,n):
        l = ['Buonconsiglio.csv', 'MART.csv', 'Pedavena.csv', 'Bookique.csv']
        i = 0
        for lk in self.link :
        
            req = requests.get(lk,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}) 
   
            scrape = Scraping(req.content,lk, parser)
            print("Scraping {} and writing it to file".format(lk))
            body = scrape.get_n_body(self.classe, n)
            
            with open(l[i], 'w', encoding = 'utf-8') as f :
                        writer = csv.writer(f)
                        writer.writerow(body)
                        f.close()
            i += 1


